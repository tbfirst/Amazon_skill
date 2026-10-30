import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'collect_competitor.py'
spec = importlib.util.spec_from_file_location('collector', SCRIPT)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class CollectorBoundaryTests(unittest.TestCase):
    def test_product_identity(self):
        self.assertEqual(collector.product_url('b012345678', 'amazon.com'), 'https://www.amazon.com/dp/B012345678')
        self.assertEqual(collector.product_url('https://www.amazon.de/gp/product/B012345678?ref=test', 'amazon.com'), 'https://www.amazon.de/dp/B012345678')

    def test_reject_non_product_or_untrusted_urls(self):
        for url in ['http://www.amazon.com/dp/B012345678', 'https://amazon.com.evil.example/dp/B012345678', 'https://www.amazon.com/s?k=chairs']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                collector.product_url(url, 'amazon.com')

    def test_media_cannot_enter_skill_package(self):
        for root in [SCRIPT.parent.parent, SCRIPT.parent.parent / 'assets', '/tmp/skills/another-skill/images']:
            with self.subTest(root=root), self.assertRaises(ValueError):
                collector.output_root(str(root))
        self.assertEqual(collector.output_root('/tmp/ordinary-project/media'), Path('/tmp/ordinary-project/media'))


if __name__ == '__main__':
    unittest.main()
