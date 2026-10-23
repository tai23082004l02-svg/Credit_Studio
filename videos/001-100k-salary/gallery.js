import {initStorage,mediaURL} from '../../assets/js/media-storage.js?v=r2-media-v3';
const workspaceParams=new URLSearchParams(location.search);const workspaceID=workspaceParams.get('project')||'finance-001';if(workspaceParams.get('embed')==='1')document.documentElement.classList.add('embedded');
'use strict';
const svgNS='http://www.w3.org/2000/svg';
function el(tag,attrs={},text=''){const n=document.createElement(tag);for(const [key,value]of Object.entries(attrs))n.setAttribute(key,value);n.textContent=text;return n;}
function link(label,href,download=false){return el('a',{href,...(download?{download:''}:{})},label);}
async function renderGallery(){
 await initStorage();const media=path=>mediaURL(path,new URL('./',import.meta.url));
 const response=await fetch('artwork.json',{cache:'no-cache'});if(!response.ok)throw Error('Không tải được danh sách ảnh.');
 const data=await response.json();
 for(const frame of data.frames){
  const card=el('article'),figure=el('figure');
  figure.append(el('img',{src:media(frame.image),alt:frame.title,loading:'lazy',width:1672,height:941}));
  const overlay=document.createElementNS(svgNS,'svg');overlay.setAttribute('viewBox','0 0 1920 1080');overlay.setAttribute('aria-hidden','true');
  for(const item of frame.overlays){
   const text=document.createElementNS(svgNS,'text');
   for(const [key,value]of Object.entries({fill:item.fill??'#272c2a','font-family':'Times New Roman','font-weight':'700','font-size':item.size}))text.setAttribute(key,value);
   item.text.split('\n').forEach((line,i)=>{const span=document.createElementNS(svgNS,'tspan');span.setAttribute('x',item.x);span.setAttribute('y',item.y+item.size+i*item.size*1.2);span.textContent=line;text.append(span);});overlay.append(text);
  }
  figure.append(overlay);
  const copy=el('div',{class:'copy'});copy.append(el('h3',{},frame.id+' · '+frame.title),el('p',{},'Phần '+frame.section+' · “'+frame.cue+'”'),el('p',{},frame.motion));
  const links=el('div',{class:'links'});const editURL=new URL('../../',location.href);editURL.searchParams.set('project',workspaceID);editURL.searchParams.set('tab','images');editURL.searchParams.set('scene',frame.id);const edit=link('Chỉnh cảnh trong dự án',editURL.href);edit.target='_top';links.append(edit,link('Xem PNG gốc',media(frame.image)),link('Tải dự án JSON',frame.project,true));copy.append(links);card.append(figure,copy);document.querySelector('#scenes').append(card);
 }
 for(const sheet of data.sheets){const card=el('article'),imageLink=link('',media(sheet.image));imageLink.className='sheet-image';imageLink.append(el('img',{src:media(sheet.image),alt:sheet.title,loading:'lazy'}));const copy=el('div',{class:'copy'});copy.append(el('h3',{},sheet.title),link('Mở PNG nền trong suốt',media(sheet.image)));card.append(imageLink,copy);document.querySelector('#sheets').append(card);}
 document.querySelector('#error').textContent='';
}
renderGallery().catch(e=>{document.querySelector('#error').textContent=e.message+' Hãy tải lại trang hoặc xem thư mục ảnh trên GitHub.';});
