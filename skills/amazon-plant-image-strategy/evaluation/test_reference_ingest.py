"""Local ingestion invariants: real images, duplicate sources and honest review states."""
import importlib.util
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from PIL import Image

spec = importlib.util.spec_from_file_location('ingest', Path(__file__).resolve().parents[1]/'scripts/reference_ingest.py')
ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest)


class IngestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.library = self.root/'library'
        (self.library/'assets').mkdir(parents=True)
        self.source = self.root/'capture'
        self.source.mkdir()
        ingest.write_json(self.library/'prompts.json', {'cards':[]})

    def image(self, path, color='green', compress_level=6):
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new('RGB', (16, 20), color).save(path, compress_level=compress_level)

    def test_renamed_duplicate_has_one_record_and_combined_origin(self):
        self.image(self.library/'assets/original.png')
        (self.source/'renamed.png').write_bytes((self.library/'assets/original.png').read_bytes())
        a = ingest.scan(self.library, [self.source])
        self.assertEqual(a['stats']['newOriginals'], 0)
        self.assertEqual(a['stats']['exactDuplicates'], 1)
        index = ingest.build_index(self.library, a)
        self.assertEqual(index['imageCount'], 1)
        self.assertEqual(index['pendingCount'], 1)
        self.assertEqual(len(index['images'][0]['aliases']), 1)

    def test_reencoding_deduplicates_pixels_not_just_filename(self):
        self.image(self.library/'assets/a.png', compress_level=0)
        self.image(self.source/'different.png', compress_level=9)
        self.image(self.source/'other-color.png', color='red')
        a = ingest.scan(self.library, [self.source])
        self.assertEqual(a['stats']['pixelDuplicates'], 1)
        self.assertEqual(a['stats']['newOriginals'], 1)
        self.assertEqual(len(a['images']), 2)

    def test_sync_is_idempotent_and_keeps_original_filename(self):
        self.image(self.source/'new-product.png')
        index = ingest.build_index(self.library, ingest.scan(self.library, [self.source]))
        first = index['images'][0]
        second = ingest.build_index(self.library, ingest.scan(self.library, [self.source]))
        self.assertEqual(second['imageCount'], 1)
        self.assertEqual(second['images'][0]['id'], first['id'])
        self.assertEqual(second['images'][0]['originalName'], 'new-product.png')
        self.assertEqual(len(second['images'][0]['aliases']), 1)
        self.assertEqual(len(list((self.library/'assets/collected').iterdir())), 1)

    def test_scraper_manifest_provenance_and_thumbnails_excluded(self):
        self.image(self.source/'B012345678/White/01_MAIN.png')
        self.image(self.source/'html/thumbs/01_MAIN.png')
        ingest.write_json(self.source/'B012345678/manifest.json', {
            'asin':'B012345678', 'scrapedAt':'2026-10-19', 'variants':[
                {'asin':'B087654321','color':'White','dir':'White','files':[
                    {'n':1,'variant':'MAIN','file':'01_MAIN.png','hiRes':'https://example.test/original.png'}]}]})
        a = ingest.scan(self.library, [self.source])
        self.assertEqual(a['stats']['sourceFiles'], 1)
        origin = a['images'][0]['aliases'][0]
        self.assertEqual(origin['variantAsin'], 'B087654321')
        self.assertEqual(origin['position'], 'MAIN')
        self.assertEqual(origin['order'], 1)
        self.assertEqual(origin['url'], 'https://example.test/original.png')

    def test_empty_annotation_does_not_promote_download_to_observed(self):
        self.image(self.source/'new.png')
        a = ingest.scan(self.library, [self.source])
        index = ingest.build_index(self.library, a, {'images':{}})
        self.assertEqual(index['observedCount'], 0)
        self.assertEqual(index['images'][0]['visualStatus'], 'pending')

    def test_aplus_only_manifest_keeps_module_occurrences_and_native_text_separate(self):
        folder = self.source/'B012345678'
        self.image(folder/'Aplus/01.png')
        self.image(folder/'Other/card.png', color='blue')
        identity = {'id':'tree-a', 'label':'Light tree', 'reviewStatus':'confirmed'}
        occurrences = [dict(sourceAsin='B012345678', sourceUrl='https://example.test/dp/B012345678',
                            moduleKind='product_description', moduleIndex=i, imageIndex=1,
                            extraction='dom') for i in [1, 3]]
        ingest.write_json(folder/'manifest.json', {
            'schemaVersion':2, 'asin':'B012345678', 'scrapedAt':'2026-10-20',
            'aplus':[dict(n=1, dir='Aplus', file='01.png', assetKey='asset-a',
                          url='https://example.test/a.png', principalProduct=identity,
                          provenance=occurrences)],
            'aplusOther':[dict(n=1, dir='Other', file='card.png', role='other',
                               provenance=[dict(moduleKind='brand_story', moduleIndex=2, imageIndex=1)])],
            'aplusNativeText':[dict(moduleKind='product_description', moduleIndex=1,
                                    text='Source native title, not image copy')]})
        audit = ingest.scan(self.library,[self.source])
        by_name = {r['originalName']:r for r in audit['images']}
        origin = by_name['01.png']['aliases'][0]
        self.assertEqual(origin['section'], 'aplus')
        self.assertEqual([p['moduleIndex'] for p in origin['occurrences']], [1,3])
        self.assertEqual(by_name['card.png']['aliases'][0]['collectionRole'], 'other')
        digest = by_name['01.png']['sha256']
        result = ingest.build_index(self.library,audit,{'images':{digest:self.observation(digest)}})
        accepted = next(r for r in result['images'] if r['sha256'] == digest)
        self.assertTrue(accepted['aplusTemplateEligible'])
        self.assertEqual(accepted['principalProducts'][0]['id'], 'tree-a')
        self.assertEqual(result['aplusNativeText'][0]['content']['text'], 'Source native title, not image copy')
        self.assertNotIn('aplusNativeText', accepted)

    def test_legacy_aplus_does_not_infer_family_identity_or_verified_module_order(self):
        folder = self.source/'B012345678'
        self.image(folder/'Aplus/01.png')
        ingest.write_json(folder/'manifest.json', {
            'asin':'B012345678','parentAsin':'B099999999', 'aplus':[
                {'n':4,'file':'01.png','url':'https://example.test/a.png'}]})
        audit=ingest.scan(self.library,[self.source])
        digest=audit['images'][0]['sha256']
        origin=audit['images'][0]['aliases'][0]
        self.assertEqual(origin['order'],4)
        self.assertIsNone(origin['occurrences'][0]['moduleIndex'])
        self.assertIsNone(origin['occurrences'][0]['sourceAsin'])
        result=ingest.build_index(self.library,audit,{'images':{digest:self.observation(digest)}})
        self.assertTrue(result['images'][0]['reuseEligible'])
        self.assertFalse(result['images'][0]['aplusTemplateEligible'])

    def test_aplus_resync_preserves_prior_module_occurrences(self):
        folder=self.source/'B012345678'
        self.image(folder/'Aplus/01.png')
        doc={'asin':'B012345678','aplus':[dict(file='01.png',provenance=[
            dict(sourceAsin='B012345678',moduleKind='product_description',moduleIndex=1,imageIndex=1)])]}
        ingest.write_json(folder/'manifest.json',doc)
        first=ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        doc['aplus'][0]['provenance'][0]['moduleIndex']=3
        ingest.write_json(folder/'manifest.json',doc)
        second=ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        self.assertEqual(first['imageCount'],second['imageCount'])
        self.assertEqual([p['moduleIndex'] for p in second['images'][0]['aliases'][0]['occurrences']],[1,3])
        third=ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        self.assertEqual(len(third['images'][0]['aliases'][0]['occurrences']),2)

    def test_conflicting_confirmed_products_share_media_bytes_but_not_template_identity(self):
        for asin, identity in [('B012345678','product-a'),('B087654321','product-b')]:
            folder=self.source/asin
            self.image(folder/'Aplus/01.png')
            ingest.write_json(folder/'manifest.json',{'asin':asin,'aplus':[dict(
                file='01.png',principalProduct={'id':identity,'reviewStatus':'confirmed'})]})
        audit=ingest.scan(self.library,[self.source])
        self.assertEqual(len(audit['images']),1)
        digest=audit['images'][0]['sha256']
        result=ingest.build_index(self.library,audit,{'images':{digest:self.observation(digest)}})
        row=result['images'][0]
        self.assertEqual(len(row['aliases']),2)
        self.assertEqual({p['id'] for p in row['principalProducts']},{'product-a','product-b'})
        self.assertFalse(row['aplusTemplateEligible'])

    def test_visual_identity_can_scope_legacy_aplus_without_manifest_metadata(self):
        self.image(self.source/'old.png')
        audit=ingest.scan(self.library,[self.source])
        digest=audit['images'][0]['sha256']
        note=self.observation(digest)
        note.update(imageTypes=['A+图'],principalProduct={
            'id':'reviewed-tree','label':'Tree','reviewStatus':'reviewed'})
        result=ingest.build_index(self.library,audit,{'images':{digest:note}})
        self.assertTrue(result['images'][0]['aplusTemplateEligible'])

    def test_manifest_path_cannot_assign_product_scope_to_sibling_directory(self):
        folder=self.source/'B012345678'
        folder.mkdir()
        self.image(self.source/'other.png')
        ingest.write_json(folder/'manifest.json',{'asin':'B012345678','aplus':[
            {'dir':'..','file':'other.png'}]})
        audit=ingest.scan(self.library,[self.source])
        self.assertTrue(audit['warnings'])
        self.assertNotIn('section',audit['images'][0]['aliases'][0])

    def test_incomplete_or_wrong_hash_observation_rejected(self):
        self.image(self.source/'new.png')
        a = ingest.scan(self.library, [self.source])
        digest = a['images'][0]['sha256']
        with self.assertRaises(ValueError):
            ingest.build_index(self.library, a, {'images':{digest:{'status':'observed-overview'}}})
        self.assertFalse((self.library/'assets/collected').exists())
        self.assertFalse((self.library/'agent-index.json').exists())
        with self.assertRaises(ValueError):
            ingest.build_index(self.library, ingest.scan(self.library,[self.source]),
                               {'images':{digest:{'sha256':'wrong','status':'pending'}}})

    def observation(self, digest):
        return dict(sha256=digest, status='observed-overview', reviewMethod='Synthetic fixture',
                    imageTypes=['detail'], overview='A branch', layout='Single macro',
                    copyIntegration='No text', lighting='Soft left key', shadows='Right shadow',
                    transferable='Macro framing', limitations='Synthetic test only', recipe='One macro')

    def test_alpha_difference_is_not_a_pixel_duplicate(self):
        Image.new('RGBA', (16,20), (20,40,60,0)).save(self.source/'transparent.png')
        Image.new('RGBA', (16,20), (20,40,60,255)).save(self.source/'opaque.png')
        self.assertEqual(ingest.scan(self.library,[self.source])['stats']['newOriginals'], 2)

    def test_approved_only_admission_does_not_copy_rejected_or_unreviewed_bytes(self):
        for name,color in [('yes.png','red'),('no.png','blue'),('pending.png','green')]:
            self.image(self.source/name,color=color)
        audit=ingest.scan(self.library,[self.source])
        digests={r['originalName']:r['sha256'] for r in audit['images']}
        approved=self.observation(digests['yes.png'])
        approved['reuseDecision']='accept'
        rejected=self.observation(digests['no.png'])
        rejected.update(reuseDecision='reject',qualityReasons=['Distracting clutter'])
        filtered,notes,excluded=ingest.screen_new_sources(audit,{'images':{
            digests['yes.png']:approved,digests['no.png']:rejected}})
        result=ingest.build_index(self.library,filtered,notes)
        self.assertEqual(result['imageCount'],1)
        self.assertEqual(result['eligibleCount'],1)
        self.assertEqual(set(excluded),{digests['no.png'],digests['pending.png']})
        self.assertEqual(len(list((self.library/'assets/collected').iterdir())),1)
        self.assertEqual(len(audit['images']),3)

    def test_existing_archive_is_preserved_but_rejected_reference_is_not_eligible(self):
        self.image(self.library/'assets/old.png')
        audit=ingest.scan(self.library,[])
        digest=audit['images'][0]['sha256']
        note=self.observation(digest)
        note['reuseDecision']='reject'
        filtered,notes,excluded=ingest.screen_new_sources(audit,{'images':{digest:note}})
        result=ingest.build_index(self.library,filtered,notes)
        self.assertTrue((self.library/'assets/old.png').is_file())
        self.assertFalse(result['images'][0]['reuseEligible'])
        self.assertFalse(excluded)

    def test_partial_observations_preserve_previous_records_and_audit(self):
        self.image(self.source/'one.png')
        a = ingest.scan(self.library,[self.source])
        untouched = deepcopy(a)
        first = a['images'][0]['sha256']
        ingest.build_index(self.library,a,{'images':{first:self.observation(first)}})
        self.assertEqual(a, untouched)
        self.image(self.source/'two.png', color='blue')
        a = ingest.scan(self.library,[self.source])
        second = next(r['sha256'] for r in a['images'] if r['sha256'] != first)
        ingest.build_index(self.library,a,{'images':{second:self.observation(second)}})
        saved = ingest.read_json(self.library/'visual-observations.json')['images']
        self.assertEqual(set(saved), {first,second})
        again = ingest.build_index(self.library,ingest.scan(self.library,[self.source]),{'images':{}})
        self.assertEqual(again['observedCount'], 2)

    def test_sync_preserves_hash_bound_visual_navigation_but_not_source_classification(self):
        self.image(self.source/'one.png')
        initial=ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        row=initial['images'][0]
        navigation=dict(imageId=row['id'],sha256=row['sha256'],primary='combined',
                        imageTypes=['细节+尺寸图'],reviewMethod='Synthetic prior visual review')
        row['navigationClassification']=navigation
        initial['classificationPolicy']={'version':'fixture','aplusAspectRange':[2.2,2.7]}
        ingest.write_json(self.library/'agent-index.json',initial)
        folder=self.source/'B012345678'
        self.image(folder/'White/two.png',color='red')
        ingest.write_json(folder/'manifest.json',{'asin':'B012345678','variants':[dict(
            dir='White',files=[dict(file='two.png',navigationClassification=navigation)])]})
        result=ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        old=next(r for r in result['images'] if r['sha256']==row['sha256'])
        fresh=next(r for r in result['images'] if r['sha256']!=row['sha256'])
        self.assertEqual(old['navigationClassification'],navigation)
        self.assertEqual(result['classificationPolicy'],initial['classificationPolicy'])
        self.assertNotIn('navigationClassification',fresh)
        old['navigationClassification']['sha256']='stale-hash'
        ingest.write_json(self.library/'agent-index.json',result)
        again=ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        self.assertNotIn('navigationClassification',next(r for r in again['images'] if r['id']==row['id']))

    def test_rejected_reference_cannot_lose_restriction_on_new_review(self):
        self.image(self.source/'one.png')
        a = ingest.scan(self.library,[self.source])
        digest = a['images'][0]['sha256']
        note = self.observation(digest)
        note['legacyReview'] = {'displayEligible':False}
        ingest.build_index(self.library,a,{'images':{digest:note}})
        result = ingest.build_index(self.library,ingest.scan(self.library,[self.source]),
                                   {'images':{digest:self.observation(digest)}})
        self.assertFalse(result['images'][0]['observation']['legacyReview']['displayEligible'])

    def test_null_historical_review_can_be_resynced(self):
        self.image(self.source/'one.png')
        a = ingest.scan(self.library,[self.source])
        digest = a['images'][0]['sha256']
        note = self.observation(digest)
        note['legacyReview'] = None
        ingest.build_index(self.library,a,{'images':{digest:note}})
        result = ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        self.assertEqual(result['observedCount'],1)

    def test_malformed_manifest_does_not_discard_valid_images(self):
        self.image(self.source/'one.png')
        (self.source/'manifest.json').write_text('{broken', encoding='utf-8')
        a = ingest.scan(self.library,[self.source])
        self.assertEqual(a['stats']['newOriginals'], 1)
        self.assertTrue(a['warnings'])
        ingest.write_json(self.source/'manifest.json', {'variants':[None, {'files':None}]})
        self.assertEqual(len(ingest.scan(self.library,[self.source])['warnings']), 2)

    def test_pixel_alias_retains_template_link(self):
        self.image(self.library/'assets/a.png', compress_level=0)
        self.image(self.library/'assets/b.png', compress_level=9)
        ingest.write_json(self.library/'prompts.json', {'cards':[
            {'id':'DIM-1', 'references':[{'file':'assets/b.png'}]}]})
        result = ingest.build_index(self.library,ingest.scan(self.library,[]))
        self.assertEqual(result['imageCount'],1)
        self.assertEqual(result['images'][0]['cardIds'],['DIM-1'])

    def test_missing_indexed_original_leaves_catalog_untouched(self):
        self.image(self.source/'one.png')
        result = ingest.build_index(self.library,ingest.scan(self.library,[self.source]))
        before = (self.library/'agent-index.json').read_bytes()
        (self.library/result['images'][0]['file']).unlink()
        with self.assertRaisesRegex(ValueError,'missing or changed'):
            ingest.build_index(self.library,ingest.scan(self.library,[]))
        self.assertEqual((self.library/'agent-index.json').read_bytes(),before)

    def test_corrupt_image_sheet_retains_pending_placeholder(self):
        (self.source/'broken.png').write_bytes(b'not an image')
        a = ingest.scan(self.library,[self.source])
        ingest.contact_sheets(a,self.root/'sheets')
        self.assertTrue((self.root/'sheets/sheet-01.jpg').is_file())
        result = ingest.build_index(self.library,a)
        self.assertEqual(result['pendingCount'],1)


if __name__ == '__main__':
    unittest.main()
