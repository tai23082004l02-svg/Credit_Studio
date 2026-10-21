import {initStorage,mediaURL} from './media-storage.js?v=r2-v1';
import {safeSource,validate} from '../../video/engine.js?v=r2-v1';
const root=new URL('../../',import.meta.url),pictures=new Map();
export function validateProp(p){
 if(!p||typeof p.id!=='string'||!/^[a-z0-9_-]{1,80}$/i.test(p.id)||typeof p.name!=='string'||!p.name.trim()||p.name.length>100||typeof p.category!=='string'||p.category.length>100||!Array.isArray(p.tags)||p.tags.some(t=>typeof t!=='string')||!safeSource(p.src)||!/^.*\.(png|jpg|jpeg|webp)$/i.test(p.src)||p.src.startsWith('data:'))throw Error('Thông tin đạo cụ không hợp lệ.');
 if(p.crop&&(!Array.isArray(p.crop)||p.crop.length!==4||p.crop.some(v=>typeof v!=='number'||!Number.isFinite(v)||v<0||v>8192)||p.crop[2]<=0||p.crop[3]<=0))throw Error('Vùng ảnh đạo cụ không hợp lệ.');
 return p;
}
export async function loadProps(){const r=await fetch(new URL('library/props/catalog.json',root),{cache:'no-cache'});if(!r.ok)throw Error('Chưa tải được kho đạo cụ. Hãy thử mở lại.');const data=await r.json();if(data.version!==1||!Array.isArray(data.items)||data.items.length>2000)throw Error('Danh mục đạo cụ không hợp lệ.');const ids=new Set();for(const p of data.items){validateProp(p);if(ids.has(p.id))throw Error('Mã đạo cụ trùng nhau.');ids.add(p.id);}return data.items;}
export async function propImage(p){validateProp(p);await initStorage();if(!pictures.has(p.src)){const task=(async()=>{const img=new Image();img.crossOrigin='anonymous';img.src=mediaURL(p.src,root);await img.decode();return img;})();pictures.set(p.src,task);task.catch(()=>pictures.delete(p.src));}const img=await pictures.get(p.src),crop=p.crop||[0,0,img.naturalWidth,img.naturalHeight];if(crop[0]+crop[2]>img.naturalWidth||crop[1]+crop[3]>img.naturalHeight)throw Error('Vùng cắt đạo cụ vượt ảnh gốc.');return {img,crop};}
export async function drawProp(canvas,p){const {img,crop}=await propImage(p),ctx=canvas.getContext('2d');ctx.clearRect(0,0,canvas.width,canvas.height);const scale=Math.min((canvas.width-40)/crop[2],(canvas.height-40)/crop[3]),w=crop[2]*scale,h=crop[3]*scale;ctx.drawImage(img,...crop,(canvas.width-w)/2,(canvas.height-h)/2,w,h);}
export async function propPNG(p){const {img,crop}=await propImage(p),canvas=document.createElement('canvas');canvas.width=Math.ceil(crop[2]);canvas.height=Math.ceil(crop[3]);canvas.getContext('2d').drawImage(img,...crop,0,0,canvas.width,canvas.height);return new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(Error('Không tải được PNG đạo cụ.')),'image/png'));}
export async function insertProp(project,p,index){validate(project);validateProp(p);if(!Number.isInteger(index)||!project.clips[index])throw Error('Hãy chọn cảnh cần thêm đạo cụ.');const {crop}=await propImage(p),key='prop-'+crypto.randomUUID(),scale=Math.min(560/crop[2],560/crop[3]);const next=structuredClone(project),w=crop[2]*scale,h=crop[3]*scale;
 next.assets[key]={src:p.src,label:p.name,...(p.crop?{crop:[...p.crop]}:{})};next.clips[index].layers.push({id:key,type:'image',asset:key,x:(1920-w)/2,y:(1080-h)/2,w,h,enter:0,effect:'pop',opacity:1,drift:0});return validate(next);
}
export function replaceProp(project,p,clipID,layerID){
 validate(project);validateProp(p);const next=structuredClone(project),clip=next.clips.find(c=>c.id===clipID),layer=clip?.layers.find(l=>l.id===layerID);
 if(!layer||layer.type!=='image')throw Error('Hãy chọn lớp ảnh cần thay.');
 const previous=layer.asset,key='prop-'+crypto.randomUUID();
 next.assets[key]={src:p.src,label:p.name,...(p.crop?{crop:[...p.crop]}:{})};layer.asset=key;
 if(!next.clips.some(c=>c.layers.some(l=>l.type==='image'&&l.asset===previous)))delete next.assets[previous];
 return validate(next);
}
