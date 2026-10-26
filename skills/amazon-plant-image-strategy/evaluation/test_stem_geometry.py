"""Synthetic stem/container arithmetic, not product measurements or visual proof."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / "scripts/scale_check.py"
spec = importlib.util.spec_from_file_location("stem_scale_check", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assess = module.assess


class StemGeometryTests(unittest.TestCase):
    def plan(self, geometry=None, **changes):
        stem = dict(total_cm=43.18, body_cm=12.7, bare_cm=30.48,
                    total_basis="user_confirmed", body_basis="user_confirmed",
                    container_height_cm=18, usable_depth_cm=17,
                    container_basis="design_assumption", tilt_degrees=0, trim_cm=0)
        stem.update(geometry or {})
        return dict(dict(asset_id="SCENE01", reference_role="container", reference_cm=18,
                         reference_basis="design_assumption", projection_mode="coplanar_parallel",
                         reference_frame_fraction=0.27, stem_geometry=stem), **changes)

    def instance(self, name, product, container, **changes):
        item = self.plan(**changes)
        del item["asset_id"]
        return dict(item, instance_id=name, product_id=product, container_id=container)

    def test_total_body_and_bare_stem_are_independent_of_vessel_height(self):
        tall = assess(self.plan())
        short = assess(self.plan(geometry=dict(container_height_cm=10, usable_depth_cm=9),
                                 reference_cm=10, reference_frame_fraction=0.15))
        self.assertEqual(tall["errors"] + short["errors"], [])
        a, b = tall["stem_geometry"], short["stem_geometry"]
        self.assertAlmostEqual(a["exposed_bare_cm"], 13.48)
        self.assertAlmostEqual(b["exposed_bare_cm"], 21.48)
        self.assertAlmostEqual(a["body_vertical_cm"], b["body_vertical_cm"])
        self.assertAlmostEqual(a["arrangement_height_cm"], 44.18)
        self.assertAlmostEqual(b["arrangement_height_cm"], 44.18)
        self.assertEqual(tall["segment_visual_check"], "not_provided")
        self.assertEqual(tall["visual_check"], "not_provided")

    def test_segment_frame_targets_are_checked_even_if_total_is_correct(self):
        correct = self.plan(product_cm=44.18, product_frame_fraction=0.6627,
                            body_frame_fraction=0.1905, exposed_bare_frame_fraction=0.2022)
        self.assertEqual(assess(correct)["errors"], [])
        wrong = assess(dict(correct, body_frame_fraction=0.35, exposed_bare_frame_fraction=0.04))
        self.assertEqual(len(wrong["errors"]), 2)

    def test_product_total_cannot_be_reused_as_the_arranged_height(self):
        self.assertTrue(assess(self.plan(product_cm=43.18))["errors"])
        self.assertTrue(assess(self.plan(reference_cm=17))["errors"])

    def test_explicit_lower_stem_trim_changes_only_the_selected_state(self):
        raw = self.plan(geometry=dict(container_height_cm=10, usable_depth_cm=9,
                                     trim_cm=21.48, trim_allowed=True, trim_decision="confirmed"),
                        reference_cm=10, reference_frame_fraction=0.3,
                        product_cm=22.7, exposed_bare_frame_fraction=0)
        result = assess(raw)
        self.assertEqual(result["errors"], [])
        g = result["stem_geometry"]
        self.assertAlmostEqual(g["trimmed_total_cm"], 21.7)
        self.assertAlmostEqual(g["arrangement_height_cm"], 22.7)
        self.assertEqual(g["exposed_bare_cm"], 0)
        self.assertEqual(raw["stem_geometry"]["total_cm"], 43.18)
        for fields in (dict(trim_allowed=False), dict(trim_decision="proposed")):
            invalid = copy.deepcopy(raw)
            invalid["stem_geometry"].update(fields)
            self.assertTrue(assess(invalid)["errors"])

    def test_impossible_dimensions_and_missing_fact_bases_are_rejected(self):
        cases = [dict(body_cm=50), dict(bare_cm=12), dict(usable_depth_cm=19),
                 dict(container_height_cm=40, usable_depth_cm=35),
                 dict(trim_cm=40, trim_allowed=True, trim_decision="confirmed"),
                 dict(body_basis="design_assumption"), dict(total_basis="unknown"),
                 dict(trim_cm=None), dict(body_cm=float("nan")), dict(tilt_degrees=90),
                 dict(usable_depth_cm=True), dict(tilt_degrees=-1)]
        for fields in cases:
            with self.subTest(fields=fields):
                self.assertTrue(assess(self.plan(geometry=fields))["errors"])

    def test_tilt_uses_vertical_projection_without_certifying_wall_clearance(self):
        result = assess(self.plan(geometry=dict(tilt_degrees=30)))
        self.assertEqual(result["errors"], [])
        g = result["stem_geometry"]
        self.assertAlmostEqual(g["insertion_cm"], 17 / math.cos(math.radians(30)))
        self.assertAlmostEqual(g["arrangement_height_cm"], 1 + 43.18 * math.cos(math.radians(30)))
        self.assertEqual(result["geometry_check"], "calculated")
        self.assertTrue(any("clearance" in w for w in result["warnings"]))

    def test_pixel_segment_drift_is_separate_from_correct_overall_ratio(self):
        good = self.plan(observed_reference_px=1800, observed_product_px=4418,
                         observed_body_px=1270, observed_exposed_bare_px=1348)
        self.assertEqual(assess(good)["segment_visual_check"], "within_supplied_threshold")
        bad = assess(dict(good, observed_body_px=2100))
        self.assertEqual(bad["visual_check"], "within_supplied_threshold")
        self.assertEqual(bad["segment_visual_check"], "outside_supplied_threshold")
        self.assertTrue(bad["errors"])

    def test_segment_only_observation_and_unresolved_perspective_are_honest(self):
        result = assess(self.plan(observed_reference_px=1800, observed_body_px=1270))
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["visual_check"], "not_provided")
        self.assertEqual(result["segment_visual_check"], "within_supplied_threshold")
        unresolved = assess(self.plan(projection_mode="unresolved", observed_reference_px=1800,
                                      observed_body_px=1270))
        self.assertEqual(unresolved["segment_visual_check"], "perspective_unresolved")
        self.assertTrue(assess(self.plan(observed_body_px=1270))["errors"])

    def test_one_asset_can_have_several_independent_product_container_pairs(self):
        a = self.instance("V1-blue", "blue", "V1")
        b = self.instance("V1-white", "white", "V1",
                          geometry=dict(total_cm=30, body_cm=10, bare_cm=20))
        c = self.instance("V2-blue", "blue", "V2",
                          geometry=dict(container_height_cm=10, usable_depth_cm=9),
                          reference_cm=10, reference_frame_fraction=0.15)
        result = assess(dict(asset_id="SCENE01", instances=[a, b, c]))
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["instances"]), 3)
        self.assertEqual(result["visual_check"], "per_instance")
        self.assertEqual(result["instances"][1]["stem_geometry"]["body_cm"], 10)

    def test_bad_instance_maps_and_conflicting_shared_container_are_rejected(self):
        a = self.instance("V1-blue", "blue", "V1")
        b = self.instance("V1-white", "white", "V1",
                          geometry=dict(container_height_cm=10, usable_depth_cm=9), reference_cm=10)
        self.assertTrue(assess(dict(asset_id="SCENE01", instances=[a, b]))["errors"])
        self.assertTrue(assess(dict(asset_id="SCENE01", instances=[a, a]))["errors"])
        self.assertTrue(assess(dict(asset_id="SCENE01", instances=[dict(a, container_id="")]))["errors"])
        self.assertTrue(assess(dict(asset_id="SCENE01", instances=[dict(a, instances=[])]))["errors"])
        self.assertTrue(assess(dict(asset_id="SCENE01", instances=[a], product_cm=44.18))["errors"])

    def test_cli_still_rejects_duplicate_assets_and_output_overwriting_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(dict(assets=[self.plan()])), encoding="utf-8")
            before = path.read_bytes()
            run = subprocess.run([sys.executable, str(SCRIPT), "--input", str(path), "--output", str(path)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(path.read_bytes(), before)
            path.write_text(json.dumps(dict(assets=[self.plan(), self.plan()])), encoding="utf-8")
            run = subprocess.run([sys.executable, str(SCRIPT), "--input", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)


if __name__ == "__main__":
    unittest.main()
