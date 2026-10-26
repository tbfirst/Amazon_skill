"""Trusted HTTPS index sync and content-addressed, on-demand reference downloads."""
import copy
from contextlib import contextmanager
import hashlib
import http.client
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import ssl
import struct
import tempfile
import urllib.error
import urllib.parse
import urllib.request

from library_catalog import DEFAULT_CATALOG, digest, inside, read_json, resolve_image, text_searchable
from library_build import checked_json, check_manifest_header, identity_ready, load_manifest

CHANNEL_KIND = 'amazon-plant-reference-channel'


class LibraryError(ValueError):
    """A user-facing error with no credential or signed-URL contents."""


def default_cache():
    if os.name == 'nt':
        base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local'))
    elif os.sys.platform == 'darwin':
        base = Path.home() / 'Library/Caches'
    else:
        base = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache'))
    return base / 'amazon-plant-image-strategy/library'


def atomic_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix='.json-', dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(handle, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write('\n')
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def descriptor_ok(entry, maximum):
    if (not isinstance(entry, dict) or not re.fullmatch(r'[a-f0-9]{64}', entry.get('sha256', ''))
            or type(entry.get('bytes')) is not int or not 0 < entry['bytes'] <= maximum):
        raise LibraryError('Invalid resource hash/byte count or configured size limit exceeded')


def checked_file(path, entry):
    return path.is_file() and path.stat().st_size == entry['bytes'] and digest(path) == entry['sha256']


@contextmanager
def resource_lock(root, key):
    lock = inside(root, 'locks/' + hashlib.sha256(key.encode()).hexdigest() + '.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise LibraryError('Resource is busy; retry after the active operation finishes (locks are not stolen)') from None
    try:
        with os.fdopen(fd, 'w') as file:
            file.write(str(os.getpid()))
        yield
    finally:
        lock.unlink(missing_ok=True)


def image_encoding(path, asset):
    """Check encoding without third-party dependencies; decode fully if Pillow exists."""
    raw = path.read_bytes()
    kind = asset.get('format')
    valid = False
    if kind == 'PNG':
        valid = (len(raw) >= 45 and raw.startswith(b'\x89PNG\r\n\x1a\n')
                 and raw[-8:-4] == b'IEND'
                 and struct.unpack('>II', raw[16:24]) == (asset['width'], asset['height']))
    elif kind == 'JPEG':
        valid = len(raw) >= 32 and raw.startswith(b'\xff\xd8') and raw.endswith(b'\xff\xd9')
    elif kind == 'WEBP':
        valid = (len(raw) >= 30 and raw[:4] == b'RIFF' and raw[8:12] == b'WEBP'
                 and int.from_bytes(raw[4:8], 'little') + 8 == len(raw))
    if not valid:
        raise LibraryError('Downloaded media encoding does not match its descriptor')
    try:
        from PIL import Image
    except ImportError:
        return 'hash-and-encoding'
    try:
        with Image.open(path) as image:
            if image.size != (asset['width'], asset['height']) or image.format != kind:
                raise LibraryError('Downloaded media dimensions/format do not match')
            image.load()
    except (OSError, ValueError, Image.DecompressionBombError):
        raise LibraryError('Downloaded media failed image decoding') from None
    return 'hash-encoding-and-decode'


class TrustedRedirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, client):
        self.client = client

    def redirect_request(self, request, response, code, message, headers, newurl):
        self.client.check_url(newurl)
        # Recompute destination credentials, never forward the first origin's headers.
        redirected = super().redirect_request(request, response, code, message, headers, newurl)
        if redirected:
            redirected.headers = self.client.headers_for(newurl)
            redirected.unredirected_hdrs = {}
        return redirected


class LibraryClient:
    def __init__(self, config_path, cache_dir=None, bundled_catalog=DEFAULT_CATALOG):
        self.config_path = Path(config_path).resolve()
        self.config = read_json(self.config_path)
        if self.config.get('schemaVersion') != 1:
            raise LibraryError('Unsupported remote source configuration schema')
        allowed_keys = {'schemaVersion', 'sourceId', 'channelUrl', 'allowedOrigins', 'credentials',
                        'requestHeaders', 'allowCandidate', 'allowLoopbackHttp', 'caFile', 'timeoutSeconds',
                        'maxJsonBytes', 'maxAssetBytes', 'maxSessionBytes', 'maxCacheBytes', 'maxBatchImages', 'mediaBaseUrl'}
        if set(self.config) - allowed_keys:
            raise LibraryError('Unknown remote source configuration field')
        if any(k in self.config and type(self.config[k]) is not bool for k in ['allowCandidate', 'allowLoopbackHttp']):
            raise LibraryError('Source mode flags must be booleans')
        self.loopback_http = self.config.get('allowLoopbackHttp') is True
        self.origins = {self.origin(url, origin_only=True) for url in self.config.get('allowedOrigins', [])}
        if not self.origins:
            raise LibraryError('Configure at least one trusted origin')
        self.channel_url = self.config.get('channelUrl', '')
        self.check_url(self.channel_url)
        self.request_headers = {}
        for origin_url, values in self.config.get('requestHeaders', {}).items():
            origin = self.origin(origin_url, origin_only=True)
            if origin not in self.origins or set(values) - {'Accept', 'X-GitHub-Api-Version'}:
                raise LibraryError('Only non-secret media/API headers are allowed for trusted origins')
            if any(not isinstance(v, str) or '\r' in v or '\n' in v for v in values.values()):
                raise LibraryError('Invalid configured request header')
            self.request_headers[origin] = values
        self.credentials = {}
        for item in self.config.get('credentials', []):
            origin = self.origin(item['origin'], origin_only=True)
            if origin not in self.origins or origin in self.credentials:
                raise LibraryError('Credential origin must be unique and explicitly trusted')
            if set(item) - {'origin', 'env', 'header', 'prefix'}:
                raise LibraryError('Credentials must name an environment variable, not embed secrets')
            if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', item.get('env', '')):
                raise LibraryError('Invalid credential environment variable name')
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*', item.get('header', 'Authorization')):
                raise LibraryError('Invalid authentication header name')
            if '\r' in item.get('prefix', '') or '\n' in item.get('prefix', ''):
                raise LibraryError('Invalid authentication prefix')
            self.credentials[origin] = item
        source_id = self.config.get('sourceId', 'reference-library')
        if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}', source_id):
            raise LibraryError('Invalid sourceId')
        base = Path(cache_dir).resolve() if cache_dir else default_cache().resolve()
        skill_root = Path(__file__).resolve().parents[1]
        if base == skill_root or base.is_relative_to(skill_root):
            raise LibraryError('Cache must be outside the skill installation directory')
        self.root = base / (source_id + '-' + hashlib.sha256(self.channel_url.encode()).hexdigest()[:12])
        self.root.mkdir(parents=True, exist_ok=True)
        self.state_path = self.root / 'state.json'
        self.timeout = self.number('timeoutSeconds', 20, 1, 30)
        self.max_json = self.number('maxJsonBytes', 32 * 1024**2, 1024, 128 * 1024**2)
        self.max_asset = self.number('maxAssetBytes', 40 * 1024**2, 1024, 512 * 1024**2)
        self.max_session = self.number('maxSessionBytes', 160 * 1024**2, 1024, 2 * 1024**3)
        self.max_cache = self.number('maxCacheBytes', 1024**3, 1024, 100 * 1024**3)
        self.max_batch = self.number('maxBatchImages', 32, 1, 200)
        self.downloaded = 0
        ca_file = self.config.get('caFile')
        if ca_file:
            ca_file = str((self.config_path.parent / ca_file).resolve())
        context = ssl.create_default_context(cafile=ca_file)
        self.opener = urllib.request.build_opener(TrustedRedirects(self), urllib.request.HTTPSHandler(context=context))
        self.bundled_catalog = Path(bundled_catalog)
        self._bundled = None

    def number(self, key, default, minimum, maximum):
        value = self.config.get(key, default)
        if type(value) is not int or not minimum <= value <= maximum:
            raise LibraryError('Invalid configured limit: ' + key)
        return value

    def origin(self, url, origin_only=False):
        try:
            parts = urllib.parse.urlsplit(url)
            port = parts.port
            host = parts.hostname
        except (ValueError, TypeError):
            raise LibraryError('Invalid resource URL') from None
        if not host or parts.username or parts.password or parts.fragment:
            raise LibraryError('URL must have a host and no embedded credentials or fragment')
        if origin_only and (parts.path not in {'', '/'} or parts.query):
            raise LibraryError('Trusted origins must not contain a path/query')
        if parts.scheme != 'https':
            try:
                permitted = self.loopback_http and parts.scheme == 'http' and ipaddress.ip_address(host).is_loopback
            except ValueError:
                permitted = False
            if not permitted:
                raise LibraryError('HTTPS is required (HTTP is permitted only for explicit loopback tests)')
        host = host.lower()
        authority = ('[' + host + ']') if ':' in host else host
        if port and port != (443 if parts.scheme == 'https' else 80):
            authority += ':' + str(port)
        return parts.scheme + '://' + authority

    def check_url(self, url):
        if self.origin(url) not in self.origins:
            raise LibraryError('Download/redirect origin is outside the configured trusted sources')
        return url

    def headers_for(self, url):
        headers = {'User-Agent': 'AmazonPlantReferenceClient/1.11.0', 'Accept-Encoding': 'identity'}
        headers.update(self.request_headers.get(self.origin(url), {}))
        item = self.credentials.get(self.origin(url))
        if item:
            value = os.environ.get(item['env'])
            if not value:
                raise LibraryError('Missing credential environment variable: ' + item['env'])
            if '\r' in value or '\n' in value:
                raise LibraryError('Invalid credential value')
            headers[item.get('header', 'Authorization')] = item.get('prefix', 'Bearer ') + value
        return headers

    def cache_bytes(self):
        return sum(p.stat().st_size for p in self.root.rglob('*') if p.is_file())

    def download(self, url, target, maximum, expected=None, conditional=None, validator=None):
        self.check_url(url)
        if expected:
            descriptor_ok(expected, maximum)
            if self.downloaded + expected['bytes'] > self.max_session:
                raise LibraryError('Download session budget exceeded; select fewer candidates or configure the budget')
        headers = self.headers_for(url)
        for key, value in (conditional or {}).items():
            if value and '\r' not in value and '\n' not in value:
                headers[key] = value
        target.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(2):
            temporary = None
            try:
                request = urllib.request.Request(url, headers=headers)
                with self.opener.open(request, timeout=self.timeout) as response:
                    size = response.headers.get('Content-Length')
                    if size and (not size.isdigit() or int(size) > maximum):
                        raise LibraryError('Resource Content-Length exceeds limit or is invalid')
                    fd, name = tempfile.mkstemp(prefix='.download-', dir=target.parent)
                    temporary = Path(name)
                    total, checksum = 0, hashlib.sha256()
                    cache_used = self.cache_bytes()
                    with os.fdopen(fd, 'wb') as file:
                        while True:
                            chunk = response.read(65536)
                            if not chunk:
                                break
                            total += len(chunk)
                            self.downloaded += len(chunk)
                            if total > maximum or self.downloaded > self.max_session or cache_used + total > self.max_cache:
                                raise LibraryError('Resource, session or cache byte budget exceeded')
                            checksum.update(chunk)
                            file.write(chunk)
                    if expected and (total != expected['bytes'] or checksum.hexdigest() != expected['sha256']):
                        raise LibraryError('Downloaded resource failed byte count/SHA-256 verification')
                    validation = validator(temporary) if validator else None
                    temporary.replace(target)
                    return dict(notModified=False, etag=response.headers.get('ETag'),
                                lastModified=response.headers.get('Last-Modified'), validation=validation)
            except urllib.error.HTTPError as exc:
                if exc.code == 304 and conditional:
                    exc.close()
                    return dict(notModified=True)
                if exc.code in {500, 502, 503, 504} and attempt == 0:
                    exc.close()
                    continue
                exc.close()
                raise LibraryError('Remote request failed: HTTP ' + str(exc.code)) from None
            except (urllib.error.URLError, TimeoutError, ConnectionError, ssl.SSLError, http.client.HTTPException):
                if attempt == 0:
                    continue
                raise LibraryError('Remote connection/TLS request failed') from None
            finally:
                if temporary:
                    temporary.unlink(missing_ok=True)

    def state(self):
        return read_json(self.state_path) if self.state_path.is_file() else dict(versions={})

    def snapshot(self, version=None):
        state = self.state()
        version = version or state.get('currentVersion')
        entry = state.get('versions', {}).get(version)
        if not entry:
            raise LibraryError('No validated index is cached for this source/version; run sync or use bundled references')
        path = inside(self.root, entry['path'])
        if not checked_file(path, entry):
            raise LibraryError('Cached manifest failed integrity verification')
        data, manifest = load_manifest(path)
        self.validate_index(data, manifest, entry['manifestUrl'])
        return data, manifest, path, entry

    def locator(self, entry, manifest_url, media=False, version=None):
        path = entry.get('path')
        if not isinstance(path, str) or '\\' in path or re.match(r'^[A-Za-z]:', path):
            raise LibraryError('Invalid relative resource path')
        # Validate as a filesystem path as well as rejecting URL/absolute traversal forms.
        inside(self.root, path)
        parts = urllib.parse.urlsplit(path)
        if parts.scheme or parts.netloc or path.startswith('/') or any(p in {'.', '..'} for p in path.split('/')):
            raise LibraryError('Unsafe resource path')
        base = urllib.parse.urljoin(manifest_url, './')
        if media and self.config.get('mediaBaseUrl'):
            base = self.config['mediaBaseUrl'].replace('{libraryVersion}', version or '')
            if not base.endswith('/'):
                raise LibraryError('mediaBaseUrl must end with a slash')
        url = entry.get('url') or urllib.parse.urljoin(base, path)
        if not media and not entry.get('url'):
            # GitHub Contents API needs its pinned ref on each relative JSON request.
            query = urllib.parse.urlsplit(manifest_url).query
            if query:
                parts = urllib.parse.urlsplit(url)
                url = urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, query, ''))
        return self.check_url(url)

    def validate_index(self, data, manifest, manifest_url):
        ids = [i['id'] for i in data['images']]
        if len(ids) != len(set(ids)) or manifest['counts']['images'] != len(ids):
            raise LibraryError('Invalid complete-index image coverage')
        for record in data['images']:
            if (not text_searchable(record) or not identity_ready(record)
                    or not re.fullmatch(r'[0-9a-f]{64}', record.get('sha256', ''))
                    or record['id'] != 'IMG-' + record['sha256'][:16]):
                raise LibraryError('Restricted or mismatched image in published search index')
            descriptor_ok(record['record'], self.max_json)
            self.locator(record['record'], manifest_url)
            for kind, asset in record.get('media', {}).items():
                if kind not in {'preview', 'original'} or kind not in record['publication']['scopes']:
                    raise LibraryError('Image media exceeds declared publication scope')
                descriptor_ok(asset, self.max_asset)
                if asset.get('format') not in {'JPEG', 'PNG', 'WEBP'}:
                    raise LibraryError('Unsupported image encoding in index')
                if any(type(asset.get(k)) is not int or not 0 < asset[k] <= 16384 for k in ['width', 'height']):
                    raise LibraryError('Invalid image dimensions in index')
                if asset['width'] * asset['height'] > 64_000_000:
                    raise LibraryError('Image pixel limit exceeded')
                if kind == 'original' and asset['sha256'] != record['sha256']:
                    raise LibraryError('Original hash does not match image identity')
                self.locator(asset, manifest_url, media=True, version=manifest['libraryVersion'])
        known = set(ids)
        for recipe in data['layoutRecipes']:
            if not recipe.get('sourceImageIds') or not set(recipe['sourceImageIds']).issubset(known):
                raise LibraryError('Recipe refers to unpublished images')
            variants = recipe.get('promptVariants') or {}
            branch_ids = set(variants) if isinstance(variants, dict) else {v['imageId'] for v in variants}
            if not branch_ids.issubset(recipe['sourceImageIds']):
                raise LibraryError('Recipe branch refers to another image source')
        for series in data['series']:
            for member in series['members']:
                if member.get('published') and (member.get('imageId') not in known or member.get('status') != 'approved'):
                    raise LibraryError('Series refers to unpublished images')

    def sync(self, offline=False, strict=False):
        try:
            if offline:
                _, manifest, path, _ = self.snapshot()
                return dict(status='offline-cache', manifest=str(path), libraryVersion=manifest['libraryVersion'],
                            manifestHash=digest(path), downloadedBytes=0)
            with resource_lock(self.root, 'sync'):
                return self._sync()
        except (ValueError, OSError, KeyError, TypeError) as exc:
            if strict:
                raise
            try:
                _, manifest, path, _ = self.snapshot()
                return dict(status='cached-fallback', manifest=str(path), libraryVersion=manifest['libraryVersion'],
                            manifestHash=digest(path), reason=str(exc), downloadedBytes=self.downloaded)
            except (ValueError, OSError, KeyError, TypeError):
                return dict(status='bundled-fallback', catalog=str(self.bundled_catalog.resolve()),
                            reason=str(exc), downloadedBytes=self.downloaded)

    def _sync(self):
        state = self.state()
        channel_meta = state.get('channel', {})
        conditional = dict(**{'If-None-Match': channel_meta.get('etag'), 'If-Modified-Since': channel_meta.get('lastModified')})
        stage = Path(tempfile.mkdtemp(prefix='.sync-', dir=self.root)).resolve()
        try:
            headers = self.download(self.channel_url, stage / 'channel.json', 1024**2, conditional=conditional)
            if headers['notModified']:
                try:
                    _, manifest, path, _ = self.snapshot()
                    return dict(status='not-modified', manifest=str(path), libraryVersion=manifest['libraryVersion'],
                                manifestHash=digest(path), downloadedBytes=self.downloaded)
                except (ValueError, OSError, KeyError, TypeError):
                    headers = self.download(self.channel_url, stage / 'channel.json', 1024**2)
            channel = read_json(stage / 'channel.json')
            if channel.get('kind') != CHANNEL_KIND or channel.get('schemaVersion') != 1:
                raise LibraryError('Unsupported library channel schema')
            manifest_entry = channel['manifest']
            descriptor_ok(manifest_entry, self.max_json)
            manifest_url = manifest_entry.get('url') or self.locator(manifest_entry, self.channel_url)
            self.check_url(manifest_url)
            manifest_file = stage / 'manifest.json'
            self.download(manifest_url, manifest_file, self.max_json, manifest_entry)
            manifest = read_json(manifest_file)
            check_manifest_header(manifest)
            version = manifest['libraryVersion']
            if not isinstance(version, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}', version):
                raise LibraryError('Invalid library version')
            if channel.get('libraryVersion') != version:
                raise LibraryError('Channel and manifest versions do not match')
            if (manifest.get('status') != 'published' or manifest.get('hostingVerified') is not True) and not self.config.get('allowCandidate'):
                raise LibraryError('Candidate library requires an explicit private-test configuration')
            previous = state.get('versions', {}).get(version)
            if previous and previous['sha256'] != manifest_entry['sha256']:
                raise LibraryError('An immutable library version changed; publisher must issue a new version')
            file_paths = [e['path'] for e in manifest['files'].values()]
            if 'manifest.json' in file_paths or len(set(file_paths)) != len(file_paths):
                raise LibraryError('Duplicate or reserved index resource path')
            for entry in manifest['files'].values():
                descriptor_ok(entry, self.max_json)
                target = inside(stage, entry['path'])
                self.download(self.locator(entry, manifest_url), target, self.max_json, entry)
            data, manifest = load_manifest(manifest_file)
            self.validate_index(data, manifest, manifest_url)
            destination = inside(self.root, 'indexes/' + version + '-' + manifest_entry['sha256'][:16])
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                # Repair damaged index files in place, only after the new staging set passes validation.
                for name in ['manifest.json'] + [e['path'] for e in manifest['files'].values()]:
                    target = inside(destination, name)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    inside(stage, name).replace(target)
            else:
                stage.rename(destination)
            relative = (destination / 'manifest.json').relative_to(self.root).as_posix()
            entry = dict(path=relative, sha256=manifest_entry['sha256'], bytes=manifest_entry['bytes'], manifestUrl=manifest_url)
            state.setdefault('versions', {})[version] = entry
            state.update(currentVersion=version, channel=dict(etag=headers.get('etag'), lastModified=headers.get('lastModified')))
            atomic_json(self.state_path, state)
            return dict(status='synced', manifest=str(destination / 'manifest.json'), libraryVersion=version,
                        manifestHash=manifest_entry['sha256'], imageCount=len(data['images']), downloadedBytes=self.downloaded)
        finally:
            if stage.exists() and stage.is_relative_to(self.root):
                shutil.rmtree(stage)

    def media_path(self, asset):
        extension = {'PNG': '.png', 'JPEG': '.jpg', 'WEBP': '.webp'}[asset['format']]
        return inside(self.root, 'assets/' + asset['sha256'][:2] + '/' + asset['sha256'] + extension)

    def revoked_ids(self):
        try:
            state = self.state()
            entry = state.get('versions', {}).get(state.get('currentVersion'))
            if not entry:
                return set()
            path = inside(self.root, entry['path'])
            manifest = read_json(path)
            if not checked_file(path, entry):
                raise LibraryError('Cached manifest failed integrity verification')
            revocations = checked_json(path.parent, manifest['files']['revocations'])
            return {i['id'] for i in revocations['images']}
        except (OSError, KeyError, TypeError) as exc:
            raise LibraryError('Cached revocation data is unavailable; run sync') from exc

    def bundled(self, record):
        if self._bundled is None:
            data = read_json(self.bundled_catalog)
            self._bundled = {r['id']: r for r in data.get('images', [])}
        candidate = self._bundled.get(record['id'])
        if candidate and candidate.get('sha256') == record.get('sha256'):
            return resolve_image(candidate, self.bundled_catalog.resolve().parent, portable=True)
        return None

    def resolve(self, record, manifest_url, version):
        result = copy.deepcopy(record)
        allowed = text_searchable(record) and record['id'] not in self.revoked_ids()
        available, fetchable = {}, {}
        for kind in ['preview', 'original']:
            asset = record.get('media', {}).get(kind)
            available[kind] = None
            fetchable[kind] = False
            if asset and allowed:
                path = self.media_path(asset)
                if checked_file(path, asset):
                    available[kind] = path
                try:
                    self.locator(asset, manifest_url, media=True, version=version)
                    fetchable[kind] = True
                except ValueError:
                    pass
        fallback = self.bundled(record) if allowed else None
        original = available['original'] or (Path(fallback['resolvedFile']) if fallback and fallback['originalAvailable'] else None)
        preview = available['preview']
        selected = original or preview
        result.update(available=bool(selected), localAvailable=bool(selected), resolvedFile=str(selected) if selected else None,
                      previewAvailable=bool(preview), originalAvailable=bool(original), textSearchable=allowed,
                      fetchable=any(fetchable.values()), previewFetchable=fetchable['preview'], originalFetchable=fetchable['original'],
                      observedThisRun=False, mediaStatus='local' if selected else 'fetchable' if any(fetchable.values()) else 'text-only')
        return result

    def detail(self, summary, manifest_path, entry, offline=False):
        target = inside(Path(manifest_path).parent, summary['record']['path'])
        with resource_lock(self.root, 'record-' + summary['record']['sha256']):
            if not checked_file(target, summary['record']):
                if offline:
                    raise LibraryError('Selected detailed record is not cached for offline use')
                self.download(self.locator(summary['record'], entry['manifestUrl']), target, self.max_json, summary['record'])
            record = read_json(target)
        if (record['id'] != summary['id'] or record['sha256'] != summary['sha256']
                or record.get('media') != summary.get('media') or record.get('publication') != summary.get('publication')):
            raise LibraryError('Downloaded detail does not match the selected image identity')
        return record

    def fetch(self, image_ids=None, series_id=None, size='preview', version=None, offline=False, limit=8):
        data, manifest, manifest_path, entry = self.snapshot(version)
        by_id = {i['id']: i for i in data['images']}
        if series_id:
            if image_ids:
                raise LibraryError('Choose image IDs or a series, not both')
            series = next((s for s in data['series'] if s['id'] == series_id), None)
            if not series:
                raise LibraryError('Unknown series ID')
            image_ids = [m['imageId'] for m in series['members'] if m.get('published') and m.get('status') == 'approved']
        ids = list(dict.fromkeys(image_ids or []))
        if not ids or not 1 <= limit <= self.max_batch or len(ids) > self.max_batch and not series_id:
            raise LibraryError('Select a bounded set of image IDs within maxBatchImages')
        ids = ids[:limit] if series_id else ids
        successes, failures = [], []
        for identity in ids:
            try:
                record = by_id.get(identity)
                if not record or not text_searchable(record) or identity in self.revoked_ids():
                    raise LibraryError('Unknown, restricted or withdrawn image ID')
                state = self.resolve(record, entry['manifestUrl'], manifest['libraryVersion'])
                if state['originalAvailable'] or (size == 'preview' and state['previewAvailable']):
                    successes.append(dict(id=identity, requestedSize=size, servedSize='original' if state['originalAvailable'] else 'preview',
                                          status='cached', **{k: state[k] for k in ['resolvedFile', 'localAvailable', 'observedThisRun']}))
                    continue
                if offline:
                    raise LibraryError('Requested image is not cached for offline use')
                asset = record.get('media', {}).get(size)
                if not asset or size not in record['publication']['scopes']:
                    raise LibraryError('Requested image size is not in the published media scope')
                target = self.media_path(asset)
                with resource_lock(self.root, 'asset-' + asset['sha256']):
                    if not checked_file(target, asset):
                        self.download(self.locator(asset, entry['manifestUrl'], media=True, version=manifest['libraryVersion']),
                                      target, self.max_asset, asset, validator=lambda p: image_encoding(p, asset))
                    try:
                        validation = image_encoding(target, asset)
                    except LibraryError:
                        target.unlink(missing_ok=True)
                        raise
                successes.append(dict(id=identity, requestedSize=size, servedSize=size, status='downloaded',
                                      resolvedFile=str(target), localAvailable=True, observedThisRun=False, validation=validation))
            except (ValueError, OSError, KeyError, TypeError) as exc:
                failures.append(dict(id=identity, reason=str(exc)))
        return dict(status='complete' if not failures else 'partial' if successes else 'failed',
                    libraryVersion=manifest['libraryVersion'], manifestHash=digest(manifest_path),
                    items=successes, failures=failures, downloadedBytes=self.downloaded)

    def cache_status(self):
        state = self.state()
        return dict(cacheRoot=str(self.root), bytes=self.cache_bytes(), maxCacheBytes=self.max_cache,
                    currentVersion=state.get('currentVersion'), cachedVersions=list(state.get('versions', {})))
