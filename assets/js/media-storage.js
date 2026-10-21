// Logical project paths stay stable; this maps only registered public media to R2.
const ROOT=new URL('../../',import.meta.url);
let config={version:1,enabled:false,publicBaseURL:'',assets:{}},opening;
export function validateStorage(value){
 if(!value||value.version!==1||typeof value.enabled!=='boolean'||typeof value.publicBaseURL!=='string'||!value.assets||typeof value.assets!=='object'||Array.isArray(value.assets))throw Error('Invalid media storage manifest');
 if(value.publicBaseURL){const u=new URL(value.publicBaseURL);if(u.protocol!=='https:'||u.username||u.password||u.search||u.hash||u.pathname!=='/')throw Error('Invalid public media origin');}
 if(value.enabled&&!value.publicBaseURL)throw Error('Missing public media origin');
 for(const [path,item] of Object.entries(value.assets)){
  if(!/^(videos\/|library\/props\/|assets\/samples\/)/.test(path)||/[\\\u0000-\u001f]/.test(path)||path.split('/').some(p=>p==='.'||p==='..')||!item||!/^credit-studio\/media\/[a-f0-9]{64}\.(png|jpe?g|webp|gif|mp3|wav|mp4|webm)$/.test(item.key)||!/^[a-f0-9]{64}$/.test(item.sha256)||!Number.isSafeInteger(item.size)||item.size<0)throw Error('Invalid media entry');
 }
 return value;
}
export async function initStorage(){if(!opening)opening=(async()=>{try{const r=await fetch(new URL('storage/manifest.json',ROOT),{cache:'no-cache'});if(!r.ok)throw Error();config=validateStorage(await r.json());}catch{config={version:1,enabled:false,publicBaseURL:'',assets:{}};}return config;})();return opening;}
export function mediaURL(path,base=ROOT){
 const local=new URL(path,base);if(!config.enabled||local.protocol==='data:'||local.origin!==ROOT.origin||!local.pathname.startsWith(ROOT.pathname))return local.href;
 const logical=decodeURIComponent(local.pathname.slice(ROOT.pathname.length)),entry=config.assets[logical];return entry?new URL(entry.key,config.publicBaseURL).href:local.href;
}
