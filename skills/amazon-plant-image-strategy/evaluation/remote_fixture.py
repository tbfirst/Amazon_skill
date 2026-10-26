"""Ephemeral private HTTPS test servers; keys and credentials are synthetic and temporary."""
from collections import Counter
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import ipaddress
import json
from pathlib import Path
import ssl
import sys
import threading
import urllib.parse

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from PIL import Image

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import library_build as builder
import library_catalog as catalog


def tls_files(root):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Ephemeral private library test')])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(subject).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - timedelta(minutes=1))
            .not_valid_after(now + timedelta(days=2))
            .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]), critical=False)
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(key, hashes.SHA256()))
    root.mkdir(parents=True, exist_ok=True)
    cert_file, key_file = root / 'test-ca.pem', root / 'test-key.pem'
    cert_file.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_file.write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                         serialization.NoEncryption()))
    return cert_file, key_file


class PrivateServer:
    def __init__(self, root, cert, key, token):
        self.root, self.token = Path(root).resolve(), token
        self.counts, self.auth_seen, self.overrides = Counter(), [], {}
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                path = urllib.parse.urlsplit(self.path).path
                owner.counts[path] += 1
                owner.auth_seen.append((path, self.headers.get('Authorization'), self.headers.get('X-Test-Auth')))
                if self.headers.get('Authorization') != 'Bearer ' + owner.token:
                    self.send_response(401)
                    self.end_headers()
                    return
                if path in owner.overrides:
                    override = owner.overrides[path]
                    self.send_response(override.get('status', 200))
                    for k, v in override.get('headers', {}).items():
                        self.send_header(k, v)
                    self.end_headers()
                    self.wfile.write(override.get('body', b''))
                    return
                target = (owner.root / urllib.parse.unquote(path).lstrip('/')).resolve()
                if not target.is_relative_to(owner.root) or not target.is_file():
                    self.send_response(404)
                    self.end_headers()
                    return
                etag = '"' + catalog.digest(target) + '"'
                if self.headers.get('If-None-Match') == etag:
                    self.send_response(304)
                    self.send_header('ETag', etag)
                    self.end_headers()
                    return
                raw = target.read_bytes()
                self.send_response(200)
                self.send_header('Content-Length', str(len(raw)))
                self.send_header('ETag', etag)
                self.end_headers()
                self.wfile.write(raw)

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.server.daemon_threads = True
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert, key)
        self.server.socket = context.wrap_socket(self.server.socket, server_side=True)
        self.origin = 'https://127.0.0.1:' + str(self.server.server_address[1])
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.closed = False

    def close(self):
        if not self.closed:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=2)
            self.closed = True


def channel_file(publication_root, version, index_origin):
    manifest = Path(publication_root) / 'versions' / version / 'manifest.json'
    channel = dict(kind='amazon-plant-reference-channel', schemaVersion=1, libraryVersion=version,
                   manifest=dict(url=index_origin + '/versions/' + version + '/manifest.json',
                                 sha256=catalog.digest(manifest), bytes=manifest.stat().st_size))
    builder.write_json(Path(publication_root) / 'channels/private-test.json', channel)
    return channel


def source_config(path, index, media, cert, allow_candidate=True):
    config = dict(schemaVersion=1, sourceId='private-test', channelUrl=index.origin + '/channels/private-test.json',
                  allowedOrigins=[index.origin, media.origin], mediaBaseUrl=media.origin + '/versions/{libraryVersion}/',
                  allowCandidate=allow_candidate, caFile=str(cert), timeoutSeconds=2,
                  credentials=[dict(origin=index.origin, env='PLANT_TEST_INDEX_TOKEN', prefix='Bearer '),
                               dict(origin=media.origin, env='PLANT_TEST_MEDIA_TOKEN', prefix='Bearer ')])
    builder.write_json(Path(path), config)
    return config


def synthetic_master(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    images = []
    for number, color in enumerate(['green', 'red', 'blue'], 1):
        file = root / f'{number}.png'
        Image.new('RGB', (80, 120), color).save(file)
        checksum = catalog.digest(file)
        images.append(dict(id='IMG-' + checksum[:16], sha256=checksum, file=file.name, width=80, height=120,
                           visualStatus='observed-full', reuseEligible=number != 3,
                           observation=dict(title='Synthetic plant', overview='Two-region detail', imageTypes=['细节图'],
                                            recipe='Owned synthetic example ' + str(number),
                                            reuseDecision='reject' if number == 3 else 'accept')))
    builder.write_json(root / 'prompts.json', dict(cards=[dict(id='TEST-01', prompt='Synthetic template')]))
    builder.write_json(root / 'agent-index.json', dict(images=images))
    builder.write_json(root / 'layout-recipes.json', dict(recipes=[dict(id='LAYOUT-test', prompt='Synthetic layout',
                        sourceImageIds=[i['id'] for i in images], promptVariants={i['id']: dict(prompt='Branch ' + i['id']) for i in images})]))
    builder.write_json(root / 'series-index.json', dict(series=[dict(id='SET-test', title='Synthetic complete sequence',
        members=[dict(section='gallery', order=n, imageId=i['id'], sha256=i['sha256'], status='approved') for n, i in enumerate(images, 1)])]))
    return images
