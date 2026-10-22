#!/usr/bin/env node
// Package generated originals into padded atlases, isolated PNGs and editable artwork.
// Uses browser canvas for lossless rectangular extraction and the actual Studio renderer.
const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),REL='videos/003-car-payment-trap',DIR=path.join(ROOT,REL);
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
 await text(f,`0${section}  /  THE CAR PAYMENT TRAP`,80,24,22,C.green);
 await text(f,caption,80,76,58,C.ink,1760,true);
 await text(f,note,80,1010,24,C.green,1760,true);return f;
}
async function cards(f,items,{y=330,h=510,x=120,gap=48,width=1680}={}){
 const w=(width-gap*(items.length-1))/items.length;
 for(let i=0;i<items.length;i++){
  const left=x+i*(w+gap),it=items[i];rect(f,left,y,w,h,i%2?C.mint:C.sand);
  if(it.symbol)await text(f,it.symbol,left+20,y+36,120,C.green,w-40,true);else icon(f,it.icon,left+48,y+36,w-96,190);
  await text(f,it.label,left+20,y+250,it.labelSize||36,C.ink,w-40,true);
  if(it.value)await text(f,it.value,left+20,y+350,it.valueSize||54,it.color||C.green,w-40,true);
  if(it.detail)await text(f,it.detail,left+20,y+435,30,C.ink,w-40,true);
 }
}
async function main(){
 const executablePath=process.env.CREDIT_CHROMIUM||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined);
 browser=await chromium.launch({executablePath});page=await browser.newPage({viewport:{width:1920,height:1080}});
 await page.goto(base+'/');await page.evaluate(async()=>{await document.fonts.ready;});
 for(const sheet of spec.sheets){
  for(const item of sheet.items){
   const src=base+'/'+REL+'/'+sheet.sourceImage;
   const result=await page.evaluate(async({src,crop})=>{const im=new Image();im.src=src;await im.decode();const [x,y,w,h]=crop,temp=document.createElement('canvas');temp.width=w;temp.height=h;const g=temp.getContext('2d');g.drawImage(im,x,y,w,h,0,0,w,h);const pixels=g.getImageData(0,0,w,h).data;let left=w,top=h,right=-1,bottom=-1;for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++)if(pixels[(yy*w+xx)*4+3]>8){left=Math.min(left,xx);top=Math.min(top,yy);right=Math.max(right,xx);bottom=Math.max(bottom,yy);}if(right<left)throw Error('Empty source cell');left=Math.max(0,left-8);top=Math.max(0,top-8);right=Math.min(w,right+9);bottom=Math.min(h,bottom+9);const c=document.createElement('canvas');c.width=right-left+64;c.height=bottom-top+64;c.getContext('2d').drawImage(temp,left,top,right-left,bottom-top,32,32,right-left,bottom-top);return{b64:c.toDataURL('image/png').split(',')[1],sourceArtCrop:[x+left,y+top,right-left,bottom-top]};},{src,crop:item.sourceCrop});
   item.sourceArtCrop=result.sourceArtCrop;write(item.image,Buffer.from(result.b64,'base64'));lookup.set(item.slug,item);
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

 const oldCatalog=JSON.parse(fs.readFileSync(path.join(ROOT,'library/props/catalog.json')));
 for(const r of spec.reuse){const old=oldCatalog.items.find(p=>p.id===r.id);if(!old)throw Error('Missing shared prop '+r.id);const output='images/reused/'+r.slug+'.png';const result=await page.evaluate(async({src,crop})=>{const im=new Image();im.src=src;await im.decode();const box=crop||[0,0,im.width,im.height],c=document.createElement('canvas');c.width=box[2]+64;c.height=box[3]+64;c.getContext('2d').drawImage(im,...box,32,32,box[2],box[3]);return c.toDataURL('image/png').split(',')[1];},{src:base+'/'+old.src,crop:old.crop});write(output,Buffer.from(result,'base64'));lookup.set(r.slug,{image:output,reusedFrom:r.id});}

 for(const job of spec.jobs){const f=await frame(job.id,job.section,job.title,job.caption,job.cue);picture(f,job.image,80,254,1760,738);f.motion=job.motion;f.scene=job.scene;frames.push(f);}
 let f;
 f=await frame('01b',1,'Khoản trả và toàn bộ chi phí xe','THE PAYMENT IS ONE NUMBER.\nOWNERSHIP IS ANOTHER.','Alex’s checking account is supporting a thousand-dollar transportation commitment.');
 await cards(f,[{icon:'red-sedan',label:'LOAN PAYMENT',value:'≈ $614 / month',valueSize:52},{icon:'auto-insurance',label:'ILLUSTRATIVE ALL-IN COST',labelSize:32,value:'≈ $1,044 / month',valueSize:52}],{gap:100,h:560,y:290});frames.push(f);
 f=await frame('02b',2,'Bốn khoản tạo thành chi phí mỗi tháng','THE COSTS ADD UP.','Now the car needs about a thousand and forty-four dollars a month.','Illustrative monthly amounts · Parking and tolls not included');
 await cards(f,[{icon:'red-sedan',label:'PAYMENT',value:'$614'},{icon:'auto-insurance',label:'INSURANCE',value:'$180'},{icon:'fuel-pump',label:'GAS',value:'$160'},{icon:'wrench',label:'UPKEEP +\nREGISTRATION',labelSize:29,value:'$90'}],{y:290,h:550,gap:30});await text(f,'≈ $1,044 / MONTH · ≈ $12,500 / YEAR',100,905,54,C.coral,1720,true);frames.push(f);
 f=await frame('03b',3,'Thời gian và tổng khoản trả','SIX YEARS.\nABOUT $44,200 REPAID.','That’s about nine thousand two hundred dollars in interest','Simplified fixed-rate example · Rounded totals · No additional financed fees');
 await cards(f,[{icon:'loan-folder',label:'AMOUNT FINANCED',value:'$35,000'},{symbol:'8%',label:'ANNUAL RATE',value:'8% APR'},{icon:'calendar',label:'LOAN LENGTH',value:'72 months'}],{y:290,h:520});await text(f,'$35,000 PRINCIPAL + ≈ $9,200 INTEREST',100,900,52,C.coral,1720,true);frames.push(f);
 f=await frame('04b',4,'Khoản thiếu khi đổi xe','THE $5,000 GAP\nDOESN’T DISAPPEAR.','That leaves a five-thousand-dollar gap.','Hypothetical trade-in · Rolling debt into a new loan requires lender approval');
 await cards(f,[{icon:'loan-folder',label:'STILL OWED',value:'$28,000'},{icon:'red-sedan',label:'TRADE-IN OFFER',value:'$23,000'},{icon:'trade-in-envelope',label:'NEGATIVE EQUITY',labelSize:32,value:'$5,000',color:C.coral}],{y:290,h:520});await text(f,'$30,000 REPLACEMENT + $5,000 OLD DEBT = $35,000',100,900,42,C.coral,1720,true);frames.push(f);
 f=await frame('05b',5,'Hai thước đo cần phân biệt','TWO MEASURES.\nDON’T DOUBLE-COUNT.','Part of the payment reduces the debt.','Do not add depreciation to the entire payment and call it monthly cash spending.');
 await cards(f,[{icon:'cash-stack',label:'CASH FLOW',value:'MONEY LEAVING',valueSize:40,detail:'Payment + operating costs'},{icon:'teal-sedan',label:'RESALE VALUE',value:'WHAT IT MAY SELL FOR',valueSize:34,detail:'Changes as the vehicle ages'}],{gap:100,h:560,y:290});frames.push(f);
 f=await frame('06b',6,'Khoảng thở từ một thay đổi nhỏ','$200 LESS PER MONTH.\n$2,400 MORE ROOM PER YEAR.','that would free up twenty-four hundred dollars a year.','Illustrative reduction · Keep transportation safe and reliable');
 await cards(f,[{icon:'red-sedan',label:'MONTHLY REDUCTION',value:'$200'},{icon:'savings-jar',label:'ANNUAL ROOM',value:'$2,400'}],{gap:100,h:560,y:290});frames.push(f);
 f=await frame('07b',7,'Năm số cần xem trước khi ký','COMPARE THESE SIDE BY SIDE.','The out-the-door price.','Also check optional products, fees and any trade-in loan balance.');
 await cards(f,[{icon:'offer-sheet',label:'OUT-THE-DOOR\nPRICE',labelSize:27},{icon:'loan-folder',label:'AMOUNT\nFINANCED',labelSize:28},{symbol:'%',label:'APR',labelSize:32},{icon:'clock',label:'LOAN\nLENGTH',labelSize:30},{icon:'cash-stack',label:'TOTAL OF\nPAYMENTS',labelSize:28}],{x:80,width:1760,gap:24,h:500,y:330});frames.push(f);
 f=await frame('08b',8,'Các phương án phải tính toàn bộ chi phí','WHAT FITS YOUR BUDGET\nAND YOUR LIFE?','Sometimes keeping a reliable car and finishing the loan is the better move.','Compare negative equity, replacement transport, fees and total remaining cost.');
 await cards(f,[{icon:'red-sedan',label:'KEEP A RELIABLE CAR',labelSize:28,value:'FINISH THE LOAN',valueSize:34},{icon:'comparison-cards',label:'REFINANCE IF IT HELPS',labelSize:26,value:'COMPARE TOTAL COST',valueSize:29},{icon:'teal-sedan',label:'SELL OR DOWNSIZE',labelSize:29,value:'COUNT THE GAP',valueSize:34}],{y:310,h:550});await text(f,'STRUGGLING TO PAY? CONTACT THE LENDER EARLY.',100,915,38,C.coral,1720,true);frames.push(f);
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
 const project={kind:'credit-studio-video',version:1,revision:'car-artwork-board-v01',name:'Car Payment Trap — Bảng cảnh hình, chưa căn audio',width:1920,height:1080,fps:30,audio:{src:'',offset:0,volume:1},assets,clips,captions:[],waveform:[],waveformDuration:96,showCaptions:false,productionNote:'16 still artwork boards at 6 seconds each for browsing only. No narration, no final timing, no finished video.'};
 write('storyboard/project.json',project);
 // Export each frame through the exact same renderer used in video preview.
 await page.evaluate(async p=>{const engine=await import('/video/engine.js?v=r2-v1');engine.validate(p);window.boardEngine=engine;window.boardProject=p;window.boardImages=await engine.loadAssets(p,location.origin+'/');},project);
 for(let i=0;i<frames.length;i++){
  const b64=await page.evaluate(i=>{const c=document.createElement('canvas');c.width=1920;c.height=1080;boardEngine.render(c.getContext('2d'),boardProject,boardImages,i*6+3);return c.toDataURL('image/png').split(',')[1];},i);
  write(frames[i].image,Buffer.from(b64,'base64'));
 }
 const artwork={version:1,video:'003-car-payment-trap',title:'Your Car Payment Is Keeping You Broke',canvas:{width:1920,height:1080},status:'Artwork prepared; no narration received; storyboard timings are placeholders.',frames:frames.map(({elements,...f})=>f),sheets:spec.sheets};
 write('artwork.json',artwork);
 write('images/crop-map.json',{version:1,coordinateFormat:'[x, y, width, height], zero-based. sourceCrop/sourceArtCrop use sourceImage pixels; crop/artBounds use packed image pixels.',padding:32,sheets:spec.sheets});
 const catalogFile=path.join(ROOT,'library/props/catalog.json'),catalog=JSON.parse(fs.readFileSync(catalogFile));
 for(const s of spec.sheets)for(const it of s.items){const item={id:it.id,name:it.name,category:s.id==='alex-actions'?'Nhân vật':'Ô tô & khoản vay',tags:['car payment','auto loan','car3',it.slug],src:REL+'/'+s.image,crop:it.crop};const old=catalog.items.findIndex(p=>p.id===item.id);if(old<0)catalog.items.push(item);else catalog.items[old]=item;}
 fs.writeFileSync(catalogFile,JSON.stringify(catalog,null,2)+'\n');
 console.log(`Built ${frames.length} editable frames, ${spec.sheets.length} atlases, ${spec.sheets.reduce((n,s)=>n+s.items.length,0)} new isolated PNGs plus ${spec.reuse.length} reused icons; shared library ${catalog.items.length} items.`);
}
main().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
