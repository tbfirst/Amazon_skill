"""Classified local references retain identity and stay usable after moves/deletions."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import library_catalog as library
import refresh_local_library as refresh


class ClassifiedLibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.raw = b'Existing reviewed reference bytes; synthetic, not an image'
        self.sha = hashlib.sha256(self.raw).hexdigest()
        self.old = 'previews/assets/old/source.png'
        self.new = 'previews/assets/dimensions/moved.png'
        path = self.root / self.new
        path.parent.mkdir(parents=True)
        path.write_bytes(self.raw)
        self.observation = dict(title='Synthetic detail', imageTypes=['细节图'],
                                reuseDecision='accept', recipe='Historical source observation')
        self.data = dict(cardCount=1, source={'sha256':'source'},
                         cards=[dict(id='DIM-01', title='Test', imageTypes=['尺寸图'],
                                     prompt='Historical template', references=[],
                                     bundledPreviews=[dict(file=self.old, sha256=self.sha)])],
                         images=[dict(id='IMG-test', sha256=self.sha, file=self.old,
                                      bundled=True, reuseEligible=True, visualStatus='observed-full',
                                      observation=self.observation, cardIds=['DIM-01'])],
                         bundledAssets=[dict(file=self.old, sha256=self.sha, sourceFile='source.png')],
                         bundledPreviewCount=1, agentPolicy={}, selection={},
                         layoutRecipes=[], series=[dict(id='SET-test',title='test',members=[
                             dict(imageId='IMG-test',section='gallery',status='approved',bundled=True,file=self.old)])])
        self.catalog = self.root / 'catalog.json'
        self.write()
        (self.root/'classified-layouts.json').write_text(json.dumps(dict(dimensionLayouts=[
            dict(imageId='IMG-test',layoutZh='左全貌右细节',layoutEn='Whole view left, detail right.',
                 dimensionAdaptation='Bind a verified dimension to the complete view.',
                 detailAdaptation='Use a genuine close-up with supported visible labels.')
        ])),encoding='utf-8')

    def write(self):
        self.catalog.write_text(json.dumps(self.data),encoding='utf-8')

    def test_move_repairs_active_links_without_changing_source_observation(self):
        data, report = refresh.reconcile(self.catalog)
        self.assertEqual(report['bundledFiles'],1)
        self.assertEqual(data['images'][0]['file'],self.new)
        self.assertEqual(data['images'][0]['sourceFile'],self.old)
        self.assertEqual(data['images'][0]['observation'],self.observation)
        self.assertEqual(data['cards'][0]['bundledPreviews'][0]['file'],self.new)
        self.assertEqual(data['series'][0]['members'][0]['file'],self.new)
        self.assertEqual((self.root/self.new).read_bytes(),self.raw)
        self.catalog.write_text(json.dumps(data),encoding='utf-8')
        second,_=refresh.reconcile(self.catalog)
        self.assertEqual(second,data)

    def test_deleted_media_retains_searchable_history_but_is_unavailable(self):
        (self.root/self.new).unlink()
        data,_=refresh.reconcile(self.catalog)
        image=data['images'][0]
        resolved=library.resolve_image(image,self.root,portable=True)
        self.assertTrue(resolved['textSearchable'])
        self.assertFalse(resolved['localAvailable'])
        self.assertEqual(image['observation'],self.observation)
        self.assertEqual(data['cards'][0]['bundledPreviews'],[])
        self.assertIsNone(data['series'][0]['members'][0]['file'])

    def test_same_reference_supports_both_search_roles_and_independent_prompts(self):
        data,_=refresh.reconcile(self.catalog)
        for image_type in ['尺寸图','细节图']:
            self.assertEqual(library.search_cards(data['cards'],image_type=image_type)[0]['id'],'DIM-01')
            self.assertEqual(library.search_images(data['images'],image_type=image_type)[0]['id'],'IMG-test')
        branches=data['images'][0]['planningPrompts']
        self.assertEqual(set(branches),{'DIM01','DETAIL01'})
        self.assertNotEqual(branches['DIM01']['prompt'],branches['DETAIL01']['prompt'])
        for role,branch in branches.items():
            self.assertEqual(branch['role'],role)
            self.assertEqual(branch['sourceImageId'],'IMG-test')
            self.assertEqual(branch['referenceFile'],self.new)
        self.assertEqual(data['images'][0]['observation']['imageTypes'],['细节图'])

    def test_unknown_bytes_fail_without_mutating_existing_catalog(self):
        before=self.catalog.read_bytes()
        (self.root/self.new).write_bytes(b'Unknown changed bytes')
        with self.assertRaisesRegex(ValueError,'Unreviewed'):
            refresh.reconcile(self.catalog)
        self.assertEqual(self.catalog.read_bytes(),before)

    def enable_grounded_catalog(self):
        (self.root/'reviewed-layouts.json').write_text(json.dumps({'layouts':[]}), encoding='utf-8')
        data,_=refresh.reconcile(self.catalog)
        self.catalog.write_text(json.dumps(data),encoding='utf-8')
        return data

    def test_grounded_refresh_keeps_reviewed_text_after_preview_deletion(self):
        data=self.enable_grounded_catalog()
        self.assertEqual(data['cards'][0]['promptSourceImageId'],'IMG-test')
        self.assertNotIn('prompt',data['cards'][0])
        second,_=refresh.reconcile(self.catalog)
        self.assertEqual(second,data)
        (self.root/self.new).unlink()
        data,_=refresh.reconcile(self.catalog)
        self.assertEqual(len(data['images']),1)
        self.assertEqual(len(data['cards']),1)
        self.assertFalse(data['images'][0]['bundled'])
        self.assertTrue(data['images'][0]['planningPrompts']['DIM01']['textOnlyUsable'])
        self.assertIsNone(data['images'][0]['planningPrompts']['DIM01']['referenceFile'])
        self.assertFalse(data['cards'][0]['bundledPreviews'])

    def test_grounded_cli_discloses_missing_media_but_keeps_reviewed_text(self):
        self.enable_grounded_catalog()
        (self.root/self.new).unlink()
        for source_id in ['IMG-test','DIM-01']:
            result=subprocess.run([sys.executable,'-B',str(SCRIPTS/'library_catalog.py'),
                'show',source_id,'--catalog',str(self.catalog)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            shown=json.loads(result.stdout)
            self.assertFalse(shown['image']['localAvailable'])
            self.assertTrue(shown['image']['planningPrompts']['DIM01']['textOnlyUsable'])
            self.assertIsNone(shown['image']['planningPrompts']['DIM01']['referenceFile'])

    def test_grounded_cli_does_not_attach_changed_media(self):
        self.enable_grounded_catalog()
        (self.root/self.new).write_bytes(b'Changed image')
        result=subprocess.run([sys.executable,'-B',str(SCRIPTS/'library_catalog.py'),
            'show','IMG-test','--catalog',str(self.catalog)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        shown=json.loads(result.stdout)
        self.assertFalse(shown['image']['localAvailable'])
        self.assertIsNone(shown['image']['planningPrompts']['DIM01']['referenceFile'])

    def test_curated_text_template_survives_refresh_without_any_reference(self):
        self.enable_grounded_catalog()
        pack={'revision':'test','templates':[dict(id='KEEP-test',title='Explicit edit',
            templateKind='operation',taskEn='Preserve geometry while replacing the selected background.',
            summaryZh='保留商品几何，只换已选背景',copyMode='none',sourceEvidence=[],
            qualityReview={'decision':'retain-rewritten'})]}
        (self.root/'curated-templates.json').write_text(json.dumps(pack),encoding='utf-8')
        (self.root/self.new).unlink()
        data,_=refresh.reconcile(self.catalog)
        self.catalog.write_text(json.dumps(data),encoding='utf-8')
        card=next(c for c in data['cards'] if c['id']=='KEEP-test')
        self.assertTrue(card['prompt'])
        self.assertFalse(card['bundledPreviews'])
        second,_=refresh.reconcile(self.catalog)
        self.assertEqual(second,data)

        command=[sys.executable,'-B',str(SCRIPTS/'library_catalog.py'),'search',
                 '--kind','template','--query','KEEP-test','--catalog',str(self.catalog)]
        found=json.loads(subprocess.check_output(command,text=True))
        self.assertEqual([c['id'] for c in found['matches']],['KEEP-test'])
        visible=json.loads(subprocess.check_output(command+['--available-only'],text=True))
        self.assertEqual(visible['matches'],[])

    def test_curated_rejection_or_out_id_cannot_be_reintroduced(self):
        self.enable_grounded_catalog()
        for card in [dict(id='KEEP-test',qualityReview={'decision':'reject'}),
                     dict(id='OUT-S01',qualityReview={'decision':'retain-rewritten'})]:
            (self.root/'curated-templates.json').write_text(json.dumps(
                {'revision':'test','templates':[card]}),encoding='utf-8')
            with self.assertRaises(ValueError):
                refresh.reconcile(self.catalog)

    def test_duplicate_bytes_across_categories_need_resolution(self):
        target=self.root/'previews/assets/Aplus/duplicate.png'
        target.parent.mkdir(parents=True)
        target.write_bytes(self.raw)
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            refresh.reconcile(self.catalog)

    def test_cli_selects_the_requested_branch_and_actual_media(self):
        data,_=refresh.reconcile(self.catalog)
        self.catalog.write_text(json.dumps(data),encoding='utf-8')
        cmd=[sys.executable,'-B','-X','utf8',str(SCRIPTS/'library_catalog.py'),'show','IMG-test',
             '--catalog',str(self.catalog),'--asset-role','DETAIL01']
        result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',check=True)
        shown=json.loads(result.stdout)
        self.assertEqual(shown['planningTemplate']['role'],'DETAIL01')
        self.assertEqual(Path(shown['image']['resolvedFile']),self.root/self.new)
        self.assertFalse(shown['image']['observedThisRun'])
        (self.root/self.new).unlink()
        result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
        self.assertNotEqual(result.returncode,0)

    def test_selection_rebuild_does_not_restore_excluded_media_or_old_paths(self):
        source=self.root/'source'
        source.mkdir()
        (source/'source.png').write_bytes(self.raw)
        other=b'Excluded historical image'
        (source/'excluded.png').write_bytes(other)
        cards=[dict(id='DIM-01',title='Test',imageTypes=['尺寸图'],prompt='source',
                    references=[dict(file='source.png')])]
        (source/'prompts.json').write_text(json.dumps({'cards':cards}),encoding='utf-8')
        record=dict(id='IMG-test',sha256=self.sha,file='source.png',observation=self.observation,
                    reuseEligible=True,visualStatus='observed-full')
        excluded=dict(record,id='IMG-excluded',file='excluded.png',sha256=hashlib.sha256(other).hexdigest())
        (source/'agent-index.json').write_text(json.dumps({'images':[record,excluded]}),encoding='utf-8')
        data,_=refresh.reconcile(self.catalog)
        selection=data['selection']
        selection['imageIds'].append('IMG-excluded')
        selected=self.root/'selected.json'
        selected.write_text(json.dumps(selection),encoding='utf-8')
        dest=self.root/'rebuilt'
        library.import_catalog(source,dest,selected)
        rebuilt=library.read_json(dest/'catalog.json')
        self.assertTrue((dest/self.new).is_file())
        self.assertFalse((dest/'previews/source.png').exists())
        self.assertFalse((dest/'previews/excluded.png').exists())
        self.assertFalse(next(i for i in rebuilt['images'] if i['id']=='IMG-excluded')['bundled'])


if __name__ == '__main__':
    unittest.main()
