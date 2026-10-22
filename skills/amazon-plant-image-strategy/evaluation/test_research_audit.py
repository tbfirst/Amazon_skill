"""Synthetic behavioral tests for the offline checker; no live network calls."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from research_audit import normalize, audit_record, audit_folder


def record():
    return {
        "schema_version": 1, "asin": "B000000001", "marketplace": "US",
        "identity": {"verified": True, "title": "Synthetic plant fixture", "variant": "test",
                     "final_asin": "B000000001", "source": "fixture://product",
                     "observed_at": "2026-10-16T10:00:00+08:00"},
        "sections": {k: {"status": "pending", "inventory_total": None}
                     for k in ("gallery", "aplus", "review_photos", "reviews")},
        "visuals": [], "reviews": [], "attempts": []}


def visual():
    return {"id": "V-fixture-G01", "section": "gallery", "observed": True,
            "source": "fixture://product", "locator": "gallery image 1",
            "observed_at": "2026-10-16T10:00:00+08:00", "layout": "central",
            "lighting": "soft left", "shadow": "soft right", "transfer_to": ["DETAIL01"]}


class ResearchAuditTests(unittest.TestCase):
    def test_normalization_deduplicates_tracking_urls(self):
        result = normalize(["b000000001", "https://www.amazon.com/title/dp/B000000001?th=1",
                            "https://www.amazon.com/gp/product/B000000001/ref=x"])
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]["inputs"]), 3)

    def test_marketplaces_remain_distinct(self):
        result = normalize(["B000000001", "https://www.amazon.co.uk/dp/B000000001"])
        self.assertEqual([r["marketplace"] for r in result], ["US", "UK"])

    def test_false_hosts_short_links_and_query_ids_are_rejected(self):
        for url in ["https://amazon.com.example.org/dp/B000000001", "https://amzn.to/test",
                    "https://www.amazon.com/s?k=B000000001", "https://u:p@amazon.com/dp/B000000001"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                normalize([url])

    def test_valid_visual_count(self):
        data = record()
        data["visuals"] = [visual()]
        data["sections"]["gallery"] = {"status": "observed", "inventory_total": 1, "source": "fixture://gallery"}
        self.assertFalse(audit_record(data)[0])

    def test_uninspected_inventory_cannot_pass_as_complete(self):
        data = record()
        data["visuals"] = [visual()]
        data["sections"]["gallery"] = {"status": "observed", "inventory_total": 9, "source": "fixture://gallery"}
        self.assertTrue(any("every unit" in e for e in audit_record(data)[0]))

    def test_text_only_is_not_visual_evidence(self):
        data = record()
        item = visual()
        item["observed"] = False
        data["visuals"] = [item]
        self.assertTrue(any("actual observation" in e for e in audit_record(data)[0]))

    def test_login_wall_is_honest_incomplete_record(self):
        data = record()
        data["sections"]["reviews"] = {"status": "access-blocked", "reason": "login required",
                                          "source": "fixture://reviews"}
        data["attempts"] = [{"section": "reviews", "route": "browser", "result": "login required"}]
        errors, warnings, counts, _, _ = audit_record(data)
        self.assertFalse(errors)
        self.assertTrue(warnings)
        self.assertEqual(counts.get("reviews", 0), 0)

    def test_ai_summary_not_in_sample(self):
        data = record()
        data["reviews"] = [{"id": "fixture-R1", "kind": "ai_summary", "themes": ["size"]}]
        self.assertTrue(any("cannot enter" in e for e in audit_record(data)[0]))

    def test_theme_once_per_review_and_duplicate_rejected(self):
        data = record()
        data["reviews"] = [{"id": "fixture-R1", "kind": "original", "source": "fixture://review",
                            "summary": "Synthetic concern", "variant_scope": "test",
                            "themes": ["size", "size", "appearance"]}]
        data["sections"]["reviews"] = {"status": "observed", "sampling": "one fixture",
                                          "source": "fixture://reviews"}
        errors, _, counts, themes, _ = audit_record(data)
        self.assertFalse(errors)
        self.assertEqual(counts["reviews"], 1)
        self.assertEqual(themes, {"size": 1, "appearance": 1})
        data["reviews"].append(copy.deepcopy(data["reviews"][0]))
        self.assertTrue(any("duplicated" in e for e in audit_record(data)[0]))

    def test_identity_and_asset_scope_are_enforced(self):
        data = record()
        data["identity"]["verified"] = False
        item = visual()
        item["transfer_to"] = ["MAIN", "APLUS06"]
        data["visuals"] = [item]
        errors = audit_record(data)[0]
        self.assertTrue(any("unverified" in e for e in errors))
        self.assertTrue(any("fixed 11" in e for e in errors))

    def test_invalid_record_types_report_errors(self):
        for data in [[], None, {"marketplace": [], "identity": [], "sections": [], "reviews": {}, "visuals": {}}]:
            self.assertTrue(audit_record(data)[0])

    def test_folder_audit_is_read_only_and_flags_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            payload = json.dumps(record()).encode()
            (folder / "first.json").write_bytes(payload)
            (folder / "second.json").write_bytes(payload)
            report, failed = audit_folder(folder)
            self.assertTrue(failed)
            self.assertIn("duplicate competitor", report)
            self.assertEqual((folder / "first.json").read_bytes(), payload)

    def test_malformed_status_and_identity_types(self):
        for status in ([], {}, None):
            data = record()
            data["sections"]["gallery"]["status"] = status
            data["identity"]["verified"] = "true"
            data["schema_version"] = True
            errors = audit_record(data)[0]
            self.assertTrue(any("invalid status" in e for e in errors))
            self.assertTrue(any("boolean" in e for e in errors))
            self.assertTrue(any("schema_version" in e for e in errors))

    def test_absent_section_cannot_have_nonzero_inventory(self):
        data = record()
        data["sections"]["gallery"] = {"status": "absent", "inventory_total": 2,
                                        "source": "fixture://gallery", "reason": "none found"}
        self.assertTrue(any("nonzero inventory" in e for e in audit_record(data)[0]))


if __name__ == "__main__":
    unittest.main()
