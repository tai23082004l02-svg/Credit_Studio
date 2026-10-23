import {initStorage,mediaURL} from '../../assets/js/media-storage.js?v=r2-media-v2';
const params=new URLSearchParams(location.search),project=params.get('project')||'finance-002';
if(params.get('embed')==='1')document.documentElement.classList.add('embedded');
const node=(tag,attrs={},text='')=>{const n=document.createElement(tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);n.textContent=text;return n;};
const link=(text,href,download=false)=>node('a',{href,...(download?{download:''}:{})},text);
async function main(){
 const response=await fetch('artwork.json',{cache:'no-cache'});if(!response.ok)throw Error('Không tải được danh sách hình.');const data=await response.json();
 await initStorage();const media=path=>mediaURL(path,new URL('./',import.meta.url));
 for(const f of data.frames)f.image=media(f.image);
 for(const s of data.sheets){s.image=media(s.image);s.guide=media(s.guide);for(const item of s.items)item.image=media(item.image);}
 for(const f of data.frames){const article=node('article');const view=link('',f.image);view.append(node('img',{class:'frame-image',src:f.image,alt:f.title,loading:'lazy',width:1920,height:1080}));article.append(view);const copy=node('div',{class:'copy'});copy.append(node('h3',{},f.id+' · '+f.title),node('p',{},'Phần '+f.section+' · “'+f.cue+'”'),node('p',{},f.motion));const edit=new URL('../../',location.href);edit.searchParams.set('project',project);edit.searchParams.set('tab','images');edit.searchParams.set('scene',f.id);const editLink=link('Chỉnh cảnh trong Studio',edit.href);editLink.target='_top';const links=node('div',{class:'links'});links.append(editLink,link('Tải khung PNG',f.image,true),link('Tải JSON chỉnh được',f.project,true));copy.append(links);article.append(copy);document.querySelector('#frames').append(article);}
 for(const s of data.sheets){const article=node('article');const view=link('',s.guide);view.append(node('img',{class:'sheet-image',src:s.guide,alt:s.title,loading:'lazy'}));article.append(view);const copy=node('div',{class:'copy'});copy.append(node('h3',{},s.title));const links=node('div',{class:'links'});links.append(link('PNG trong suốt',s.image,true),link('Bản hướng dẫn',s.guide,true),link('Tọa độ cắt JSON','images/crop-map.json',true));copy.append(links);article.append(copy);document.querySelector('#sheets').append(article);
  for(const item of s.items){const card=node('article',{class:'asset','data-asset':item.id});card.append(node('img',{src:item.image,alt:item.name,loading:'lazy'}),node('h3',{},item.name),link('Tải PNG riêng',item.image,true));document.querySelector('#assets').append(card);}
 }
 document.querySelector('#status').textContent='';
}
main().catch(e=>document.querySelector('#status').textContent=e.message);
