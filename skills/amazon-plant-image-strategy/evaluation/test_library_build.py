"""Publication and text/media independence checks with synthetic, owned test images."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
builder = importlib.import_module('library_build')
library = importlib.import_module('library_catalog')


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'master'
        self.source.mkdir()
        self.output = self.root / 'build'
        self.policy = self.root / 'policy.json'
        self.rules = dict(schemaVersion=1, defaults=dict(status='published', scopes=['text']), images={})
        self.images = []
        for number, color in enumerate(['green', 'red', 'blue'], 1):
            path = self.source / f'{number}.png'
            Image.new('RGB', (64, 96), color).save(path)
            checksum = library.digest(path)
            self.images.append(dict(id='IMG-' + checksum[:16], sha256=checksum, file=path.name,
                                    width=64, height=96, visualStatus='observed-full', reuseEligible=number != 3,
                                    observation=dict(title='Synthetic plant', imageTypes=['细节图'],
                                                     overview='One synthetic plant detail', recipe='Synthetic prompt ' + str(number),
                                                     reuseDecision='accept' if number != 3 else 'reject')))
        self.cards = [dict(id='TEST-01', prompt='Synthetic template'), dict(id='DSTYLE-01', prompt='Retired')]
        self.recipes = [dict(id='LAYOUT-test', sourceImageIds=[i['id'] for i in self.images],
                             prompt='Shared synthetic prompt', promptVariants={i['id']: dict(prompt='Branch ' + i['id']) for i in self.images})]
        self.series = [dict(id='SET-test', title='Synthetic plant', members=[
            dict(section='gallery', order=n, status='approved', imageId=i['id'], sha256=i['sha256'])
            for n, i in enumerate(self.images, 1)])]
        self.save()

    def save(self):
        for name, data in [('prompts.json', dict(cards=self.cards)), ('agent-index.json', dict(images=self.images)),
                           ('layout-recipes.json', dict(recipes=self.recipes)), ('series-index.json', dict(series=self.series))]:
            builder.write_json(self.source / name, data)
        builder.write_json(self.policy, self.rules)

    def build(self, version='2026.10.22.1'):
        return builder.build_library(self.source, self.output, version, self.policy)

    def cli(self, *args):
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(SCRIPTS / 'library_catalog.py'), *args],
                                capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_complete_text_collection_without_selection_or_source_disk(self):
        before = {p.name: p.read_bytes() for p in self.source.iterdir()}
        report = self.build()
        self.assertEqual(report['counts']['images'], 2)
        self.assertEqual(report['counts']['cards'], 1)
        self.assertEqual(report['mediaFiles'], 0)
        self.assertFalse(report['stableChanged'])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.source.iterdir()})
        self.source.rename(self.root / 'disconnected-master')
        result = self.cli('search', '--manifest', report['manifest'], '--kind', 'image', '--limit', '10')
        self.assertEqual(len(result['images']), 2)
        self.assertTrue(all(i['textSearchable'] and not i['localAvailable'] and not i['fetchable'] for i in result['images']))
        selected = self.cli('show', self.images[1]['id'], '--manifest', report['manifest'])
        self.assertEqual(selected['image']['observation']['recipe'], 'Synthetic prompt 2')
        self.assertIsNone(selected['image']['resolvedFile'])
        self.assertFalse(selected['image']['observedThisRun'])

    def test_preview_original_hashes_are_independent_and_original_exact(self):
        self.rules['images'][self.images[0]['id']] = dict(scopes=['text', 'preview', 'original'])
        self.save()
        report = self.build()
        result = self.cli('show', self.images[0]['id'], '--manifest', report['manifest'])
        image = result['image']
        self.assertTrue(image['previewAvailable'] and image['originalAvailable'])
        self.assertNotEqual(image['media']['preview']['sha256'], image['media']['original']['sha256'])
        self.assertEqual(Path(image['resolvedFile']).read_bytes(), (self.source / '1.png').read_bytes())
        self.assertEqual(builder.verify_manifest(report['manifest'])['mediaFiles'], 2)

    def test_withdrawal_filters_recipe_branches_and_marks_series_gap(self):
        self.rules['images'][self.images[1]['id']] = dict(status='withdrawn', reason='Synthetic withdrawal')
        self.save()
        report = self.build()
        data, manifest = builder.load_manifest(report['manifest'])
        self.assertEqual(data['layoutRecipes'][0]['sourceImageIds'], [self.images[0]['id']])
        self.assertEqual(set(data['layoutRecipes'][0]['promptVariants']), {self.images[0]['id']})
        members = data['series'][0]['members']
        self.assertEqual([m['order'] for m in members], [1, 2, 3])
        self.assertEqual([m['published'] for m in members], [True, False, False])
        revocations = builder.checked_json(Path(report['manifest']).parent, manifest['files']['revocations'])
        self.assertEqual(revocations['images'][0]['id'], self.images[1]['id'])

    def test_bad_source_hash_aborts_without_version_or_stable(self):
        (self.source / '1.png').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'hash changed'):
            self.build()
        self.assertFalse((self.output / 'versions/2026.10.22.1').exists())
        self.assertFalse((self.output / 'channels/stable.json').exists())

    def test_existing_version_cannot_be_overwritten(self):
        report = self.build()
        before = Path(report['manifest']).read_bytes()
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.build()
        self.assertEqual(Path(report['manifest']).read_bytes(), before)

    def test_prompt_revision_keeps_image_identity_and_changes_record_hash(self):
        first = self.build()
        old, _ = builder.load_manifest(first['manifest'])
        self.images[0]['observation']['recipe'] = 'Revised synthetic prompt'
        self.images[0]['promptRevision'] = 2
        self.save()
        second = self.build('2026.10.22.2')
        new, _ = builder.load_manifest(second['manifest'])
        old_image = next(i for i in old['images'] if i['id'] == self.images[0]['id'])
        new_image = next(i for i in new['images'] if i['id'] == self.images[0]['id'])
        self.assertEqual(old_image['sha256'], new_image['sha256'])
        self.assertNotEqual(old_image['record']['sha256'], new_image['record']['sha256'])

    def test_hosting_split_has_no_images_in_metadata_and_keeps_exact_media(self):
        self.rules['images'][self.images[0]['id']] = dict(scopes=['text', 'preview', 'original'])
        self.save()
        report = self.build()
        output = self.root / 'hosting'
        prepared = builder.prepare_hosting(report['manifest'], output)
        self.assertEqual(prepared['mediaFiles'], 2)
        self.assertFalse(any(p.suffix in {'.png', '.webp', '.jpg'} for p in (output / 'metadata').rglob('*')))
        self.assertTrue(any(catalog.suffix == '.png' for catalog in (output / 'media').rglob('*')))
        for asset in (output / 'media').rglob('*'):
            if asset.is_file():
                self.assertEqual(library.digest(asset), asset.stem)
        with self.assertRaisesRegex(ValueError, 'new directory'):
            builder.prepare_hosting(report['manifest'], output)

    def test_private_channel_has_expected_hash_without_stable_or_credentials(self):
        report = self.build()
        output = self.root / 'private-channel.json'
        builder.private_channel(report['manifest'], 'https://index.example.invalid/version/manifest.json', output)
        channel = library.read_json(output)
        self.assertEqual(channel['manifest']['sha256'], library.digest(Path(report['manifest'])))
        self.assertEqual(channel['audience'], 'private-test')
        with self.assertRaisesRegex(ValueError, 'HTTPS'):
            builder.private_channel(report['manifest'], 'https://secret:token@example.invalid/manifest.json', self.root/'bad.json')

    def test_incompatible_client_and_changed_local_media_are_not_available(self):
        self.rules['images'][self.images[0]['id']] = dict(scopes=['text', 'original'])
        self.save()
        report = self.build()
        data, _ = builder.load_manifest(report['manifest'])
        record = data['images'][0]
        root = Path(report['manifest']).parent
        original = root / record['media']['original']['path']
        original.write_bytes(b'corrupt cached image')
        resolved = library.resolve_image(record, root)
        self.assertFalse(resolved['localAvailable'])
        self.assertIsNone(resolved['resolvedFile'])
        manifest = library.read_json(report['manifest'])
        manifest['minSkillVersion'] = '99.0.0'
        builder.write_json(Path(report['manifest']), manifest)
        with self.assertRaisesRegex(ValueError, 'newer skill'):
            builder.load_manifest(report['manifest'])

    def test_policy_cannot_override_rejection_or_missing_product_identity(self):
        self.images[1].update(aplusTemplateEligible=True, principalProducts=[])
        self.rules['images'][self.images[2]['id']] = dict(scopes=['text', 'preview', 'original'])
        self.save()
        report = self.build()
        self.assertEqual(report['counts']['images'], 1)
        self.assertEqual(report['mediaFiles'], 0)

    def test_unknown_policy_id_and_scope_fail_instead_of_silently_ignoring(self):
        self.rules['images']['IMG-typo'] = dict(scopes=['text'])
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unknown images'):
            self.build()
        self.rules['images'] = {self.images[0]['id']: dict(scopes=['text', 'unrecognized'])}
        self.save()
        with self.assertRaisesRegex(ValueError, 'scopes'):
            self.build()

    def test_manifest_corruption_and_future_schema_are_rejected(self):
        report = self.build()
        manifest_path = Path(report['manifest'])
        index = manifest_path.parent / 'search-index.json'
        raw = index.read_bytes()
        index.write_bytes(raw + b' ')
        with self.assertRaisesRegex(ValueError, 'integrity'):
            builder.load_manifest(manifest_path)
        index.write_bytes(raw)
        manifest = library.read_json(manifest_path)
        manifest['schemaVersion'] = 200
        builder.write_json(manifest_path, manifest)
        with self.assertRaisesRegex(ValueError, 'Unsupported'):
            builder.load_manifest(manifest_path)

    def test_path_escape_and_duplicate_id_are_rejected(self):
        self.images[0]['file'] = '../outside.png'
        self.save()
        with self.assertRaisesRegex(ValueError, 'outside library'):
            self.build()
        self.images[0]['file'] = '1.png'
        self.images[1]['id'] = self.images[0]['id']
        self.save()
        with self.assertRaisesRegex(ValueError, 'Duplicate image'):
            self.build()

    def test_portable_search_does_not_require_local_image(self):
        catalog = self.root / 'catalog.json'
        builder.write_json(catalog, dict(schemaVersion=2, cards=self.cards[:1], images=self.images,
                                        layoutRecipes=self.recipes, series=self.series))
        result = self.cli('search', '--catalog', str(catalog), '--kind', 'all', '--limit', '10')
        self.assertEqual(len(result['images']), 2)
        self.assertEqual(len(result['recipes']), 1)
        self.assertFalse(any(i['available'] for i in result['images']))
        local = self.cli('search', '--catalog', str(catalog), '--kind', 'image', '--available-only')
        self.assertEqual(local['images'], [])
        selected = self.cli('show', 'LAYOUT-test', '--image-id', self.images[1]['id'], '--catalog', str(catalog))
        self.assertEqual(selected['recipe']['selectedImageId'], self.images[1]['id'])
        self.assertFalse(selected['referenceImages'][0]['available'])

    def test_text_series_branch_is_readable_but_wrong_image_is_rejected(self):
        report = self.build()
        image_id = self.images[1]['id']
        result = self.cli('show', 'SET-test', '--image-id', image_id, '--manifest', report['manifest'])
        self.assertEqual(result['image']['id'], image_id)
        self.assertFalse(result['image']['available'])
        bad = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'library_catalog.py'), 'show', 'SET-test',
                              '--image-id', self.images[2]['id'], '--manifest', report['manifest']], capture_output=True)
        self.assertEqual(bad.returncode, 2)


if __name__ == '__main__':
    unittest.main()
