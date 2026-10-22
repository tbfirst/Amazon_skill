"""Synthetic geometric cases; no product photographs or market claims."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("scale_check", Path(__file__).parents[1]/"scripts/scale_check.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assess = module.assess


class ScaleCheckTests(unittest.TestCase):
    def plan(self, **changes):
        data = dict(asset_id="SYNTHETIC", product_cm=30, reference_cm=60,
                    reference_basis="design_assumption", projection_mode="coplanar_parallel",
                    reference_frame_fraction=0.8, product_frame_fraction=0.4)
        return dict(data, **changes)

    def test_compatible_frame_is_derived_but_not_a_visual_pass(self):
        r = assess(self.plan())
        self.assertEqual(r["errors"], [])
        self.assertAlmostEqual(r["expected_product_frame_fraction"], 0.4)
        self.assertEqual(r["visual_check"], "not_provided")
        self.assertTrue(r["warnings"])

    def test_inconsistent_frame_and_enlarged_observation_are_caught(self):
        r = assess(self.plan(product_frame_fraction=0.7, observed_product_px=850, observed_reference_px=1000))
        self.assertEqual(len(r["errors"]), 2)
        self.assertEqual(r["visual_check"], "outside_supplied_threshold")

    def test_foreground_reference_needs_explicit_perspective(self):
        r = assess(self.plan(projection_mode="explicit_factor", perspective_factor=0.5,
                             product_frame_fraction=0.2, observed_product_px=250, observed_reference_px=1000))
        self.assertEqual(r["errors"], [])
        self.assertAlmostEqual(r["expected_projected_ratio"], 0.25)
        self.assertEqual(r["visual_check"], "within_supplied_threshold")
        unresolved = assess(self.plan(projection_mode="unresolved", observed_product_px=900, observed_reference_px=1000))
        self.assertEqual(unresolved["visual_check"], "perspective_unresolved")
        self.assertNotIn("observed_relative_drift", unresolved)

    def test_invalid_numbers_and_partial_observation_are_rejected(self):
        for changes in [{"reference_cm": 0}, {"product_cm": True}, {"product_cm": float('nan')},
                        {"product_frame_fraction": 1.2}, {"observed_product_px": 12},
                        {"projection_mode": "explicit_factor"}, {"relative_tolerance": 1}]:
            with self.subTest(changes=changes):
                self.assertTrue(assess(self.plan(**changes))["errors"])

    def test_tall_floor_product_and_small_table_flower_use_same_math(self):
        tall = assess(self.plan(product_cm=150, reference_cm=75,
                                reference_frame_fraction=0.4, product_frame_fraction=0.8))
        small = assess(self.plan(product_cm=12, reference_cm=48,
                                 reference_frame_fraction=0.8, product_frame_fraction=0.2))
        self.assertEqual(tall["errors"], [])
        self.assertEqual(small["errors"], [])
        self.assertAlmostEqual(tall["world_ratio"], 2)
        self.assertAlmostEqual(small["world_ratio"], 0.25)

    def test_hanging_ratio_is_not_a_global_frame_percentage(self):
        close = assess(self.plan(product_cm=61, reference_cm=91,
                                 reference_frame_fraction=0.9, product_frame_fraction=61/91*0.9))
        wide = assess(self.plan(product_cm=61, reference_cm=91,
                                reference_frame_fraction=0.55, product_frame_fraction=61/91*0.55))
        self.assertEqual(close["world_ratio"], wide["world_ratio"])
        self.assertNotEqual(close["expected_product_frame_fraction"], wide["expected_product_frame_fraction"])
        self.assertEqual(close["errors"]+wide["errors"], [])

    def test_product_too_large_for_full_view_and_double_projection_are_caught(self):
        self.assertTrue(assess(self.plan(product_cm=180, reference_cm=60))["errors"])
        self.assertTrue(assess(self.plan(perspective_factor=0.5))["errors"])

    def test_diagnostic_tolerance_is_explicit_and_configurable(self):
        input_data = dict(observed_product_px=550, observed_reference_px=1000)
        self.assertEqual(assess(self.plan(relative_tolerance=0.12, **input_data))["errors"], [])
        self.assertTrue(assess(self.plan(relative_tolerance=0.05, **input_data))["errors"])


if __name__ == "__main__":
    unittest.main()
