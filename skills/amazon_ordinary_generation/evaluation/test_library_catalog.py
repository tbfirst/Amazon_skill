"""Offline catalog behavior: scope, role branches and portable retrieval."""

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/library_catalog.py'
spec = importlib.util.spec_from_file_location('ordinary_library', SCRIPT)
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)


class LibraryCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = library.load_catalog()

    def test_complete_unique_task_migration(self):
        cards = self.catalog['templates']
        self.assertEqual(len(cards), 200)
        self.assertEqual(len({c['provenance']['sourceTemplateId'] for c in cards}), 200)
        self.assertEqual(len({c['taskEn'] for c in cards}), 200)
        self.assertTrue(all(c['textOnlyUsable'] and not c['mediaRequired'] for c in cards))
        self.assertTrue(all(not c['generationTested'] for c in cards))

    def test_search_honors_group_and_role(self):
        results = library.search(self.catalog, kind='template', design_group='dimensions-details', limit=300, asset_role='DETAIL01')
        self.assertTrue(results)
        self.assertTrue(all('dimensions-details' in c['designGroups'] and 'DETAIL01' in c['targetRoles'] for c in results))
        self.assertFalse(any('MAIN01' in c['targetRoles'] for c in results))
        exact = library.search(self.catalog, query='ORD-LIGHT-02', kind='template')
        self.assertEqual([c['id'] for c in exact], ['ORD-LIGHT-02'])

    def test_dim_and_detail_share_source_but_have_distinct_instructions(self):
        dim = library.show(self.catalog, 'ORD-DETAIL-07', 'DIM01')
        detail = library.show(self.catalog, 'ORD-DETAIL-07', 'DETAIL01')
        self.assertEqual(dim['taskEn'], detail['taskEn'])
        self.assertIn(dim['taskEn'], dim['planningTemplate'])
        self.assertIn(detail['taskEn'], detail['planningTemplate'])
        self.assertNotEqual(dim['planningTemplate'], detail['planningTemplate'])

    def test_invalid_role_and_implicit_main_are_rejected(self):
        for ident, role in [('ORD-MAIN-01', 'SCENE01'), ('ORD-INFO-06', 'DIM01'), ('ORD-DETAIL-07', 'TYPO')]:
            with self.subTest(ident=ident, role=role), self.assertRaises(ValueError):
                library.show(self.catalog, ident, role)
        with self.assertRaises(ValueError):
            library.show(self.catalog, 'missing')

    def test_visual_direction_reaches_every_planning_template(self):
        for card in self.catalog['templates']:
            with self.subTest(template=card['id']):
                result = library.show(self.catalog, card['id'])
                self.assertTrue(card['artDirectionEn'].strip())
                self.assertIn(card['artDirectionEn'], result['planningTemplate'])
                self.assertIn(card['taskEn'], result['planningTemplate'])

    def test_selected_profiles_do_not_leak_other_material_or_form_branches(self):
        cases = [('ORD-DETAIL-02', 'DETAIL01', 'soft', 'textile'),
                 ('ORD-AMZ-93', 'APLUS01', 'packaged', 'printed'),
                 ('ORD-DETAIL-04', 'DETAIL01', 'rigid', 'transparent')]
        for ident, role, form, material in cases:
            result = library.show(self.catalog, ident, role, form, material)
            self.assertEqual(result['selectedProductForm'], form)
            self.assertEqual(result['selectedMaterial'], material)
            for collection, selected in [('productProfiles', form), ('materialProfiles', material)]:
                for key, profile in self.catalog[collection].items():
                    self.assertEqual(profile['promptEn'] in result['planningTemplate'], key == selected)

    def test_profile_selection_is_optional_and_invalid_selection_fails(self):
        result = library.show(self.catalog, 'ORD-DETAIL-07', 'DETAIL01')
        self.assertIsNone(result['selectedProductForm'])
        self.assertIsNone(result['selectedMaterial'])
        for collection in ('productProfiles', 'materialProfiles'):
            for profile in self.catalog[collection].values():
                self.assertNotIn(profile['promptEn'], result['planningTemplate'])
        for kwargs in ({'product_form': 'unknown'}, {'material': 'unknown'}):
            with self.assertRaises(ValueError):
                library.show(self.catalog, 'ORD-DETAIL-07', **kwargs)
        with self.assertRaises(ValueError):
            library.show(self.catalog, 'ORD-SET-SOFT', product_form='soft')

    def test_legacy_external_catalog_can_omit_profile_and_direction_extensions(self):
        data = copy.deepcopy(self.catalog)
        for collection in ('productProfiles', 'materialProfiles'):
            del data[collection]
        for card in data['templates']:
            card.pop('artDirectionEn')
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'catalog.json'
            file.write_text(json.dumps(data), encoding='utf-8')
            legacy = library.load_catalog(file)
            self.assertTrue(library.show(legacy, 'ORD-DETAIL-07')['planningTemplate'])
            with self.assertRaises(ValueError):
                library.show(legacy, 'ORD-DETAIL-07', product_form='soft')

    def test_malformed_profile_fails_at_load(self):
        for bad in ([], {'rigid': None}, {'rigid': {'title': 'Rigid', 'promptEn': ''}}):
            data = copy.deepcopy(self.catalog)
            data['productProfiles'] = bad
            with tempfile.TemporaryDirectory() as tmp:
                file = Path(tmp) / 'catalog.json'
                file.write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaises(ValueError):
                    library.load_catalog(file)

    def test_ordered_recipes_preserve_default_budget(self):
        expected = ['DIM01', 'DETAIL01', *[f'SCENE{i:02}' for i in range(1, 5)], *[f'APLUS{i:02}' for i in range(1, 6)]]
        recipes = library.search(self.catalog, kind='series', limit=100)
        self.assertEqual(len(recipes), 8)
        for recipe in recipes:
            self.assertEqual([s['assetId'] for s in recipe['slots']], expected)
            for slot in recipe['slots']:
                self.assertTrue(library.show(self.catalog, slot['templateId'], slot['assetId'])['planningTemplate'])

    def test_duplicate_and_dangling_template_refs_fail(self):
        for mutate in ('duplicate', 'missing'):
            data = copy.deepcopy(self.catalog)
            if mutate == 'duplicate':
                data['templates'].append(data['templates'][0])
            else:
                data['series'][0]['slots'][0]['templateId'] = 'ORD-NOT-FOUND'
            with tempfile.TemporaryDirectory() as tmp:
                file = Path(tmp) / 'catalog.json'
                file.write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaises(ValueError):
                    library.load_catalog(file)

    def test_portable_cli_without_plant_skill_or_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'isolated'
            (root / 'scripts').mkdir(parents=True)
            (root / 'assets/reference-library').mkdir(parents=True)
            shutil.copyfile(SCRIPT, root / 'scripts/library_catalog.py')
            shutil.copyfile(library.DEFAULT_CATALOG, root / 'assets/reference-library/catalog.json')
            result = subprocess.run([sys.executable, str(root / 'scripts/library_catalog.py'), 'check'], cwd=tmp, text=True, encoding='utf-8', capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['templates'], 200)
            result = subprocess.run([sys.executable, str(root / 'scripts/library_catalog.py'), 'show', 'ORD-DETAIL-07', '--asset-role', 'DETAIL01'], cwd=tmp, text=True, encoding='utf-8', capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('planningTemplate', json.loads(result.stdout))
            result = subprocess.run([sys.executable, str(root / 'scripts/library_catalog.py'), 'show', 'ORD-DETAIL-02', '--asset-role', 'DETAIL01', '--product-form', 'soft', '--material', 'textile'], cwd=tmp, text=True, encoding='utf-8', capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            selected = json.loads(result.stdout)
            self.assertIn(self.catalog['productProfiles']['soft']['promptEn'], selected['planningTemplate'])
            self.assertEqual(selected['selectedMaterial'], 'textile')


if __name__ == '__main__':
    unittest.main()
