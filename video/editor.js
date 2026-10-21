import {mediaURL} from '../assets/js/media-storage.js?v=r2-v1';
import {loadProps,drawProp,propImage,replaceProp} from '../assets/js/prop-library.js?v=r2-v1';
import {APP_ROOT,FINANCE_ID,getWorkspace,getDocument,saveDocument,blankVideo,resourceURL,notifySaved,videoHistory,promotePublishedVideo,canUpgradePublishedVideo} from '../assets/js/workspace-store.js?v=salary-v02-v1';
import {finalizeWebM} from './webm.js';
import {WIDTH,HEIGHT,clone,clamp,duration,locate,clipStart,validate,loadAssets,layerBox,render} from './engine.js?v=r2-v1';
const $=s=>document.querySelector(s);
const canvas=$('#preview'),ctx=canvas.getContext('2d'),audio=$('#audio');
const baseURL=APP_ROOT,params=new URLSearchParams(location.search),workspaceID=params.get('project')||FINANCE_ID;
let workspaceMeta,defaultURL,pendingSave=Promise.resolve();
if(params.get('embed')==='1')document.documentElement.classList.add('embedded');
const KEY='credit-studio-video-intro-v1';
let project,images=new Map(),time=0,selected=null,activeIndex=0,playing=false,raf=0;
let history=[],future=[],drag=null,loading=true,audioReady=false,loadTicket=0,toastTimer,tail=null;
let recording=null,audioContext,audioSource,audioDestination,gainNode,audioBlobURL;
const uid=()=>crypto.randomUUID();
const current=()=>project?.clips[activeIndex];
const layer=()=>current()?.layers.find(l=>l.id===selected);
const clock=n=>`${Math.floor(n/60).toString().padStart(2,'0')}:${(n%60).toFixed(1).padStart(4,'0')}`;
function toast(text){$('#toast').textContent=text;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,5000);}
function remember(){history.push(JSON.stringify(project));if(history.length>40)history.shift();future=[];}
function persist(){const snapshot=clone(project);$('#save-status').textContent='Đang lưu…';pendingSave=pendingSave.catch(()=>{}).then(()=>saveDocument(workspaceID,'video',snapshot)).then(()=>{$('#save-status').textContent='Đã lưu vào dự án';notifySaved(workspaceID);}).catch(e=>{$('#save-status').textContent='Chưa lưu — hãy tải JSON';toast(e.message);throw e;});pendingSave.catch(()=>{});return pendingSave;}
function refreshMP4(){$('#mp4').hidden=!workspaceMeta?.review;if(workspaceMeta?.review)$('#mp4').href=resourceURL(workspaceMeta.review);$('#mp4').title='MP4 là bản nháp gốc. Để lấy bản bạn đã sửa, dùng Xuất WebM.';$('#mp4').textContent='MP4 bản nháp gốc';}
function draw(clean=false){if(!project)return;render(ctx,project,images,time,{selection:!clean&&!playing?selected:null,captions:$('#captions').checked});}
function updateTime(){if(!project)return;const at=locate(project,time);$('#time').value=`${clock(time)} / ${clock(at.total)}`;$('#scrub').max=at.total;$('#scrub').value=time;$('#playhead').style.left=`${time/at.total*100}%`;
 document.querySelectorAll('.scene-card').forEach((b,i)=>b.classList.toggle('active',i===at.index));
 if(activeIndex!==at.index){activeIndex=at.index;selected=null;updateProperties();highlight();}
}
function highlight(){document.querySelectorAll('[data-scene]').forEach(b=>b.classList.toggle('selected',Number(b.dataset.scene)===activeIndex));}
function setTime(value){if(!project)return;time=clamp(value,0,duration(project));const desired=clamp(time+project.audio.offset,0,Math.max(0,audio.duration||0));if(audioReady&&Math.abs(audio.currentTime-desired)>.01)audio.currentTime=desired;tail=null;updateTime();draw();}
function stop(){playing=false;audio.pause();cancelAnimationFrame(raf);$('#play').textContent='▶ Phát';draw();}
function tick(){if(!playing)return;
 if(tail)time=tail.time+(performance.now()-tail.clock)/1000;else time=Math.max(0,audio.currentTime-project.audio.offset);
 if(time>=duration(project)){time=duration(project);stop();updateTime();draw(true);if(recording)finishExport(false);return;}
 updateTime();draw(true);raf=requestAnimationFrame(tick);
}
async function play(){if(loading||!audioReady)return;
 if(time>=duration(project)-.02)setTime(0);
 try{if(audioContext)await audioContext.resume();
  if(!project.audio.src){tail={time,clock:performance.now()};playing=true;$('#play').textContent='Ⅱ Dừng';raf=requestAnimationFrame(tick);return;}
  audio.currentTime=clamp(time+project.audio.offset,0,audio.duration);
  if(audio.currentTime>=audio.duration-.02){tail={time,clock:performance.now()};}else{tail=null;await audio.play();}
  playing=true;$('#play').textContent='Ⅱ Dừng';raf=requestAnimationFrame(tick);
 }catch{toast('Chưa phát được âm thanh. Nhấn Phát để thử lại.');if(recording)finishExport(true);}
}
audio.onended=()=>{if(!playing)return;tail={time:Math.max(time,audio.duration-project.audio.offset),clock:performance.now()};};
function setBusy(busy){document.querySelectorAll('button,input,select,textarea').forEach(n=>{if(n.id!=='cancel-export')n.disabled=busy;});$('#mp4').style.pointerEvents=busy?'none':'';if(!busy){updateProperties();$('#play').disabled=loading||!audioReady;$('#undo').disabled=!history.length;$('#redo').disabled=!future.length;}}
function change(fn,{seek=true}={}){if(loading||recording)return;stop();const before=clone(project),oldIndex=activeIndex,oldSelected=selected;try{fn();validate(project);}catch(e){project=before;activeIndex=oldIndex;selected=oldSelected;toast(e.message);build();return;}history.push(JSON.stringify(before));if(history.length>40)history.shift();future=[];time=clamp(time,0,duration(project));if(seek){const start=clipStart(project,activeIndex);time=clamp(time,start,Math.max(start,start+current().duration-.01));}persist();build();setTime(time);}
async function prepareAudio(){audioReady=false;$('#play').disabled=true;$('#audio-status').textContent='Đang tải giọng đọc…';const ticket=loadTicket;
 if(!project.audio.src){audio.removeAttribute('src');audio.load();audioReady=true;$('#audio-status').textContent='Chưa có giọng đọc. Chọn Thay giọng đọc để thêm.';$('#play').disabled=false;return;}
 const src=project.audio.src.startsWith('data:')?project.audio.src:mediaURL(project.audio.src,baseURL);
 const response=await fetch(src,{signal:AbortSignal.timeout(30000)});if(!response.ok)throw Error('Không tải được giọng đọc.');const blob=await response.blob();
 if(ticket!==loadTicket)return;if(audioBlobURL)URL.revokeObjectURL(audioBlobURL);audioBlobURL=URL.createObjectURL(blob);
 await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>{cleanup();reject(Error('Âm thanh tải quá lâu. Kiểm tra kết nối rồi mở lại dự án.'));},30000);
  function cleanup(){clearTimeout(timer);audio.removeEventListener('canplay',done);audio.removeEventListener('error',error);}
  function done(){cleanup();resolve();}function error(){cleanup();reject(Error('Không tải được tệp âm thanh.'));}
  audio.addEventListener('canplay',done);audio.addEventListener('error',error);audio.src=audioBlobURL;audio.load();
 });
 if(ticket!==loadTicket)return;
 audioReady=true;setVolume();$('#audio-status').textContent=`Giọng đọc ${clock(audio.duration)} · bắt đầu từ ${project.audio.offset.toFixed(1)}s`;$('#play').disabled=false;
}
function setVolume(){if(gainNode){audio.volume=1;gainNode.gain.value=project.audio.volume;}else audio.volume=project.audio.volume;}
async function loadProject(data,{resetHistory=true,save=false}={}){
 const checked=validate(clone(data));stop();loading=true;audioReady=false;const ticket=++loadTicket;$('#loading').hidden=false;$('#loading').textContent='Đang tải hình và giọng đọc…';setBusy(true);
 try{
  const loaded=await loadAssets(checked,baseURL);if(ticket!==loadTicket)return;
  project=checked;images=loaded;time=0;activeIndex=0;selected=null;if(resetHistory){history=[];future=[];}
  $('#captions').checked=!!project.showCaptions;build();draw();await prepareAudio();if(ticket!==loadTicket)return;
  if(save)await persist();loading=false;$('#loading').hidden=true;setBusy(false);setTime(0);if(!save)$('#save-status').textContent='Dự án đã sẵn sàng';
 }catch(e){loading=false;$('#loading').hidden=false;$('#loading').textContent=e.message+' Chọn Bản gốc để thử lại.';setBusy(false);toast(e.message);throw e;}
}
function updateProperties(){const c=current();if(!c)return;
 $('#project-name').value=project.name;$('#scene-title').value=c.title;$('#scene-duration').value=c.duration;$('#scene-background').value=c.background;$('#scene-fade').value=c.fade;$('#audio-offset').value=project.audio.offset;$('#volume').value=project.audio.volume;
 const l=layer();$('#layer-controls').disabled=!l;$('#replace-prop').hidden=l?.type!=='image';
 const items=[...c.layers].reverse();if($('#layers').dataset.signature!==items.map(i=>i.id).join('|')){$('#layers').replaceChildren();$('#layers').dataset.signature=items.map(i=>i.id).join('|');}
 items.forEach((item,index)=>{const b=$('#layers').children[index]||document.createElement('button');b.textContent=item.type==='text'?'T  '+item.text.replaceAll('\n',' '):item.type==='image'?'▧  '+(project.assets[item.asset].label||item.asset):'▭  Khối màu';b.classList.toggle('selected',item.id===selected);b.onclick=()=>{stop();selected=item.id;setTime(clipStart(project,activeIndex)+Math.min(c.duration-.02,item.enter+.7));updateProperties();draw();};if(!b.parentNode)$('#layers').append(b);});
 if(l){for(const k of ['x','y','w','h','enter','effect','opacity'])$('#layer-'+k).value=l[k];$('#text-label').hidden=l.type!=='text';$('#type-controls').hidden=l.type!=='text';$('#rect-fill-label').hidden=l.type!=='rect';if(l.type==='text'){for(const k of ['text','size','fill','align'])$('#layer-'+k).value=l[k];}if(l.type==='rect')$('#rect-fill').value=l.fill;}
 $('#undo').disabled=!history.length;$('#redo').disabled=!future.length;$('#delete-scene').disabled=project.clips.length<=1;refreshMP4();
}
function build(){const c=current();if(!c)return;const total=duration(project);const signature=project.clips.map(c=>c.id).join('|');
 $('#timeline-track').style.minWidth=`${Math.max(600,total*12,project.clips.length*70)}px`;
 if($('#scene-list').dataset.signature!==signature){$('#scene-list').replaceChildren();$('#clips').replaceChildren();$('#scene-list').dataset.signature=signature;}
 let start=0;
 project.clips.forEach((clip,index)=>{
  const b=$('#scene-list').children[index]||document.createElement('button');b.className='scene-card';b.dataset.scene=index;
  if(!b.children.length){const n=document.createElement('span');n.className='number';const info=document.createElement('span');info.append(document.createElement('span'),document.createElement('small'));b.append(n,info);}
  b.children[0].textContent=String(index+1).padStart(2,'0');b.children[1].children[0].textContent=clip.title;b.children[1].children[1].textContent=`${clock(start)} · ${clip.duration.toFixed(2)}s`;b.onclick=()=>selectScene(index);if(!b.parentNode)$('#scene-list').append(b);
  const t=$('#clips').children[index]||document.createElement('button');t.dataset.scene=index;t.style.width=`${clip.duration/total*100}%`;t.title=clip.title;
  if(!t.children.length){t.append(document.createElement('span'),document.createElement('small'));}
  t.children[0].textContent=clip.title;t.children[1].textContent=clip.duration.toFixed(2)+'s';t.onclick=()=>selectScene(index);if(!t.parentNode)$('#clips').append(t);start+=clip.duration;
 });
 $('#timeline-ruler').replaceChildren();for(let i=0;i<=5;i++){const s=document.createElement('span');s.textContent=clock(total*i/5);$('#timeline-ruler').append(s);}
 highlight();updateProperties();updateTime();drawWave();draw();
}
function selectScene(index){if(recording)return;stop();activeIndex=index;selected=null;setTime(clipStart(project,index)+Math.min(.4,current().duration/2));const scroller=$('.timeline-scroll');scroller.scrollLeft=$('#timeline-track').scrollWidth*time/duration(project)-scroller.clientWidth/2;highlight();updateProperties();draw();}
function drawWave(){if(!project)return;const wave=$('#waveform'),wctx=wave.getContext('2d');wave.width=1000;wctx.clearRect(0,0,1000,48);wctx.fillStyle='#9eaf90';document.querySelector('.audio-track span').textContent=project.audio.src?'♫ Giọng đọc của bạn':'Chưa có âm thanh';const peaks=project.waveform||[];const total=duration(project);for(let i=0;i<400;i++){const seconds=i/400*total+project.audio.offset;const idx=Math.floor(seconds/(project.waveformDuration||total)*peaks.length);const value=peaks[idx]||0;wctx.fillRect(i*2.5,24-value*20,1.5,Math.max(1,value*40));}}
function property(selector,fn){$(selector).onchange=event=>{const input=event.target;if(input.type==='number'&&(!Number.isFinite(Number(input.value))||!input.checkValidity())){toast('Giá trị nằm ngoài phạm vi.');updateProperties();return;}change(()=>fn(input.value));};}
property('#project-name',v=>project.name=v.trim()||'Video của tôi');property('#scene-title',v=>current().title=v.trim()||'Cảnh');
property('#scene-duration',v=>current().duration=Number(v));property('#scene-background',v=>current().background=v);property('#scene-fade',v=>current().fade=Number(v));
for(const k of ['x','y','w','h','size','enter','opacity'])property('#layer-'+k,v=>{if(layer())layer()[k]=Number(v);});
for(const k of ['text','fill','align','effect'])property('#layer-'+k,v=>{if(layer())layer()[k]=v;});
property('#rect-fill',v=>{if(layer())layer().fill=v;});
property('#audio-offset',v=>{project.audio.offset=Number(v);$('#audio-status').textContent=`Giọng đọc ${clock(audio.duration)} · bắt đầu từ ${v}s`;});
$('#volume').onchange=()=>change(()=>{project.audio.volume=Number($('#volume').value);setVolume();});
$('#volume').oninput=()=>{if(gainNode)gainNode.gain.value=Number($('#volume').value);else audio.volume=Number($('#volume').value);};
$('#captions').onchange=()=>{if(!project)return;project.showCaptions=$('#captions').checked;persist();draw();};
$('#play').onclick=()=>playing?stop():play();$('#restart').onclick=()=>{stop();setTime(0);};$('#scrub').oninput=event=>{stop();selected=null;setTime(Number(event.target.value));};
$('#add-text').onclick=()=>change(()=>{const l={id:uid(),type:'text',text:'Nội dung của bạn',x:100,y:120,w:1200,h:160,size:75,fill:'#27332f',align:'left',enter:0,effect:'fade',opacity:1,drift:0};current().layers.push(l);selected=l.id;});
let pickerItems=[],pickerTarget=null;
const normalizeProp=s=>s.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d');
function renderPropPicker(){const terms=normalizeProp($('#prop-picker-search').value).split(/\s+/).filter(Boolean),category=$('#prop-picker-category').value,grid=$('#prop-picker-grid');grid.replaceChildren();const items=pickerItems.filter(p=>(!category||p.category===category)&&terms.every(t=>normalizeProp(p.name+' '+p.tags.join(' ')).includes(t)));$('#prop-picker-status').textContent=`${items.length} mẫu · Bấm vào hình để thay`;
 for(const p of items){const b=document.createElement('button');b.type='button';b.className='prop-choice';b.dataset.prop=p.id;b.disabled=!!pickerTarget?.busy;const pic=document.createElement('canvas');pic.width=320;pic.height=240;pic.setAttribute('aria-hidden','true');const label=document.createElement('span');label.textContent=p.name;b.append(pic,label);b.onclick=()=>applyProp(p);grid.append(b);drawProp(pic,p).catch(()=>{if(b.isConnected){b.disabled=true;label.textContent=p.name+' — chưa tải được ảnh';}});}
 if(!items.length){const empty=document.createElement('p');empty.textContent='Không tìm thấy mẫu phù hợp.';grid.append(empty);}
}
async function applyProp(p){const target=pickerTarget;if(!target||target.busy||loading||recording)return;target.busy=true;$('#prop-picker-status').textContent='Đang thay đạo cụ…';$('#prop-picker-grid').querySelectorAll('button').forEach(b=>b.disabled=true);
 try{const {img}=await propImage(p);if(pickerTarget!==target||!$('#prop-picker').open||target.ticket!==loadTicket)return;
  const next=replaceProp(project,p,target.clip,target.layer);images.set(p.src,img);change(()=>{project=next;selected=target.layer;},{seek:false});$('#prop-picker').close();toast('Đã thay bằng '+p.name+'. Có thể Hoàn tác để trở lại.');
 }catch(e){if(pickerTarget===target){target.busy=false;renderPropPicker();$('#prop-picker-status').textContent=e.message;}}
}
$('#replace-prop').onclick=async()=>{const l=layer();if(!l||l.type!=='image'||loading||recording)return;stop();const target={clip:current().id,layer:l.id,ticket:loadTicket,busy:false};pickerTarget=target;$('#prop-picker-target').textContent='Đang chọn: '+(project.assets[l.asset].label||'Lớp ảnh');$('#prop-picker-search').value='';$('#prop-picker-category').replaceChildren(new Option('Tất cả',''));$('#prop-picker-grid').replaceChildren();$('#prop-picker-status').textContent='Đang tải kho…';$('#prop-picker').showModal();
 try{const items=await loadProps();if(pickerTarget!==target||!$('#prop-picker').open)return;pickerItems=items;for(const category of [...new Set(items.map(p=>p.category))].sort())$('#prop-picker-category').append(new Option(category,category));renderPropPicker();}catch(e){if(pickerTarget===target)$('#prop-picker-status').textContent=e.message;}
};
$('#prop-picker-close').onclick=()=>$('#prop-picker').close();$('#prop-picker').addEventListener('close',()=>{pickerTarget=null;});$('#prop-picker-search').oninput=renderPropPicker;$('#prop-picker-category').onchange=renderPropPicker;
$('#delete-layer').onclick=()=>{if(layer())change(()=>{current().layers=current().layers.filter(l=>l.id!==selected);selected=null;});};
$('#duplicate-layer').onclick=()=>{const l=layer();if(l)change(()=>{const copy={...l,id:uid(),x:clamp(l.x+25,-1920,3840),y:clamp(l.y+25,-1080,2160)};current().layers.push(copy);selected=copy.id;});};
for(const [id,delta]of [['layer-up',1],['layer-down',-1]])$('#'+id).onclick=()=>{const i=current().layers.findIndex(l=>l.id===selected),j=i+delta;if(i>=0&&j>=0&&j<current().layers.length)change(()=>{[current().layers[i],current().layers[j]]=[current().layers[j],current().layers[i]];});};
$('#duplicate-scene').onclick=()=>{if(project.clips.length>=100)return toast('Tối đa 100 cảnh.');if(duration(project)+current().duration>900)return toast('Tổng thời lượng tối đa 15 phút.');change(()=>{const copy=clone(current());copy.id=uid();copy.title+=' (bản sao)';project.clips.splice(activeIndex+1,0,copy);activeIndex++;selected=null;time=clipStart(project,activeIndex)+.2;});};
$('#delete-scene').onclick=()=>{if(project.clips.length<=1)return;change(()=>{project.clips.splice(activeIndex,1);activeIndex=Math.min(activeIndex,project.clips.length-1);selected=null;time=clipStart(project,activeIndex)+.2;});};
for(const [id,delta]of [['earlier',-1],['later',1]])$('#'+id).onclick=()=>{const j=activeIndex+delta;if(j<0||j>=project.clips.length)return;change(()=>{[project.clips[activeIndex],project.clips[j]]=[project.clips[j],project.clips[activeIndex]];activeIndex=j;time=clipStart(project,j)+.2;selected=null;});};
async function restore(stack,other){if(!stack.length||loading||recording)return;stop();const old=clone(project),snapshot=stack.pop();other.push(JSON.stringify(old));const next=JSON.parse(snapshot);const audioChanged=next.audio.src!==old.audio.src;
 if(audioChanged){await loadProject(next,{resetHistory:false,save:true});}else{project=validate(next);time=clamp(time,0,duration(project));activeIndex=locate(project,time).index;selected=null;setVolume();$('#captions').checked=!!project.showCaptions;build();setTime(time);persist();}}
