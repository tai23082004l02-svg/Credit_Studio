const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000';
const folder='videos/004-living-alone',art=JSON.parse(fs.readFileSync(folder+'/artwork.json'));
const itemCount=JSON.parse(fs.readFileSync('library/props/catalog.json')).items.length;
const scratch=path.resolve('work/living-artwork');fs.mkdirSync(scratch,{recursive:true});
(async()=>{const browser=await chromium.launch();try{
 const page=await browser.newPage({viewport:{width:1440,height:1100},acceptDownloads:true}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/'+folder+'/');await page.waitForFunction(()=>document.querySelectorAll('#frames article').length===16);
 assert.equal(await page.locator('#sheets article').count(),2);assert.equal(await page.locator('#assets article').count(),16);
 await page.locator('#assets article').last().scrollIntoViewIfNeeded();
 await page.evaluate(()=>Promise.all([...document.images].map(im=>{im.loading='eager';return im.decode();})));
 await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));
 const checks=await page.evaluate(async({art,folder})=>{
  const {validate}=await import('/video/engine.js?v=r2-v1'),{validateDesign}=await import('/assets/js/design-model.js');
  const root=location.origin+'/'+folder+'/',video=validate(await(await fetch(root+'storyboard/project.json')).json());
  if(video.clips.length!==16||video.audio.src!=='')throw Error('Unexpected completed-video claim or missing frames');
  for(const f of art.frames){
   const design=validateDesign(await(await fetch(root+f.project)).json());
   for(const e of design.elements){
    if(e.x<0||e.y<0||e.x+e.w>1921||e.y+e.h>1080)throw Error(f.id+': element outside canvas');
    if(e.type==='text'&&e.font!=='Times New Roman')throw Error(f.id+': wrong font');
   }
   if(f.id.endsWith('a')){
    const image=design.elements.find(e=>e.type==='image');
    const title=design.elements.filter(e=>e.type==='text'&&e.y>=76&&e.y<254);
    if(image.y<254||title.some(e=>e.y+e.h>image.y))throw Error(f.id+': title overlaps illustration');
   }
   const overlap=(a,b)=>a.x<b.x+b.w-.5&&a.x+a.w>b.x+.5&&a.y<b.y+b.h-.5&&a.y+a.h>b.y+.5;
   const texts=design.elements.filter(e=>e.type==='text'),images=design.elements.filter(e=>e.type==='image');
   for(let i=0;i<texts.length;i++)for(let j=i+1;j<texts.length;j++)if(overlap(texts[i],texts[j]))throw Error(f.id+': text collision');
   for(const t of texts)for(const im of images)if(overlap(t,im))throw Error(f.id+': text overlaps image');
   if(['01b','04b','07b','08b'].includes(f.id))for(const panel of design.elements.filter(e=>e.type==='rect'&&e.h>400)){
    const inside=e=>e.x>=panel.x&&e.x+e.w<=panel.x+panel.w+.1&&e.y>=panel.y&&e.y+e.h<=panel.y+panel.h+.1;
    for(const e of design.elements.filter(e=>['image','text'].includes(e.type)&&inside(e)))if(Math.abs(e.x+e.w/2-(panel.x+panel.w/2))>2)throw Error(f.id+': card is not centered');
   }
   for(const e of design.elements)if(e.type==='image'){const im=new Image();im.src=e.src;await im.decode();if(Math.abs(e.w/e.h-im.width/im.height)>.001)throw Error(f.id+': image is stretched');}
  }
  for(const sheet of art.sheets){
   const source=new Image();source.src=root+sheet.sourceImage;await source.decode();const sc=document.createElement('canvas');sc.width=source.width;sc.height=source.height;const sg=sc.getContext('2d');sg.drawImage(source,0,0);
   for(const it of sheet.items){const[x,y,w,h]=it.sourceCrop,d=sg.getImageData(x,y,w,h).data;for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++)if((xx<4||yy<4||xx>=w-4||yy>=h-4)&&d[(yy*w+xx)*4+3]>8)throw Error(it.id+': source image cut at cell edge');}

   const im=new Image();im.src=root+sheet.image;await im.decode();const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);
   for(const it of sheet.items){
    const[x,y,w,h]=it.crop;if(x<0||y<0||x+w>im.width||y+h>im.height)throw Error(it.id+': bad crop');
    const data=g.getImageData(x,y,w,h).data;let count=0;
    for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++){const a=data[(yy*w+xx)*4+3];if(a>20){count++;if(xx<40||yy<40||xx>=w-40||yy>=h-40)throw Error(it.id+': silhouette too close to cell edge');}}
    if(count<100)throw Error(it.id+': empty crop');
    const cut=new Image();cut.src=root+it.image;await cut.decode();const cc=document.createElement('canvas');cc.width=cut.width;cc.height=cut.height;const z=cc.getContext('2d');z.drawImage(cut,0,0);const d=z.getImageData(0,0,cc.width,cc.height).data;
    for(let yy=0;yy<cc.height;yy++)for(let xx=0;xx<cc.width;xx++)if((xx<32||yy<32||xx>=cc.width-32||yy>=cc.height-32)&&d[(yy*cc.width+xx)*4+3]!==0)throw Error(it.id+': missing transparent padding');
   }
  }
  if(video.clips.reduce((s,c)=>s+c.duration,0)!==96)throw Error('Not a 96 second artwork board');
  return {frames:video.clips.length,atlasCount:art.sheets.length,isolatedPNGs:art.sheets.reduce((n,s)=>n+s.items.length,0)};
 },{art,folder});
 const budgetText=art.frames.map(f=>JSON.parse(fs.readFileSync(folder+'/'+f.project)).elements.filter(e=>e.type==='text').map(e=>e.text).join(' ')).join(' ');
 assert.equal(1800+60,1860);assert.equal(2400/2+60/2,1230);assert.equal((1860-1230)*12,7560);assert.equal(1860*2,3720);
 for(const value of ['$1,860','$1,230','$630','$7,560','$3,720','+4.3%','38.5 million','29% of U.S. households'])assert.ok(budgetText.includes(value),'Missing: '+value);
 assert.ok(budgetText.includes('Not a complete emergency-fund target'));
 assert.ok(budgetText.includes('12 months ending December 2024'));
 const narrated=fs.readFileSync(folder+'/narration.txt','utf8');for(const f of art.frames)assert.ok(narrated.includes(f.cue),'Cue does not match narration: '+f.id);
 const cdp=await page.context().newCDPSession(page);await cdp.send('DOM.enable');await cdp.send('CSS.enable');
 const dom=await cdp.send('DOM.getDocument');const hn=await cdp.send('DOM.querySelector',{nodeId:dom.root.nodeId,selector:'h1'});
 const fonts=await cdp.send('CSS.getPlatformFontsForNode',{nodeId:hn.nodeId});assert.ok(fonts.fonts.some(f=>f.familyName==='Times New Roman'),JSON.stringify(fonts));
 fs.writeFileSync(path.join(scratch,'actual-font.json'),JSON.stringify(fonts,null,2));
 const download=page.waitForEvent('download');await page.locator('[data-asset="solo4-house-keys"] a').click();const file=path.join(scratch,'house-keys-download.png');await(await download).saveAs(file);assert.ok(fs.statSync(file).size>10000);
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await page.screenshot({path:path.join(scratch,'gallery-mobile.png')});
 await page.goto(base+'/?project=finance-004&tab=video');const editor=page.frameLocator('#tool-frame');await editor.locator('#play:not([disabled])').waitFor();const published=JSON.parse(fs.readFileSync('projects.json')).projects.find(p=>p.id==='finance-004'),publishedVideo=JSON.parse(fs.readFileSync(published.defaultVideo));assert.equal(await editor.locator('#scene-list .scene-card').count(),publishedVideo.clips.length);assert.equal(await editor.locator('#mp4').isVisible(),!!published.review);
 await page.locator('#tool-frame').evaluate(f=>{f.contentWindow.creditVideo.seek(93);});
 await page.goto(base+'/?project=finance-004&tab=images&scene=05b');await editor.locator('#artboard').filter({hasText:/\$3,720/}).waitFor();assert.match(await editor.locator('#artboard').textContent(),/\$3,720/);
 assert.equal(await editor.locator('#artboard image').count(),2);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.goto(base+'/?view=props');await page.waitForFunction(n=>document.querySelectorAll('.prop-card').length===n,itemCount);await page.fill('#prop-search','solo4');assert.equal(await page.locator('.prop-card').count(),16);await page.waitForFunction(()=>[...document.querySelectorAll('.prop-card canvas')].every(c=>c.getContext('2d').getImageData(0,0,c.width,c.height).data.some((v,i)=>i%4===3&&v>0)));
 // Contact sheet for human inspection, using actual exported 1920x1080 boards.
 fs.writeFileSync(path.join(scratch,'contact.html'),'<!doctype html><html><head><meta charset="utf-8"><title>Artwork contact sheet</title></head><body></body></html>');
 await page.setViewportSize({width:1920,height:1200});await page.goto(base+'/work/living-artwork/contact.html');
 await page.evaluate(({art,folder,base})=>{document.body.replaceChildren();document.body.style.cssText='margin:0;display:grid;grid-template-columns:repeat(4,1fr);background:white;font:16px "Times New Roman"';for(const f of art.frames){const box=document.createElement('div'),im=new Image();im.src=base+'/'+folder+'/'+f.image;im.style.cssText='width:480px;height:270px;display:block';const label=document.createElement('div');label.textContent=f.id+' · '+f.title;label.style.cssText='height:30px;padding:3px 8px';box.append(im,label);document.body.append(box);}},{art,folder,base});
 await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));await page.screenshot({path:path.join(scratch,'all-frames.png'),fullPage:true});
 fs.writeFileSync(path.join(scratch,'artwork-checks.json'),JSON.stringify(checks,null,2));assert.deepEqual(errors,[]);console.log('PASS:',checks,'all crop bounds, transparent padding, title separation, unstretched images, arithmetic, downloads, Studio editing, silent board, mobile, shared props.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
