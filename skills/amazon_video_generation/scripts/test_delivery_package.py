"""Check file scope, all upload roles and exact image-dimension boundaries."""
import tempfile
from pathlib import Path
import unittest
from PIL import Image
from check_delivery_package import check, check_image


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'delivery'
        self.root.mkdir()
        (self.root / '分析说明书.md').write_text('测试说明', encoding='utf-8')
        (self.root / 'README.md').write_text('测试使用说明', encoding='utf-8')
        (self.root / 'shot-list.csv').write_text('S-ID,C-ID\nS01,C01\n', encoding='utf-8-sig')
        self.segment('C01')

    def segment(self, name):
        folder = self.root / name
        folder.mkdir()
        (folder / f'{name}.draft.txt').write_text('本段完整提示词测试', encoding='utf-8')
        for filename in ('01-shot-table.png', '02-storyboard.png', '03-product.png'):
            Image.new('RGB', (400, 400), 'white').save(folder / filename)
        return folder

    def test_one_or_two_segments_and_no_files_created(self):
        original = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(list(check(self.root)['segments']), ['C01'])
        self.assertEqual(original, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        self.segment('C02')
        self.assertEqual(list(check(self.root)['segments']), ['C01', 'C02'])

    def test_height_and_ratio_inclusive_boundaries(self):
        path = Path(self.tmp.name) / 'test.png'
        for size in ((210, 350), (560, 350), (350, 350), (600, 1000)):
            with self.subTest(size=size):
                Image.new('RGB', size).save(path)
                self.assertEqual(check_image(path)['height'], size[1])
        for size in ((349, 349), (209, 350), (561, 350), (599, 1000)):
            with self.subTest(size=size):
                Image.new('RGB', size).save(path)
                with self.assertRaisesRegex(ValueError, 'require height'):
                    check_image(path)

    def test_checks_product_image_not_just_boards(self):
        Image.new('RGB', (1920, 1080)).save(self.root / 'C01/03-product.png')
        with self.assertRaisesRegex(ValueError, '03-product.png'):
            check(self.root)

    def test_valid_non_square_warns_without_failing(self):
        Image.new('RGB', (560, 350)).save(self.root / 'C01/03-product.png')
        result = check(self.root)
        self.assertEqual(len(result['warnings']), 1)

    def test_exif_orientation_is_applied(self):
        path = Path(self.tmp.name) / 'rotated.jpg'
        photo = Image.new('RGB', (210, 350))
        exif = Image.Exif()
        exif[274] = 6
        photo.save(path, exif=exif)
        with self.assertRaisesRegex(ValueError, '350x210'):
            check_image(path)

    def test_extra_root_or_segment_files_rejected(self):
        for rel in ('boards-manifest.json', 'shot-list.md', 'C01/boards-manifest.json', 'C01/C01.txt'):
            with self.subTest(rel=rel):
                p = self.root / rel
                p.write_text('not requested')
                with self.assertRaises(ValueError):
                    check(self.root)
                p.unlink()
        (self.root / 'C01/images').mkdir()
        with self.assertRaisesRegex(ValueError, 'nested'):
            check(self.root)

    def test_missing_prompt_and_missing_board_rejected(self):
        p = self.root / 'C01/C01.draft.txt'
        p.write_text('  ')
        with self.assertRaisesRegex(ValueError, 'draft.txt'):
            check(self.root)
        p.write_text('prompt')
        (self.root / 'C01/02-storyboard.png').rename(self.root / 'C01/02-other.png')
        with self.assertRaisesRegex(ValueError, 'missing storyboard'):
            check(self.root)

    def test_upload_number_gaps_and_duplicates_rejected(self):
        p = self.root / 'C01/03-product.png'
        for name in ('04-product.png', '02-product.png'):
            q = p.with_name(name)
            p.rename(q)
            with self.assertRaisesRegex(ValueError, 'unique and contiguous'):
                check(self.root)
            q.rename(p)

    def test_csv_bom_and_row_structure(self):
        p = self.root / 'shot-list.csv'
        p.write_text('S-ID,C-ID\nS01,C01', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'BOM'):
            check(self.root)
        p.write_text('S-ID,C-ID\nS01', encoding='utf-8-sig')
        with self.assertRaisesRegex(ValueError, 'consistently'):
            check(self.root)

    def test_corrupt_or_mismatched_images_rejected(self):
        path = self.root / 'C01/03-product.png'
        path.write_bytes(b'not image data')
        with self.assertRaises(OSError):
            check(self.root)
        Image.new('RGB', (400, 400)).save(path, format='JPEG')
        with self.assertRaisesRegex(ValueError, 'matching'):
            check(self.root)

    def test_unrequested_third_segment_rejected(self):
        self.segment('C03')
        with self.assertRaisesRegex(ValueError, 'C01 only'):
            check(self.root)


if __name__ == '__main__':
    unittest.main()
