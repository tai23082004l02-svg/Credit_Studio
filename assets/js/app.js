import {validateDesign as validate} from './design-model.js';
import {APP_ROOT,LEGACY_DESIGN_ID,getWorkspace,getDocument,saveDocument,resourceURL,getFile,dataURL,notifySaved} from './workspace-store.js?v=r2-v1';
const $ = s => document.querySelector(s);
const svg = $('#artboard');
const NS = 'http://www.w3.org/2000/svg';
const KEY = 'credit-studio-v1';
const params=new URLSearchParams(location.search),workspaceID=params.get('project')||LEGACY_DESIGN_ID;
const slot=params.get('scene')?'scene-'+params.get('scene'):params.get('file')?'file-'+params.get('file'):'main';
let initializing=true,pendingSave=Promise.resolve();
if(params.get('embed')==='1')document.documentElement.classList.add('embedded');
let selected = null, history = [], future = [], drag = null, toastTimer;
const uid = () => crypto.randomUUID();
function element(type, props = {}) { return {id:uid(),type,x:80,y:80,w:240,h:160,fill:'#8657dc',opacity:100,...props}; }
function template(kind) {
  if (kind === 'blank') return {version:1,name:'Thiết kế của tôi',width:800,height:1000,bg:'#ffffff',elements:[]};
  if (kind === 'social') return {version:1,name:'Một chút cảm hứng',width:1080,height:1080,bg:'#eef1df',elements:[element('circle',{x:650,y:80,w:520,h:520,fill:'#d0dab0'}),element('rect',{x:70,y:110,w:100,h:12,fill:'#41604b'}),element('text',{x:70,y:350,w:940,h:250,text:'Một chút\ncảm hứng mới.',size:98,font:'Times New Roman',weight:400,fill:'#344c3c'}),element('text',{x:75,y:870,w:900,h:80,text:'DÀNH THỜI GIAN CHO NHỮNG ĐIỀU BẠN YÊU.',size:24,font:'Times New Roman',weight:400,fill:'#41604b'})]};
  return {version:1,name:'Make it happen',width:800,height:1000,bg:'#e5dcff',elements:[element('circle',{x:420,y:80,w:480,h:480,fill:'#b9ed9c'}),element('text',{x:65,y:75,w:500,h:50,text:'C R E D I T   S T U D I O',size:20,font:'Times New Roman',weight:700,fill:'#503379'}),element('text',{x:60,y:335,w:700,h:340,text:'MAKE\nIT HAPPEN.',size:108,font:'Times New Roman',weight:700,fill:'#3d2462'}),element('rect',{x:65,y:770,w:90,h:10,fill:'#7250b0'}),element('text',{x:65,y:830,w:670,h:100,text:'Ý tưởng của bạn. Dấu ấn của bạn.\nBắt đầu sáng tạo ngay hôm nay.',size:25,font:'Times New Roman',weight:400,fill:'#624881'})]};
}
let state = template('poster');
function toast(message) { $('#toast').textContent=message; $('#toast').hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>$('#toast').hidden=true,3500); }
function remember() { history.push(JSON.stringify(state)); if(history.length>35) history.shift(); future=[]; }
function persist() {
 const snapshot=JSON.parse(JSON.stringify(state));$('#save-status').textContent='Đang lưu…';
 pendingSave=pendingSave.catch(()=>{}).then(()=>saveDocument(workspaceID,'design',snapshot,slot)).then(()=>{$('#save-status').textContent='Đã lưu vào dự án';notifySaved(workspaceID);}).catch(e=>{$('#save-status').textContent='Chưa lưu — hãy tải JSON';toast(e.message);throw e;});
 pendingSave.catch(()=>{});return pendingSave;
}
function change(fn) { if(initializing)return;remember();fn();render();persist(); }
function current() {return state.elements.find(e=>e.id===selected);}
function node(tag, attrs={}, parent=svg) {const n=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,String(v));parent.append(n);return n;}
function renderCanvas() {
 svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${state.width} ${state.height}`);
 node('rect',{width:state.width,height:state.height,fill:state.bg});
 for(const e of state.elements) {
  const g=node('g',{'data-id':e.id,opacity:e.opacity/100,transform:`translate(${e.x} ${e.y})`});
  if(e.type==='rect') node('rect',{width:e.w,height:e.h,fill:e.fill},g);
  if(e.type==='circle') node('ellipse',{cx:e.w/2,cy:e.h/2,rx:e.w/2,ry:e.h/2,fill:e.fill},g);
  if(e.type==='image') node('image',{href:e.src,width:e.w,height:e.h,preserveAspectRatio:'none'},g);
  if(e.type==='text') {
   const t=node('text',{fill:e.fill,'font-family':e.font,'font-size':e.size,'font-weight':e.weight},g);
   e.text.split('\n').forEach((line,i)=>{node('tspan',{x:0,y:e.size+i*e.size*1.2},t).textContent=line;});
  }
 }
 const e=current(); if(e) node('rect',{'data-selection':'true',x:e.x,y:e.y,width:e.w,height:e.h,fill:'none',stroke:'#8657dc','stroke-width':2,'vector-effect':'non-scaling-stroke','stroke-dasharray':'6 3','pointer-events':'none'});
 fit();
}
function fit() {
 const box=$('#workspace');let scale=Number($('#zoom').value);
 if(!scale) scale=Math.min((box.clientWidth-76)/state.width,(box.clientHeight-76)/state.height,1);
 scale=Math.max(.05,scale);svg.style.width=`${state.width*scale}px`;svg.style.height=`${state.height*scale}px`;
}
function render() {
 renderCanvas();$('#project-name').value=state.name;$('#page-width').value=state.width;$('#page-height').value=state.height;$('#page-color').value=state.bg;
 $('#dimensions').textContent=`${state.width} × ${state.height} px`;
 const e=current();$('#element-controls').disabled=!e;$('#empty-selection').hidden=!!e;
 $('#selection-status').textContent=e?'Kéo để di chuyển · Chỉnh kích thước ở bảng bên phải':'Chọn một phần tử để chỉnh sửa';
 if(e) {
  document.querySelectorAll('[data-prop]').forEach(input=>{input.value=e[input.dataset.prop]??'';});
  $('#text-controls').hidden=e.type!=='text';$('#fill-label').hidden=e.type==='image';
 }
 $('#undo').disabled=!history.length;$('#redo').disabled=!future.length;
 $('#layers').replaceChildren();$('#layer-count').textContent=state.elements.length;
 [...state.elements].reverse().forEach(e=>{const b=document.createElement('button');b.textContent=(e.type==='text'?'T  '+e.text:e.type==='image'?'▧  Ảnh':e.type==='circle'?'○  Hình tròn':'▭  Hình chữ nhật');b.classList.toggle('selected',e.id===selected);b.onclick=()=>{selected=e.id;render();};$('#layers').append(b);});
}
function add(e) {change(()=>{state.elements.push(e);selected=e.id;});}
$('#add-text').onclick=()=>add(element('text',{text:'Nhập nội dung của bạn',size:42,font:'Times New Roman',weight:700,fill:'#392753',w:600,h:65}));
$('#add-rect').onclick=()=>add(element('rect'));
$('#add-circle').onclick=()=>add(element('circle',{w:220,h:220,fill:'#b9ed9c'}));
function replaceTemplate(kind) { if(!confirm('Thay trang hiện tại bằng mẫu mới? Bạn có thể hoàn tác.'))return; change(()=>{state=template(kind);selected=null;}); }
document.querySelectorAll('[data-template]').forEach(b=>b.onclick=()=>replaceTemplate(b.dataset.template));$('#blank').onclick=()=>replaceTemplate('blank');
$('#project-name').onchange=e=>change(()=>state.name=e.target.value.trim()||'Thiết kế của tôi');
for(const [id,key] of [['page-width','width'],['page-height','height']]) $( `#${id}`).onchange=e=>{const n=Number(e.target.value);if(!Number.isFinite(n)||n<100||n>4096){toast('Kích thước từ 100 đến 4096 px.');render();return;}change(()=>state[key]=Math.round(n));};
$('#page-color').onchange=e=>change(()=>state.bg=e.target.value);
document.querySelectorAll('[data-prop]').forEach(input=>input.onchange=()=>{
 const e=current();if(!e)return;const key=input.dataset.prop;
 let v=input.value;if(input.type==='number'||input.type==='range'){v=Number(v);if(!Number.isFinite(v)||v<Number(input.min)||v>Number(input.max)){toast('Giá trị nằm ngoài phạm vi cho phép.');render();return;}}
 change(()=>e[key]=v);
});
$('#zoom').onchange=fit;new ResizeObserver(fit).observe($('#workspace'));
function undo() {if(!history.length)return;future.push(JSON.stringify(state));state=JSON.parse(history.pop());selected=null;render();persist();}
function redo() {if(!future.length)return;history.push(JSON.stringify(state));state=JSON.parse(future.pop());selected=null;render();persist();}
$('#undo').onclick=undo;$('#redo').onclick=redo;
function remove(){if(current())change(()=>{state.elements=state.elements.filter(e=>e.id!==selected);selected=null;});}
$('#delete').onclick=remove;
$('#duplicate').onclick=()=>{const e=current();if(e)add({...e,id:uid(),x:e.x+20,y:e.y+20});};
for(const [id,delta] of [['backward',-1],['forward',1]]) $(`#${id}`).onclick=()=>{const i=state.elements.findIndex(e=>e.id===selected),j=i+delta;if(i<0||j<0||j>=state.elements.length)return;change(()=>{[state.elements[i],state.elements[j]]=[state.elements[j],state.elements[i]];});};
function point(event){const p=new DOMPoint(event.clientX,event.clientY);return p.matrixTransform(svg.getScreenCTM().inverse());}
svg.onpointerdown=event=>{
 if(event.button!==0)return;const target=event.target.closest('[data-id]');selected=target?.dataset.id??null;render();
 const e=current();if(e){const p=point(event);drag={id:e.id,x:p.x,y:p.y,ox:e.x,oy:e.y,before:JSON.stringify(state)};svg.setPointerCapture(event.pointerId);}
};
svg.onpointermove=event=>{if(!drag)return;const e=current();if(!e)return;const p=point(event);e.x=Math.round(drag.ox+p.x-drag.x);e.y=Math.round(drag.oy+p.y-drag.y);renderCanvas();};
function endDrag(){if(!drag)return;const before=drag.before;drag=null;if(before!==JSON.stringify(state)){history.push(before);if(history.length>35)history.shift();future=[];persist();}render();}
svg.onpointerup=endDrag;svg.onpointercancel=endDrag;
document.addEventListener('keydown',event=>{
 if(event.target.closest('input,textarea,select,[contenteditable]'))return;
 if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='z'){event.preventDefault();event.shiftKey?redo():undo();return;}
 if(event.key==='Delete'||event.key==='Backspace'){if(current()){event.preventDefault();remove();}return;}
 const e=current(),d={ArrowLeft:[-1,0],ArrowRight:[1,0],ArrowUp:[0,-1],ArrowDown:[0,1]}[event.key];
 if(e&&d){event.preventDefault();change(()=>{e.x+=d[0]*(event.shiftKey?10:1);e.y+=d[1]*(event.shiftKey?10:1);});}
});
function download(blob,ext){const a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download=(state.name.replace(/[^\p{L}\p{N} _-]/gu,'').slice(0,80)||'design')+ext;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('#save-project').onclick=()=>download(new Blob([JSON.stringify(state,null,2)],{type:'application/json'}),'.json');
$('#export').onclick=async()=>{
 const button=$('#export');button.disabled=true;button.textContent='Đang xuất…';let url;
 try {
  await document.fonts.ready;
  const copy=svg.cloneNode(true);copy.querySelector('[data-selection]')?.remove();copy.removeAttribute('style');copy.setAttribute('width',state.width);copy.setAttribute('height',state.height);
  url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(copy)],{type:'image/svg+xml;charset=utf-8'}));
  const img=new Image();img.src=url;await img.decode();
  const canvas=document.createElement('canvas');canvas.width=state.width;canvas.height=state.height;canvas.getContext('2d').drawImage(img,0,0);
  const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));if(!blob)throw new Error();download(blob,'.png');toast('Đã xuất PNG đúng kích thước thiết kế.');
 }catch{toast('Không thể xuất ảnh. Hãy thử giảm kích thước trang.');}finally{if(url)URL.revokeObjectURL(url);button.disabled=false;button.textContent='↓ Xuất PNG';}
};
$('#upload').onclick=()=>$('#image-file').click();
$('#image-file').onchange=async event=>{
 const file=event.target.files[0];event.target.value='';if(!file)return;
 if(!['image/png','image/jpeg','image/webp','image/gif'].includes(file.type)||file.size>15*1024*1024){toast('Chọn PNG, JPEG, WebP hoặc GIF tối đa 15 MB.');return;}
 try{const src=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=reject;r.readAsDataURL(file);});const img=new Image();img.src=src;await img.decode();const scale=Math.min(1,state.width*.7/img.width,state.height*.7/img.height);add(element('image',{src,w:Math.round(img.width*scale),h:Math.round(img.height*scale)}));}catch{toast('Không thể đọc tệp ảnh.');}
};
$('#open-project').onclick=()=>$('#project-file').click();
$('#project-file').onchange=async event=>{const file=event.target.files[0];event.target.value='';if(!file)return;if(file.size>30*1024*1024){toast('Dự án tối đa 30 MB.');return;}try{const data=validate(JSON.parse(await file.text()));change(()=>{state=data;selected=null;});toast('Đã mở dự án.');}catch{toast('Tệp dự án không hợp lệ hoặc không được hỗ trợ.');}};
window.creditDesign={get ready(){return !initializing;},get project(){return JSON.parse(JSON.stringify(state));},flush:()=>pendingSave};
async function init(){
 document.querySelectorAll('button').forEach(b=>b.disabled=true);
 try{
  const meta=await getWorkspace(workspaceID);let saved=await getDocument(workspaceID,'design',slot);
  if(saved)state=validate(saved);
  else if(params.get('scene')){
   if(!meta.artwork)throw Error('Dự án chưa có bộ hình cảnh.');
   const manifestURL=resourceURL(meta.artwork),response=await fetch(manifestURL,{cache:'no-cache'});if(!response.ok)throw Error('Không tải được danh sách cảnh.');
   const manifest=await response.json(),frame=manifest.frames.find(f=>f.id===params.get('scene'));if(!frame)throw Error('Không tìm thấy cảnh.');
   const source=new URL(frame.project,manifestURL);if(source.origin!==APP_ROOT.origin||!source.pathname.startsWith(APP_ROOT.pathname+'videos/'))throw Error('Đường dẫn cảnh không hợp lệ.');
   const r=await fetch(source);if(!r.ok)throw Error('Không tải được dự án cảnh.');state=validate(await r.json());
  }else if(params.get('file')){
   const file=await getFile(workspaceID,params.get('file'));if(!file||!file.type.startsWith('image/'))throw Error('Không tìm thấy ảnh trong dự án.');
   const src=await dataURL(file.blob),image=new Image();image.src=src;await image.decode();const scale=Math.min(1920/image.width,1080/image.height,1);
   state={version:1,name:file.name,width:1920,height:1080,bg:'#faf6ec',elements:[element('image',{src,x:(1920-image.width*scale)/2,y:(1080-image.height*scale)/2,w:image.width*scale,h:image.height*scale})]};
  }else if(workspaceID===LEGACY_DESIGN_ID){
   try{const raw=localStorage.getItem(KEY);if(raw)state=validate(JSON.parse(raw));}catch{}
  }else state={version:1,name:(meta.name+' — Thiết kế').slice(0,100),width:1920,height:1080,bg:'#faf6ec',elements:[]};
  if(workspaceID===LEGACY_DESIGN_ID){try{const migration=KEY+'-times-new-roman-v1';if(!localStorage.getItem(migration)){state.elements.forEach(e=>{if(e.type==='text')e.font='Times New Roman';});localStorage.setItem(migration,'1');}}catch{}}
  await persist();initializing=false;document.querySelectorAll('button').forEach(b=>b.disabled=false);render();
 }catch(e){toast(e.message);$('#save-status').textContent='Không mở được dự án';}
}
render();init();
