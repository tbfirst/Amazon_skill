"""Build and verify an immutable reference-library candidate; never upload or switch stable."""
import argparse
import copy
import hashlib
import json
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
import urllib.parse

from library_catalog import (check_cards, digest, filter_recipe, inside, read_json,
                             retired, reusable)

SCHEMA = 1
KIND = 'amazon-plant-reference-library'
SKILL_VERSION = '1.11.0'
SCOPES = {'text', 'preview', 'original'}


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return dict(path=path.name, sha256=digest(path), bytes=path.stat().st_size)


def descriptor(root, path):
    return dict(path=path.relative_to(root).as_posix(), sha256=digest(path), bytes=path.stat().st_size)


def clean_paths(value):
    """Retain provenance without publishing the author's absolute filesystem paths."""
    if isinstance(value, dict):
        return {k: clean_paths(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean_paths(v) for v in value]
    if isinstance(value, str) and (re.match(r'^[A-Za-z]:[\\/]', value) or value.startswith('/')):
        return None
    return value


def publication(policy, category, identity):
    value = dict(policy.get('defaults', {}))
    value.update(policy.get(category, {}).get(identity, {}))
    if value.get('status') not in {'published', 'draft', 'withdrawn'}:
        raise ValueError(f'Invalid publication status: {identity}')
    scopes = value.get('scopes')
    if not isinstance(scopes, list) or not set(scopes).issubset(SCOPES):
        raise ValueError(f'Invalid publication scopes: {identity}')
    if value['status'] == 'published' and 'text' not in scopes:
        raise ValueError(f'Published records require text scope: {identity}')
    return value


def validate_policy(policy, sources):
    if policy.get('schemaVersion') != 1:
        raise ValueError('Unsupported publication policy schema')
    if set(policy) - {'schemaVersion', 'description', 'defaults', 'images', 'cards', 'recipes'}:
        raise ValueError('Unknown publication policy category')
    publication(policy, 'images', '__defaults__')
    for category, ids in sources.items():
        for identity in policy.get(category, {}):
            if identity not in ids:
                raise ValueError(f'Unknown {category} publication ID: {identity}')
            publication(policy, category, identity)


def identity_ready(record):
    if record.get('aplusTemplateEligible') is False:
        return False
    if record.get('aplusTemplateEligible') is True:
        products = record.get('principalProducts') or []
        return (len(products) == 1 and products[0].get('reviewStatus') in {'reviewed', 'confirmed'}
                and bool(products[0].get('id')))
    return True


def read_image(path):
    # Pillow is a build/verification dependency, not a text-search dependency.
    from PIL import Image
    with Image.open(path) as image:
        image.load()
        return dict(width=image.width, height=image.height, format=image.format)


def build_media(record, source, stage, scopes, base_url):
    from PIL import Image, ImageOps
    path = inside(source, record['file'])
    if digest(path) != record.get('sha256'):
        raise ValueError(f'Source image hash changed: {record["id"]}')
    info = read_image(path)
    if (record.get('width') and info['width'] != record['width']) or (record.get('height') and info['height'] != record['height']):
        raise ValueError(f'Source image dimensions changed: {record["id"]}')
    media = {}
    if 'original' in scopes:
        extensions = {'JPEG': '.jpg', 'PNG': '.png', 'WEBP': '.webp'}
        if info['format'] not in extensions:
            raise ValueError(f'Unsupported original format: {info["format"]}')
        target = stage / 'originals' / record['sha256'][:2] / (record['sha256'] + extensions[info['format']])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        media['original'] = dict(descriptor(stage, target), **info)
    if 'preview' in scopes:
        # Keep the whole frame and transparency; this is not a crop or an original replacement.
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail((1000, 1000))
            alpha = 'A' in image.getbands() or 'transparency' in image.info
            image = image.convert('RGBA' if alpha else 'RGB')
            preview = stage / 'preview.tmp.webp'
            image.save(preview, 'WEBP', quality=82, method=4)
            checksum = digest(preview)
            target = stage / 'previews' / checksum[:2] / (checksum + '.webp')
            target.parent.mkdir(parents=True, exist_ok=True)
            preview.replace(target)
            media['preview'] = dict(descriptor(stage, target), width=image.width, height=image.height, format='WEBP')
    for asset in media.values():
        if base_url:
            asset['url'] = base_url.rstrip('/') + '/' + asset['path']
    return media


def checked_json(root, entry):
    path = inside(root, entry['path'])
    if path.stat().st_size != entry['bytes'] or digest(path) != entry['sha256']:
        raise ValueError(f'File integrity check failed: {entry["path"]}')
    return read_json(path)


def check_manifest_header(manifest):
    if manifest.get('kind') != KIND or manifest.get('schemaVersion') != SCHEMA:
        raise ValueError('Unsupported reference-library manifest schema/kind')
    def version(value):
        if not isinstance(value, str) or not re.fullmatch(r'\d+\.\d+\.\d+', value):
            raise ValueError('Invalid skill compatibility version')
        return tuple(map(int, value.split('.')))
    if version(manifest['minSkillVersion']) > version(SKILL_VERSION):
        raise ValueError('Library requires a newer skill version')


def load_manifest(path):
    path = Path(path).resolve()
    manifest = read_json(path)
    check_manifest_header(manifest)
    root = path.parent
    files = manifest['files']
    index = checked_json(root, files['searchIndex'])
    cards = checked_json(root, files['cards'])['cards']
    recipes = checked_json(root, files['recipes'])['recipes']
    series = checked_json(root, files['series'])['series']
    return dict(schemaVersion='published-1', cards=cards, images=index['images'],
                layoutRecipes=recipes, series=series, libraryVersion=manifest['libraryVersion'],
                manifestHash=digest(path), agentPolicy=manifest.get('agentPolicy', {})), manifest


def verify_manifest(path):
    data, manifest = load_manifest(path)
    root = Path(path).resolve().parent
    for entry in manifest['files'].values():
        checked_json(root, entry)
    ids = [r['id'] for r in data['images']]
    if len(set(ids)) != len(ids):
        raise ValueError('Duplicate published image ID')
    by_id = {}
    media_count = 0
    for summary in data['images']:
        record = checked_json(root, summary['record'])
        if record['id'] != summary['id'] or record['sha256'] != summary['sha256']:
            raise ValueError('Search index/detail identity mismatch')
        if not re.fullmatch(r'[0-9a-f]{64}', record['sha256']) or record['id'] != 'IMG-' + record['sha256'][:16]:
            raise ValueError('Published image ID does not match its content hash')
        if not reusable(record) or not identity_ready(record) or record['publication']['status'] != 'published':
            raise ValueError('Restricted record in published index')
        by_id[record['id']] = record
        if record.get('media', {}) != summary.get('media', {}):
            raise ValueError('Search index/detail media mismatch')
        for kind, asset in record.get('media', {}).items():
            if kind not in record['publication']['scopes']:
                raise ValueError('Media exceeds publication scope')
            file = inside(root, asset['path'])
            if file.stat().st_size != asset['bytes'] or digest(file) != asset['sha256']:
                raise ValueError('Media integrity check failed')
            if kind == 'original' and asset['sha256'] != record['sha256']:
                raise ValueError('Original image identity mismatch')
            info = read_image(file)
            if any(info[k] != asset[k] for k in ['width', 'height', 'format']):
                raise ValueError('Media metadata mismatch')
            media_count += 1
    for recipe in data['layoutRecipes']:
        if not recipe['sourceImageIds'] or not set(recipe['sourceImageIds']).issubset(by_id):
            raise ValueError('Recipe refers to unpublished source')
        variants = recipe.get('promptVariants') or {}
        branch_ids = set(variants) if isinstance(variants, dict) else {v['imageId'] for v in variants}
        if not branch_ids.issubset(recipe['sourceImageIds']):
            raise ValueError('Recipe branch refers to another source')
    for series in data['series']:
        for member in series['members']:
            if member.get('published') and (member.get('imageId') not in by_id or member.get('status') != 'approved'):
                raise ValueError('Series member is not a published approved source')
    if manifest['counts']['images'] != len(by_id):
        raise ValueError('Manifest coverage count mismatch')
    return dict(libraryVersion=manifest['libraryVersion'], images=len(by_id),
                cards=len(data['cards']), recipes=len(data['layoutRecipes']),
                series=len(data['series']), mediaFiles=media_count, verified=True)


def build_library(source_root, output, version, policy_path, base_url=None):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}', version):
        raise ValueError('Invalid library version')
    if base_url and not re.match(r'^https://[^/]+/', base_url):
        raise ValueError('base-url must be an HTTPS directory for this immutable version')
    source, output = Path(source_root).resolve(), Path(output).resolve()
    if source == output or output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError('Build output must be separate from source library')
    target = output / 'versions' / version
    if target.exists():
        raise ValueError('Immutable library version already exists; choose a new version')
    inputs = ['prompts.json', 'agent-index.json', 'layout-recipes.json', 'series-index.json']
    input_hashes = {f: digest(source / f) for f in inputs}
    data, knowledge, layouts, sets = [read_json(source / f) for f in inputs]
    policy_hash = digest(policy_path)
    policy = read_json(policy_path)
    images = knowledge['images']
    image_ids = [i['id'] for i in images]
    if len(set(image_ids)) != len(image_ids) or len({i['sha256'] for i in images}) != len(images):
        raise ValueError('Duplicate image identity/hash in source library')
    for record in images:
        if not re.fullmatch(r'[0-9a-f]{64}', record.get('sha256', '')) or record['id'] != 'IMG-' + record['sha256'][:16]:
            raise ValueError(f'Image ID does not match its content hash: {record["id"]}')
    cards = check_cards(data)
    recipes = layouts['recipes']
    for name, rows in [('cards', cards), ('recipes', recipes), ('series', sets['series'])]:
        if len({r['id'] for r in rows}) != len(rows):
            raise ValueError(f'Duplicate {name} IDs')
    validate_policy(policy, dict(images=set(image_ids), cards={c['id'] for c in cards},
                                 recipes={r['id'] for r in recipes}))
    decisions, accepted, excluded = {}, [], []
    for record in images:
        p = publication(policy, 'images', record['id'])
        decisions[record['id']] = p
        reason = ('visual-review' if not reusable(record) else 'principal-product' if not identity_ready(record)
                  else 'publication-scope' if p['status'] != 'published' or 'text' not in p['scopes'] else None)
        if reason:
            excluded.append(dict(id=record['id'], reason=reason, publication=p))
        else:
            accepted.append(record)
    published_ids = {r['id'] for r in accepted}
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.' + version + '.staging-', dir=target.parent)).resolve()
    try:
        summaries = []
        for original in accepted:
            record = clean_paths(copy.deepcopy(original))
            record['publication'] = decisions[record['id']]
            record['media'] = build_media(original, source, stage, record['publication']['scopes'], base_url)
            record.update(file=None, bundled=False, recordRevision=record.get('recordRevision', 1),
                          promptRevision=record.get('promptRevision', 1))
            # The detailed record is content addressed independently of its image identity.
            raw = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
            checksum = hashlib.sha256(raw).hexdigest()
            record_path = stage / 'records' / checksum[:2] / (checksum + '.json')
            record_path.parent.mkdir(parents=True, exist_ok=True)
            record_path.write_bytes(raw)
            summary = {k: copy.deepcopy(record.get(k)) for k in [
                'id', 'sha256', 'file', 'visualStatus', 'reuseEligible', 'principalProducts',
                'aplusTemplateEligible', 'aplusTemplateScope', 'cardIds', 'publication', 'media']}
            observation = record.get('observation') or {}
            summary['observation'] = {k: observation[k] for k in [
                'title', 'imageTypes', 'overview', 'layout', 'lighting', 'shadows', 'reviewMethod',
                'limitations', 'reuseDecision'] if k in observation}
            summary['record'] = descriptor(stage, record_path)
            summaries.append(summary)
        final_cards = []
        for card in cards:
            p = publication(policy, 'cards', card['id'])
            if retired(card) or p['status'] != 'published' or 'text' not in p['scopes']:
                continue
            c = clean_paths(copy.deepcopy(card))
            # Card preview files are not implicitly licensed by a text publication rule.
            c.update(reference=None, references=[], bundledPreviews=[], layoutSketch=None, publication=p)
            final_cards.append(c)
        final_recipes = []
        for recipe in recipes:
            p = publication(policy, 'recipes', recipe['id'])
            filtered = filter_recipe(recipe, published_ids)
            if filtered['sourceImageIds'] and p['status'] == 'published' and 'text' in p['scopes']:
                filtered['publication'] = p
                final_recipes.append(clean_paths(filtered))
        final_series = clean_paths(copy.deepcopy(sets['series']))
        by_id = {i['id']: i for i in images}
        for series in final_series:
            for member in series['members']:
                identity = member.get('imageId')
                if identity and identity not in by_id:
                    raise ValueError(f'Unknown series image: {identity}')
                if identity and member.get('sha256') and member['sha256'] != by_id[identity]['sha256']:
                    raise ValueError('Series/image hash mismatch')
                member.update(file=None, published=identity in published_ids and member.get('status') == 'approved')
                if not member['published']:
                    member['publicationReason'] = member.get('reason') or 'Not in published collection'
        files = {}
        payloads = dict(searchIndex=('search-index.json', dict(images=summaries)),
                        cards=('cards.json', dict(cards=final_cards)),
                        recipes=('recipes.json', dict(recipes=final_recipes)),
                        series=('series.json', dict(series=final_series)),
                        revocations=('revocations.json', dict(images=[dict(id=i, **p) for i, p in decisions.items() if p['status'] == 'withdrawn'])),
                        coverage=('coverage.json', dict(sourceImages=len(images), publishedImages=len(accepted), excluded=excluded,
                                                       publicationPolicy=policy)))
        for name, (filename, payload) in payloads.items():
            path = stage / filename
            write_json(path, payload)
            files[name] = descriptor(stage, path)
        if input_hashes != {f: digest(source / f) for f in inputs}:
            raise ValueError('Source snapshot changed during build; retry from a frozen source')
        if policy_hash != digest(policy_path):
            raise ValueError('Publication policy changed during build; retry')
        counts = dict(images=len(accepted), cards=len(final_cards), recipes=len(final_recipes), series=len(final_series),
                      previewImages=sum('preview' in i['media'] for i in summaries),
                      originalImages=sum('original' in i['media'] for i in summaries), excludedImages=len(excluded))
        manifest = dict(kind=KIND, schemaVersion=SCHEMA, libraryVersion=version, minSkillVersion=SKILL_VERSION,
                        createdAt=datetime.now(timezone.utc).isoformat(), files=files, counts=counts,
                        sourceHashes=input_hashes, policyHash=policy_hash,
                        agentPolicy=knowledge.get('policy', {}),
                        status='candidate', hostingVerified=False)
        write_json(stage / 'manifest.json', manifest)
        report = verify_manifest(stage / 'manifest.json')
        stage.rename(target)
    except Exception:
        # This path was created by mkdtemp under the checked output root in this call.
        if stage.is_relative_to(output) and stage.exists():
            shutil.rmtree(stage)
        raise
    candidate = dict(libraryVersion=version, manifest=dict(descriptor(output, target / 'manifest.json')),
                     status='candidate', hostingVerified=False)
    write_json(output / ('candidate-' + version + '.json'), candidate)
    return dict(report, manifest=str(target / 'manifest.json'), manifestHash=digest(target / 'manifest.json'),
                counts=counts, stableChanged=False, uploaded=False)


