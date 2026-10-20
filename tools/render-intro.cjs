#!/usr/bin/env node
// Render the same canvas frames as the browser editor, then mux the original excerpt.
// Requires Playwright + Chromium, ffmpeg, and the README local server running.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const {spawn}=require('node:child_process');
const {once}=require('node:events');
const ROOT=path.resolve(__dirname,'..');
const input=path.resolve(process.argv[2]||path.join(ROOT,'videos/001-100k-salary/intro/project.json'));
const output=path.resolve(process.argv[3]||path.join(ROOT,'videos/001-100k-salary/exports/intro-v01.mp4'));
const url=(process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000')+'/video/';
(async()=>{
 const project=JSON.parse(fs.readFileSync(input,'utf8'));
 const {validate,duration}=await import('../video/engine.js');validate(project);
 let browser,encoder,tmp;
 try{
  let audioFile;
  if(project.audio.src.startsWith('data:')){tmp=fs.mkdtempSync(path.join(os.tmpdir(),'credit-video-'));audioFile=path.join(tmp,'audio');fs.writeFileSync(audioFile,Buffer.from(project.audio.src.split(',')[1],'base64'));}
  else if(project.audio.src)audioFile=path.resolve(ROOT,project.audio.src);
  if(audioFile&&!fs.existsSync(audioFile))throw Error('Audio file missing: '+audioFile);
  if(fs.existsSync(output)&&process.env.CREDIT_STUDIO_OVERWRITE!=='1')throw Error('Output exists; choose a new filename or set CREDIT_STUDIO_OVERWRITE=1.');
  fs.mkdirSync(path.dirname(output),{recursive:true});
  browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1600,height:1100}});
  await page.goto(url);await page.waitForFunction(()=>window.creditVideo?.ready,null,{timeout:45000});
  await page.evaluate(async data=>{await window.creditVideo.load(data);},project);
  const total=duration(project),count=Math.ceil(total*project.fps);
  const inputs=['-v','error','-y','-threads','2','-f','image2pipe','-vcodec','mjpeg','-framerate',String(project.fps),'-i','pipe:0'];if(audioFile)inputs.push('-ss',String(project.audio.offset),'-i',audioFile);
  const audioOptions=audioFile?['-map','1:a:0','-af',`volume=${project.audio.volume},apad`,'-c:a','aac','-b:a','160k','-ar','48000']:['-an'];
  encoder=spawn('ffmpeg',[...inputs,'-t',String(total),'-map','0:v:0','-c:v','libx264','-threads','3','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',...audioOptions,'-movflags','+faststart',output],{stdio:['pipe','ignore','pipe']});
  let errors='';encoder.stderr.on('data',d=>{errors=(errors+d).slice(-12000);});encoder.on('error',e=>{errors+=e.message;});
  const ended=once(encoder,'close');
  for(let frame=0;frame<count;frame++){
   if(encoder.exitCode!==null)throw Error('ffmpeg stopped: '+errors);
   const jpg=await page.evaluate(t=>{window.creditVideo.renderAt(t);return document.querySelector('#preview').toDataURL('image/jpeg',.95).split(',')[1];},frame/project.fps);
   if(!encoder.stdin.write(Buffer.from(jpg,'base64')))await once(encoder.stdin,'drain');
   if(frame%150===0)console.log(`Rendering ${frame}/${count} frames (${Math.round(frame/count*100)}%)`);
  }
  encoder.stdin.end();const [code]=await ended;if(code!==0)throw Error('ffmpeg failed: '+errors);
  console.log(`Rendered ${count} frames; ${total.toFixed(2)} seconds; MP4: ${output}`);
 }finally{if(encoder&&encoder.exitCode===null)encoder.kill('SIGTERM');if(browser)await browser.close();if(tmp)fs.rmSync(tmp,{recursive:true,force:true});}
})().catch(e=>{console.error(e);process.exit(1);});