$('#undo').onclick=()=>restore(history,future).catch(e=>toast(e.message));$('#redo').onclick=()=>restore(future,history).catch(e=>toast(e.message));
function point(event){const r=canvas.getBoundingClientRect();return{x:(event.clientX-r.left)*WIDTH/r.width,y:(event.clientY-r.top)*HEIGHT/r.height};}
canvas.onpointerdown=event=>{if(loading||recording||event.button!==0)return;stop();const p=point(event),at=locate(project,time);const hit=[...at.clip.layers].reverse().find(l=>{const b=layerBox(l,at.local);return b.alpha>.1&&p.x>=b.x&&p.x<=b.x+b.w&&p.y>=b.y&&p.y<=b.y+b.h;});selected=hit?.id??null;if(hit){drag={x:p.x,y:p.y,ox:hit.x,oy:hit.y,before:JSON.stringify(project)};canvas.setPointerCapture(event.pointerId);}updateProperties();draw();};
canvas.onpointermove=event=>{if(!drag||!layer())return;const p=point(event);layer().x=clamp(Math.round(drag.ox+p.x-drag.x),-1920,3840);layer().y=clamp(Math.round(drag.oy+p.y-drag.y),-1080,2160);draw();};
function endDrag(){if(!drag)return;const before=drag.before;drag=null;if(before!==JSON.stringify(project)){history.push(before);if(history.length>40)history.shift();future=[];persist();}updateProperties();draw();}
canvas.onpointerup=endDrag;canvas.onpointercancel=endDrag;
document.addEventListener('keydown',event=>{if($('#prop-picker').open||event.target.closest('input,textarea,select,[contenteditable]')||loading||recording)return;if(event.code==='Space'){event.preventDefault();playing?stop():play();}else if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='z'){event.preventDefault();event.shiftKey?$('#redo').click():$('#undo').click();}else if(['ArrowLeft','ArrowRight'].includes(event.key)){event.preventDefault();stop();setTime(time+(event.key==='ArrowLeft'?-1:1)/30);}else if(event.key==='Delete'&&layer())$('#delete-layer').click();});
function download(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1500);}
$('#mp4').onclick=async event=>{const url=new URL($('#mp4').href);if(url.origin===location.origin)return;event.preventDefault();try{const r=await fetch(url);if(!r.ok)throw Error('Chưa tải được MP4.');download(await r.blob(),'credit-studio-review.mp4');}catch(e){toast(e.message);}};
$('#save').onclick=()=>download(new Blob([JSON.stringify(project,null,2)],{type:'application/json'}),'credit-studio-video.json');
$('#load').onclick=()=>$('#json-file').click();$('#json-file').onchange=async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;if(file.size>45*1024*1024)return toast('Dự án tối đa 45 MiB.');try{const data=validate(JSON.parse(await file.text()));if(!confirm('Mở dự án này? Hãy Lưu JSON trước nếu muốn giữ bản hiện tại.'))return;await loadProject(data,{save:true});}catch(error){toast(error.message);}};
$('#reset').onclick=async()=>{if(!confirm('Mở lại bản dựng gốc mới nhất? Hãy Sao lưu dự án hoặc Lưu JSON trước để giữ bản sửa hiện tại.'))return;try{let data;if(defaultURL){const r=await fetch(defaultURL,{cache:'no-cache'});if(!r.ok)throw Error('Không tải được bản gốc.');data=await r.json();}else data=blankVideo(workspaceMeta.name);await loadProject(data,{save:true});$('#published-update')?.remove();}catch(e){toast(e.message);}};
$('#upload-audio').onclick=()=>$('#audio-file').click();$('#audio-file').onchange=async event=>{const file=event.target.files[0];event.target.value='';if(!file)return;if(!/^audio\//.test(file.type)||file.size>25*1024*1024)return toast('Chọn tệp audio tối đa 25 MiB.');
 try{const data=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsDataURL(file);});const next=clone(project);next.audio.src=data;next.audio.offset=0;next.waveform=[];next.captions=[];next.showCaptions=false;validate(next);remember();await loadProject(next,{resetHistory:false,save:true});toast('Đã thay giọng đọc. Phụ đề cũ đã bỏ; hãy kiểm tra lại nhịp cảnh.');}catch(e){toast(e.message);}};
