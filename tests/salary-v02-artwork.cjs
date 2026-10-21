const fs=require('node:fs'),assert=require('node:assert/strict'),{chromium}=require('playwright');
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000',folder='videos/001-100k-salary';
(async()=>{const browser=await chromium.launch();try{const page=await browser.newPage({viewport:{width:1500,height:1100}}),errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(base+'/'+folder+'/');await page.waitForFunction(()=>document.querySelectorAll('#scenes article').length===20);await page.evaluate(async()=>{for(const im of document.images){im.loading='eager';await im.decode();}});
 for(const id of ['cashflow','annual-funds','social-context','raise-plan']){
  const design=JSON.parse(fs.readFileSync(folder+'/projects/v02-'+id+'.json')),image=design.elements.find(e=>e.type==='image');assert.ok(image.y>=285&&image.y+image.h<=936);for(const line of design.elements.filter(e=>e.id.startsWith('title-')))assert.ok(line.y+line.h<285);
  await page.goto(base+'/?project=finance-001&tab=images&scene=v02-'+id);const frame=page.frameLocator('#tool-frame');await frame.locator('#artboard').filter({hasText:design.elements.find(e=>e.id==='title-0').text}).waitFor();
  const metrics=await frame.locator('#artboard').evaluate(svg=>[...svg.querySelectorAll('text')].map(t=>{const b=t.getBBox();return {font:t.getAttribute('font-family'),center:t.parentElement.transform.baseVal.consolidate().matrix.e+b.x+b.width/2,id:t.parentElement.getAttribute('data-id')};}));for(const m of metrics){assert.equal(m.font,'Times New Roman');if(m.id.startsWith('title-'))assert.ok(Math.abs(m.center-960)<8,JSON.stringify(m));}
  await frame.locator('#artboard').screenshot({path:'work/salary-v02/design-'+id+'.png'});
 }
 assert.deepEqual(errors,[]);console.log('PASS: 20 gallery images decode; four editable designs load with centered Times New Roman titles and separate safe artwork.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
