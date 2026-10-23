#!/usr/bin/env python3
"""R2 media sync using direct environment credentials; never prints credentials/headers.
Commands: check, plan, sync, verify, cors. Uses only the Python standard library.
"""
import argparse,datetime,hashlib,hmac,json,mimetypes,os,re,subprocess,sys,urllib.error,urllib.parse,urllib.request,uuid,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MANIFEST=ROOT/'storage/manifest.json'
class StorageError(Exception):pass
class R2:
 def __init__(self):
  self.access=os.environ.get('R2_ACCESS_KEY_ID','').strip();self.secret=os.environ.get('R2_SECRET_ACCESS_KEY','').strip();self.endpoint=os.environ.get('R2_ENDPOINT_URL','').strip().rstrip('/');self.bucket=os.environ.get('R2_BUCKET','').strip()
  if not all([self.access,self.secret,self.endpoint,self.bucket]):raise StorageError('Missing R2 environment variables.')
  # Cloudflare documents S3 access ID = token ID; secret = SHA-256(token value).
  # Accept the earlier UI entry where token value and token ID were put into S3 fields.
  is_id=lambda v:bool(re.fullmatch(r'[a-fA-F0-9]{32}',v))
  is_secret=lambda v:bool(re.fullmatch(r'[a-fA-F0-9]{64}',v))
  self.credential_mode='s3_keys'
  if is_id(self.secret) and 40<=len(self.access)<=256:
   token=self.access;self.access=self.secret;self.secret=hashlib.sha256(token.encode()).hexdigest();self.credential_mode='token_value_and_id'
  elif is_id(self.access) and not is_secret(self.secret) and 40<=len(self.secret)<=256:
   self.secret=hashlib.sha256(self.secret.encode()).hexdigest();self.credential_mode='id_and_token_value'
  if not is_id(self.access) or not is_secret(self.secret):raise StorageError('Use S3 access ID/secret or Cloudflare token ID/value in environment variables.')
  u=urllib.parse.urlsplit(self.endpoint)
  if u.scheme!='https' or not u.hostname or not u.hostname.endswith('.r2.cloudflarestorage.com') or u.path not in ('','/') or u.query or u.fragment or u.username or u.password or u.port not in (None,443):raise StorageError('Invalid R2 S3 endpoint; use HTTPS without a bucket path.')
  if not re.fullmatch(r'[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]',self.bucket):raise StorageError('Invalid bucket name.')
  self.host=u.netloc
 def request(self,method,key='',query='',body=b'',extra=None,missing_ok=False):
  path='/'+urllib.parse.quote(self.bucket,safe='')+('/'+urllib.parse.quote(key,safe='/') if key else '')
  now=datetime.datetime.now(datetime.timezone.utc);date=now.strftime('%Y%m%d');stamp=now.strftime('%Y%m%dT%H%M%SZ');digest=hashlib.sha256(body).hexdigest();headers={'host':self.host,'x-amz-content-sha256':digest,'x-amz-date':stamp,**(extra or {})};headers={k.lower():str(v).strip() for k,v in headers.items()};signed=';'.join(sorted(headers));chs=''.join(k+':'+headers[k]+'\n' for k in sorted(headers));canonical='\n'.join([method,path,query,chs,signed,digest]);scope=date+'/auto/s3/aws4_request';string='\n'.join(['AWS4-HMAC-SHA256',stamp,scope,hashlib.sha256(canonical.encode()).hexdigest()]);signing=('AWS4'+self.secret).encode()
  for value in [date,'auto','s3','aws4_request']:signing=hmac.new(signing,value.encode(),hashlib.sha256).digest()
  signature=hmac.new(signing,string.encode(),hashlib.sha256).hexdigest();headers['authorization']=f'AWS4-HMAC-SHA256 Credential={self.access}/{scope}, SignedHeaders={signed}, Signature={signature}'
  url=self.endpoint+path+('?'+query if query else '');request=urllib.request.Request(url,data=body if method in ('PUT','POST') else None,headers=headers,method=method)
  try:
   with urllib.request.urlopen(request,timeout=90) as r:return r.status,dict(r.headers.items()),r.read()
  except urllib.error.HTTPError as e:
   if missing_ok and e.code==404:return 404,{},b''
   try:
    error=ET.fromstring(e.read());code=error.findtext('{*}Code') or 'unknown';message=error.findtext('{*}Message') or ''
    for private in [self.access,self.secret,headers.get('authorization','')]:
     if private:message=message.replace(private,'[redacted]')
    message=message[:300]
   except Exception:code='unknown';message=''
   raise StorageError(f'R2 {method} HTTP {e.code}: {code} {message}') from None
  except (urllib.error.URLError,TimeoutError):raise StorageError(f'R2 {method}: network request failed') from None

