const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000';
const folder='videos/002-monthly-payment-trap',art=JSON.parse(fs.readFileSync(folder+'/artwork.json'));
const itemCount=JSON.parse(fs.readFileSync('library/props/catalog.json')).items.length;
const scratch=path.resolve('work/monthly-payment-trap');fs.mkdirSync(scratch,{recursive:true});
(async()=>{const browser=await chromium.launch();try{
 const page=await browser.newPage({viewport:{width:1440,height:1100},acceptDownloads:true}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/'+folder+'/');await page.waitForFunction(()=>document.querySelectorAll('#frames article').length===16);
 assert.equal(await page.locator('#sheets article').count(),3);assert.equal(await page.locator('#assets article').count(),30);
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
   for(const e of design.elements)if(e.type==='image'){const im=new Image();im.src=e.src;await im.decode();if(Math.abs(e.w/e.h-im.width/im.height)>.001)throw Error(f.id+': image is stretched');}
  }
  for(const sheet of art.sheets){
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
  return {frames:video.clips.length,atlasCount:art.sheets.length,isolatedPNGs:art.sheets.reduce((n,s)=>n+s.items.length,0)};
 },{art,folder});
 assert.equal(525+37.5+90+120+45,817.5);assert.equal(37.5*24,900);assert.equal(60*36-75*24,360);
 const download=page.waitForEvent('download');await page.locator('[data-asset="mpt-alex-repair"] a').click();const file=path.join(scratch,'alex-repair-download.png');await(await download).saveAs(file);assert.ok(fs.statSync(file).size>10000);
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await page.screenshot({path:path.join(scratch,'gallery-mobile.png')});
 await page.goto(base+'/?project=finance-002&tab=video');const editor=page.frameLocator('#tool-frame');await editor.locator('#play:not([disabled])').waitFor();const published=JSON.parse(fs.readFileSync('projects.json')).projects.find(p=>p.id==='finance-002'),publishedVideo=JSON.parse(fs.readFileSync(published.defaultVideo));assert.equal(await editor.locator('#scene-list .scene-card').count(),publishedVideo.clips.length);assert.equal(await editor.locator('#mp4').isVisible(),!!published.review);
 await page.locator('#tool-frame').evaluate(f=>{f.contentWindow.creditVideo.seek(93);});
 await page.goto(base+'/?project=finance-002&tab=images&scene=04b');await editor.locator('#artboard').filter({hasText:/\$2,160/}).waitFor();assert.match(await editor.locator('#artboard').textContent(),/\$2,160/);
 assert.equal(await editor.locator('#artboard image').count(),2);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.goto(base+'/?view=props');await page.waitForFunction(n=>document.querySelectorAll('.prop-card').length===n,itemCount);await page.fill('#prop-search','mpt');assert.equal(await page.locator('.prop-card').count(),30);await page.waitForFunction(()=>[...document.querySelectorAll('.prop-card canvas')].every(c=>c.getContext('2d').getImageData(0,0,c.width,c.height).data.some((v,i)=>i%4===3&&v>0)));
 // Contact sheet for human inspection, using actual exported 1920x1080 boards.
 fs.writeFileSync(path.join(scratch,'contact.html'),'<!doctype html><html><head><meta charset="utf-8"><title>Artwork contact sheet</title></head><body></body></html>');
 await page.setViewportSize({width:1920,height:1200});await page.goto(base+'/work/monthly-payment-trap/contact.html');
 await page.evaluate(({art,folder,base})=>{document.body.replaceChildren();document.body.style.cssText='margin:0;display:grid;grid-template-columns:repeat(4,1fr);background:white;font:16px "Times New Roman"';for(const f of art.frames){const box=document.createElement('div'),im=new Image();im.src=base+'/'+folder+'/'+f.image;im.style.cssText='width:480px;height:270px;display:block';const label=document.createElement('div');label.textContent=f.id+' · '+f.title;label.style.cssText='height:30px;padding:3px 8px';box.append(im,label);document.body.append(box);}},{art,folder,base});
 await page.waitForFunction(()=>[...document.images].every(im=>im.complete&&im.naturalWidth>0));await page.screenshot({path:path.join(scratch,'all-frames.png'),fullPage:true});
 assert.deepEqual(errors,[]);console.log('PASS:',checks,'all crop bounds, transparent padding, title separation, unstretched images, arithmetic, downloads, Studio editing, silent board, mobile, shared props.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
