#!/usr/bin/env python3
"""Register newly uploaded prop images, preserving existing IDs and crop metadata."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];folder=ROOT/'library/props';catalog=folder/'catalog.json'
data=json.loads(catalog.read_text());known={p['src'] for p in data['items']};ids={p['id'] for p in data['items']};added=0
for path in sorted(folder.rglob('*')):
 if not path.is_file() or path.suffix.lower() not in {'.png','.jpg','.jpeg','.webp'}:continue
 src=path.relative_to(ROOT).as_posix()
 if not re.fullmatch(r'library/props/[A-Za-z0-9_./-]+\.(png|jpg|jpeg|webp)',src,re.I) or '..' in src:raise SystemExit(f'Use an ASCII filename with letters, digits, hyphens or underscores: {src}')
 if src in known:continue
 id='prop-'+hashlib.sha256(src.encode()).hexdigest()[:16]
 if id in ids:raise SystemExit('Duplicate prop ID: '+id)
 data['items'].append({'id':id,'name':path.stem.replace('-',' ').replace('_',' ')[:100],'category':'Đạo cụ mới','tags':[],'src':src});ids.add(id);known.add(src);added+=1
catalog.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'{added} new props registered; {len(data["items"])} total. Existing assets and crops are unchanged.')
