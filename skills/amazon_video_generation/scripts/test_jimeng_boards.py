"""Test paired image identity, detail preservation and segmented time labels.

Synthetic tiles are layout fixtures, never SKU deliverables.
"""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image
from build_jimeng_boards import build, FIELDS, TABLE_HEADERS


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
        result = build(self.plan, self.out, table_page_size=1)
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

    def test_fixed_nine_slots_and_full_pages_before_overflow(self):
        self.data['shots'] = [self.shot(f'S{i+1:02}', i*4) for i in range(5)]
        self.data['total_duration_s'] = 20
        self.write()
        result = build(self.plan, self.out, reference_image_count=5)
        grids = [p for p in result['pages'] if p['kind'] == 'storyboard']
        self.assertEqual([len(p['slots']) for p in grids], [9, 9])
        self.assertEqual([len(p['records']) for p in grids], [9, 1])
        self.assertTrue(all(s['occupied'] for s in grids[0]['slots']))
        self.assertEqual([s['occupied'] for s in grids[1]['slots']], [True] + [False]*8)
        self.assertEqual(result['upload_budget']['total'], 9)
        for page in grids:
            self.assertEqual(len({s['box'][0] for s in page['slots']}), 3)
            self.assertEqual(len({s['box'][1] for s in page['slots']}), 3)
        with Image.open(self.out / grids[1]['file']) as image:
            for slot in grids[1]['slots'][1:]:
                x,y,w,h = slot['box']
                self.assertEqual(image.getpixel((x+w//2,y+20)), (255,255,255))

    def test_non_nine_grid_and_over_budget_leave_no_output(self):
        self.write()
        for kwargs in ({'columns': 2}, {'grid_page_size': 6},
                       {'reference_image_count': 8}, {'reference_image_count': -1}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    build(self.plan, self.out, **kwargs)
                self.assertFalse(self.out.exists())

    def test_unsupported_segment_ids_rejected_before_output(self):
        for cid in ('C1', 'C03'):
            self.data['generation_id'] = cid
            self.write()
            with self.assertRaisesRegex(ValueError, 'C01 or C02'):
                build(self.plan, self.out)
            self.assertFalse(self.out.exists())

    def test_exact_nine_panels_do_not_create_empty_page(self):
        self.data['shots'] = [self.shot(f'S{i+1:02}', i*4) for i in range(3)]
        for shot in self.data['shots']:
            shot['frames'].insert(1, {'state':'key', 'file':'frame.png', 'summary':'关键接触'})
        self.data['total_duration_s'] = 12
        self.write()
        result = build(self.plan, self.out)
        grids = [p for p in result['pages'] if p['kind'] == 'storyboard']
        self.assertEqual(len(grids), 1)
        self.assertEqual(len(grids[0]['records']), 9)

    def test_ten_column_table_preserves_every_execution_field(self):
        self.data['shots'][0]['details']['dialogue'] = '无旁白'
        self.data['shots'][0]['details']['copy'] = '画面文字：Ready'
        self.write()
        result = build(self.plan, self.out, table_page_size=1)
        for page in result['pages']:
            if page['kind'] != 'shot-table': continue
            self.assertEqual(page['headers'], list(TABLE_HEADERS))
            for row in page['records']:
                self.assertEqual(list(row['columns']), list(TABLE_HEADERS))
                rendered = '\n'.join(row['columns'].values())
                for value in row['details'].values():
                    self.assertIn(value, rendered)
        first = result['pages'][0]['records'][0]['columns']
        self.assertEqual(first['台词/旁白'], '无旁白')
        self.assertEqual(first['字幕'], '画面文字：Ready')

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

    def test_internal_planning_notes_do_not_change_upload_pixels(self):
        self.write()
        baseline = build(self.plan, self.out)
        self.data['planning_notes'] = {'research': '内部参考模板与未知音轨；不属于执行内容'}
        self.data['shots'][0]['planning_notes'] = {'evidence': '内部讨论与待核来源记录'}
        self.write()
        other = self.root / 'with-internal-notes'
        updated = build(self.plan, other)
        self.assertNotEqual(baseline['plan_sha256'], updated['plan_sha256'])
        self.assertEqual([p['sha256'] for p in baseline['pages']], [p['sha256'] for p in updated['pages']])
        self.assertEqual([p['records'] for p in baseline['pages']], [p['records'] for p in updated['pages']])
        self.assertTrue(all(p.suffix == '.png' for p in other.iterdir()))


if __name__ == '__main__':
    unittest.main()
