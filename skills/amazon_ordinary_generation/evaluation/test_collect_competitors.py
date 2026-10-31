"""Offline batch-scope regression: failures must not skip requested competitors."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collect_competitors import run_batch
from research_audit import normalize


class BatchTests(unittest.TestCase):
    def test_failure_and_timeout_do_not_skip_later_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inputs = root / 'inputs.json'
            rows = normalize(['B000000001', 'https://amazon.com/dp/B000000001?ref=x',
                              'B000000002', 'B000000003', 'B000000004'])
            inputs.write_text(json.dumps(rows), encoding='utf-8')
            calls = []

            def runner(command, **kwargs):
                # All inputs are queued on disk before the first request.
                manifest = next((root / 'media').glob('batch-*/batch-manifest.json'))
                self.assertEqual(len(json.loads(manifest.read_text())['competitors']), 4)
                calls.append(command)
                if len(calls) == 1:
                    return types.SimpleNamespace(returncode=2, stdout='', stderr='login required')
                if len(calls) == 2:
                    raise subprocess.TimeoutExpired(command, 300)
                return types.SimpleNamespace(returncode=0, stdout='partial media manifest', stderr='')

            file, report = run_batch(inputs, str(root / 'media'), runner=runner)
            self.assertEqual(len(calls), 4)
            self.assertEqual([r['status'] for r in report['competitors']],
                             ['capture-failed', 'capture-failed', 'captured-partial', 'captured-partial'])
            self.assertEqual(report, json.loads(file.read_text()))
            self.assertEqual(report['status'], 'partial')

    def test_different_markets_have_separate_media_roots(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inputs = root / 'inputs.json'
            inputs.write_text(json.dumps(normalize(['B000000001', 'https://amazon.de/dp/B000000001'])))
            commands = []
            def runner(cmd, **kwargs):
                commands.append(cmd)
                return types.SimpleNamespace(returncode=0, stdout='', stderr='')
            run_batch(inputs, str(root / 'media'), runner=runner)
            self.assertNotEqual(commands[0][-1], commands[1][-1])


if __name__ == '__main__':
    unittest.main()
