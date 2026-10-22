const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000';
const board=JSON.parse(fs.readFileSync('videos/001-100k-salary/review/project.json')),review=JSON.parse(fs.readFileSync(JSON.parse(fs.readFileSync('projects.json')).projects.find(p=>p.id==='finance-001').defaultVideo));
const scratch=path.resolve('work/salary-v02');
(async()=>{const b=await chromium.launch();try{
 const page=await b.newPage({viewport:{width:1500,height:1100},acceptDownloads:true}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/');const original=structuredClone(board);original.name='Bảng hình đã sửa cần giữ';original.clips[0].layers.find(l=>l.type==='text').text='GIỮ NGUYÊN BẢN SỬA';
 await page.evaluate(async p=>{const s=await import('/assets/js/workspace-store.js?v=salary-v02-v1');await s.saveDocument('finance-001','video',p);},original);
 await page.goto(base+'/?project=finance-001&tab=video');const editor=page.frameLocator('#tool-frame');await editor.locator('#play:not([disabled])').waitFor();
 assert.equal(await editor.locator('#scene-list .scene-card').count(),review.clips.length);assert.match(await editor.locator('#audio-status').textContent(),/8|15|Đã|sẵn|giọng/i);
 let docs=await page.evaluate(async()=>{const s=await import('/assets/js/workspace-store.js?v=salary-v02-v1');return {main:await s.getDocument('finance-001','video'),old:await s.videoHistory('finance-001')};});
 assert.equal(docs.main.revision,review.revision);assert.equal(docs.old.length,1);assert.deepEqual(docs.old[0].data,original);
 await editor.locator('#video-history summary').click();const dl=page.waitForEvent('download');await editor.locator('#video-history button').click();const oldFile=path.join(scratch,'archived-board.json');await(await dl).saveAs(oldFile);assert.deepEqual(JSON.parse(fs.readFileSync(oldFile)),original);
 const bp=page.waitForEvent('download');await page.click('#backup-project');const backupFile=path.join(scratch,'review-upgrade.credit.json');await(await bp).saveAs(backupFile);const backup=JSON.parse(fs.readFileSync(backupFile));assert.equal(backup.documents.filter(d=>d.kind==='video').length,2);assert.deepEqual(backup.documents.find(d=>d.slot.startsWith('history-')).data,original);
 // Save a user edit to the current review, reload: never reset it or duplicate history.
 await page.locator('#tool-frame').evaluate(async f=>{const p=f.contentWindow.creditVideo.project;p.clips[0].layers.find(l=>l.id==='headline').text='CURRENT REVIEW EDIT KEPT';await f.contentWindow.creditVideo.load(p);await import('/assets/js/workspace-store.js?v=salary-v02-v1').then(s=>s.saveDocument('finance-001','video',p));});
 await page.reload();await editor.locator('#play:not([disabled])').waitFor();docs=await page.evaluate(async()=>{const s=await import('/assets/js/workspace-store.js?v=salary-v02-v1');return {main:await s.getDocument('finance-001','video'),old:await s.videoHistory('finance-001')};});assert.equal(docs.old.length,1);assert.match(JSON.stringify(docs.main),/CURRENT REVIEW EDIT KEPT/);
 for(const t of [0,10,100,200,300,400,480,485]){await page.locator('#tool-frame').evaluate((f,t)=>f.contentWindow.creditVideo.seek(t),t);const delta=await page.locator('#tool-frame').evaluate(f=>Math.abs(f.contentDocument.querySelector('#audio').currentTime-f.contentWindow.creditVideo.time));assert.ok(delta<.08,'audio follows scrub time');}
 await editor.locator('#play').click();await page.waitForTimeout(600);assert.equal(await page.locator('#tool-frame').evaluate(f=>f.contentWindow.creditVideo.playing),true);await editor.locator('#play').click();
 await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);assert.equal(await page.locator('#tool-frame').evaluate(f=>f.contentDocument.documentElement.scrollWidth>f.contentWindow.innerWidth),false);assert.equal(await editor.locator('#video-history summary').isVisible(),true);
 // Overview upgrades the known old board too, while a restored project ID never does.
 const fresh=await b.newPage();await fresh.goto(base+'/');await fresh.evaluate(async p=>{const s=await import('/assets/js/workspace-store.js?v=salary-v02-v1');await s.saveDocument('finance-001','video',p);},original);await fresh.goto(base+'/?project=finance-001');await fresh.locator('#overview video').waitFor();await fresh.waitForFunction(()=>document.querySelector('.overview-facts').textContent.includes('88'));
 const rules=await fresh.evaluate(async()=>{const s=await import('/assets/js/workspace-store.js?v=salary-v02-v1');return [s.canUpgradePublishedVideo('finance-001','full-review-v01',undefined),s.canUpgradePublishedVideo('restored-copy','full-review-v01','salary-review-v02'),s.canUpgradePublishedVideo('finance-001','salary-review-v02','salary-review-v02')];});assert.deepEqual(rules,[false,false,false]);await fresh.close();

 // Direct editor entry must also archive an edited intro before loading v02.
 const isolated=await b.newContext(),direct=await isolated.newPage();await direct.goto(base+'/');
 const intro=JSON.parse(fs.readFileSync('videos/001-100k-salary/intro/project.json'));intro.name='Edited intro remains recoverable';intro.clips[0].layers.find(l=>l.type==='text').text='KEEP INTRO EDIT';
 await direct.evaluate(async p=>{const s=await import('/assets/js/workspace-store.js?v=salary-v02-v1');await s.saveDocument('finance-001','video',p);},intro);
 await direct.goto(base+'/video/?project=finance-001');await direct.locator('#play:not([disabled])').waitFor();assert.equal(await direct.locator('#scene-list .scene-card').count(),88);
 const saved=await direct.evaluate(async()=>{const s=await import('/assets/js/workspace-store.js?v=salary-v02-v1');return (await s.videoHistory('finance-001'))[0].data;});assert.deepEqual(saved,intro);await isolated.close();
 assert.deepEqual(errors,[]);console.log('PASS: old edited full v01 archived verbatim, backup/history download, 88-scene review, current edits/reload, audio seek/playback, mobile, overview promotion, unknown/restored/current revisions excluded.');
}finally{await b.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
