"""Offline behavior checks using synthetic catalogs and prompts; no browser/generation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).resolve().parents[1] / 'scripts' / f'{name}.py')
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


library = module('library_catalog')
summary = module('build_prompt_summary')


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.cards = [dict(id='DIM-01', title='尺寸双圆窗', category='尺寸',
                           imageTypes=['尺寸图'], productTypes=['花束'], tags=['白底'],
                           prompt='Synthetic template', promptZh='合成测试模板',
                           references=[dict(file='preview.png', kind='user-approved')]),
                      dict(id='TEST-02', title='住宅场景', imageTypes=['场景图'],
                           prompt='Synthetic scene', promptZh='合成场景', references=[])]
        (self.source / 'preview.png').write_bytes(b'synthetic preview bytes, not an actual image')

    def write(self):
        (self.source / 'prompts.json').write_text(json.dumps({'cards': self.cards}, ensure_ascii=False), encoding='utf-8')

    def test_search_filters_and_chinese(self):
        self.assertEqual(library.search_cards(self.cards, '圆窗', '尺寸图')[0]['id'], 'DIM-01')
        self.assertEqual(library.search_cards(self.cards, '圆窗', '场景图'), [])

    def test_import_preserves_source_and_hashes(self):
        self.write()
        before = (self.source / 'prompts.json').read_bytes()
        dest = self.root / 'snapshot'
        stats = library.import_catalog(self.source, dest)
        self.assertEqual(stats['cardCount'], 2)
        self.assertEqual(stats['bundledPreviewCount'], 1)
        data = library.read_json(dest / 'catalog.json')
        self.assertIn('尺寸双圆窗', (dest / 'index.md').read_text(encoding='utf-8'))
        ref = data['cards'][0]['bundledPreviews'][0]
        self.assertEqual(library.digest(dest / ref['file']), ref['sha256'])
        self.assertEqual(data['source']['sha256'], hashlib.sha256(before).hexdigest())
        self.assertEqual((self.source / 'prompts.json').read_bytes(), before)

    def test_missing_preview_is_not_reported_as_available(self):
        self.cards[0]['references'][0]['file'] = 'missing.png'
        self.write()
        result = library.import_catalog(self.source, self.root / 'snapshot')
        self.assertEqual(result['bundledPreviewCount'], 0)
        self.assertEqual(len(result['missingSelectedPreviews']), 1)

    def test_preview_cannot_escape_source(self):
        self.cards[0]['references'][0]['file'] = '../secret.png'
        self.write()
        with self.assertRaises(ValueError):
            library.import_catalog(self.source, self.root / 'snapshot')

    def test_import_never_targets_source_tree(self):
        self.write()
        for dest in [self.source, self.source / 'nested', self.root]:
            with self.assertRaises(ValueError):
                library.import_catalog(self.source, dest)

    def test_duplicate_cards_rejected(self):
        self.cards[1]['id'] = 'DIM-01'
        self.write()
        with self.assertRaises(ValueError):
            library.import_catalog(self.source, self.root / 'snapshot')

    def test_agent_index_and_english_only_recipe_need_no_translation(self):
        self.cards[0].pop('promptZh')
        self.write()
        image = dict(id='IMG-synthetic', file='unbundled-source.png', visualStatus='pending',
                     originalName='downloaded.png', observation=None)
        (self.source / 'agent-index.json').write_text(json.dumps({
            'policy':{'translationService':False}, 'images':[image]}), encoding='utf-8')
        dest = self.root / 'snapshot'
        library.import_catalog(self.source, dest)
        data = library.read_json(dest/'catalog.json')
        self.assertFalse(data['agentPolicy']['translationService'])
        self.assertEqual(data['images'][0]['visualStatus'], 'pending')
        self.assertFalse((dest/'unbundled-source.png').exists())
        results = library.search_images(data['images'], query='downloaded')
        self.assertEqual(results[0]['id'], 'IMG-synthetic')
        self.assertIsNone(results[0]['overview'])

    def test_bundled_catalog_integrity(self):
        data = library.read_json(library.DEFAULT_CATALOG)
        cards = library.check_cards(data)
        self.assertEqual(len(cards), data['cardCount'])
        refs = {r['file']: r for r in data.get('bundledAssets', [])}
        if not refs:
            refs = {r['file']: r for c in cards for r in c['bundledPreviews']}
        self.assertEqual(len(refs), data['bundledPreviewCount'])
        for relative, record in refs.items():
            self.assertEqual(library.digest(library.inside(library.DEFAULT_CATALOG.parent, relative)), record['sha256'])

    def series_source(self):
        self.write()
        raw = b'Synthetic approved image bytes; no actual photo or product claim'
        (self.source/'approved.png').write_bytes(raw)
        record = dict(id='IMG-approved', file='approved.png', sha256=hashlib.sha256(raw).hexdigest(),
                      visualStatus='observed-full', reuseEligible=True,
                      observation=dict(reuseDecision='accept', title='Synthetic detail', imageTypes=['细节图'],
                                       recipe='Synthetic whole-view plus detail instruction'))
        (self.source/'agent-index.json').write_text(json.dumps({'images':[record]}),encoding='utf-8')
        entry = dict(id='SET-synthetic',title='Synthetic plant',variant='test',requestedAsin='B000000001',
                     members=[dict(section='gallery',order=1,status='approved',imageId=record['id'],
                                   sha256=record['sha256'],file='approved.png',imageType='detail'),
                              dict(section='gallery',order=2,status='excluded-or-missing',imageId=None,
                                   file=None,imageType='scene',reason='Synthetic excluded frame')])
        (self.source/'series-index.json').write_text(json.dumps({'series':[entry]}),encoding='utf-8')
        selection=self.root/'selection.json'
        selection.write_text(json.dumps({'seriesIds':['SET-synthetic']}),encoding='utf-8')
        return selection

    def test_portable_series_preserves_order_gaps_and_approved_bytes(self):
        selection=self.series_source()
        dest=self.root/'portable'
        stats=library.import_catalog(self.source,dest,selection)
        data=library.read_json(dest/'catalog.json')
        self.assertEqual(stats['seriesCount'],1)
        self.assertEqual(stats['bundledImageCount'],1)
        first,second=data['series'][0]['members']
        self.assertEqual([first['order'],second['order']],[1,2])
        self.assertTrue(first['bundled'])
        self.assertFalse(second['bundled'])
        self.assertEqual(second['status'],'excluded-or-missing')
        image=data['images'][0]
        self.assertEqual((dest/image['file']).read_bytes(),(self.source/'approved.png').read_bytes())
        self.assertEqual(image['observation']['recipe'],'Synthetic whole-view plus detail instruction')

    def test_retired_detail_templates_are_not_reimported(self):
        self.cards.append(dict(id='DSTYLE-01',prompt='Retired synthetic wireframe',layoutSketch='assets/layouts/old.svg'))
        self.write()
        dest=self.root/'portable'
        library.import_catalog(self.source,dest)
        data=library.read_json(dest/'catalog.json')
        self.assertNotIn('DSTYLE-01',[c['id'] for c in data['cards']])
        self.assertIn('DSTYLE-01',data['retiredCardIds'])
        self.assertFalse((dest/'previews/assets/layouts').exists())

    def test_rejected_and_changed_sources_cannot_be_bundled(self):
        selection=self.series_source()
        data=library.read_json(self.source/'agent-index.json')
        data['images'][0]['observation']['reuseDecision']='reject'
        (self.source/'agent-index.json').write_text(json.dumps(data),encoding='utf-8')
        selection.write_text(json.dumps({'imageIds':['IMG-approved']}),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'not reviewed'):
            library.import_catalog(self.source,self.root/'rejected',selection)
        data['images'][0]['observation']['reuseDecision']='accept'
        (self.source/'agent-index.json').write_text(json.dumps(data),encoding='utf-8')
        (self.source/'approved.png').write_bytes(b'Changed source bytes')
        with self.assertRaisesRegex(ValueError,'hash changed'):
            library.import_catalog(self.source,self.root/'changed',selection)

    def test_portable_cli_works_after_source_is_unavailable(self):
        selection=self.series_source()
        dest=self.root/'portable'
        library.import_catalog(self.source,dest,selection)
        self.source.rename(self.root/'source-unavailable')
        command=[sys.executable,'-B','-X','utf8',library.__file__,'show','SET-synthetic',
                 '--catalog',str(dest/'catalog.json'),'--image-id','IMG-approved']
        result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout)
        self.assertEqual(Path(data['imageRoot']),dest)
        self.assertTrue(data['image']['available'])
        self.assertTrue(Path(data['image']['resolvedFile']).is_relative_to(dest))
        bad=subprocess.run(command[:-1]+['IMG-missing'],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(bad.returncode,2)

    def test_series_search_returns_compact_choices_and_positive_limit(self):
        selection=self.series_source()
        dest=self.root/'portable'
        library.import_catalog(self.source,dest,selection)
        data=library.read_json(dest/'catalog.json')
        result=library.search_series(data['series'],'plant')[0]
        self.assertEqual(result['bundledGallery'],1)
        self.assertNotIn('members',result)
        with self.assertRaises(ValueError):
            library.search_series(data['series'],limit=0)

    def test_image_search_does_not_turn_negative_constraints_into_evidence(self):
        records = [dict(id='IMG-1', file='care-infographic.png', visualStatus='observed-overview',
                        originalName='care-infographic.png', observation={
                            'overview':'White studio branch', 'layout':'Single product',
                            'limitations':'Do not add flowers or care instructions',
                            'recipe':'Never add flowers',
                            'legacyReview':{'displayEligible':False}})]
        self.assertEqual(library.search_images(records,'flowers'),[])
        self.assertEqual(library.search_images(records,'care'),[])
        self.assertEqual(library.search_images(records,'branch'), [])
        match = library.search_images(records,'branch',include_restricted=True)[0]
        self.assertTrue(match['restricted'])
        self.assertIn('care instructions',match['limitations'])

    def test_pending_image_cannot_supply_visual_evidence(self):
        records = [dict(id='IMG-2',file='download.png',originalName='download.png',
                        visualStatus='pending',observation={'overview':'Invented red flowers'})]
        self.assertEqual(library.search_images(records,'flowers'),[])
        match = library.search_images(records,'download')[0]
        self.assertIsNone(match['overview'])
        self.assertIn('Metadata only', match['selectionUse'])

    def test_null_historical_review_is_searchable(self):
        record = dict(id='IMG-3',file='plant.png',visualStatus='observed-overview',
                      observation={'overview':'Plant', 'legacyReview':None})
        self.assertFalse(library.search_images([record],'plant')[0]['restricted'])

    def test_product_scoped_aplus_and_selected_prompt_variants_survive_search_and_snapshot(self):
        identity={'id':'tree-a','label':'Light tree','reviewStatus':'reviewed'}
        variants=[dict(referenceFile='a.png',prompt='First source layout',promptZh='第一张横幅'),
                  dict(referenceFile='b.png',prompt='Second source split layout',promptZh='第二张左右分区')]
        self.cards[1].update(imageTypes=['A+图'],productKey='tree-a',principalProduct=identity,
                             sourceAsins=['B012345678'],promptZh='同一主要产品模板',promptVariants=variants)
        self.write()
        recipes=[dict(self.cards[1])]
        (self.source/'layout-recipes.json').write_text(json.dumps({'recipes':recipes}),encoding='utf-8')
        native=[{'section':'aplus-native-text','content':{'text':'Native field'}}]
        (self.source/'agent-index.json').write_text(json.dumps({'aplusNativeText':native}),encoding='utf-8')
        match=library.search_cards(self.cards,'tree-a','A+图')[0]
        self.assertEqual(match['promptVariants'],variants)
        self.assertEqual(match['principalProduct'],identity)
        self.assertEqual(match['promptZh'],'同一主要产品模板')
        self.assertEqual(library.search_recipes(recipes,'第二张')[0]['productKey'],'tree-a')
        dest=self.root/'snapshot'
        library.import_catalog(self.source,dest)
        result=library.read_json(dest/'catalog.json')
        self.assertEqual(result['cards'][1]['promptVariants'],variants)
        self.assertEqual(result['layoutRecipes'][0]['principalProduct'],identity)
        self.assertEqual(result['aplusNativeText'],native)

    def test_aplus_image_lookup_reports_unresolved_product_scope(self):
        row=dict(id='IMG-a',file='a.png',visualStatus='observed-overview',reuseEligible=True,
                 observation={'overview':'Light tree','imageTypes':['A+图']},
                 principalProducts=[],aplusTemplateEligible=False,
                 aplusTemplateScope='One visually reviewed principal product')
        match=library.search_images([row],'tree')[0]
        self.assertFalse(match['aplusTemplateEligible'])
        self.assertEqual(match['principalProducts'],[])

    def branch_recipe(self):
        return dict(id='APLUS-TREE',title='灯树',imageTypes=['A+图'],productKey='tree-a',
                    principalProduct={'id':'tree-a','reviewStatus':'reviewed'},
                    sourceImageIds=['IMG-timer','IMG-porch'],sourceCount=2,
                    prompt='Default timer prompt',promptZh='默认定时提示词',copyMode='approved-literal',
                    promptVariants={
                        'IMG-timer':dict(prompt='Independent timer prompt: verified timing only.',
                                         promptZh='完整定时图提示词',copyMode='approved-literal'),
                        'IMG-porch':dict(prompt='Independent porch scene, no timer overlay.',
                                         promptZh='完整门廊场景提示词',copyMode='none')})

    def test_recipe_search_is_compact_but_still_matches_branch_content(self):
        recipe=self.branch_recipe()
        match=library.search_recipes([recipe],'verified timing')[0]
        self.assertEqual(match['productKey'],'tree-a')
        self.assertEqual(match['variantCount'],2)
        self.assertEqual([v['imageId'] for v in match['variants']],['IMG-timer','IMG-porch'])
        serialized=json.dumps(match)
        self.assertNotIn('Independent timer prompt',serialized)
        self.assertNotIn('Default timer prompt',serialized)
        self.assertNotIn('promptVariants',match)
        with self.assertRaises(ValueError):
            library.search_recipes([recipe],limit=0)

    def test_recipe_show_selects_full_branch_without_unrelated_prompt_spill(self):
        recipe=self.branch_recipe()
        selected=library.show_recipe(recipe,'IMG-porch')
        self.assertEqual(selected['prompt'],'Independent porch scene, no timer overlay.')
        self.assertEqual(selected['promptZh'],'完整门廊场景提示词')
        self.assertEqual(selected['copyMode'],'none')
        self.assertEqual(selected['principalProduct']['id'],'tree-a')
        self.assertEqual(selected['sourceImageIds'],['IMG-porch'])
        self.assertNotIn('timer prompt',json.dumps(selected))
        self.assertNotIn('promptVariants',selected)
        self.assertIn('IMG-timer',recipe['promptVariants'])
        default=library.show_recipe(recipe)
        self.assertEqual(default['prompt'],'Default timer prompt')
        self.assertEqual(len(default['variants']),2)
        self.assertNotIn('Independent porch scene',json.dumps(default))
        with self.assertRaisesRegex(ValueError,'Unknown or unavailable image branch'):
            library.show_recipe(recipe,'IMG-missing')

    def test_cli_show_image_id_selects_branch_and_rejects_invalid_id(self):
        self.write()
        (self.source/'layout-recipes.json').write_text(json.dumps({'recipes':[self.branch_recipe()]}),encoding='utf-8')
        command=[sys.executable,'-B','-X','utf8',library.__file__,'show','APLUS-TREE',
                 '--source-root',str(self.source),'--image-id']
        selected=subprocess.run(command+['IMG-porch'],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(selected.returncode,0,selected.stderr)
        self.assertEqual(json.loads(selected.stdout)['recipe']['selectedImageId'],'IMG-porch')
        invalid=subprocess.run(command+['IMG-missing'],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(invalid.returncode,2)
        self.assertIn('Unknown or unavailable image branch',invalid.stderr)


class SummaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.entries = []
        for asset in summary.ASSETS:
            relative = f'prompts/{asset}.txt'
            p = self.root / relative
            p.parent.mkdir(exist_ok=True)
            p.write_text(f'ASSET {asset}\nExact synthetic text — 测试\n', encoding='utf-8')
            self.entries.append(dict(id=asset, status='READY', prompt=relative,
                                     references=['actual-product.jpg — identity'], condition=''))

    def write(self):
        (self.root / 'prompt-manifest.json').write_text(json.dumps({'assets': self.entries}), encoding='utf-8')

    def test_full_text_order_and_no_pdf(self):
        self.write()
        self.assertEqual(summary.compile_summary(self.root), dict(executable=11, blocked=0, total=11))
        for filename in ['all-prompts.md', 'all-prompts.txt']:
            text = (self.root / filename).read_text(encoding='utf-8')
            for asset in summary.ASSETS:
                self.assertIn((self.root / f'prompts/{asset}.txt').read_text(encoding='utf-8'), text)
            self.assertLess(text.index('DIM01'), text.index('APLUS05'))
        self.assertEqual(list(self.root.glob('*.pdf')), [])

    def test_blocked_body_excluded_and_condition_preserved(self):
        e = self.entries[0]
        e.update(status='BLOCKED', prompt='prompts/blocked/DIM01.txt', condition='Missing verified height')
        p = self.root / e['prompt']
        p.parent.mkdir()
        p.write_text('CONDITIONAL DRAFT — NOT READY TO GENERATE\nSECRET CONDITIONAL BODY', encoding='utf-8')
        self.write()
        self.assertEqual(summary.compile_summary(self.root)['blocked'], 1)
        for filename in ['all-prompts.md', 'all-prompts.txt']:
            text = (self.root / filename).read_text(encoding='utf-8')
            self.assertIn('Missing verified height', text)
            self.assertNotIn('SECRET CONDITIONAL BODY', text)

    def test_provisional_is_copyable_with_condition(self):
        self.entries[-1].update(status='PROVISIONAL', condition='Account slot review pending')
        self.write()
        summary.compile_summary(self.root)
        text = (self.root / 'all-prompts.md').read_text(encoding='utf-8')
        self.assertIn('APLUS05 — PROVISIONAL', text)
        self.assertIn('Account slot review pending', text)

    def test_duplicate_or_extra_id_rejected(self):
        self.entries[-1]['id'] = 'DIM01'
        self.write()
        with self.assertRaises(ValueError):
            summary.compile_summary(self.root)
        self.assertFalse((self.root / 'all-prompts.md').exists())

    def test_status_and_path_mismatch_rejected(self):
        self.entries[0]['prompt'] = '../outside.txt'
        self.write()
        with self.assertRaises(ValueError):
            summary.compile_summary(self.root)

    def test_unmarked_conditional_cannot_enter_collection(self):
        (self.root / 'prompts/DIM01.txt').write_text('CONDITIONAL DRAFT — NOT READY TO GENERATE\nDraft', encoding='utf-8')
        self.write()
        with self.assertRaises(ValueError):
            summary.compile_summary(self.root)

    def test_missing_condition_rejected(self):
        self.entries[0]['status'] = 'PROVISIONAL'
        self.write()
        with self.assertRaises(ValueError):
            summary.compile_summary(self.root)

    def test_nested_backticks_preserve_copy_block(self):
        (self.root / 'prompts/DIM01.txt').write_text('Literal ```text\ninside\n```\n', encoding='utf-8')
        self.write()
        summary.compile_summary(self.root)
        self.assertIn('````text\nLiteral ```text', (self.root / 'all-prompts.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
