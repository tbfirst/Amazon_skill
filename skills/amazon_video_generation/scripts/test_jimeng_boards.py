"""Test paired image identity, detail preservation and segmented time labels.

Synthetic tiles are layout fixtures, never SKU deliverables.
"""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image
from build_jimeng_boards import build, FIELDS


class JimengBoardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        Image.new('RGB', (160, 90), 'red').save(self.root / 'frame.png')
        self.plan = self.root / 'plan.json'
        self.out = self.root / 'out'
        self.data = {'title': 'Test', 'revision': 'v1', 'generation_id': 'C02',
                     'global_offset_s': 15, 'aspect_ratio': '16:9', 'total_duration_s': 8,
                     'shots': [self.shot('S05', 0), self.shot('S07', 4)]}

    def shot(self, shot_id, start):
        return {'id': shot_id, 'start_s': start, 'duration_s': 4,
                'details': {key: '明确内容 ' + key for key in FIELDS},
                'frames': [{'state': state, 'file': 'frame.png', 'summary': '当前画面状态：' + state}
                           for state in ('start', 'end')]}

    def write(self):
        self.plan.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')

    def test_paired_ids_and_states_across_pages(self):
        self.write()
        result = build(self.plan, self.out, grid_page_size=3, table_page_size=1)
        grids = [p for p in result['pages'] if p['kind'] == 'storyboard']
        tables = [p for p in result['pages'] if p['kind'] == 'shot-table']
        records = [r for p in grids for r in p['records']]
        rows = [r for p in tables for r in p['records']]
        self.assertEqual([r['shot_id'] for r in rows], ['S05', 'S07'])
        self.assertEqual([f"{r['shot_id']}/{r['state']}" for r in records],
                         [frame_id for row in rows for frame_id in row['frame_ids']])
        self.assertEqual(result['plan_snapshot']['global_offset_s'], 15)
        self.assertIn('全片 15–19秒', rows[0]['timeline_label'])
        self.assertEqual(rows[0]['timeline_label'], records[0]['timeline_label'])
        self.assertEqual(rows[0]['details'], self.data['shots'][0]['details'])
        for page in result['pages']:
            with Image.open(self.out / page['file']) as image:
                self.assertEqual(list(image.size), page['size'])
                self.assertEqual(image.width, image.height)
                self.assertGreaterEqual(image.height, 350)
                for record in page['records']:
                    if 'image_box' in record:
                        x, y, width, height = record['image_box']
                        self.assertEqual(image.getpixel((x + width // 2, y + height // 2)), (255, 0, 0))
                        self.assertEqual(record['caption_box'][1], y + height)
        before = {p.name: p.read_bytes() for p in self.out.iterdir()}
        self.assertTrue(all(p.suffix == '.png' for p in self.out.iterdir()))
        self.assertEqual([int(p['file'].split('-')[0]) for p in result['pages']], list(range(1, len(result['pages']) + 1)))
        with self.assertRaisesRegex(ValueError, 'already exists'):
            build(self.plan, self.out)
        self.assertEqual({p.name: p.read_bytes() for p in self.out.iterdir()}, before)

    def test_missing_details_summary_and_bad_timing_fail_without_output(self):
        original = copy.deepcopy(self.data)
        for mutation in ('summary', 'detail', 'gap', 'duplicate', 'offset', 'missing_image'):
            with self.subTest(mutation=mutation):
                self.data = copy.deepcopy(original)
                if mutation == 'summary':
                    self.data['shots'][0]['frames'][0]['summary'] = ''
                elif mutation == 'detail':
                    del self.data['shots'][0]['details']['action']
                elif mutation == 'gap':
                    self.data['shots'][1]['start_s'] = 5
                elif mutation == 'duplicate':
                    self.data['shots'][1]['id'] = 'S05'
                elif mutation == 'offset':
                    self.data['global_offset_s'] = -1
                else:
                    self.data['shots'][0]['frames'][0]['file'] = 'missing.png'
                self.write()
                with self.assertRaises(ValueError):
                    build(self.plan, self.out)
                self.assertFalse(self.out.exists())

    def test_long_detail_expands_row_without_truncation(self):
        self.write()
        baseline = build(self.plan, self.out, table_page_size=1)
        self.data['shots'][0]['details']['action'] = '手部逐次插入、落位、松手。' * 40
        self.write()
        expanded = build(self.plan, self.root / 'long', table_page_size=1)
        before = next(p for p in baseline['pages'] if p['kind'] == 'shot-table')
        after = next(p for p in expanded['pages'] if p['kind'] == 'shot-table')
        self.assertGreater(after['content_size'][1], before['content_size'][1])
        self.assertEqual(after['records'][0]['details']['action'], self.data['shots'][0]['details']['action'])

    def test_square_canvas_budget_checked_before_writing(self):
        self.data['shots'][0]['details']['action'] = '逐次插入落位松手并检查容器状态。' * 1000
        self.write()
        with self.assertRaisesRegex(ValueError, 'page too large'):
            build(self.plan, self.out)
        self.assertFalse(self.out.exists())


if __name__ == '__main__':
    unittest.main()
