#!/usr/bin/env python3
"""Read-only R2 diagnosis. Never print credential values or raw remote errors."""
import importlib.util
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def main():
    required = ('R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_ENDPOINT_URL', 'R2_BUCKET')
    missing = [name for name in required if not os.environ.get(name, '').strip()]
    if missing:
        print('FAIL: Missing GitHub Actions configuration: ' + ', '.join(missing))
        print('Cloud environment variables are separate from repository Actions secrets.')
        return 1
    spec = importlib.util.spec_from_file_location('r2_storage', Path(__file__).with_name('r2-storage.py'))
    storage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(storage)
    try:
        client = storage.R2()
    except Exception:
        print('FAIL: Invalid credential, endpoint or bucket format. Use the S3 access key pair and HTTPS S3 endpoint without a bucket path.')
        return 1
    stage = 'ListObjectsV2'
    try:
        status, _, body = client.request('GET', query='list-type=2&max-keys=1')
        root = ET.fromstring(body)
        print('PASS: Authenticated ListObjectsV2 HTTP ' + str(status))
        objects = root.findall('{*}Contents')
        if objects:
            stage = 'GetObject'
            status, _, data = client.request('GET', objects[0].findtext('{*}Key'), extra={'range': 'bytes=0-63'})
            print('PASS: Authenticated object read HTTP ' + str(status))
        else:
            print('Bucket listing is empty; object read was not tested.')
        print('Read-only check complete. Upload/delete permissions were not tested.')
        return 0
    except storage.StorageError as error:
        match = re.search(r'HTTP (\d{3})', str(error))
        code = match.group(1) if match else 'network error'
        print('FAIL: ' + stage + ' returned ' + code)
        if code == '401':
            print('Authentication rejected. Check key validity and account/endpoint pairing.')
        elif code == '403':
            print('Access denied. Check token permissions, bucket scope and token restrictions.')
        elif code == '404':
            print('Check the configured bucket and endpoint account.')
        else:
            print('Check network connectivity, endpoint and service availability.')
        return 1
    except Exception:
        print('FAIL: Unexpected response; raw details suppressed to protect credentials.')
        return 1


if __name__ == '__main__':
    sys.exit(main())
