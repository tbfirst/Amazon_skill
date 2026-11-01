import copy
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from build_storyboard_editor import build_editor, build_payload


class StoryboardEditorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Image.new('RGB', (600, 100), 'green').save(self.root / 'board.png')
        self.plan = {
            'title': '测试分镜', 'revision': 'v1', 'delivery_mode': 'connected-clips',
            'total_duration_s': 45, 'board': {'file': 'board.png'},
            'clips': [{'id': f'C{i+1:02}', 'duration_s': 15} for i in range(3)],
            'shots': [{'id': f'S{i+1:02}', 'clip_id': f'C{i+1:02}', 'start_s': i*15,
                       'duration_s': 15, 'region_px': [i*200, 0, 200, 100],
                       'caption': {'action': '商品静止'}} for i in range(3)]}

    def write(self, plan=None):
        path = self.root / 'plan.json'
        path.write_text(json.dumps(plan or self.plan, ensure_ascii=False), encoding='utf-8')
        return path

    def test_actual_board_embedded_and_revision_bound(self):
        p = self.write()
        payload = build_payload(p)
        self.assertEqual([s['local_start_s'] for s in payload['shots']], [0, 0, 0])
        self.assertEqual(len(payload['plan_sha256']), 64)
        self.assertEqual(len(payload['image_hashes']['board.png']), 64)
        self.assertTrue(all(s['image'].startswith('data:image/jpeg;base64,') for s in payload['shots']))
        build_editor(p, self.root / 'editor.html')
        self.assertEqual(json.loads(p.read_text(encoding='utf-8')), self.plan)

    def test_missing_image_is_not_a_placeholder(self):
        self.plan['board']['file'] = 'missing.png'
        with self.assertRaises(ValueError): build_payload(self.write())

    def test_no_guessed_grid_when_regions_absent(self):
        for s in self.plan['shots']: del s['region_px']
        payload = build_payload(self.write())
        self.assertIsNotNone(payload['board'])
        self.assertTrue(all(s['image'] is None for s in payload['shots']))

    def test_wrong_timing_and_cross_clip_shot_rejected(self):
        self.plan['shots'][0]['duration_s'] = 16
        with self.assertRaisesRegex(ValueError, 'crosses'): build_payload(self.write())
        self.plan['shots'][0]['duration_s'] = 15
        self.plan['shots'][1]['start_s'] = 16
        with self.assertRaisesRegex(ValueError, 'continuous'): build_payload(self.write())

    def test_outside_board_region_rejected(self):
        self.plan['shots'][0]['region_px'] = [500, 0, 200, 100]
        with self.assertRaisesRegex(ValueError, 'outside'): build_payload(self.write())

    def test_explicit_custom_contract(self):
        self.plan['clips'] = [{'id': 'C01', 'duration_s': 20}]
        self.plan['shots'] = [self.plan['shots'][0]]
        self.plan['shots'][0]['duration_s'] = 20
        self.plan['total_duration_s'] = 20
        with self.assertRaisesRegex(ValueError, 'Default'): build_payload(self.write())
        self.plan['default_contract'] = False
        self.assertEqual(build_payload(self.write())['total_duration_s'], 20)

    def test_image_change_updates_hash(self):
        p = self.write()
        before = build_payload(p)
        Image.new('RGB', (600, 100), 'red').save(self.root / 'board.png')
        after = build_payload(p)
        self.assertEqual(before['plan_sha256'], after['plan_sha256'])
        self.assertNotEqual(before['image_hashes'], after['image_hashes'])

    def test_existing_output_preserved_and_script_content_escaped(self):
        self.plan['title'] = '</script><script>alert(1)</script>'
        p = self.write(); out = self.root / 'editor.html'
        build_editor(p, out)
        original = out.read_bytes()
        self.assertNotIn(self.plan['title'], original.decode('utf-8'))
        with self.assertRaisesRegex(ValueError, 'already exists'): build_editor(p, out)
        self.assertEqual(original, out.read_bytes())

    def test_frame_files_are_accepted(self):
        del self.plan['board']
        for s in self.plan['shots']:
            s['frames'] = [{'state': 'key', 'file': 'board.png'}]
            del s['region_px']
        self.assertTrue(all(s['image'] for s in build_payload(self.write())['shots']))


if __name__ == '__main__': unittest.main()
