import {finalizeWebM} from './webm.js';
import {WIDTH,HEIGHT,clone,clamp,duration,locate,clipStart,validate,loadAssets,layerBox,render} from './engine.js?v=times-v1';
const $=s=>document.querySelector(s);
const canvas=$('#preview'),ctx=canvas.getContext('2d'),audio=$('#audio');
const baseURL=new URL('../',location.href),defaultURL=new URL('videos/001-100k-salary/intro/project.json',baseURL);
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
function persist(){try{localStorage.setItem(KEY,JSON.stringify(project));$('#save-status').textContent='Đã lưu trong trình duyệt';}catch{$('#save-status').textContent='Hãy Lưu JSON để giữ bản sửa';toast('Bộ nhớ trình duyệt đầy. Chọn Lưu JSON để giữ bản sửa.');}}
function refreshMP4(){$('#mp4').title='MP4 là bản nháp gốc. Để lấy bản bạn đã sửa, dùng Xuất WebM.';$('#mp4').textContent='MP4 bản nháp gốc';}
function draw(clean=false){if(!project||!images.size)return;render(ctx,project,images,time,{selection:!clean&&!playing?selected:null,captions:$('#captions').checked});}
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
  audio.currentTime=clamp(time+project.audio.offset,0,audio.duration);
  if(audio.currentTime>=audio.duration-.02){tail={time,clock:performance.now()};}else{tail=null;await audio.play();}
  playing=true;$('#play').textContent='Ⅱ Dừng';raf=requestAnimationFrame(tick);
 }catch{toast('Chưa phát được âm thanh. Nhấn Phát để thử lại.');if(recording)finishExport(true);}
}
audio.onended=()=>{if(!playing)return;tail={time:Math.max(time,audio.duration-project.audio.offset),clock:performance.now()};};
function setBusy(busy){document.querySelectorAll('button,input,select,textarea').forEach(n=>{if(n.id!=='cancel-export')n.disabled=busy;});$('#mp4').style.pointerEvents=busy?'none':'';if(!busy){updateProperties();$('#play').disabled=loading||!audioReady;$('#undo').disabled=!history.length;$('#redo').disabled=!future.length;}}
function change(fn,{seek=true}={}){if(loading||recording)return;stop();const before=clone(project),oldIndex=activeIndex,oldSelected=selected;try{fn();validate(project);}catch(e){project=before;activeIndex=oldIndex;selected=oldSelected;toast(e.message);build();return;}history.push(JSON.stringify(before));if(history.length>40)history.shift();future=[];time=clamp(time,0,duration(project));if(seek){const start=clipStart(project,activeIndex);time=clamp(time,start,Math.max(start,start+current().duration-.01));}persist();build();setTime(time);}
async function prepareAudio(){audioReady=false;$('#play').disabled=true;$('#audio-status').textContent='Đang tải giọng đọc…';const ticket=loadTicket;
 const src=project.audio.src.startsWith('data:')?project.audio.src:new URL(project.audio.src,baseURL).href;
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
  loading=false;$('#loading').hidden=true;setBusy(false);setTime(0);if(save)persist();else $('#save-status').textContent='Bản nháp đã sẵn sàng';
 }catch(e){loading=false;$('#loading').hidden=false;$('#loading').textContent=e.message+' Chọn Bản gốc để thử lại.';setBusy(false);toast(e.message);throw e;}
}
function updateProperties(){const c=current();if(!c)return;
 $('#project-name').value=project.name;$('#scene-title').value=c.title;$('#scene-duration').value=c.duration;$('#scene-background').value=c.background;$('#scene-fade').value=c.fade;$('#audio-offset').value=project.audio.offset;$('#volume').value=project.audio.volume;
 const l=layer();$('#layer-controls').disabled=!l;
 const items=[...c.layers].reverse();if($('#layers').dataset.signature!==items.map(i=>i.id).join('|')){$('#layers').replaceChildren();$('#layers').dataset.signature=items.map(i=>i.id).join('|');}
 items.forEach((item,index)=>{const b=$('#layers').children[index]||document.createElement('button');b.textContent=item.type==='text'?'T  '+item.text.replaceAll('\n',' '):item.type==='image'?'▧  '+(project.assets[item.asset].label||item.asset):'▭  Khối màu';b.classList.toggle('selected',item.id===selected);b.onclick=()=>{stop();selected=item.id;setTime(clipStart(project,activeIndex)+Math.min(c.duration-.02,item.enter+.7));updateProperties();draw();};if(!b.parentNode)$('#layers').append(b);});
 if(l){for(const k of ['x','y','w','h','enter','effect','opacity'])$('#layer-'+k).value=l[k];$('#text-label').hidden=l.type!=='text';$('#type-controls').hidden=l.type!=='text';$('#rect-fill-label').hidden=l.type!=='rect';if(l.type==='text'){for(const k of ['text','size','fill','align'])$('#layer-'+k).value=l[k];}if(l.type==='rect')$('#rect-fill').value=l.fill;}
 $('#undo').disabled=!history.length;$('#redo').disabled=!future.length;$('#delete-scene').disabled=project.clips.length<=1;refreshMP4();
}
function build(){const c=current();if(!c)return;const total=duration(project);const signature=project.clips.map(c=>c.id).join('|');
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
function selectScene(index){if(recording)return;stop();activeIndex=index;selected=null;setTime(clipStart(project,index)+Math.min(.4,current().duration/2));highlight();updateProperties();draw();}
function drawWave(){if(!project)return;const wave=$('#waveform'),wctx=wave.getContext('2d');wave.width=1000;wctx.clearRect(0,0,1000,48);wctx.fillStyle='#9eaf90';const peaks=project.waveform||[];const total=duration(project);for(let i=0;i<400;i++){const seconds=i/400*total+project.audio.offset;const idx=Math.floor(seconds/(project.waveformDuration||total)*peaks.length);const value=peaks[idx]||0;wctx.fillRect(i*2.5,24-value*20,1.5,Math.max(1,value*40));}}
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
document.addEventListener('keydown',event=>{if(event.target.closest('input,textarea,select,[contenteditable]')||loading||recording)return;if(event.code==='Space'){event.preventDefault();playing?stop():play();}else if((event.ctrlKey||event.metaKey)&&event.key.toLowerCase()==='z'){event.preventDefault();event.shiftKey?$('#redo').click():$('#undo').click();}else if(['ArrowLeft','ArrowRight'].includes(event.key)){event.preventDefault();stop();setTime(time+(event.key==='ArrowLeft'?-1:1)/30);}else if(event.key==='Delete'&&layer())$('#delete-layer').click();});
function download(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1500);}
$('#save').onclick=()=>download(new Blob([JSON.stringify(project,null,2)],{type:'application/json'}),'credit-studio-video.json');
$('#load').onclick=()=>$('#json-file').click();$('#json-file').onchange=async e=>{const file=e.target.files[0];e.target.value='';if(!file)return;if(file.size>45*1024*1024)return toast('Dự án tối đa 45 MiB.');try{const data=validate(JSON.parse(await file.text()));if(!confirm('Mở dự án này? Hãy Lưu JSON trước nếu muốn giữ bản hiện tại.'))return;await loadProject(data,{save:true});}catch(error){toast(error.message);}};
$('#reset').onclick=async()=>{if(!confirm('Mở lại bản dựng gốc? Hãy Lưu JSON trước để giữ bản sửa.'))return;try{const r=await fetch(defaultURL,{cache:'no-cache'});if(!r.ok)throw Error('Không tải được bản gốc.');await loadProject(await r.json(),{save:true});}catch(e){toast(e.message);}};
$('#upload-audio').onclick=()=>$('#audio-file').click();$('#audio-file').onchange=async event=>{const file=event.target.files[0];event.target.value='';if(!file)return;if(!/^audio\//.test(file.type)||file.size>25*1024*1024)return toast('Chọn tệp audio tối đa 25 MiB.');
 try{const data=await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsDataURL(file);});const next=clone(project);next.audio.src=data;next.audio.offset=0;next.waveform=[];next.captions=[];next.showCaptions=false;validate(next);remember();await loadProject(next,{resetHistory:false,save:true});toast('Đã thay giọng đọc. Phụ đề cũ đã bỏ; hãy kiểm tra lại nhịp cảnh.');}catch(e){toast(e.message);}};
