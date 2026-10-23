#!/usr/bin/env python3
"""Restore archived media by logical path or directory, verifying SHA-256.
Example: python3 tools/restore-media.py videos/004-living-alone/audio/
Use --all only when every original is needed. Use this before running builders that need local source media.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'storage/manifest.json').read_text())
    if not args.all and not args.path:
        parser.error('Specify a logical media path/directory or --all.')
    selected = [(p, item) for p, item in manifest['assets'].items()
                if args.all or p == args.path or p.startswith(args.path.rstrip('/') + '/')]
    if not selected:
        parser.error('No registered media matches that path.')
    for path, item in selected:
        target = (ROOT / path).resolve()
        if not target.is_relative_to(ROOT):
            raise ValueError('Invalid archive path')
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError('Local file differs; refusing to overwrite: ' + path)
            print('Already verified:', path)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(manifest['publicBaseURL'].rstrip('/') + '/' + item['key'], headers={'User-Agent': 'Mozilla/5.0'})
        scratch = None
        try:
            digest = hashlib.sha256()
            size = 0
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as output:
                scratch = Path(output.name)
                with urllib.request.urlopen(request, timeout=90) as response:
                    while chunk := response.read(1024 * 1024):
                        size += len(chunk)
                        if size > item['size']:
                            raise ValueError('Unexpected object size')
                        digest.update(chunk)
                        output.write(chunk)
            if size != item['size'] or digest.hexdigest() != item['sha256']:
                raise ValueError('Archive verification failed: ' + path)
            os.replace(scratch, target)
            print('Restored and verified:', path)
        finally:
            if scratch and scratch.exists():
                scratch.unlink()


if __name__ == '__main__':
    main()
