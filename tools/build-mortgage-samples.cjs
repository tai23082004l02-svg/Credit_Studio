#!/usr/bin/env node
// Three actual-audio excerpts for style review, not the full narrated production.
// Keeps the original WAV unchanged; outputs one self-contained editable project.
const fs=require('node:fs'),path=require('node:path'),{execFileSync}=require('node:child_process');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),V=path.join(ROOT,'videos/005-mortgage-payment');
const [voice,timingFile,scratch]=process.argv.slice(2);
if(!voice||!timingFile||!scratch)throw Error('Usage: node tools/build-mortgage-samples.cjs normalized.mp3 script-timing.json scratch-directory');
const out=path.join(V,'samples/project.json');
if(fs.existsSync(out))throw Error('Samples already exist; preserve manual edits and choose a new version before rebuilding.');
const timing=JSON.parse(fs.readFileSync(timingFile)),norm=s=>s.toLowerCase().replace(/[^a-z0-9]/g,''),tokens=timing.map(w=>norm(w.word));
function cue(phrase){const q=phrase.split(/\s+/).map(norm);const i=tokens.findIndex((_,i)=>q.every((w,j)=>tokens[i+j]===w));if(i<0)throw Error('Cue not found: '+phrase);return timing[i].start;}
const BG='#f6f0e5',INK='#302e29',RED='#873e3d',SAND='#e9dfce',SAGE='#718372',MUTED='#786b5d';
const tx=(id,text,x,y,w,size=48,fill=INK,enter=0,align='left')=>({id,type:'text',text,x,y,w,h:Math.ceil(size*1.18*(text.split('\n').length)+8),size,fill,align,enter,effect:'none',opacity:1,drift:0});
const rect=(id,x,y,w,h,fill,enter=0,radius=0)=>({id,type:'rect',x,y,w,h,fill,radius,enter,effect:'none',opacity:1,drift:0});
const image=(id,x,y,w,h)=>({id,type:'image',asset:'house',x,y,w,h,enter:0,effect:'fade',opacity:1,drift:0});
function motion(l,property,keys,extra={}){l.animation={property,easing:'smooth',keys:keys.map(([time,value])=>({time:+time.toFixed(4),value})),...extra};return l;}
function money(l,keys){return motion(l,'number',keys,{format:'currency',prefix:'',suffix:''});}
function header(n,title){return [tx('chapter',`MORTGAGE / ${String(n).padStart(2,'0')}`,90,38,1300,25,MUTED),tx('sample','STYLE SAMPLE',1530,38,300,24,MUTED,0,'right'),rect('top-rule',90,83,1740,2,RED),tx('headline',title,90,126,1740,70),tx('scope','FICTIONAL EXAMPLE  /  Not a quote or national average',90,984,1740,24,MUTED)];}
const excerpts=[
 {id:'calculator',title:'ONE PAYMENT. PART OF THE PICTURE.',start:12.55,end:25.08},
 {id:'allocation',title:'BUILD THE WHOLE NUMBER.',start:80.95,end:123.12},
 {id:'cash-equity',title:'WHAT IS LEFT IN CASH?',start:222.92,end:255.02}
];
function local(s,phrase){const t=cue(phrase)-s.start;if(t<-.01||t>s.end-s.start)throw Error('Cue outside sample: '+phrase);return Math.max(0,t);}
function layers(s){
 if(s.id==='calculator'){
  const enter=local(s,'About fifteen hundred dollars');
  const a=header(1,s.title);a.push(image('home',100,304,790,620));
  a.push(tx('home-label','A PLACE TO CALL YOUR OWN',120,878,750,30,INK,0,'center'));
  a.push(rect('calculator-shadow',1000,330,720,580,'#ded3c0',0,22),rect('calculator-body',980,310,720,580,INK,0,22));
  a.push(rect('display',1020,350,640,240,BG,0,12),tx('display-label','PRINCIPAL + INTEREST',1060,382,560,31,MUTED,0,'center'));
  a.push(tx('amount','≈ $1,500',1060,449,560,108,RED,enter,'center'));
  for(let i=0;i<6;i++){const x=1025+i%3*214,y=633+Math.floor(i/3)*105;a.push(rect('key-'+i,x,y,188,80,SAND,0,8),tx('key-label-'+i,['7','8','9','4','5','6'][i],x,y+13,188,42,INK,0,'center'));}
  a.push(tx('note','Opening rounded estimate · loan payment only',1000,920,700,26,MUTED,enter,'center'));return a;
 }
 if(s.id==='allocation'){
  const a=header(2,s.title),D=s.end-s.start;
  const points=[0,local(s,'Now add three hundred dollars'),local(s,'one hundred twenty-five'),local(s,'and seventy-five'),local(s,'Then Jamie sets aside')];
  const totals=[1517,1817,1942,2017,2267],keys=[[0,1517]];
  const rows=[['LOAN','Principal + interest',1517,RED],['TAX','Property taxes',300,'#b76b5c'],['INS','Homeowners insurance',125,'#c29876'],['HOA','Association fee',75,'#9e8873'],['SAVE','Saved for repairs',250,SAGE]];
  rows.forEach(([tag,label,value,color],i)=>{
   const y=315+i*94,t=points[i];a.push(rect('chip-'+i,100,y,100,66,color,t,5),tx('tag-'+i,tag,100,y+17,100,23,'#ffffff',t,'center'),tx('label-'+i,label,230,y+12,660,39,INK,t),tx('cost-'+i,'$'+value.toLocaleString('en-US'),910,y+10,240,42,i===4?SAGE:INK,t,'right'));
   if(i){keys.push([t,totals[i-1]],[Math.min(t+.65,D-.1),totals[i]]);}
   const before=rows.slice(0,i).reduce((n,r)=>n+r[2],0),width=1700*value/2267;
   const bar=rect('bar-'+i,100+1700*before/2267,858,width,46,color,t);
   if(i)motion(bar,'width',[[t,0],[Math.min(t+.65,D-.1),width]]);a.push(bar);
  });
  a.push(rect('total-panel',1250,312,570,470,SAND,0,8),tx('total-label','MONTHLY ALLOCATION',1285,355,500,30,INK,0,'center'),money(tx('total','$1,517',1285,432,500,100,RED,0,'center'),keys));
  a.push(tx('total-note','BEFORE UTILITIES',1285,580,500,30,MUTED,0,'center'),tx('savings-note','Bills + money kept for repairs',1285,667,500,28,MUTED,points[4],'center'));
  a.push(tx('loan-assumptions','Assumed loan: $240,000 · 6.5% fixed interest · 30 years · no financed fees',100,805,1700,25,MUTED));
  a.push(tx('bar-note','One shared scale · repair savings remain your money',100,930,1700,27,MUTED));
  return a;
 }
 const a=header(3,s.title),down=local(s,'The down payment takes sixty thousand'),closing=local(s,'Assume another nine thousand dollars'),moving=local(s,'Then moving and immediate essentials');
 a.push(rect('cash-panel',100,310,760,565,SAND,0,9),tx('cash-label','CASH AVAILABLE',140,350,680,33,INK,0,'center'));
 a.push(money(tx('cash','$75,000',140,430,680,105,RED,0,'center'),[[0,75000],[down,75000],[down+1.1,15000],[closing,15000],[closing+1.1,6000],[moving,6000],[moving+1.1,4000]]));
 a.push(tx('down-ledger','− $60,000  down payment',145,605,670,35,INK,down),tx('closing-ledger','− $9,000  other closing amounts',145,679,670,35,INK,closing),tx('moving-ledger','− $2,000  moving + essentials',145,753,670,35,INK,moving));
 a.push(tx('equity-label','DOWN PAYMENT → EQUITY',1050,330,760,34,INK,0,'center'),image('equity-home',1125,450,610,440));
 a.push(money(tx('equity','$0',1100,392,660,65,SAGE,0,'center'),[[0,0],[down,0],[down+1.1,60000]]));
 for(let i=0;i<3;i++){
  const x=880+i*10,y=600-i*10,to=1010+i*10;
  a.push(motion(rect('cash-note-'+i,x,y,110,55,SAGE,down),'x',[[down,x],[down+1.1,to]]));
  a.push(motion(rect('cash-note-inner-'+i,x+6,y+6,98,43,'#d6dfcd',down),'x',[[down,x+6],[down+1.1,to+6]]));
  a.push(motion(tx('cash-note-symbol-'+i,'$',x+10,y+10,90,27,SAGE,down,'center'),'x',[[down,x+10],[down+1.1,to+10]]));
 }
 a.push(tx('equity-foot','Value in the home ≠ cash in the bank',1020,918,800,29,MUTED,down,'center'),tx('closing-foot','Closing amounts include fees, prepaids and initial escrow funding.',100,918,760,25,MUTED,closing));return a;
}
(async()=>{
 fs.mkdirSync(scratch,{recursive:true});
 const sampleAudio=path.join(scratch,'sample-audio-v01.mp3');if(fs.existsSync(sampleAudio))throw Error('Scratch audio already exists; use a new scratch directory.');
 const filters=excerpts.map((s,i)=>`[0:a]atrim=start=${s.start}:end=${s.end},asetpts=PTS-STARTPTS[a${i}]`).join(';')+';'+excerpts.map((_,i)=>`[a${i}]`).join('')+`concat=n=${excerpts.length}:v=0:a=1[out]`;
 execFileSync('ffmpeg',['-v','error','-n','-i',path.resolve(voice),'-filter_complex',filters,'-map','[out]','-ar','24000','-c:a','libmp3lame','-b:a','128k',sampleAudio]);
 const browser=await chromium.launch();let png;
 try{const page=await browser.newPage();const svg=fs.readFileSync(path.join(V,'samples/house.svg'),'utf8');png=await page.evaluate(async svg=>{const im=new Image();im.src='data:image/svg+xml;base64,'+btoa(svg);await im.decode();const c=document.createElement('canvas');c.width=1000;c.height=800;c.getContext('2d').drawImage(im,0,0);return c.toDataURL('image/png');},svg);}finally{await browser.close();}
 const clips=excerpts.map(s=>({id:s.id,title:s.title,duration:+(s.end-s.start).toFixed(5),background:BG,fade:.05,layers:layers(s)}));
 const project={kind:'credit-studio-video',version:1,revision:'mortgage-style-samples-v01',name:'Mortgage — 3 cảnh mẫu v01 (chưa phải bản đầy đủ)',width:1920,height:1080,fps:30,assets:{house:{src:png}},audio:{src:'data:audio/mpeg;base64,'+fs.readFileSync(sampleAudio).toString('base64'),offset:0,volume:1},clips,captions:[],showCaptions:false,sampleExcerpts:excerpts,sourceDuration:566.45};
 const {validate,duration}=await import('../video/engine.js');validate(project);
 fs.writeFileSync(out,JSON.stringify(project,null,2)+'\n');
 fs.writeFileSync(path.join(V,'samples/excerpts.json'),JSON.stringify({sourceDuration:566.45,duration:duration(project),excerpts},null,2)+'\n');
 console.log(JSON.stringify({project:out,duration:duration(project),excerpts,bytes:fs.statSync(out).size}));
})().catch(e=>{console.error(e);process.exitCode=1;});
