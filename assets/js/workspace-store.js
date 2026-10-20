// Shared project registry and durable per-project browser storage.
export const APP_ROOT=new URL('../../',import.meta.url);
export const FINANCE_ID='finance-001';
export const LEGACY_DESIGN_ID='legacy-design';
let opening,catalogPromise;
const validID=id=>typeof id==='string'&&/^[a-zA-Z0-9_-]{1,80}$/.test(id);
export function requireID(id){if(!validID(id))throw Error('Mã dự án không hợp lệ.');return id;}
export function resourceURL(path){
 if(typeof path!=='string'||!path.startsWith('videos/')||/[\\\u0000-\u001f]/.test(path))throw Error('Đường dẫn tài nguyên không hợp lệ.');
 const url=new URL(path,APP_ROOT);if(url.origin!==APP_ROOT.origin||!decodeURIComponent(url.pathname).startsWith(APP_ROOT.pathname+'videos/')||decodeURIComponent(path).split('/').includes('..'))throw Error('Đường dẫn tài nguyên không hợp lệ.');
 return url;
}
export function cleanMeta(meta){
 if(!meta||!validID(meta.id)||!['video','design'].includes(meta.kind)||typeof meta.name!=='string'||!meta.name.trim()||meta.name.length>100)throw Error('Thông tin dự án không hợp lệ.');
 const out={id:meta.id,name:meta.name.trim(),kind:meta.kind,description:String(meta.description||'').slice(0,500),createdAt:meta.createdAt||new Date().toISOString(),updatedAt:meta.updatedAt||meta.createdAt||new Date().toISOString(),status:String(meta.status||'Đang thực hiện').slice(0,100)};
 for(const key of ['defaultVideo','artwork','gallery','script','audio','review','cover'])if(meta[key]){resourceURL(meta[key]);out[key]=meta[key];}
 return out;
}
async function database(){
 if(!opening)opening=new Promise((resolve,reject)=>{const request=indexedDB.open('credit-studio-workspaces',2);request.onupgradeneeded=()=>{const db=request.result;if(!db.objectStoreNames.contains('projects'))db.createObjectStore('projects',{keyPath:'id'});for(const name of ['documents','files']){const store=db.objectStoreNames.contains(name)?request.transaction.objectStore(name):db.createObjectStore(name,{keyPath:'key'});if(!store.indexNames.contains('projectId'))store.createIndex('projectId','projectId');}};request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(Error('Không mở được bộ nhớ dự án. Hãy cho phép lưu dữ liệu trang web.'));request.onblocked=()=>reject(Error('Bộ nhớ đang được mở ở tab khác. Hãy tải lại trang.'));});
 return opening;
}
async function read(store,key){const db=await database();return new Promise((resolve,reject)=>{const req=db.transaction(store).objectStore(store).get(key);req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);});}
async function all(store){const db=await database();return new Promise((resolve,reject)=>{const req=db.transaction(store).objectStore(store).getAll();req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);});}
async function byProject(store,id){const db=await database();return new Promise((resolve,reject)=>{const req=db.transaction(store).objectStore(store).index('projectId').getAll(id);req.onsuccess=()=>resolve(req.result);req.onerror=()=>reject(req.error);});}
async function write(stores,callback){const db=await database();return new Promise((resolve,reject)=>{const tx=db.transaction(stores,'readwrite');try{callback(tx);}catch(e){tx.abort();reject(e);return;}tx.oncomplete=()=>resolve();tx.onerror=()=>reject(tx.error||Error('Không lưu được dự án.'));tx.onabort=()=>reject(tx.error||Error('Không lưu được dự án.'));});}
export async function catalog(){if(!catalogPromise)catalogPromise=fetch(new URL('projects.json',APP_ROOT),{cache:'no-cache'}).then(async r=>{if(!r.ok)throw Error('Không tải được danh sách dự án đã xuất bản.');const data=await r.json();return data.projects.map(cleanMeta);});return catalogPromise;}
function mergeMeta(published,local){if(!published)return cleanMeta(local);const merged={...published,...local,status:published.status,description:published.description,kind:published.kind};for(const key of ['defaultVideo','artwork','gallery','script','audio','review','cover']){if(published[key])merged[key]=published[key];else delete merged[key];}return cleanMeta(merged);}
export async function getWorkspace(id){requireID(id);const local=await read('projects',id);let published;try{published=(await catalog()).find(p=>p.id===id);}catch(e){if(!local)throw e;}if(local)return mergeMeta(published,local);if(published)return published;if(id===LEGACY_DESIGN_ID)return cleanMeta({id,name:'Thiết kế đã lưu trước đây',kind:'design'});throw Error('Không tìm thấy dự án. Hãy trở về trang Dự án.');}
export async function listWorkspaces(){const [published,local]=await Promise.all([catalog(),all('projects')]);const merged=new Map(published.map(p=>[p.id,p]));for(const p of local)merged.set(p.id,mergeMeta(merged.get(p.id),p));return [...merged.values()].sort((a,b)=>String(b.updatedAt).localeCompare(String(a.updatedAt)));}
export async function registerWorkspace(meta){const checked=cleanMeta(meta);await write(['projects'],tx=>tx.objectStore('projects').put(checked));return checked;}
export async function getDocument(id,kind,slot='main'){requireID(id);requireID(slot);const row=await read('documents',`${id}:${kind}:${slot}`);return row?.data;}
export async function saveDocument(id,kind,data,slot='main'){
 requireID(id);requireID(slot);if(!['video','design'].includes(kind))throw Error('Loại tài liệu không hợp lệ.');const meta=await getWorkspace(id);const now=new Date().toISOString();meta.updatedAt=now;
 if(meta.kind===kind&&slot==='main'&&typeof data.name==='string')meta.name=data.name.slice(0,100)||meta.name;
 await write(['projects','documents'],tx=>{tx.objectStore('projects').put(meta);tx.objectStore('documents').put({key:`${id}:${kind}:${slot}`,projectId:id,kind,slot,data,updatedAt:now});});
 return meta;
}
export function blankDesign(name){return {version:1,name,width:1920,height:1080,bg:'#faf6ec',elements:[]};}
export function blankVideo(name){return {kind:'credit-studio-video',version:1,name,width:1920,height:1080,fps:30,audio:{src:'',offset:0,volume:1},assets:{},clips:[{id:crypto.randomUUID(),title:'Cảnh đầu tiên',duration:8,background:'#faf6ec',fade:0,layers:[{id:crypto.randomUUID(),type:'text',text:'Câu chuyện của bạn\nbắt đầu từ đây.',x:180,y:360,w:1560,h:280,size:100,fill:'#286a52',align:'left',enter:0,effect:'none',opacity:1,drift:0}]}],captions:[],waveform:[],waveformDuration:8,showCaptions:false};}
export async function createWorkspace(name,kind='video',description=''){const meta=cleanMeta({id:crypto.randomUUID(),name,kind,description});await registerWorkspace(meta);await saveDocument(meta.id,kind,kind==='video'?blankVideo(name):blankDesign(name));return meta;}
export async function getFiles(id){requireID(id);return await byProject('files',id);}
export async function addFile(id,file){requireID(id);if(file.size>25*1024*1024)throw Error('Mỗi tệp tối đa 25 MiB.');if(!/^audio\//.test(file.type)&&!['image/png','image/jpeg','image/webp','image/gif'].includes(file.type)&&!(/\.(md|txt)$/i.test(file.name)))throw Error('Chọn ảnh, âm thanh hoặc tài liệu TXT/MD.');const f={id:crypto.randomUUID(),projectId:id,name:file.name,type:file.type||'text/plain',size:file.size,createdAt:new Date().toISOString(),blob:file.type?file:new Blob([file],{type:'text/plain'})};f.key=`${id}:${f.id}`;await write(['files'],tx=>tx.objectStore('files').put(f));return f;}
export async function getFile(id,fileID){requireID(id);requireID(fileID);return read('files',`${id}:${fileID}`);}
export function dataURL(blob){return new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=()=>reject(Error('Không đọc được tệp.'));r.readAsDataURL(blob);});}
export async function makeBackup(id){const project=await getWorkspace(id),documents=(await byProject('documents',id)).map(({kind,slot,data})=>({kind,slot,data}));const files=await Promise.all((await getFiles(id)).map(async f=>({id:f.id,name:f.name,type:f.type,createdAt:f.createdAt,data:await dataURL(f.blob)})));return {kind:'credit-studio-workspace',version:1,project,documents,files};}
export async function restoreBackup(bundle,validateVideo,validateDesign){
 if(!bundle||bundle.kind!=='credit-studio-workspace'||bundle.version!==1||!Array.isArray(bundle.documents)||bundle.documents.length>300||!Array.isArray(bundle.files)||bundle.files.length>200)throw Error('Tệp sao lưu không hợp lệ.');
 const meta=cleanMeta({...bundle.project,id:crypto.randomUUID(),name:(String(bundle.project?.name||'Dự án')+' (khôi phục)').slice(0,100),createdAt:new Date().toISOString()});
 const documents=bundle.documents.map(d=>{requireID(d.slot);if(!['video','design'].includes(d.kind))throw Error('Tài liệu không hợp lệ.');return {...d,data:d.kind==='video'?validateVideo(d.data):validateDesign(d.data)};});
 const files=await Promise.all(bundle.files.map(async f=>{requireID(f.id);if(typeof f.name!=='string'||typeof f.data!=='string'||!/^data:(audio\/[a-z0-9.+-]+|image\/(png|jpeg|webp|gif)|text\/[a-z0-9.+-]+);base64,/i.test(f.data))throw Error('Tệp đính kèm không hợp lệ.');const blob=await(await fetch(f.data)).blob();if(blob.size>25*1024*1024)throw Error('Tệp đính kèm quá lớn.');return {id:f.id,key:`${meta.id}:${f.id}`,projectId:meta.id,name:f.name.slice(0,200),type:blob.type,size:blob.size,blob,createdAt:f.createdAt||new Date().toISOString()};}));
 await write(['projects','documents','files'],tx=>{tx.objectStore('projects').put(meta);for(const d of documents)tx.objectStore('documents').put({...d,projectId:meta.id,key:`${meta.id}:${d.kind}:${d.slot}`});for(const f of files)tx.objectStore('files').put(f);});return meta;
}
export async function migrateLegacy(validateVideo,validateDesign){
 for(const [key,id,kind,validator] of [['credit-studio-video-intro-v1',FINANCE_ID,'video',validateVideo],['credit-studio-v1',LEGACY_DESIGN_ID,'design',validateDesign]]){
  if(await getDocument(id,kind))continue;
  let raw;try{raw=localStorage.getItem(key);}catch{continue;}if(!raw)continue;
  let data;try{data=validator(JSON.parse(raw));}catch{continue;}
  const meta=await getWorkspace(id);if(kind==='design'){meta.name=data.name||meta.name;await registerWorkspace(meta);}
  await saveDocument(id,kind,data);
 }
}
export function notifySaved(id){if(window.parent!==window)window.parent.postMessage({type:'credit-workspace-saved',projectId:id},location.origin);}
