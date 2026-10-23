// Real R2 integration test; no mocked media or credential values.
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000',manifest=JSON.parse(fs.readFileSync('storage/manifest.json'));
const scratch=path.resolve('work/r2-migration');fs.mkdirSync(scratch,{recursive:true});
// Newly generated props are still on GitHub until an R2 upload is verified.
// Registered archived media must never silently fall back to the origin.
const newLocalProps=new Set(['keys','bills','repair','compare'].map(p=>'library/props/jamie-mortgage/'+p+'.png'));
(async()=>{
 assert.equal(manifest.enabled,true);
 const browser=await chromium.launch({proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY,bypass:'127.0.0.1,localhost'}:undefined});
 try{
  const page=await browser.newPage({viewport:{width:1500,height:1100},acceptDownloads:true});page.setDefaultTimeout(60000);
  const errors=[],failures=[],media=new Set(),localMedia=new Set(),siteRoot=new URL(base+'/');
  page.on('request',r=>{const u=new URL(r.url());if(u.origin===siteRoot.origin&&u.pathname.startsWith(siteRoot.pathname)&&/\.(png|wav|mp3|mp4|webm)$/.test(u.pathname))localMedia.add(decodeURIComponent(u.pathname.slice(siteRoot.pathname.length)));});
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.url().startsWith(manifest.publicBaseURL)){media.add(r.url());if(r.status()>=400)failures.push(r.status());}});
  await page.goto(base+'/?view=props');
  const count=JSON.parse(fs.readFileSync('library/props/catalog.json')).items.length;
  await page.waitForFunction(n=>document.querySelectorAll('.prop-card').length===n,count);
  await page.waitForFunction(()=>[...document.querySelectorAll('.prop-card canvas')].every(c=>c.getContext('2d').getImageData(0,0,c.width,c.height).data.some((v,i)=>i%4===3&&v>0)));
  const download=page.waitForEvent('download');await page.locator('[data-prop="alex-present"]').getByRole('button',{name:'Tải PNG'}).click();await(await download).saveAs(path.join(scratch,'alex.png'));
  for(let n=1;n<=4;n++){
   await page.goto(base+'/?project=finance-00'+n+'&tab=video');
   const frame=page.frameLocator('#tool-frame');await frame.locator('#play:not([disabled])').waitFor();
   const result=await page.locator('#tool-frame').evaluate(async f=>{
    const w=f.contentWindow,p=w.creditVideo.project;w.creditVideo.seek(10);
    const canvas=f.contentDocument.querySelector('#preview');canvas.toDataURL();
    const audio=f.contentDocument.querySelector('audio');
    await w.creditVideo.flush();
    return {revision:p.revision,clips:p.clips.length,audioSrc:audio?.src};
   });
   assert.ok(result.clips>60);console.log('Editor',n,result.revision,result.clips);
   await frame.locator('#play').click();await page.waitForTimeout(600);await frame.locator('#play').click();
   assert.ok(await page.locator('#tool-frame').evaluate(f=>f.contentWindow.creditVideo.time)>10);
   await page.goto(base+'/?project=finance-00'+n);await page.waitForSelector('#overview video');
   assert.ok((await page.locator('#overview video').getAttribute('src')).startsWith(manifest.publicBaseURL));
   await page.locator('#overview video').evaluate(async v=>{if(v.readyState<1)await new Promise((resolve,reject)=>{v.onloadedmetadata=resolve;v.onerror=()=>reject(Error('MP4 failed'));});v.currentTime=10;});
  }
  for(const folder of ['001-100k-salary','002-monthly-payment-trap','003-car-payment-trap','004-living-alone']){
   await page.goto(base+'/videos/'+folder+'/');
   await page.waitForFunction(()=>document.querySelectorAll('main img').length>=16);
   const images=await page.locator('main img').evaluateAll(async imgs=>{await Promise.all(imgs.map(i=>{i.loading='eager';return i.decode();}));return imgs.map(i=>({src:i.src,width:i.naturalWidth}));});
   const localURLs=new Set(Object.entries(manifest.assets).filter(([,i])=>i.local).map(([p])=>new URL(p,base+'/').href));
   assert.ok(images.every(i=>(i.src.startsWith(manifest.publicBaseURL)||localURLs.has(i.src))&&i.width>0));console.log('Gallery',folder,images.length);
  }
  assert.deepEqual(failures,[]);assert.deepEqual(errors,[]);assert.ok(media.size>50);
  assert.ok([...localMedia].every(p=>manifest.assets[p]?manifest.assets[p].local:newLocalProps.has(p)),'only explicitly retained or listed new, unarchived props may load from GitHub');
  fs.writeFileSync(path.join(scratch,'browser.json'),JSON.stringify({passed:true,mediaRequests:media.size,propCount:count,retainedMedia:[...localMedia]},null,2));
  console.log('PASS: real R2 props/canvas/download, four editors/audio/MP4s and galleries.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
