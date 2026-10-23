const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000',folder='videos/005-mortgage-payment',scratch=path.resolve('work/mortgage/full-review');
fs.mkdirSync(scratch,{recursive:true});
(async()=>{const browser=await chromium.launch();try{
 const page=await browser.newPage({viewport:{width:1920,height:1200}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const project=JSON.parse(fs.readFileSync(folder+'/review/project.json'));assert.equal(project.clips.length,88);
 await page.goto(base+'/video/?project=finance-005');await page.waitForFunction(()=>window.creditVideo?.ready,null,{timeout:45000});await page.evaluate(async p=>creditVideo.load(p),project);
 const result=await page.evaluate(async()=>{
  const E=await import('/video/engine.js'),p=creditVideo.project,images=await E.loadAssets(p,location.origin+'/'),c=document.createElement('canvas');c.width=1920;c.height=1080;const ctx=c.getContext('2d');let start=0,frames=0,maxCaptionLines=0;
  const intersects=(a,b)=>Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>2&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>2;
  const box=(l,t)=>{const b=E.layerBox(l,t);if(l.type==='text'){ctx.font=`700 ${l.size}px "Times New Roman"`;const lines=E.wrapText(ctx,E.layerText(l,t),l.w);return {...b,h:lines.length*l.size*1.18,lines};}return b;};
  for(const clip of p.clips){
   for(let t=0;t<clip.duration;t+=.1){frames++;const visible=clip.layers.filter(l=>E.layerBox(l,t).alpha>.01);
    for(const l of visible){const b=box(l,t);if(b.x<-.01||b.y<0||b.x+b.w>1920.1||b.y+b.h>1080)throw Error(clip.id+' outside canvas: '+l.id);
     if(l.type==='text'&&b.lines.some(s=>ctx.measureText(s).width>l.w+1))throw Error(clip.id+' word overflow: '+l.id);
     if(l.type==='image'){if(b.y<280||b.y+b.h>930)throw Error(clip.id+' image outside safe stage');const index=clip.layers.indexOf(l);for(const other of visible){if(other===l)continue;if(other.type==='text'&&intersects(b,box(other,t)))throw Error(clip.id+' text over image: '+other.id);if(other.type==='rect'&&clip.layers.indexOf(other)>index&&intersects(b,box(other,t)))throw Error(clip.id+' foreground panel over image: '+other.id);}}
    }
    const texts=visible.filter(l=>l.type==='text');for(let a=0;a<texts.length;a++)for(let b=a+1;b<texts.length;b++)if(intersects(box(texts[a],t),box(texts[b],t)))throw Error(clip.id+' text collision: '+texts[a].id+'/'+texts[b].id);
    E.render(ctx,p,images,start+t,{captions:false});
   }
   start+=clip.duration;
  }
  const value=(clip,id,t)=>{const l=clip.layers.find(l=>l.id===id);return l.animation?E.animatedValue(l.animation,t):Number(l.text.replace(/[^\d.-]/g,''));};
  for(const index of [15,18]){const clip=p.clips[index];for(let t=0;t<clip.duration;t+=.05){const bars=clip.layers.filter(l=>l.id.startsWith('bar-')&&E.layerBox(l,t).alpha>.01);const sum=bars.reduce((sum,l)=>sum+E.layerBox(l,t).w/1700*2267,0);if(Math.abs(sum-value(clip,'total',t))>.01)throw Error('Budget bar/counter disagreement');}}
  const cash=p.clips[33];for(let t=0;t<cash.duration;t+=.05)if(Math.abs(value(cash,'cash',t)+value(cash,'equity',t)-75000)>.01)throw Error('Cash/equity transfer loses money');
  if(value(p.clips[35],'cash',100)!==6000||value(p.clips[37],'cash',100)!==4000)throw Error('Closing/moving arithmetic');
  if(value(p.clips[48],'reserve',100)!==3000||value(p.clips[50],'amount',100)!==500)throw Error('Reserve arithmetic');
  const split=p.clips[58];if(value(split,'part-value-0',100)!==1300||value(split,'part-value-1',100)!==217)throw Error('First-month loan split');
  const term=p.clips[59];for(let t=0;t<term.duration;t+=.02)if(value(term,'part-value-0',t)+value(term,'part-value-1',t)!==1517)throw Error('Rounded amortization split must add to1517');
  for(const cue of p.captions){ctx.font='500 35px "Times New Roman"';maxCaptionLines=Math.max(maxCaptionLines,E.wrapText(ctx,cue.text,1620).length);}
  return{clips:p.clips.length,duration:start,checkedFrames:frames,maxCaptionLines,assets:Object.keys(p.assets).length,audioDuration:document.querySelector('#audio').duration};
 });
 assert(Math.abs(result.duration-566.45)<.00001);assert(Math.abs(result.audioDuration-566.45)<.15);assert.equal(result.maxCaptionLines,1);
 assert.equal(project.captions.map(c=>c.text).join(' ').replace(/\s+/g,' ').trim(),fs.readFileSync(folder+'/narration.txt','utf8').replace(/\s+/g,' ').trim());
 const snapshotTimes=[];let start=0;
 for(let i=0;i<project.clips.length;i++){const clip=project.clips[i],t=start+clip.duration*.72;snapshotTimes.push(t);const b64=await page.evaluate(t=>{creditVideo.renderAt(t);return document.querySelector('#preview').toDataURL('image/jpeg',.92).split(',')[1];},t);fs.writeFileSync(path.join(scratch,`frame-${String(i+1).padStart(3,'0')}.jpg`),Buffer.from(b64,'base64'));start+=clip.duration;}
 for(const t of [0,65,100,225,310,390,470,558]){await page.evaluate(t=>creditVideo.seek(t),t);await page.click('#play');await page.waitForTimeout(250);assert(await page.evaluate(()=>creditVideo.playing));await page.click('#play');}
 const cdp=await page.context().newCDPSession(page);await cdp.send('DOM.enable');await cdp.send('CSS.enable');await page.evaluate(()=>{const p=document.createElement('p');p.id='font-check';p.style.font='700 40px "Times New Roman"';p.textContent='Mortgage payment';document.body.append(p);});const{root}=await cdp.send('DOM.getDocument');const{nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,selector:'#font-check'});const fonts=await cdp.send('CSS.getPlatformFontsForNode',{nodeId});assert(fonts.fonts.some(f=>f.postScriptName==='TimesNewRomanPS-BoldMT'));
 await page.setViewportSize({width:390,height:844});await page.waitForTimeout(300);assert(await page.locator('#play').isEnabled());assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));assert.deepEqual(errors,[]);
 const contact=await browser.newPage({viewport:{width:1920,height:1200}});
 for(let sheet=0;sheet<6;sheet++){
  await contact.goto(base+'/');await contact.evaluate(({base,sheet,count})=>{document.body.replaceChildren();document.body.style.cssText='margin:0;display:grid;grid-template-columns:repeat(4,480px);background:#fff;font:18px "Times New Roman"';for(let i=sheet*16;i<Math.min((sheet+1)*16,count);i++){const box=document.createElement('div'),im=new Image();im.src=base+'/work/mortgage/full-review/frame-'+String(i+1).padStart(3,'0')+'.jpg';im.style.cssText='width:480px;height:270px;display:block';const label=document.createElement('div');label.textContent=String(i+1).padStart(2,'0');label.style.cssText='height:30px;padding:3px 8px';box.append(im,label);document.body.append(box);}},{base,sheet,count:88});await contact.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));await contact.screenshot({path:path.join(scratch,'sheet-'+sheet+'.jpg'),fullPage:true});
 }
 fs.writeFileSync(folder+'/review/layout-validation.json',JSON.stringify({...result,fonts:fonts.fonts.map(f=>f.postScriptName),financialArithmetic:true,seekAndPlayback:true,mobile:true},null,2)+'\n');console.log('PASS',result);
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
