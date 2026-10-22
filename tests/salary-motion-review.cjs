const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000',folder='videos/001-100k-salary';
const project=JSON.parse(fs.readFileSync(folder+'/review-v03/project.json')),scratch=path.resolve('work/salary-v03');fs.mkdirSync(scratch,{recursive:true});
fs.writeFileSync(path.join(scratch,'contact.html'),'<!doctype html><html><head><meta charset="utf-8"><title>Review checks</title></head><body></body></html>');
(async()=>{const browser=await chromium.launch();try{
 const page=await browser.newPage({viewport:{width:1920,height:1080}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/work/salary-v03/contact.html');
 await page.evaluate(async p=>{const engine=await import('/video/engine.js?v=r2-v1');engine.validate(p);window.engine=engine;window.project=p;window.images=await engine.loadAssets(p,location.origin+'/');await document.fonts.ready;},project);
 const metrics=await page.evaluate(()=>{
  const c=document.createElement('canvas');c.width=1920;c.height=1080;const ctx=c.getContext('2d');let start=0,frames=0,maxCaptionLines=0;
  const overlap=(a,b)=>Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>2&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>2;
  for(const clip of project.clips){
   const actualText=(l,phase=0)=>{ctx.font=`700 ${l.size}px "Times New Roman"`;const lines=engine.wrapText(ctx,engine.layerText(l,phase),l.w);return {x:l.x,y:l.y,w:l.w,h:lines.length*l.size*1.18,lines};};
   for(const l of clip.layers){if(l.type==='text'){const t=actualText(l);if(t.y+t.h>1080||t.x<0||t.x+t.w>1921)throw Error(clip.title+': text outside canvas');if(l.id==='headline'&&t.y+t.h>278)throw Error(clip.title+': headline too tall');if(t.lines.some(s=>ctx.measureText(s).width>l.w+2))throw Error(clip.title+': word wider than box');}}
   for(const phase of Array.from({length:Math.ceil(clip.duration*10)+1},(_,i)=>Math.min(clip.duration-.001,i/10))){
    engine.render(ctx,project,images,start+phase,{captions:false});frames++;
    const boxes=[];
    for(let i=0;i<clip.layers.length;i++){const l=clip.layers[i],b=engine.layerBox(l,phase);if(b.alpha<.01)continue;if(l.type==='image'){
      if(b.x<0||b.y<278||b.x+b.w>1921||b.y+b.h>1001)throw Error(clip.title+': image moves outside safe stage '+l.id);
      for(const later of clip.layers.slice(i+1))if(later.type==='rect'&&overlap(b,engine.layerBox(later,phase)))throw Error(clip.title+': foreground panel occludes image '+l.id);
      for(const label of clip.layers.filter(t=>t.type==='text'))if(engine.layerBox(label,phase).alpha>.01&&overlap(b,actualText(label,phase)))throw Error(clip.title+': text overlaps image '+l.id);
      boxes.push(b);
    }}
   }
   start+=clip.duration;
  }
  for(const cue of project.captions){ctx.font='500 35px "Times New Roman"';maxCaptionLines=Math.max(maxCaptionLines,engine.wrapText(ctx,cue.text,1620).length);}
  if(Math.abs(start-486.75)>.000001)throw Error('Wrong total duration');
  return {clips:project.clips.length,duration:start,checkedFrames:frames,maxCaptionLines,assets:Object.keys(project.assets).length};
 });
 assert.equal(metrics.maxCaptionLines<=2,true,'captions fit the reserved lower area');
 // Snapshot every clip after validating its entrance, middle and exit.
 let start=0;
 for(let i=0;i<project.clips.length;i++){
  const clip=project.clips[i],b64=await page.evaluate(t=>{const c=document.createElement('canvas');c.width=1920;c.height=1080;engine.render(c.getContext('2d'),project,images,t);return c.toDataURL('image/jpeg',.9).split(',')[1];},start+clip.duration/2);
  fs.writeFileSync(path.join(scratch,`frame-${String(i+1).padStart(3,'0')}.jpg`),Buffer.from(b64,'base64'));start+=clip.duration;
 }
 for(let sheet=0;sheet<Math.ceil(project.clips.length/20);sheet++){
  await page.evaluate(({base,sheet,count})=>{document.body.replaceChildren();document.body.style.cssText='margin:0;display:grid;grid-template-columns:repeat(4,1fr);background:white;font:18px "Times New Roman"';for(let i=sheet*20;i<Math.min((sheet+1)*20,count);i++){const box=document.createElement('div'),im=new Image();im.src=base+'/work/salary-v03/frame-'+String(i+1).padStart(3,'0')+'.jpg';im.style.cssText='width:480px;height:270px;display:block';const label=document.createElement('div');label.textContent=String(i+1).padStart(2,'0');label.style.cssText='height:30px;padding:3px 8px';box.append(im,label);document.body.append(box);}},{base,sheet,count:project.clips.length});
  await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));await page.screenshot({path:path.join(scratch,'review-sheet-'+sheet+'.jpg'),fullPage:true});
 }
 assert.deepEqual(errors,[]);fs.writeFileSync(path.join(scratch,'layout-checks.json'),JSON.stringify(metrics,null,2));console.log('PASS',metrics);
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