async function audioGraph(){if(!audioContext){audioContext=new AudioContext();audioSource=audioContext.createMediaElementSource(audio);gainNode=audioContext.createGain();audioDestination=audioContext.createMediaStreamDestination();audioSource.connect(gainNode);gainNode.connect(audioContext.destination);gainNode.connect(audioDestination);}await audioContext.resume();setVolume();}
async function exportVideo(){if(loading||recording||!audioReady)return;if(!window.MediaRecorder||!canvas.captureStream)return toast('Trình duyệt chưa hỗ trợ xuất video. Hãy dùng Chrome hoặc Edge mới.');
 const mime=['video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus','video/webm'].find(t=>MediaRecorder.isTypeSupported(t));if(!mime)return toast('Trình duyệt này không hỗ trợ xuất WebM.');
 stop();setTime(0);selected=null;
 try{await audioGraph();const stream=canvas.captureStream(30);const audioTrack=audioDestination.stream.getAudioTracks()[0];if(!audioTrack)throw Error('Không tạo được luồng âm thanh.');stream.addTrack(audioTrack.clone());const recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:6500000,audioBitsPerSecond:160000});const chunks=[];
  recording={recorder,stream,cancelled:false};setBusy(true);$('#export-progress').hidden=false;$('#export-message').textContent='Đang xuất — giữ tab này mở…';
  recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recorder.onerror=()=>{toast('Xuất video thất bại.');finishExport(true);};recorder.onstop=async()=>{const cancelled=recording?.cancelled,seconds=recording?.seconds||duration(project);stream.getTracks().forEach(t=>t.stop());recording=null;$('#export-progress').hidden=true;setBusy(false);stop();if(!cancelled&&chunks.length){try{const blob=await finalizeWebM(new Blob(chunks,{type:'video/webm'}),seconds*1000);download(blob,'credit-studio-edited.webm');toast('Đã xuất WebM với âm thanh và các chỉnh sửa của bạn.');}catch{toast('Không hoàn tất được tệp WebM. Hãy thử xuất lại.');}}draw();};
  draw(true);recorder.start(500);await play();
 }catch(e){if(recording)finishExport(true);setBusy(false);$('#export-progress').hidden=true;toast(e.message);}
}
function finishExport(cancelled){if(!recording)return;recording.cancelled=cancelled;recording.seconds=time;stop();if(recording.recorder.state!=='inactive')recording.recorder.stop();}
$('#export').onclick=exportVideo;$('#cancel-export').onclick=()=>{finishExport(true);toast('Đã hủy xuất.');};
document.addEventListener('visibilitychange',()=>{if(document.hidden&&recording){finishExport(true);toast('Đã hủy xuất vì tab bị ẩn. Giữ tab mở trong khi xuất video.');}});
setInterval(()=>{if(recording)$('#export-message').textContent=`Đang xuất ${Math.round(time/duration(project)*100)}% — giữ tab mở`;},250);
window.addEventListener('beforeunload',event=>{if(recording){event.preventDefault();event.returnValue='';}});
// Deterministic render hooks for offline MP4 generation and functional checks.
window.creditVideo={get project(){return clone(project);},get time(){return time;},get ready(){return !loading&&audioReady;},get playing(){return playing;},seek:setTime,renderAt(t){stop();time=clamp(t,0,duration(project));draw(true);},async load(data){await loadProject(data);}};
async function init(){try{let saved;try{const raw=localStorage.getItem(KEY);if(raw)saved=validate(JSON.parse(raw));}catch{toast('Không đọc được bản lưu. Đang mở bản dựng gốc.');}if(saved)await loadProject(saved);else{const r=await fetch(defaultURL);if(!r.ok)throw Error('Không tải được dự án mở đầu.');await loadProject(await r.json());}}catch(e){$('#loading').textContent=e.message;toast(e.message);}}
function fitCanvas(){const stage=$('#stage'),style=getComputedStyle(stage);const w=stage.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight);const h=stage.clientHeight-parseFloat(style.paddingTop)-parseFloat(style.paddingBottom);const width=Math.max(1,Math.min(w,h*16/9));canvas.style.width=width+'px';canvas.style.height=(width*9/16)+'px';}
new ResizeObserver(fitCanvas).observe($('#stage'));
init();