def prepare_hosting(manifest_path, output):
    """Separate metadata and media locally for GitHub plus object-storage hosting."""
    manifest_path = Path(manifest_path).resolve()
    source, output = manifest_path.parent, Path(output).resolve()
    if output.exists() or output == source or output.is_relative_to(source) or source.is_relative_to(output):
        raise ValueError('Hosting output must be a new directory separate from the version source')
    verified = verify_manifest(manifest_path)
    data, manifest = load_manifest(manifest_path)
    version = manifest['libraryVersion']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}', version):
        raise ValueError('Invalid library version')
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.hosting-staging-', dir=output.parent)).resolve()
    try:
        metadata = stage / 'metadata' / 'versions' / version
        media = stage / 'media' / 'versions' / version
        metadata_files = ['manifest.json'] + [e['path'] for e in manifest['files'].values()]
        metadata_files += [r['record']['path'] for r in data['images']]
        media_files = {a['path'] for r in data['images'] for a in r.get('media', {}).values()}
        for root, names in [(metadata, metadata_files), (media, sorted(media_files))]:
            for relative in names:
                target = inside(root, relative)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(inside(source, relative), target)
        report = dict(libraryVersion=version, metadataFiles=len(metadata_files), mediaFiles=len(media_files),
                      metadataBytes=sum(p.stat().st_size for p in metadata.rglob('*') if p.is_file()),
                      mediaBytes=sum(p.stat().st_size for p in media.rglob('*') if p.is_file()),
                      uploaded=False, stableChanged=False, privateCandidate=manifest.get('status') != 'published')
        write_json(stage / 'hosting-plan.json', report)
        stage.rename(output)
    except Exception:
        if stage.exists() and stage.parent == output.parent:
            shutil.rmtree(stage)
        raise
    return dict(report, output=str(output), sourceVerified=verified['verified'])


