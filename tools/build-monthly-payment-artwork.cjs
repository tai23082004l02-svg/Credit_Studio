#!/usr/bin/env node
// Package generated originals into padded atlases, isolated PNGs and editable artwork.
// Uses browser canvas for lossless rectangular extraction and the actual Studio renderer.
const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),REL='videos/002-monthly-payment-trap',DIR=path.join(ROOT,REL);
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000';
if(fs.existsSync(path.join(DIR,'artwork.json'))&&!process.argv.includes('--force'))throw Error('Artwork exists. Back up manual changes; use --force only to rebuild derived assets.');
const spec=JSON.parse(fs.readFileSync(path.join(DIR,'asset-layout.json')));
const write=(f,v)=>{const dest=path.join(DIR,f);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,typeof v==='string'||Buffer.isBuffer(v)?v:JSON.stringify(v,null,2)+'\n');};
const png=(f)=>{const b=fs.readFileSync(path.join(DIR,f));return {w:b.readUInt32BE(16),h:b.readUInt32BE(20),data:'data:image/png;base64,'+b.toString('base64')};};
const C={bg:'#faf6ec',ink:'#27332f',green:'#286a52',mint:'#e2ecdd',coral:'#bd6555',sand:'#eee7d8'};
const lookup=new Map(),frames=[];
let page,browser,ctx;
const uid=(frame)=>frame.id+'-'+frame.elements.length;
function rect(f,x,y,w,h,fill){f.elements.push({id:uid(f),type:'rect',x,y,w,h,fill,opacity:100});}
async function text(f,str,x,y,size=48,fill=C.ink,width=1760,center=false){
 const lines=str.split('\n');const widths=await page.evaluate(({lines,size})=>{const c=document.createElement('canvas').getContext('2d');c.font=`700 ${size}px "Times New Roman"`;return lines.map(s=>c.measureText(s).width);},{lines,size});
 if(widths.some(v=>v>width))throw Error(`${f.id}: text overflows ${str}`);
 if(center){for(let i=0;i<lines.length;i++)await text(f,lines[i],x+(width-widths[i])/2,y+i*size*1.2,size,fill,widths[i]+2,false);return;}
 f.elements.push({id:uid(f),type:'text',x,y,w:width,h:Math.ceil(lines.length*size*1.2+4),text:str,size,font:'Times New Roman',weight:700,fill,opacity:100});
}
function picture(f,file,x,y,w,h){const p=png(file),scale=Math.min(w/p.w,h/p.h);f.elements.push({id:uid(f),type:'image',x:x+(w-p.w*scale)/2,y:y+(h-p.h*scale)/2,w:p.w*scale,h:p.h*scale,fill:'#ffffff',opacity:100,src:p.data,source:file});}
function icon(f,slug,x,y,w,h){picture(f,lookup.get(slug).image,x,y,w,h);}
async function frame(id,section,title,caption,cue,note='Illustrative example · Credit Studio'){
 const f={id,section,title,caption,cue,motion:'Lớp ảnh, chữ, số và thẻ chỉnh riêng; căn chuyển động theo audio thực tế sau khi nhận WAV.',elements:[]};
 await text(f,`0${section}  /  THE MONTHLY PAYMENT TRAP`,80,24,22,C.green);
 await text(f,caption,80,76,58,C.ink,1760,true);
 await text(f,note,80,1010,24,C.green,1760,true);return f;
}
async function cards(f,items,{y=330,h=510,x=120,gap=48,width=1680}={}){
 const w=(width-gap*(items.length-1))/items.length;
 for(let i=0;i<items.length;i++){
  const left=x+i*(w+gap),it=items[i];rect(f,left,y,w,h,i%2?C.mint:C.sand);
  icon(f,it.icon,left+48,y+36,w-96,190);
  await text(f,it.label,left+20,y+250,it.labelSize||36,C.ink,w-40,true);
  if(it.value)await text(f,it.value,left+20,y+350,it.valueSize||54,it.color||C.green,w-40,true);
  if(it.detail)await text(f,it.detail,left+20,y+435,30,C.ink,w-40,true);
 }
}
async function main(){
 const executablePath=process.env.CREDIT_CHROMIUM||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined);
 browser=await chromium.launch({executablePath});page=await browser.newPage({viewport:{width:1920,height:1080}});
 await page.goto(base+'/');await page.evaluate(async()=>{await document.fonts.ready;});
 // Explicit local font check: rendering a matching fallback is not sufficient.
 const actual=await page.evaluate(async()=>{const font=new FontFace('CreditTimes','url(/work/monthly-payment-trap/timesbd.ttf)');await font.load();document.fonts.add(font);return font.status;}).catch(()=>null);
 if(actual!=='loaded')throw Error('Prepare licensed Times New Roman at work/monthly-payment-trap/timesbd.ttf before building.');
 // Install a browser-local face under the exact family used by the Studio engine.
 await page.addStyleTag({content:'@font-face{font-family:"Times New Roman";font-weight:700;src:url("/work/monthly-payment-trap/timesbd.ttf")}'});
 await page.evaluate(()=>document.fonts.load('700 58px "Times New Roman"'));
 for(const sheet of spec.sheets){
  for(const item of sheet.items){
   const src=base+'/'+REL+'/'+sheet.sourceImage;
   const result=await page.evaluate(async({src,crop})=>{const im=new Image();im.src=src;await im.decode();const [x,y,w,h]=crop,c=document.createElement('canvas');c.width=w+64;c.height=h+64;c.getContext('2d').drawImage(im,x,y,w,h,32,32,w,h);return c.toDataURL('image/png').split(',')[1];},{src,crop:item.sourceCrop});
   write(item.image,Buffer.from(result,'base64'));lookup.set(item.slug,item);
  }
  const character=sheet.id==='alex-actions',cw=character?640:512,ch=character?768:448;
  sheet.image=`images/sheets/${sheet.id}.png`;sheet.guide=`images/sheets/${sheet.id}-guide.png`;sheet.width=cw*sheet.columns;sheet.height=ch*sheet.rows;
  const layout=await page.evaluate(async({items,cols,rows,cw,ch,base})=>{
   const c=document.createElement('canvas');c.width=cw*cols;c.height=ch*rows;const g=c.getContext('2d'),placements=[];
   for(let i=0;i<items.length;i++){const im=new Image();im.src=base+'/'+items[i].image;await im.decode();const x=(i%cols)*cw,y=Math.floor(i/cols)*ch,s=Math.min(1,(cw-112)/im.width,(ch-128)/im.height),w=im.width*s,h=im.height*s,dx=Math.round(x+(cw-w)/2),dy=Math.round(y+(ch-h)/2);g.drawImage(im,dx,dy,w,h);placements.push({cell:[x,y,cw,ch],art:[dx,dy,Math.ceil(w),Math.ceil(h)]});}
   const atlas=c.toDataURL('image/png').split(',')[1];
   const guide=document.createElement('canvas');guide.width=c.width;guide.height=c.height;const z=guide.getContext('2d');z.fillStyle='#faf6ec';z.fillRect(0,0,guide.width,guide.height);
   z.drawImage(c,0,0);for(let i=0;i<items.length;i++){const x=(i%cols)*cw,y=Math.floor(i/cols)*ch;z.strokeStyle='#d0d9c9';z.lineWidth=2;z.strokeRect(x+12,y+12,cw-24,ch-24);z.fillStyle='#286a52';z.font='700 22px "Times New Roman"';z.textAlign='center';z.fillText(String(i+1).padStart(2,'0')+' · '+items[i].name,x+cw/2,y+ch-26,cw-40);}
   return {atlas,guide:guide.toDataURL('image/png').split(',')[1],placements};
  },{items:sheet.items,cols:sheet.columns,rows:sheet.rows,cw,ch,base:base+'/'+REL});
  write(sheet.image,Buffer.from(layout.atlas,'base64'));write(sheet.guide,Buffer.from(layout.guide,'base64'));
  sheet.items.forEach((it,i)=>{it.crop=layout.placements[i].cell;it.artBounds=layout.placements[i].art;});
 }
 for(const job of spec.jobs){
  const f=await frame(job.id,job.section,job.title,job.caption,job.cue,job.section===4?'Illustrative comparison · Check the total cost and term':'Illustrative example');
  picture(f,job.image,80,254,1760,738);f.motion=job.motion;f.scene=job.scene;frames.push(f);
 }
 let f;
 f=await frame('01b',1,'Từng khoản trả chiếm chỗ trong lương','ONE PAYMENT AT A TIME.\nLESS ROOM IN YOUR PAYCHECK.','Alex has been buying things one manageable payment at a time.');
 await cards(f,[{icon:'pay-envelope',label:'PAYDAY',value:'MONEY IN'},{icon:'receipt',label:'AUTO PAYMENTS',value:'MONEY OUT',color:C.coral},{icon:'padlock',label:'FUTURE INCOME',value:'SPOKEN FOR',valueSize:42}]);frames.push(f);
 f=await frame('02b',2,'So sánh đúng giá điện thoại','SAME PRICE.\nVERY DIFFERENT FEELING.','Same price, assuming no interest or fees.','Assumes no interest or fees · Hypothetical example');
 await cards(f,[{icon:'new-phone',label:'PAY TODAY',value:'$900',detail:'Total: $900'},{icon:'new-phone',label:'PAY OVER 24 MONTHS',value:'$37.50 / month',valueSize:50,detail:'$37.50 × 24 = $900'}],{x:120,width:1680,gap:100,h:560});frames.push(f);
 f=await frame('03b',3,'Năm khoản cộng lại thành $817.50','FIVE SMALLER BILLS.\nONE BIGGER COMMITMENT.','That adds up to eight hundred seventeen dollars and fifty cents.','Before rent, groceries, utilities, insurance and gas · Illustrative month');
 await cards(f,[{icon:'compact-car',label:'CAR',value:'$525'},{icon:'new-phone',label:'PHONE',value:'$37.50'},{icon:'sofa',label:'FURNITURE',value:'$90'},{icon:'parcel',label:'BNPL DUE',value:'$120'},{icon:'streaming',label:'SUBSCRIPTIONS',labelSize:27,value:'$45'}],{x:90,width:1740,gap:24,h:450,y:310});
 await text(f,'TOTAL THIS MONTH: $817.50',100,850,62,C.coral,1720,true);frames.push(f);
 f=await frame('04b',4,'So sánh khoản trả, kỳ hạn và tổng chi phí','COMPARE THE TOTAL.\nCOMPARE THE PAYOFF DATE.','You need the total cost and the payoff date to know the difference.','Simplified hypothetical financing · Real rates, fees and terms vary');
 await cards(f,[{icon:'calendar',label:'24 MONTHS',value:'$75 / month',detail:'Total payments: $1,800'},{icon:'calendar',label:'36 MONTHS',value:'$60 / month',color:C.coral,detail:'Total payments: $2,160'}],{x:120,width:1680,gap:100,h:560,y:280});
 await text(f,'$15 LESS EACH MONTH · $360 MORE OVERALL',100,900,46,C.coral,1720,true);frames.push(f);
 f=await frame('05b',5,'Tiền cần có đúng ngày','ENOUGH THIS MONTH?\nENOUGH ON THE RIGHT DAY?','That’s a cash-flow problem.','Illustrative due dates · Other installments follow next week');
 await cards(f,[{icon:'wrench',label:'REPAIR NOW',value:'$600',color:C.coral},{icon:'compact-car',label:'CAR: TUESDAY',value:'$525'},{icon:'sofa',label:'SOFA: THURSDAY',value:'$90'}]);frames.push(f);
 f=await frame('06b',6,'Ba điều cần kiểm tra trước khi vay','A PAYMENT CAN HELP.\nCHECK THE WHOLE ARRANGEMENT.','The useful question is what the arrangement does to your finances.');
 await cards(f,[{icon:'bank-card',label:'FULL PRICE',value:'WORTH IT?',valueSize:46},{icon:'receipt',label:'INTEREST & FEES',labelSize:33,value:'TOTAL COST',valueSize:44},{icon:'savings-jar',label:'AN IMPERFECT MONTH',labelSize:27,value:'ROOM LEFT?',valueSize:44}]);frames.push(f);
 f=await frame('07b',7,'Bốn cột của danh sách thanh toán','ONE LIST.\nA CLEARER VIEW OF YOUR FUTURE.','Next to each one: the amount, the due date','Include remaining balances and payoff dates where applicable.');
 await cards(f,[{icon:'coins',label:'MONTHLY\nAMOUNT'},{icon:'clock',label:'DUE\nDATE'},{icon:'receipt',label:'REMAINING\nBALANCE'},{icon:'calendar',label:'PAYOFF\nDATE'}],{x:80,width:1760,gap:32,h:470});
 await text(f,'WHEN A PAYMENT ENDS, KEEP SOME ROOM.',100,880,46,C.green,1720,true);frames.push(f);
 f=await frame('08b',8,'Ba câu hỏi trước khoản trả mới','BEFORE “ONLY $49 A MONTH”…\nLOOK AT THE MONTHS IT OCCUPIES.','What will you pay in total?','A smaller payment is one part of the decision.');
 await cards(f,[{icon:'cash-stack',label:'WHAT WILL YOU',value:'PAY IN TOTAL?',valueSize:40},{icon:'calendar',label:'WHAT ELSE NEEDS',value:'THAT MONEY?',valueSize:40},{icon:'comparison-cards',label:'WHEN IT ENDS…',value:'WORTH THE TRADE?',valueSize:33}]);frames.push(f);
 frames.sort((a,b)=>a.id.localeCompare(b.id));
 const assets={},clips=[];
 for(const f of frames){
  const layers=[];
  for(const e of f.elements){
   if(e.type==='image'){const key=e.source.replace(/[^a-zA-Z0-9]/g,'-');assets[key]={src:REL+'/'+e.source,label:e.source.split('/').pop()};layers.push({id:e.id,type:'image',asset:key,x:e.x,y:e.y,w:e.w,h:e.h,enter:0,effect:'none',opacity:1,drift:0});}
   else if(e.type==='rect')layers.push({id:e.id,type:'rect',x:e.x,y:e.y,w:e.w,h:e.h,fill:e.fill,radius:0,enter:0,effect:'none',opacity:1,drift:0});
   else layers.push({id:e.id,type:'text',x:e.x,y:e.y,w:e.w,h:e.h,text:e.text,size:e.size,fill:e.fill,align:'left',enter:0,effect:'none',opacity:1,drift:0});
  }
  clips.push({id:f.id,title:f.id+' · '+f.title,duration:6,background:C.bg,fade:0,layers});
  const project={version:1,name:f.id+' — '+f.title,width:1920,height:1080,bg:C.bg,elements:f.elements.map(({source,...e})=>e)};
  write('projects/'+f.id+'.json',project);f.project='projects/'+f.id+'.json';f.image='images/scenes/'+f.id+'.png';f.overlays=[];f.layered=true;
 }
 const project={kind:'credit-studio-video',version:1,revision:'artwork-board-v01',name:'Monthly Payment Trap — Bảng cảnh hình, chưa căn audio',width:1920,height:1080,fps:30,audio:{src:'',offset:0,volume:1},assets,clips,captions:[],waveform:[],waveformDuration:96,showCaptions:false,productionNote:'16 still artwork boards at 6 seconds each for browsing only. No narration, no final timing, no finished video.'};
 write('storyboard/project.json',project);
 // Export each frame through the exact same renderer used in video preview.
 await page.evaluate(async p=>{const engine=await import('/video/engine.js?v=r2-v1');engine.validate(p);window.boardEngine=engine;window.boardProject=p;window.boardImages=await engine.loadAssets(p,location.origin+'/');},project);
 for(let i=0;i<frames.length;i++){
  const b64=await page.evaluate(i=>{const c=document.createElement('canvas');c.width=1920;c.height=1080;boardEngine.render(c.getContext('2d'),boardProject,boardImages,i*6+3);return c.toDataURL('image/png').split(',')[1];},i);
  write(frames[i].image,Buffer.from(b64,'base64'));
 }
 const artwork={version:1,video:'002-monthly-payment-trap',title:'The Monthly Payment Trap: How “Affordable” Keeps You Broke',canvas:{width:1920,height:1080},status:'Artwork prepared; no narration received; storyboard timings are placeholders.',frames:frames.map(({elements,...f})=>f),sheets:spec.sheets};
 write('artwork.json',artwork);
 write('images/crop-map.json',{version:1,coordinateFormat:'[x, y, width, height] in source pixels; zero-based',padding:32,sheets:spec.sheets});
 const catalogFile=path.join(ROOT,'library/props/catalog.json'),catalog=JSON.parse(fs.readFileSync(catalogFile));
 for(const s of spec.sheets)for(const it of s.items){const item={id:it.id,name:it.name,category:s.id==='alex-actions'?'Nhân vật':s.id==='purchase-props'?'Mua sắm & trả góp':'Lập kế hoạch',tags:['monthly payment','installment',it.slug,'mpt'],src:REL+'/'+s.image,crop:it.crop};const old=catalog.items.findIndex(p=>p.id===item.id);if(old<0)catalog.items.push(item);else catalog.items[old]=item;}
 fs.writeFileSync(catalogFile,JSON.stringify(catalog,null,2)+'\n');
 console.log(`Built ${frames.length} editable frames, ${spec.sheets.length} atlases, ${lookup.size} isolated PNGs; shared library ${catalog.items.length} items.`);
}
main().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
