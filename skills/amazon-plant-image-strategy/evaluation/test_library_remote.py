"""Actual private HTTPS behavior, atomic recovery, and offline fallback."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from remote_fixture import PrivateServer, channel_file, source_config, synthetic_master, tls_files, SCRIPTS
import library_build as builder
import library_catalog as catalog
from library_remote import LibraryClient, LibraryError, resource_lock


class RemoteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.master = self.root / 'master'
        self.images = synthetic_master(self.master)
        self.publication = self.root / 'publication'
        self.policy = self.root / 'policy.json'
        self.rules = dict(schemaVersion=1, defaults=dict(status='published', scopes=['text', 'preview', 'original']), images={})
        builder.write_json(self.policy, self.rules)
        self.report = builder.build_library(self.master, self.publication, 'test.1', self.policy)
        cert, key = tls_files(self.root / 'tls')
        self.index = PrivateServer(self.publication, cert, key, 'synthetic-index')
        self.addCleanup(self.index.close)
        self.media = PrivateServer(self.publication, cert, key, 'synthetic-media')
        self.addCleanup(self.media.close)
        self.config = self.root / 'source.json'
        self.settings = source_config(self.config, self.index, self.media, cert)
        channel_file(self.publication, 'test.1', self.index.origin)
        self.cache = self.root / 'consumer-cache'
        self.env = patch.dict('os.environ', dict(PLANT_TEST_INDEX_TOKEN='synthetic-index', PLANT_TEST_MEDIA_TOKEN='synthetic-media'))
        self.env.start()
        self.addCleanup(self.env.stop)

    def client(self):
        return LibraryClient(self.config, self.cache)

    def cli(self, *args):
        result = subprocess.run([sys.executable, '-S', '-B', '-X', 'utf8', str(SCRIPTS / 'library_catalog.py'), *args,
                                 '--config', str(self.config), '--cache-dir', str(self.cache)],
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_full_index_sync_fetch_detail_and_image_on_demand_over_private_https(self):
        client = self.client()
        result = client.sync(strict=True)
        self.assertEqual(result['imageCount'], 2)
        self.assertEqual(sum(self.media.counts.values()), 0)
        self.assertFalse(any('/records/' in p for p in self.index.counts))
        self.master.rename(self.root / 'author-disk-disconnected')
        search = self.cli('search', '--kind', 'image')
        self.assertEqual(len(search['images']), 2)
        self.assertTrue(all(i['fetchable'] and not i['available'] for i in search['images']))
        chosen = self.images[0]['id']
        detail = self.cli('show', chosen)
        self.assertEqual(detail['image']['observation']['recipe'], 'Owned synthetic example 1')
        self.assertEqual(sum('/records/' in p for p in self.index.counts), 1)
        fetched = self.cli('fetch', chosen, '--size', 'preview')
        self.assertTrue(Path(fetched['items'][0]['resolvedFile']).is_file())
        self.assertFalse(fetched['items'][0]['observedThisRun'])
        local = self.cli('search', '--kind', 'image', '--available-only')
        self.assertEqual([i['id'] for i in local['images']], [chosen])

    def test_origin_credentials_are_separate_and_not_stored_in_cache_or_output(self):
        client = self.client()
        report = client.sync(strict=True)
        report['fetch'] = client.fetch([self.images[0]['id']], size='original')
        self.assertTrue(all(auth == 'Bearer synthetic-index' for _, auth, _ in self.index.auth_seen))
        self.assertTrue(all(auth == 'Bearer synthetic-media' for _, auth, _ in self.media.auth_seen))
        for file in client.root.rglob('*.json'):
            self.assertNotIn('synthetic-index', file.read_text(encoding='utf-8'))
            self.assertNotIn('synthetic-media', file.read_text(encoding='utf-8'))
        self.assertNotIn('synthetic-index', json.dumps(report))

    def test_etag_304_and_repeated_image_fetch_reuse_cache(self):
        client = self.client()
        first = client.sync(strict=True)
        index_count = sum(self.index.counts.values())
        second = self.client().sync(strict=True)
        self.assertEqual(second['status'], 'not-modified')
        self.assertEqual(sum(self.index.counts.values()), index_count + 1)
        self.assertEqual(second['manifestHash'], first['manifestHash'])
        one = self.client().fetch([self.images[0]['id']], size='preview')
        count = sum(self.media.counts.values())
        two = self.client().fetch([self.images[0]['id']], size='preview')
        self.assertEqual(two['items'][0]['status'], 'cached')
        self.assertEqual(sum(self.media.counts.values()), count)
        self.assertEqual(one['items'][0]['resolvedFile'], two['items'][0]['resolvedFile'])

    def test_preview_and_original_are_separate_and_hash_exact(self):
        self.client().sync(strict=True)
        preview = self.client().fetch([self.images[0]['id']], size='preview')['items'][0]
        original = self.client().fetch([self.images[0]['id']], size='original')['items'][0]
        self.assertNotEqual(preview['resolvedFile'], original['resolvedFile'])
        self.assertEqual(catalog.digest(Path(original['resolvedFile'])), self.images[0]['sha256'])
        self.assertNotEqual(catalog.digest(Path(preview['resolvedFile'])), self.images[0]['sha256'])

    def test_network_failure_uses_old_index_then_bundled_when_no_cache(self):
        client = self.client()
        first = client.sync(strict=True)
        self.index.overrides['/channels/private-test.json'] = dict(status=503)
        failed = self.client().sync()
        self.assertEqual(failed['status'], 'cached-fallback')
        self.assertEqual(failed['manifestHash'], first['manifestHash'])
        empty = LibraryClient(self.config, self.root / 'empty-cache').sync()
        self.assertEqual(empty['status'], 'bundled-fallback')
        self.assertTrue(Path(empty['catalog']).is_file())

    def test_offline_cached_image_and_detail_work_but_missing_item_is_reported(self):
        client = self.client()
        client.sync(strict=True)
        data, _, path, entry = client.snapshot()
        client.detail(data['images'][0], path, entry)
        client.fetch([data['images'][0]['id']], size='original')
        self.index.close()
        self.media.close()
        self.assertEqual(self.client().sync(offline=True)['status'], 'offline-cache')
        result = self.client().fetch([data['images'][0]['id'], data['images'][1]['id']], size='original', offline=True)
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['failures'][0]['id'], data['images'][1]['id'])
        shown = self.cli('show', data['images'][0]['id'], '--offline')
        self.assertTrue(shown['image']['originalAvailable'])

    def test_bad_hash_leaves_no_partial_asset_and_other_candidate_succeeds(self):
        client = self.client()
        client.sync(strict=True)
        data, manifest, _, _ = client.snapshot()
        asset = data['images'][0]['media']['original']
        self.media.overrides['/versions/test.1/' + asset['path']] = dict(body=b'not the expected image')
        result = client.fetch([i['id'] for i in data['images']], size='original')
        self.assertEqual(result['status'], 'partial')
        self.assertFalse(client.media_path(asset).exists())
        self.assertFalse(any(client.root.rglob('.download-*')))

    def test_series_fetch_keeps_source_order_and_excludes_rejected_slot(self):
        client = self.client()
        client.sync(strict=True)
        result = client.fetch(series_id='SET-test', size='preview', limit=2)
        self.assertEqual([i['id'] for i in result['items']], [i['id'] for i in self.images[:2]])
        bad = client.fetch([self.images[2]['id']], size='original')
        self.assertEqual(bad['status'], 'failed')

    def test_redirect_recomputes_auth_and_rejects_untrusted_destinations(self):
        client = self.client()
        client.sync(strict=True)
        data, _, _, _ = client.snapshot()
        asset = data['images'][0]['media']['original']
        path = '/versions/test.1/' + asset['path']
        self.media.overrides[path] = dict(status=302, headers={'Location': self.index.origin + path})
        result = client.fetch([data['images'][0]['id']], size='original')
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(self.index.auth_seen[-1][1], 'Bearer synthetic-index')
        asset2 = data['images'][1]['media']['original']
        self.media.overrides['/versions/test.1/' + asset2['path']] = dict(status=302, headers={'Location': 'https://untrusted.invalid/asset'})
        denied = client.fetch([data['images'][1]['id']], size='original')
        self.assertEqual(denied['status'], 'failed')
        self.assertIn('trusted', denied['failures'][0]['reason'])

    def test_candidate_and_missing_credentials_do_not_silently_succeed(self):
        self.settings['allowCandidate'] = False
        builder.write_json(self.config, self.settings)
        with self.assertRaisesRegex(LibraryError, 'Candidate'):
            self.client().sync(strict=True)
        self.settings['allowCandidate'] = True
        builder.write_json(self.config, self.settings)
        with patch.dict('os.environ', {'PLANT_TEST_INDEX_TOKEN': ''}):
            result = self.client().sync()
        self.assertEqual(result['status'], 'bundled-fallback')
        self.assertIn('environment variable', result['reason'])

    def test_http_and_path_escape_and_unknown_origin_are_rejected(self):
        client = self.client()
        with self.assertRaisesRegex(LibraryError, 'HTTPS'):
            client.check_url('http://127.0.0.1/test')
        with self.assertRaisesRegex(LibraryError, 'trusted'):
            client.check_url('https://unknown.invalid/test')
        with self.assertRaises(ValueError):
            client.locator(dict(path='../outside.json'), self.index.origin + '/manifest.json')
        with self.assertRaises(LibraryError):
            client.locator(dict(path='https://unknown.invalid/file'), self.index.origin + '/manifest.json')

    def test_github_raw_accept_headers_and_pinned_ref_do_not_leak_to_media(self):
        self.settings['requestHeaders'] = {self.index.origin: {'Accept': 'application/vnd.github.raw+json'}}
        builder.write_json(self.config, self.settings)
        client = self.client()
        self.assertEqual(client.headers_for(self.index.origin + '/test')['Accept'], 'application/vnd.github.raw+json')
        self.assertNotIn('Accept', client.headers_for(self.media.origin + '/test'))
        url = client.locator(dict(path='records/abc.json'), self.index.origin + '/versions/test.1/manifest.json?ref=fixed-commit')
        self.assertEqual(url, self.index.origin + '/versions/test.1/records/abc.json?ref=fixed-commit')

    def test_tls_verification_cannot_be_disabled_by_omitting_the_private_ca(self):
        del self.settings['caFile']
        builder.write_json(self.config, self.settings)
        result = self.client().sync()
        self.assertEqual(result['status'], 'bundled-fallback')
        self.assertIn('TLS', result['reason'])

    def test_future_schema_update_keeps_the_previous_compatible_index(self):
        client = self.client()
        first = client.sync(strict=True)
        path = self.publication / 'versions/test.1/manifest.json'
        manifest = catalog.read_json(path)
        manifest['schemaVersion'] = 99
        builder.write_json(path, manifest)
        channel_file(self.publication, 'test.1', self.index.origin)
        result = self.client().sync()
        self.assertEqual(result['status'], 'cached-fallback')
        self.assertEqual(result['manifestHash'], first['manifestHash'])

    def test_bad_new_manifest_preserves_current_state_and_repairs_corrupt_cached_index(self):
        client = self.client()
        first = client.sync(strict=True)
        data, manifest, manifest_path, _ = client.snapshot()
        index_file = manifest_path.parent / manifest['files']['searchIndex']['path']
        index_file.write_bytes(b'corrupt')
        repair = self.client().sync(strict=True)
        self.assertEqual(repair['manifestHash'], first['manifestHash'])
        channel = catalog.read_json(self.publication / 'channels/private-test.json')
        channel['manifest']['sha256'] = '0' * 64
        builder.write_json(self.publication / 'channels/private-test.json', channel)
        result = self.client().sync()
        self.assertEqual(result['status'], 'cached-fallback')
        self.assertEqual(result['manifestHash'], first['manifestHash'])

    def test_withdrawal_blocks_previously_cached_image_and_recipe(self):
        client = self.client()
        client.sync(strict=True)
        client.fetch([self.images[0]['id']], size='original')
        self.rules['images'][self.images[0]['id']] = dict(status='withdrawn', reason='Synthetic withdrawal')
        builder.write_json(self.policy, self.rules)
        builder.build_library(self.master, self.publication, 'test.2', self.policy)
        channel_file(self.publication, 'test.2', self.index.origin)
        client = self.client()
        client.sync(strict=True)
        result = client.fetch([self.images[0]['id']], size='original', version='test.1')
        self.assertEqual(result['status'], 'failed')
        search = self.cli('search', '--kind', 'image', '--library-version', 'test.1')
        self.assertNotIn(self.images[0]['id'], [i['id'] for i in search['images']])

    def test_new_prompt_version_reuses_original_without_media_redownload(self):
        client = self.client()
        client.sync(strict=True)
        client.fetch([self.images[0]['id']], size='original')
        before = sum(self.media.counts.values())
        source = catalog.read_json(self.master / 'agent-index.json')
        source['images'][0]['observation']['recipe'] = 'Revised owned synthetic prompt'
        source['images'][0]['promptRevision'] = 2
        builder.write_json(self.master / 'agent-index.json', source)
        builder.build_library(self.master, self.publication, 'test.2', self.policy)
        channel_file(self.publication, 'test.2', self.index.origin)
        client = self.client()
        client.sync(strict=True)
        repeated = client.fetch([self.images[0]['id']], size='original')
        self.assertEqual(repeated['items'][0]['status'], 'cached')
        self.assertEqual(sum(self.media.counts.values()), before)

    def test_budget_and_same_resource_lock_are_enforced(self):
        client = self.client()
        client.sync(strict=True)
        with resource_lock(client.root, 'sync'):
            with self.assertRaisesRegex(LibraryError, 'busy'):
                client.sync(strict=True)
        client.max_session = 1
        result = client.fetch([self.images[0]['id']], size='original')
        self.assertEqual(result['status'], 'failed')
        self.assertIn('budget', result['failures'][0]['reason'])


if __name__ == '__main__':
    unittest.main()