async function audioGraph(){if(!audioContext){audioContext=new AudioContext();audioSource=audioContext.createMediaElementSource(audio);gainNode=audioContext.createGain();audioDestination=audioContext.createMediaStreamDestination();audioSource.connect(gainNode);gainNode.connect(audioContext.destination);gainNode.connect(audioDestination);}await audioContext.resume();setVolume();}
async function exportVideo(){if(loading||recording||!audioReady)return;if(!window.MediaRecorder||!canvas.captureStream)return toast('Trình duyệt chưa hỗ trợ xuất video. Hãy dùng Chrome hoặc Edge mới.');
 const mime=(project.audio.src?['video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus','video/webm']:['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm']).find(t=>MediaRecorder.isTypeSupported(t));if(!mime)return toast('Trình duyệt này không hỗ trợ xuất WebM.');
 stop();setTime(0);selected=null;
 try{if(project.audio.src)await audioGraph();const stream=canvas.captureStream(30);if(project.audio.src){const audioTrack=audioDestination.stream.getAudioTracks()[0];if(!audioTrack)throw Error('Không tạo được luồng âm thanh.');stream.addTrack(audioTrack.clone());}const recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:6500000,audioBitsPerSecond:160000});const chunks=[];
  recording={recorder,stream,cancelled:false};setBusy(true);$('#export-progress').hidden=false;$('#export-message').textContent='Đang xuất — giữ tab này mở…';
  recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recorder.onerror=()=>{toast('Xuất video thất bại.');finishExport(true);};recorder.onstop=async()=>{const cancelled=recording?.cancelled,seconds=recording?.seconds||duration(project);stream.getTracks().forEach(t=>t.stop());recording=null;$('#export-progress').hidden=true;setBusy(false);stop();if(!cancelled&&chunks.length){try{const blob=await finalizeWebM(new Blob(chunks,{type:'video/webm'}),seconds*1000);download(blob,'credit-studio-edited.webm');toast('Đã xuất WebM từ bản chỉnh sửa của bạn.');}catch{toast('Không hoàn tất được tệp WebM. Hãy thử xuất lại.');}}draw();};
  draw(true);recorder.start(500);await play();
 }catch(e){if(recording)finishExport(true);setBusy(false);$('#export-progress').hidden=true;toast(e.message);}
}
function finishExport(cancelled){if(!recording)return;recording.cancelled=cancelled;recording.seconds=time;stop();if(recording.recorder.state!=='inactive')recording.recorder.stop();}
$('#export').onclick=exportVideo;$('#cancel-export').onclick=()=>{finishExport(true);toast('Đã hủy xuất.');};
document.addEventListener('visibilitychange',()=>{if(document.hidden&&recording){finishExport(true);toast('Đã hủy xuất vì tab bị ẩn. Giữ tab mở trong khi xuất video.');}});
setInterval(()=>{if(recording)$('#export-message').textContent=`Đang xuất ${Math.round(time/duration(project)*100)}% — giữ tab mở`;},250);
window.addEventListener('beforeunload',event=>{if(recording){event.preventDefault();event.returnValue='';}});
// Deterministic render hooks for offline MP4 generation and functional checks.
window.creditVideo={get project(){return clone(project);},get time(){return time;},get ready(){return !loading&&audioReady;},get playing(){return playing;},get recording(){return !!recording;},flush:()=>pendingSave,pause:stop,seek:setTime,renderAt(t){stop();time=clamp(t,0,duration(project));draw(true);},async load(data){await loadProject(data);}};
async function init(){try{
 workspaceMeta=await getWorkspace(workspaceID);defaultURL=workspaceMeta.defaultVideo?resourceURL(workspaceMeta.defaultVideo):null;
 $('#workspace-label').textContent=workspaceMeta.kind==='video'?'DỰ ÁN VIDEO CỦA BẠN':'VIDEO TRONG DỰ ÁN';
 $('#gallery-link').hidden=!workspaceMeta.gallery;if(workspaceMeta.gallery)$('#gallery-link').href=resourceURL(workspaceMeta.gallery);
 let saved=await getDocument(workspaceID,'video');
 if(!saved&&workspaceID===FINANCE_ID){try{const raw=localStorage.getItem(KEY);if(raw){saved=validate(JSON.parse(raw));await saveDocument(workspaceID,'video',saved);}}catch{toast('Không đọc được bản lưu cũ. Bản cũ vẫn được giữ trong trình duyệt.');}}
 let latest;
 if(defaultURL){try{const r=await fetch(defaultURL,{cache:'no-cache'});if(!r.ok)throw Error('Không tải được bản dựng gốc.');latest=validate(await r.json());}catch(e){if(!saved)throw e;toast('Chưa tải được bản mới. Đang giữ bản lưu hiện tại.');}}
 if(canUpgradePublishedVideo(workspaceID,saved?.revision,latest?.revision)&&latest){
  // Preserve the complete old draft in the same transaction as the review upgrade.
  saved=await promotePublishedVideo(workspaceID,saved.revision,latest)||saved;
 }
 let data=saved||latest;
 if(!data)data=blankVideo(workspaceMeta.name);
 if(!saved)data.name=workspaceMeta.name;
 await loadProject(data,{save:true});
 const requestedClip=project.clips.findIndex(c=>c.id===params.get('clip'));if(requestedClip>=0)selectScene(requestedClip);
 const archived=await videoHistory(workspaceID);
 if(archived.length){const history=document.createElement('details');history.id='video-history';history.className='video-history';const summary=document.createElement('summary');summary.textContent='Bản lưu trước cập nhật';history.append(summary);
  for(const entry of archived){const b=document.createElement('button');b.textContent=`Tải bản ${duration(entry.data).toLocaleString('vi-VN')} giây`;b.onclick=()=>download(new Blob([JSON.stringify(entry.data,null,2)],{type:'application/json'}),'credit-studio-before-update-'+entry.slot+'.json');history.append(b);}
  $('#scene-list').before(history);
 }
 if(saved&&latest){
   if(latest.revision&&saved.revision!==latest.revision){
    const notice=document.createElement('p');notice.id='published-update';notice.className='published-notice';
    notice.append(document.createTextNode('Có bản dựng mới trên GitHub. Bản sửa của bạn vẫn được giữ. Hãy Sao lưu dự án trước khi chọn '));
    const open=document.createElement('button');open.textContent='Mở bản dựng mới';open.onclick=()=>$('#reset').click();notice.append(open);$('#scene-list').before(notice);
   }
 }
 }catch(e){$('#loading').textContent=e.message;toast(e.message);}}
function fitCanvas(){const stage=$('#stage'),style=getComputedStyle(stage);const w=stage.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight);const h=stage.clientHeight-parseFloat(style.paddingTop)-parseFloat(style.paddingBottom);const width=Math.max(1,Math.min(w,h*16/9));canvas.style.width=width+'px';canvas.style.height=(width*9/16)+'px';}
new ResizeObserver(fitCanvas).observe($('#stage'));
init();