def private_channel(manifest_path, manifest_url, output):
    verify_manifest(manifest_path)
    parsed = urllib.parse.urlsplit(manifest_url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        raise ValueError('Private channel manifest URL must use HTTPS without credentials')
    manifest_path, output = Path(manifest_path).resolve(), Path(output).resolve()
    if output == manifest_path.parent or output.is_relative_to(manifest_path.parent):
        raise ValueError('Channel pointer must be outside the immutable version directory')
    manifest = read_json(manifest_path)
    data = dict(kind='amazon-plant-reference-channel', schemaVersion=1,
                libraryVersion=manifest['libraryVersion'], audience='private-test',
                manifest=dict(url=manifest_url, sha256=digest(manifest_path), bytes=manifest_path.stat().st_size))
    if output.exists():
        raise ValueError('Private channel candidate already exists; use a new output file')
    write_json(output, data)
    return dict(file=str(output), privateOnly=True, uploaded=False, stableChanged=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build')
    for name in ['source-root', 'output', 'version', 'policy']:
        build.add_argument('--' + name, required=True)
    build.add_argument('--base-url', help='Actual HTTPS directory of this immutable version; no upload is performed')
    verify = sub.add_parser('verify')
    verify.add_argument('manifest', type=Path)
    prepare = sub.add_parser('prepare-hosting')
    prepare.add_argument('--manifest', type=Path, required=True)
    prepare.add_argument('--output', type=Path, required=True)
    channel = sub.add_parser('private-channel')
    channel.add_argument('--manifest', type=Path, required=True)
    channel.add_argument('--manifest-url', required=True)
    channel.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            result = build_library(args.source_root, args.output, args.version, args.policy, args.base_url)
        elif args.command == 'prepare-hosting':
            result = prepare_hosting(args.manifest, args.output)
        elif args.command == 'private-channel':
            result = private_channel(args.manifest, args.manifest_url, args.output)
        else:
            result = verify_manifest(args.manifest)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, KeyError, TypeError, ImportError) as exc:
        parser.exit(2, f'{exc}\n')


if __name__ == '__main__':
    main()
