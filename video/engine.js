// Shared deterministic renderer used by the editor, tests and MP4 rendering.
export const WIDTH = 1920, HEIGHT = 1080;
export const EFFECTS = ['fade', 'slide', 'pop', 'none'];
export const clone = value => JSON.parse(JSON.stringify(value));
export const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
export function duration(project) { return project.clips.reduce((sum, clip) => sum + clip.duration, 0); }
export function locate(project, time) {
  const total = duration(project); let start = 0;
  for (let index = 0; index < project.clips.length; index++) {
    const clip = project.clips[index];
    if (time < start + clip.duration || index === project.clips.length - 1) {
      return {clip, index, start, local:clamp(time - start, 0, clip.duration), total};
    }
    start += clip.duration;
  }
}
export function clipStart(project, index) { return project.clips.slice(0,index).reduce((sum,c)=>sum+c.duration,0); }
export function safeSource(src, media = 'image') {
  if (typeof src !== 'string') return false;
  if (/^videos\/[A-Za-z0-9_-]+\/[A-Za-z0-9_./-]+\.(png|jpg|jpeg|webp|mp3|wav)$/i.test(src) && !src.includes('..')) return true;
  const types = media === 'audio' ? '(mpeg|mp3|wav|x-wav|wave|ogg|webm|mp4)' : '(png|jpeg|webp)';
  return new RegExp('^data:'+media+'/'+types+';base64,[A-Za-z0-9+/=]+$','i').test(src);
}
export function validate(project) {
  const fail = () => { throw new Error('Dự án video không hợp lệ hoặc không được hỗ trợ.'); };
  const n = (v,a,b) => typeof v==='number' && Number.isFinite(v) && v>=a && v<=b;
  const color = v => typeof v==='string' && /^#[\da-f]{6}$/i.test(v);
  if (!project || project.kind!=='credit-studio-video' || project.version!==1 || project.width!==WIDTH || project.height!==HEIGHT || project.fps!==30 || typeof project.name!=='string' || project.name.length>100) fail();
  if (!Array.isArray(project.clips)||!project.clips.length||project.clips.length>100||!project.assets||typeof project.assets!=='object'||Array.isArray(project.assets)||Object.keys(project.assets).length>100) fail();
  for (const asset of Object.values(project.assets)) {
    if (!asset || !safeSource(asset.src)) fail();
    if (asset.crop && (!Array.isArray(asset.crop)||asset.crop.length!==4||!asset.crop.every(v=>n(v,0,8192))||asset.crop[2]===0||asset.crop[3]===0)) fail();
  }
  if (!project.audio || !(project.audio.src===''||safeSource(project.audio.src,'audio')) || !n(project.audio.offset,0,3600) || !n(project.audio.volume,0,1)) fail();
  const clips = new Set();
  for (const c of project.clips) {
    if (!c||typeof c.id!=='string'||clips.has(c.id)||typeof c.title!=='string'||c.title.length>100||!n(c.duration,.5,120)||!color(c.background)||!n(c.fade,0,1)||!Array.isArray(c.layers)||c.layers.length>100) fail();
    clips.add(c.id); const layers = new Set();
    for (const l of c.layers) {
      if (!l||typeof l.id!=='string'||layers.has(l.id)||!['text','image','rect'].includes(l.type)||!n(l.x,-1920,3840)||!n(l.y,-1080,2160)||!n(l.w,1,3840)||!n(l.h,1,2160)||!n(l.enter,0,120)||!n(l.opacity,0,1)||!EFFECTS.includes(l.effect)||!n(l.drift,-40,40)) fail();
      layers.add(l.id);
      if (l.type==='image' && !Object.hasOwn(project.assets,l.asset)) fail();
      if (l.type==='text' && (typeof l.text!=='string'||l.text.length>3000||!n(l.size,12,300)||!color(l.fill)||!['left','center','right'].includes(l.align))) fail();
      if (l.type==='rect' && (!color(l.fill)||!n(l.radius,0,200))) fail();
    }
  }
  if(duration(project)>900) fail();
  if(project.captions!==undefined && (!Array.isArray(project.captions)||project.captions.length>2000||project.captions.some(c=>!c||!n(c.start,0,3600)||!n(c.end,0,3600)||c.end<=c.start||typeof c.text!=='string'||c.text.length>500))) fail();
  return project;
}
export async function loadAssets(project, baseURL) {
  const images = new Map();
  const entries = [...new Set(Object.values(project.assets).map(a=>a.src))];
  await Promise.all(entries.map(async src => {
    const img = new Image(); img.src = src.startsWith('data:') ? src : new URL(src,baseURL).href;
    await img.decode(); images.set(src,img);
  }));
  for(const a of Object.values(project.assets)) {
    const im=images.get(a.src);
    if(a.crop && (a.crop[0]+a.crop[2]>im.naturalWidth||a.crop[1]+a.crop[3]>im.naturalHeight)) throw Error('Vùng ảnh của tài nguyên vượt kích thước gốc.');
  }
  return images;
}
const ease = t => 1 - Math.pow(1-clamp(t,0,1),3);
export function layerBox(l, local) {
  const p = l.effect==='none' ? (local>=l.enter?1:0) : ease((local-l.enter)/.55);
  const scale = l.effect==='pop' ? .82+.18*p : 1;
  return {x:l.x+(l.effect==='slide'?(1-p)*90:0)+(l.type==='image'?Math.sin(Math.max(0,local-l.enter)*1.4)*l.drift:0)+(1-scale)*l.w/2,
    y:l.y+(l.effect==='pop'?(1-p)*35:0)+(1-scale)*l.h/2,w:l.w*scale,h:l.h*scale,alpha:p*l.opacity};
}
export function wrapText(ctx, text, width) {
  const result=[];
  for(const paragraph of text.split('\n')) {
    let line='';
    for(const word of paragraph.split(' ')) {
      const next=line ? line+' '+word : word;
      if(line && ctx.measureText(next).width>width) {result.push(line);line=word;} else line=next;
    }
    result.push(line);
  }
  return result;
}
function textLayer(ctx,l,b) {
  ctx.fillStyle=l.fill;ctx.font=`700 ${l.size}px "Times New Roman", Times, serif`;ctx.textBaseline='top';ctx.textAlign=l.align;
  const lines=wrapText(ctx,l.text,l.w);const x=l.align==='center'?b.x+b.w/2:l.align==='right'?b.x+b.w:b.x;
  lines.forEach((line,i)=>ctx.fillText(line,x,b.y+i*l.size*1.18));
}
export function render(ctx, project, images, time, {selection=null,captions=false}={}) {
  const at=locate(project,time),c=at.clip;
  ctx.save();ctx.clearRect(0,0,WIDTH,HEIGHT);ctx.fillStyle=c.background;ctx.fillRect(0,0,WIDTH,HEIGHT);
  // Low contrast dots keep the generated paper aesthetic consistent in layered shots.
  ctx.fillStyle='#8c795810';for(let i=0;i<120;i++)ctx.fillRect((i*197)%WIDTH,(i*311)%HEIGHT,2,2);
  const edge=c.fade ? clamp(Math.min(at.local,c.duration-at.local)/c.fade,0,1) : 1;
  for(const l of c.layers) {
    const b=layerBox(l,at.local);if(b.alpha<=0)continue;
    ctx.save();ctx.globalAlpha=b.alpha*edge;
    if(l.type==='image') {
      const a=project.assets[l.asset],im=images.get(a.src);
      if(im) {
        const crop=a.crop||[0,0,im.naturalWidth,im.naturalHeight];
        const scale=Math.min(b.w/crop[2],b.h/crop[3]),w=crop[2]*scale,h=crop[3]*scale;
        ctx.drawImage(im,...crop,b.x+(b.w-w)/2,b.y+(b.h-h)/2,w,h);
      }
    } else if(l.type==='text') textLayer(ctx,l,b);
    else {ctx.fillStyle=l.fill;ctx.beginPath();ctx.roundRect(b.x,b.y,b.w,b.h,l.radius);ctx.fill();}
    ctx.restore();
  }
  if(captions && project.captions) {
    const cue=project.captions.find(cue=>time>=cue.start&&time<cue.end);
    if(cue) {
      ctx.font='500 35px "Times New Roman", Times, serif';ctx.textBaseline='middle';ctx.textAlign='center';
      const lines=wrapText(ctx,cue.text,1620),h=lines.length*45+24,y=HEIGHT-h-24;
      ctx.fillStyle='#1f2b29e8';ctx.beginPath();ctx.roundRect(90,y,1740,h,14);ctx.fill();ctx.fillStyle='#ffffff';
      lines.forEach((line,i)=>ctx.fillText(line,WIDTH/2,y+34+i*45));
    }
  }
  if(selection) {
    const l=c.layers.find(l=>l.id===selection);
    if(l) {const b=layerBox(l,at.local);ctx.save();ctx.strokeStyle='#7955e8';ctx.lineWidth=4;ctx.setLineDash([12,8]);ctx.strokeRect(b.x,b.y,b.w,b.h);ctx.restore();}
  }
  ctx.restore();return at;
}
