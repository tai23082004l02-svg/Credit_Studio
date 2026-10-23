#!/usr/bin/env python3
"""Verify media from a staging draft release without committing binaries to Git.
Uses GitHub Actions R2 credentials; never prints keys, headers or error bodies.
Does not modify Git, old objects, CORS, or the runtime manifest.
"""
import hashlib, importlib.util, json, mimetypes, os, re, subprocess, sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    repo, tag, map_name = (os.environ.get(n, '') for n in ('GITHUB_REPOSITORY', 'RELEASE_TAG', 'MAP_FILE'))
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository')
    if not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', tag) or not re.fullmatch(r'[A-Za-z0-9_.-]+\.json', map_name):
        raise ValueError('Invalid staging reference')
    work = ROOT / 'work/release-media'
    work.mkdir(parents=True, exist_ok=True)
    def download(name):
        if '/' in name or '\\' in name or any(c in name for c in '*?[]\r\n') or name.startswith('-'):
            raise ValueError('Invalid asset name')
        subprocess.run(['gh', 'release', 'download', tag, '--repo', repo, '--pattern', name, '--dir', str(work)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return work / name
    plan = json.loads(download(map_name).read_text())
    if plan.get('version') != 1 or not isinstance(plan.get('assets'), list) or not 1 <= len(plan['assets']) <= 32:
        raise ValueError('Invalid media map')
    spec = importlib.util.spec_from_file_location('r2_storage', ROOT / 'tools/r2-storage.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    client = module.R2()
    public = json.loads((ROOT / 'storage/manifest.json').read_text())['publicBaseURL'].rstrip('/')
    verified = []
    for item in plan['assets']:
        logical = item['path']
        if not re.fullmatch(r'videos/[A-Za-z0-9_-]+/[^\x00-\x1f\\]+\.(wav|mp3|mp4|png)', logical) or any(p in ('.', '..') for p in logical.split('/')):
            raise ValueError('Invalid logical path')
        if not re.fullmatch(r'[a-f0-9]{64}', item['sha256']):
            raise ValueError('Invalid expected hash')
        source = download(item['filename']); data = source.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != item['sha256'] or len(data) != item['size']:
            raise ValueError('Staged file differs from expected source')
        key = 'credit-studio/media/' + digest + source.suffix.lower()
        kind = mimetypes.guess_type(source.name)[0] or 'application/octet-stream'
        status, headers, _ = client.request('HEAD', key, missing_ok=True)
        headers = {k.lower(): v for k, v in headers.items()}
        if status == 404:
            client.request('PUT', key, body=data, extra={'content-type': kind, 'cache-control': 'public, max-age=31536000, immutable', 'x-amz-meta-sha256': digest, 'if-none-match': '*'})
        elif headers.get('x-amz-meta-sha256') != digest or int(headers.get('content-length', '-1')) != len(data):
            raise ValueError('Existing object metadata differs; refusing overwrite')
        _, _, actual = client.request('GET', key)
        if hashlib.sha256(actual).hexdigest() != digest or len(actual) != len(data):
            raise ValueError('Authenticated download verification failed')
        req = urllib.request.Request(public + '/' + key, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-63', 'Origin': 'https://tai23082004l02-svg.github.io'})
        with urllib.request.urlopen(req, timeout=90) as response:
            if response.status != 206 or response.headers.get('Access-Control-Allow-Origin') != 'https://tai23082004l02-svg.github.io' or response.read() != data[:64]:
                raise ValueError('Public Range/CORS verification failed')
        verified.append({'path': logical, 'key': key, 'sha256': digest, 'size': len(data), 'type': kind})
        print('Uploaded or reused and verified:', logical, flush=True)
    (work / 'verified.json').write_text(json.dumps({'version': 1, 'assets': verified, 'authenticatedFullHash': True, 'publicRangeCors': True}, indent=2) + '\n')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        # Never disclose signed requests, SDK error messages, endpoints or tokens.
        print('Media staging failed:', type(error).__name__, file=sys.stderr)
        sys.exit(1)
