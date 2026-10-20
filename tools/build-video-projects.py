#!/usr/bin/env python3
"""Package original PNGs and editable text as Credit Studio JSON; no image changes."""
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / 'videos' / '001-100k-salary'
manifest = json.loads((VIDEO / 'artwork.json').read_text(encoding='utf-8'))
for frame in manifest['frames']:
    original = (VIDEO / frame['image']).read_bytes()
    assert original.startswith(b'\x89PNG\r\n\x1a\n'), frame['image']
    elements = [{
        'id': frame['id'] + '-art', 'type': 'image',
        'x': 0, 'y': 0, 'w': 1920, 'h': 1080,
        'fill': '#ffffff', 'opacity': 100,
        'src': 'data:image/png;base64,' + base64.b64encode(original).decode('ascii'),
    }]
    for i, overlay in enumerate(frame['overlays']):
        elements.append({
            'id': f"{frame['id']}-text-{i}", 'type': 'text',
            'x': overlay['x'], 'y': overlay['y'],
            'w': 1920 - overlay['x'] - 70,
            'h': round(overlay['size'] * 1.2 * len(overlay['text'].splitlines()) + 12),
            'text': overlay['text'], 'size': overlay['size'],
            'font': 'Arial', 'weight': 700,
            'fill': overlay.get('fill', '#272c2a'), 'opacity': 100,
        })
    project = {
        'version': 1, 'name': f"{frame['id']} — {frame['title']}",
        'width': 1920, 'height': 1080, 'bg': '#faf6ec', 'elements': elements,
    }
    target = VIDEO / frame['project']
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(project, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(target.relative_to(ROOT))
