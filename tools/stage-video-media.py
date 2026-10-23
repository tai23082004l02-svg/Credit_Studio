#!/usr/bin/env python3
"""Stage new video bytes as temporary Git blobs, never as a branch/tree/commit.
Usage: python3 tools/stage-video-media.py work/media-map.json
The Actions worker reassembles and verifies SHA-256 before registering R2 URLs.
"""
import base64,concurrent.futures,hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPO='tai23082004l02-svg/Credit_Studio'
WORK=ROOT/'work/media-staging';WORK.mkdir(parents=True,exist_ok=True)
CACHE=WORK/'cache.json'
def upload(payload,name):
    target=WORK/(name+'.json');target.write_text(json.dumps(payload))
    try:
        r=subprocess.run(['gh','api','--method','POST',f'repos/{REPO}/git/blobs','--input',str(target),'--jq','.sha'],capture_output=True,text=True,check=True)
        sha=r.stdout.strip()
        if not re.fullmatch(r'[a-f0-9]{40}',sha):raise ValueError('Invalid staging response')
        return sha
    finally:target.unlink(missing_ok=True)
def main():
    data=json.loads(Path(sys.argv[1]).read_text());cache=json.loads(CACHE.read_text()) if CACHE.exists() else {};plan=[]
    for row in data['assets']:
        p=(ROOT/row['path']).resolve()
        if not p.is_relative_to(ROOT) or p.suffix not in ['.mp3','.wav','.mp4','.png']:raise ValueError('Invalid source')
        content=p.read_bytes();digest=hashlib.sha256(content).hexdigest()
        if digest!=row['sha256'] or len(content)!=row['size']:raise ValueError('Source differs from map')
        if digest not in cache:
            chunks=[content[i:i+8*1024*1024] for i in range(0,len(content),8*1024*1024)]
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
                futures=[pool.submit(upload,{'encoding':'base64','content':base64.b64encode(b).decode()},digest+'-'+str(i)) for i,b in enumerate(chunks)]
                cache[digest]=[f.result() for f in futures]
            CACHE.write_text(json.dumps(cache,indent=2)+'\n')
        plan.append({**row,'blobs':cache[digest]})
        print('Staged outside Git commits:',row['path'],flush=True)
    result={'version':1,'assets':plan};(WORK/'last-map.json').write_text(json.dumps(result,indent=2)+'\n')
    sha=upload({'encoding':'utf-8','content':json.dumps(result)},'map')
    (WORK/'last-map.sha').write_text(sha+'\n');print('Media map blob:',sha,flush=True)
if __name__=='__main__':main()
