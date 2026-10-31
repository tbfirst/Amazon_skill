"""Deterministic handoff invariants, using temporary fixtures (not real SKU evidence)."""

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_prompt_summary.py"
spec = importlib.util.spec_from_file_location("summary", SCRIPT)
summary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(summary)


class PromptSummaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "prompts" / "blocked").mkdir(parents=True)
        (self.root / "identity.jpg").write_bytes(b"test fixture only; not visual evidence")
        self.body = "Exact text\r\nKeep 8 x 10, not 10 x 8.\r\n```nested```\r\n"
        self.manifest = {"schemaVersion": 1, "campaignMode": "new-set",
                         "targetAssetIds": summary.DEFAULT_IDS.copy(), "assets": []}
        for index, asset_id in enumerate(summary.DEFAULT_IDS):
            status = ("READY", "PROVISIONAL", "BLOCKED")[index % 3]
            file = f"prompts/{'blocked/' if status == 'BLOCKED' else ''}{asset_id}.txt"
            body = f"{asset_id} CONDITIONAL SECRET" if status == "BLOCKED" else self.body + asset_id
            with (self.root / file).open("w", encoding="utf-8", newline="") as stream:
                stream.write(body)
            self.manifest["assets"].append({
                "id": asset_id, "status": status, "file": file,
                "canvas": {"width": 1600, "height": 1600},
                "references": [{"filename": "identity.jpg", "role": "identity", "path": "identity.jpg"}],
                "conditions": ["slot pending"] if status == "PROVISIONAL" else [],
                "gaps": ["rear view missing"] if status == "BLOCKED" else [],
                "policyReview": "verified", "uploadReview": "pending" if status == "PROVISIONAL" else "not-applicable"
            })
        self.save()

    def save(self):
        (self.root / "prompt-manifest.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_exact_text_and_blocked_isolation(self):
        outputs = summary.compile_campaign(self.root)
        for content in outputs.values():
            self.assertIn(self.body + "DIM01", content)
            self.assertNotIn("CONDITIONAL SECRET", content)
            self.assertIn("PROVISIONAL", content)
            self.assertIn("slot pending", content)
            self.assertIn("rear view missing", content)
        self.assertIn("````text", outputs["all-prompts.md"])

    def test_competitor_reference_cannot_be_replaced_by_provenance_text(self):
        asset = self.manifest['assets'][0]
        asset['referenceRoute'] = 'competitor-derived'
        asset['visualTransfer'] = dict(mode='reference-replace', delivery='visual',
                                       sourceReference='competitor.jpg', retained=['two photo columns and right sunlight'])
        self.save()
        with self.assertRaisesRegex(ValueError, 'uploaded layout reference'):
            summary.load_campaign(self.root)
        (self.root / 'competitor.jpg').write_bytes(b'fixture only')
        asset['references'].append(dict(filename='competitor.jpg', role='layout', path='competitor.jpg'))
        self.save()
        with self.assertRaisesRegex(ValueError, 'prompt must name'):
            summary.load_campaign(self.root)
        with (self.root / asset['file']).open('a', encoding='utf-8') as stream:
            stream.write('\nUpload competitor.jpg as full-scene layout reference.')
        self.assertEqual(len(summary.load_campaign(self.root)), 11)

    def test_text_only_downgrade_needs_explicit_record(self):
        asset = self.manifest['assets'][0]
        asset['referenceRoute'] = 'competitor-derived'
        asset['visualTransfer'] = dict(mode='structure-adapt', delivery='text-only', retained=['four-window hierarchy'])
        self.save()
        with self.assertRaisesRegex(ValueError, 'user authorization'):
            summary.load_campaign(self.root)
        asset['visualTransfer'].update(sourceLocator='fixture://G02', reason='reference unavailable',
                                       authorization='User explicitly selected text-only adaptation.')
        self.save()
        with (self.root / asset['file']).open('a', encoding='utf-8') as stream:
            stream.write('\nText-only adaptation; no competitor image input supplied.')
        self.assertEqual(len(summary.load_campaign(self.root)), 11)

    def test_v2_handoff_cannot_omit_route_to_skip_source_checks(self):
        self.manifest['handoffVersion'] = 2
        self.save()
        with self.assertRaisesRegex(ValueError, 'explicit referenceRoute'):
            summary.load_campaign(self.root)
        self.manifest['referenceRoute'] = 'original'
        self.save()
        self.assertEqual(len(summary.load_campaign(self.root)), 11)
        self.manifest['assets'][0]['referenceRoute'] = 'competitor-derived'
        self.save()
        with self.assertRaisesRegex(ValueError, 'needs visualTransfer'):
            summary.load_campaign(self.root)

    def test_missing_reference_does_not_replace_previous_output(self):
        output = self.root / "all-prompts.md"
        output.write_text("previous", encoding="utf-8")
        (self.root / "identity.jpg").unlink()
        with self.assertRaisesRegex(ValueError, "reference file missing"):
            summary.compile_campaign(self.root)
        self.assertEqual(output.read_text(), "previous")

    def test_duplicate_and_scope_errors(self):
        self.manifest["assets"].append(copy.deepcopy(self.manifest["assets"][0]))
        self.save()
        with self.assertRaisesRegex(ValueError, "duplicate asset"):
            summary.load_campaign(self.root)
        self.manifest["assets"].pop()
        self.manifest["targetAssetIds"] = ["DIM01"]
        self.save()
        with self.assertRaisesRegex(ValueError, "default 11"):
            summary.load_campaign(self.root)

    def test_pending_review_and_provisional_gaps_rejected(self):
        self.manifest["assets"][0]["policyReview"] = "pending"
        self.save()
        with self.assertRaisesRegex(ValueError, "cannot be READY"):
            summary.load_campaign(self.root)
        self.manifest["assets"][0]["policyReview"] = "verified"
        self.manifest["assets"][1]["gaps"] = ["load capacity unknown"]
        self.save()
        with self.assertRaisesRegex(ValueError, "cannot retain gaps"):
            summary.load_campaign(self.root)

    def test_path_escape_and_blocked_path_rejected(self):
        self.manifest["assets"][0]["file"] = "../outside.txt"
        self.save()
        with self.assertRaisesRegex(ValueError, "inside project"):
            summary.load_campaign(self.root)
        self.manifest["assets"][0]["file"] = self.manifest["assets"][2]["file"]
        self.save()
        with self.assertRaisesRegex(ValueError, "path mismatch"):
            summary.load_campaign(self.root)

    def test_refresh_and_authorized_scope_override(self):
        self.manifest["assets"] = self.manifest["assets"][:1]
        self.manifest["targetAssetIds"] = ["DIM01"]
        self.manifest["campaignMode"] = "set-refresh"
        self.save()
        self.assertEqual(len(summary.load_campaign(self.root)), 1)
        self.manifest["campaignMode"] = "new-set"
        self.manifest["scopeOverrideReason"] = "User explicitly requested only one dimension image."
        self.save()
        self.assertEqual(len(summary.load_campaign(self.root)), 1)


if __name__ == "__main__":
    unittest.main()