def plan():
 old=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
 # Keep archived entries after their originals have been removed from Git.
 assets=dict(old.get('assets',{}));extensions={'.png','.jpg','.jpeg','.webp','.gif','.mp3','.wav','.mp4','.webm'}
 tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
 for relative in sorted(tracked):
  if not relative or not relative.startswith(('videos/','library/props/','assets/samples/')):continue
  p=ROOT/relative
  if p.suffix.lower() not in extensions or not p.is_file():continue
  digest=hashlib.sha256(p.read_bytes()).hexdigest();assets[relative]={'key':'credit-studio/media/'+digest+p.suffix.lower(),'sha256':digest,'size':p.stat().st_size,'type':mimetypes.guess_type(p.name)[0] or 'application/octet-stream'}
 out={'version':1,'enabled':old.get('enabled',False),'publicBaseURL':old.get('publicBaseURL',''),'assets':assets};MANIFEST.parent.mkdir(exist_ok=True);MANIFEST.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'planned_files':len(assets),'bytes':sum(x['size'] for x in assets.values())}));return out

def check(client):
 status,_,data=client.request('GET',query='list-type=2&max-keys=1');root=ET.fromstring(data);print(json.dumps({'list_status':status,'sample_objects':len(root.findall('.//{*}Contents'))}))
 key='_credit-studio-checks/'+uuid.uuid4().hex+'.txt';data=b'Credit Studio R2 connection check.\n'
 try:
  client.request('PUT',key,body=data);status,_,actual=client.request('GET',key)
  if actual!=data:raise StorageError('Test download differs from original.')
 finally:client.request('DELETE',key)
 print('Read/write/download comparison and test cleanup passed.')

def cors(client):
 status,_,data=client.request('GET',query='cors=',missing_ok=True)
 ns='http://s3.amazonaws.com/doc/2006-03-01/';ET.register_namespace('',ns)
 root=ET.Element('{'+ns+'}CORSConfiguration') if status==404 else ET.fromstring(data)
 # Preserve other rules; replace only the rule managed by this tool.
 for child in list(root):
  if child.findtext('{*}ID')=='credit-studio-media':root.remove(child)
 rule=ET.SubElement(root,'{'+ns+'}CORSRule');ET.SubElement(rule,'{'+ns+'}ID').text='credit-studio-media'
 for origin in ['https://tai23082004l02-svg.github.io','http://127.0.0.1:8000','http://127.0.0.1:8002','http://localhost:8000']:ET.SubElement(rule,'{'+ns+'}AllowedOrigin').text=origin
 for method in ['GET','HEAD']:ET.SubElement(rule,'{'+ns+'}AllowedMethod').text=method
 for name in ['Range','Content-Type']:ET.SubElement(rule,'{'+ns+'}AllowedHeader').text=name
 for name in ['ETag','Content-Length','Content-Range','Accept-Ranges']:ET.SubElement(rule,'{'+ns+'}ExposeHeader').text=name
 ET.SubElement(rule,'{'+ns+'}MaxAgeSeconds').text='3600';payload=ET.tostring(root,encoding='utf-8',xml_declaration=True)
 client.request('PUT',query='cors=',body=payload,extra={'content-type':'application/xml'});_,_,actual=client.request('GET',query='cors=');rules=ET.fromstring(actual).findall('{*}CORSRule')
 if not any(r.findtext('{*}ID')=='credit-studio-media' for r in rules):raise StorageError('CORS readback did not contain the saved rule.')
 print('CORS rule saved and read back; unrelated rules preserved.')

def sync(client,manifest):
 changed=0
 for relative,item in manifest['assets'].items():
  status,headers,_=client.request('HEAD',item['key'],missing_ok=True);headers={k.lower():v for k,v in headers.items()}
  if status==200:
   if headers.get('x-amz-meta-sha256')!=item['sha256'] or int(headers.get('content-length','-1'))!=item['size']:raise StorageError('Existing content-addressed object does not match expected metadata; not overwriting.')
   continue
  client.request('PUT',item['key'],body=(ROOT/relative).read_bytes(),extra={'content-type':item['type'],'cache-control':'public, max-age=31536000, immutable','x-amz-meta-sha256':item['sha256'],'if-none-match':'*'});changed+=1;print('Uploaded:',relative,flush=True)
 print(json.dumps({'uploaded':changed,'total_files':len(manifest['assets'])}))

def verify(client,manifest):
 for relative,item in manifest['assets'].items():
  _,_,data=client.request('GET',item['key'])
  if len(data)!=item['size'] or hashlib.sha256(data).hexdigest()!=item['sha256']:raise StorageError('Media verification failed: '+relative)
  print('Verified:',relative,flush=True)
 print(json.dumps({'verified_files':len(manifest['assets']),'verified_bytes':sum(i['size'] for i in manifest['assets'].values())}))

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['plan','check','sync','verify','cors']);args=parser.parse_args()
 if args.command=='plan':plan();return
 client=R2()
 if args.command=='check':check(client)
 elif args.command=='cors':cors(client)
 else:
  manifest=plan() if args.command=='sync' else json.loads(MANIFEST.read_text())
  (sync if args.command=='sync' else verify)(client,manifest)
if __name__=='__main__':
 try:main()
 except (StorageError,OSError,ValueError) as e:
  # OSError messages can contain URLs; disclose only their class outside known errors.
  print(str(e) if isinstance(e,StorageError) else type(e).__name__,file=sys.stderr);sys.exit(1)
