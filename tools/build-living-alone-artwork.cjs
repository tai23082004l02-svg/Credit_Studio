#!/usr/bin/env node
// Package generated originals into padded atlases, isolated PNGs and editable artwork.
// Uses browser canvas for lossless rectangular extraction and the actual Studio renderer.
const fs=require('fs'),path=require('path');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),REL='videos/004-living-alone',DIR=path.join(ROOT,REL);
const base=process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000';
if(fs.existsSync(path.join(DIR,'artwork.json'))&&!process.argv.includes('--force'))throw Error('Artwork exists. Back up manual changes; use --force only to rebuild derived assets.');
const spec=JSON.parse(fs.readFileSync(path.join(DIR,'asset-layout.json')));
const write=(f,v)=>{const dest=path.join(DIR,f);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,typeof v==='string'||Buffer.isBuffer(v)?v:JSON.stringify(v,null,2)+'\n');};
const png=(f)=>{const b=fs.readFileSync(path.join(DIR,f));return {w:b.readUInt32BE(16),h:b.readUInt32BE(20),data:'data:image/png;base64,'+b.toString('base64')};};
const C={bg:'#f6f0e5',ink:'#292722',green:'#685747',mint:'#e8e8da',coral:'#873e3d',sand:'#eee3d4'};
const lookup=new Map(),frames=[];
let page,browser,ctx;
const uid=(frame)=>frame.id+'-'+frame.elements.length;
function rect(f,x,y,w,h,fill){f.elements.push({id:uid(f),type:'rect',x,y,w,h,fill,opacity:100});}
async function text(f,str,x,y,size=48,fill=C.ink,width=1760,center=false){
 const lines=str.split('\n');const widths=await page.evaluate(({lines,size})=>{const c=document.createElement('canvas').getContext('2d');c.font=`700 ${size}px "Times New Roman"`;return lines.map(s=>c.measureText(s).width);},{lines,size});
 if(widths.some(v=>v>width))throw Error(`${f.id}: text overflows ${str}`);
 if(center){for(let i=0;i<lines.length;i++)await text(f,lines[i],x+(width-widths[i])/2,y+i*size*1.3,size,fill,widths[i]+2,false);return;}
 f.elements.push({id:uid(f),type:'text',x,y,w:width,h:Math.ceil(lines.length*size*1.2+4),text:str,size,font:'Times New Roman',weight:700,fill,opacity:100});
}
function picture(f,file,x,y,w,h){const p=png(file),scale=Math.min(w/p.w,h/p.h);f.elements.push({id:uid(f),type:'image',x:x+(w-p.w*scale)/2,y:y+(h-p.h*scale)/2,w:p.w*scale,h:p.h*scale,fill:'#ffffff',opacity:100,src:p.data,source:file});}
function icon(f,slug,x,y,w,h){picture(f,lookup.get(slug).image,x,y,w,h);}
async function frame(id,section,title,caption,cue,note='Generated editorial collage · Illustrative imagery, not documentary photographs'){
 const f={id,section,title,caption,cue,motion:'Lớp ảnh, chữ, số và thẻ chỉnh riêng; căn chuyển động theo audio thực tế sau khi nhận WAV.',elements:[]};
 await text(f,`0${section}  /  THE COST OF LIVING ALONE`,80,24,22,C.green);
 rect(f,80,60,1760,2,C.coral);
 await text(f,caption,80,90,60,C.ink,1760,true);
 rect(f,80,985,1760,2,C.coral);
 await text(f,note,80,1010,23,C.green,1760,true);return f;
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
   const result=await page.evaluate(async({src,crop})=>{const im=new Image();im.src=src;await im.decode();const [x,y,w,h]=crop,temp=document.createElement('canvas');temp.width=w;temp.height=h;const g=temp.getContext('2d');g.drawImage(im,x,y,w,h,0,0,w,h);const pixels=g.getImageData(0,0,w,h).data;let left=w,top=h,right=-1,bottom=-1;for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++)if(pixels[(yy*w+xx)*4+3]>8){left=Math.min(left,xx);top=Math.min(top,yy);right=Math.max(right,xx);bottom=Math.max(bottom,yy);}if(right<left)throw Error('Empty source cell');if(left<4||top<4||right>w-5||bottom>h-5)throw Error('Source art touches crop boundary; fix sheet or sourceCrop before packaging.');left=Math.max(0,left-8);top=Math.max(0,top-8);right=Math.min(w,right+9);bottom=Math.min(h,bottom+9);const c=document.createElement('canvas');c.width=right-left+64;c.height=bottom-top+64;c.getContext('2d').drawImage(temp,left,top,right-left,bottom-top,32,32,right-left,bottom-top);return{b64:c.toDataURL('image/png').split(',')[1],sourceArtCrop:[x+left,y+top,right-left,bottom-top]};},{src,crop:item.sourceCrop});
   item.sourceArtCrop=result.sourceArtCrop;write(item.image,Buffer.from(result.b64,'base64'));lookup.set(item.slug,item);
  }
  const character=sheet.id==='alex-actions',cw=character?640:512,ch=character?768:448;
  sheet.image=`images/sheets/${sheet.id}.png`;sheet.guide=`images/sheets/${sheet.id}-guide.png`;sheet.width=cw*sheet.columns;sheet.height=ch*sheet.rows;
  const layout=await page.evaluate(async({items,cols,rows,cw,ch,base})=>{
   const c=document.createElement('canvas');c.width=cw*cols;c.height=ch*rows;const g=c.getContext('2d'),placements=[];
   for(let i=0;i<items.length;i++){const im=new Image();im.src=base+'/'+items[i].image;await im.decode();const x=(i%cols)*cw,y=Math.floor(i/cols)*ch,s=Math.min(1,(cw-112)/im.width,(ch-128)/im.height),w=im.width*s,h=im.height*s,dx=Math.round(x+(cw-w)/2),dy=Math.round(y+(ch-h)/2);g.drawImage(im,dx,dy,w,h);placements.push({cell:[x,y,cw,ch],art:[dx,dy,Math.ceil(w),Math.ceil(h)]});}
   const atlas=c.toDataURL('image/png').split(',')[1];
   const guide=document.createElement('canvas');guide.width=c.width;guide.height=c.height;const z=guide.getContext('2d');z.fillStyle='#f6f0e5';z.fillRect(0,0,guide.width,guide.height);
   z.drawImage(c,0,0);for(let i=0;i<items.length;i++){const x=(i%cols)*cw,y=Math.floor(i/cols)*ch;z.strokeStyle='#c4b7a1';z.lineWidth=2;z.strokeRect(x+12,y+12,cw-24,ch-24);z.fillStyle='#873e3d';z.font='700 22px "Times New Roman"';z.textAlign='center';z.fillText(String(i+1).padStart(2,'0')+' · '+items[i].name,x+cw/2,y+ch-26,cw-40);}
   return {atlas,guide:guide.toDataURL('image/png').split(',')[1],placements};
  },{items:sheet.items,cols:sheet.columns,rows:sheet.rows,cw,ch,base:base+'/'+REL});
  write(sheet.image,Buffer.from(layout.atlas,'base64'));write(sheet.guide,Buffer.from(layout.guide,'base64'));
  sheet.items.forEach((it,i)=>{it.crop=layout.placements[i].cell;it.artBounds=layout.placements[i].art;});
 }

 const oldCatalog=JSON.parse(fs.readFileSync(path.join(ROOT,'library/props/catalog.json')));
 for(const r of spec.reuse){const old=oldCatalog.items.find(p=>p.id===r.id);if(!old)throw Error('Missing shared prop '+r.id);const output='images/reused/'+r.slug+'.png';const result=await page.evaluate(async({src,crop})=>{const im=new Image();im.src=src;await im.decode();const box=crop||[0,0,im.width,im.height],c=document.createElement('canvas');c.width=box[2]+64;c.height=box[3]+64;c.getContext('2d').drawImage(im,...box,32,32,box[2],box[3]);return c.toDataURL('image/png').split(',')[1];},{src:base+'/'+old.src,crop:old.crop});write(output,Buffer.from(result,'base64'));lookup.set(r.slug,{image:output,reusedFrom:r.id});}

 for(const job of spec.jobs){const f=await frame(job.id,job.section,job.title,job.caption,job.cue);picture(f,job.image,120,270,1680,695);f.motion=job.motion;f.scene=job.scene;frames.push(f);}
 let f;
 f=await frame('01b',1,'Những hóa đơn không tự chia đôi','ONE PERSON. FOUR BILLS.','Rent. Electricity. Internet. Groceries.','Conceptual categories · Actual costs depend on your home and usage');
 await cards(f,[{icon:'apartment',label:'RENT',value:'ONE FULL BILL',valueSize:32},{icon:'bills',label:'UTILITIES',value:'USAGE + FIXED COSTS',valueSize:23},{icon:'router',label:'INTERNET',value:'ONE CONNECTION',valueSize:29},{icon:'groceries',label:'GROCERIES',value:'PORTIONS MATTER',valueSize:28}],{y:320,h:510,gap:28});
 await text(f,'Many bills follow the home, not the number of people.',100,900,40,C.coral,1720,true);frames.push(f);
 f=await frame('02b',2,'So sánh tiền nhà và internet mỗi người','THE COST OF NOT SPLITTING.','A difference of six hundred and thirty dollars a month.','Illustrative example — not national averages · Rent + internet only');
 for(const [x,label,rent,total,share]of [[100,'LIVING ALONE','$1,800','$1,860',1860],[1020,'SHARING WITH ONE FRIEND','$2,400 ÷ 2 = $1,200','$1,230',1230]]){
  rect(f,x,300,800,530,C.sand);icon(f,x===100?'house-keys':'apartment',x+38,330,200,195);
  await text(f,label,x+260,350,28,C.green,500,true);await text(f,rent,x+260,410,x===100?60:38,C.ink,500,true);
  await text(f,x===100?'Internet: $60':'Internet: $60 ÷ 2 = $30',x+45,550,34,C.ink,710,true);
  await text(f,total+' / month',x+45,625,62,C.coral,710,true);
  rect(f,x+70,755,660,18,C.mint);rect(f,x+70,755,660*share/1860,18,C.coral);
 }
 await text(f,'GAP: $630 / MONTH  ·  $7,560 / YEAR',100,885,52,C.coral,1720,true);frames.push(f);
 f=await frame('03b',3,'Dữ liệu lịch sử, hai đơn vị khác nhau','A GROWING COST. A COMMON LIFE.','Living alone is also far from unusual.','Historical data · BLS: Dec. 2024 CPI release · Census: 2024 households');
 rect(f,100,300,800,620,C.sand);rect(f,1020,300,800,620,C.mint);
 await text(f,'+4.3%',140,355,140,C.coral,720,true);
 await text(f,'RENT PRICE INDEX',140,550,38,C.ink,720,true);
 await text(f,'12 months ending December 2024',140,625,34,C.ink,720,true);
 await text(f,'A national change, not a rent quote.',140,760,31,C.green,720,true);
 await text(f,'38.5 million',1060,355,100,C.coral,720,true);
 await text(f,'ONE-PERSON HOUSEHOLDS',1060,510,34,C.ink,720,true);
 await text(f,'29% of U.S. households',1060,615,52,C.ink,720,true);
 await text(f,'2024 · Households, not people.',1060,760,33,C.green,720,true);frames.push(f);
 f=await frame('04b',4,'Tách chi định kỳ, theo dùng và trả trước','NOT EVERY COST BEHAVES THE SAME.','Then there are the costs of setting up a home.','Categories only · Deposits may be refundable; they still tie up cash');
 await cards(f,[{icon:'fridge',label:'RUNNING THE HOME',labelSize:31,value:'RECURRING',valueSize:44,detail:'Internet · utilities'},{icon:'groceries',label:'WHAT YOU USE',labelSize:34,value:'VARIABLE',valueSize:44,detail:'Food · portions'},{icon:'moving-box',label:'MOVING IN',labelSize:34,value:'UPFRONT',valueSize:44,detail:'Furniture · moving'}],{y:300,h:540,gap:40});
 icon(f,'deposit',600,865,105,100);await text(f,'A refundable deposit is cash tied up, not automatically money lost.',725,890,29,C.coral,1080,false);frames.push(f);
 f=await frame('05b',5,'Hai tháng của riêng tiền nhà và internet','THE BILL KEEPS COMING.','Two months of just those bills would be thirty-seven hundred and twenty dollars.','Illustrative example — not national averages · Not a complete emergency-fund target');
 icon(f,'pay-envelope',130,325,390,300);icon(f,'calendar',130,655,390,260);
 await text(f,'2 MONTHS × $1,860',620,335,62,C.ink,1160,true);
 await text(f,'$3,720',620,440,155,C.coral,1160,true);
 await text(f,'RENT + INTERNET ONLY',620,655,46,C.ink,1160,true);
 await text(f,'Food, utilities, transport and healthcare are extra.',620,770,34,C.green,1160,true);frames.push(f);
 f=await frame('06b',6,'Đánh giá sự riêng tư và khoản đánh đổi','PRIVACY HAS VALUE.','Once you estimate your own difference, you can decide what you\'re getting for it,','Illustrative example — not national averages · This is a tradeoff, not a rule');
 rect(f,100,300,800,610,C.sand);icon(f,'armchair',1060,320,680,450);
 await text(f,'$630',140,335,145,C.coral,720,true);await text(f,'MORE PER MONTH',140,535,40,C.ink,720,true);
 await text(f,'Alex’s rent + internet difference',140,625,32,C.green,720,true);
 await text(f,'Your own comparison may differ.',140,745,31,C.ink,720,true);
 await text(f,'REST · SAFETY · QUIET',1040,820,38,C.ink,760,true);frames.push(f);
 f=await frame('07b',7,'Lập kế hoạch đủ chi phí và dự phòng','PLAN BEYOND THE RENT.','Then build a bare-bones monthly budget:','Budget the whole home · Choose a cash buffer that fits your situation');
 await cards(f,[{icon:'calculator',label:'FULL MONTHLY COST',labelSize:32,value:'ADD IT ALL',valueSize:44,detail:'Home + transport'},{icon:'moving-box',label:'MOVE-IN CASH',labelSize:34,value:'LIST SEPARATELY',valueSize:33,detail:'Deposits + setup'},{icon:'reserve-jar',label:'BARE-BONES BUDGET',labelSize:30,value:'BUILD A BUFFER',valueSize:34,detail:'Essential obligations'}],{y:300,h:550,gap:40});
 await text(f,'Compare safety, commute and moving costs before changing homes.',100,905,36,C.coral,1720,true);frames.push(f);
 f=await frame('08b',8,'Một căn nhà và khoảng thở để giữ nó','A HOME YOU CAN ENJOY AND KEEP.','The goal is to enjoy the home you worked for, with enough breathing room to keep it.','Living independently does not mean handling every problem alone');
 await cards(f,[{icon:'plant',label:'A HOME THAT FITS',labelSize:34,value:'ENJOY THE SPACE',valueSize:34},{icon:'notebook',label:'AN HONEST PLAN',labelSize:34,value:'LEAVE SOME ROOM',valueSize:32},{icon:'support-phone',label:'PEOPLE TO CALL',labelSize:34,value:'STAY CONNECTED',valueSize:33}],{y:330,h:530,gap:40});frames.push(f);
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
 const project={kind:'credit-studio-video',version:1,revision:'living-artwork-board-v01',name:'Living Alone — Bảng hình 96 giây, chưa có audio',width:1920,height:1080,fps:30,audio:{src:'',offset:0,volume:1},assets,clips,captions:[],waveform:[],waveformDuration:96,showCaptions:false,productionNote:'16 still artwork boards at 6 seconds each for browsing only. No narration, no final timing, no finished video.'};
 write('storyboard/project.json',project);
 // Export each frame through the exact same renderer used in video preview.
 await page.evaluate(async p=>{const engine=await import('/video/engine.js?v=r2-v1');engine.validate(p);window.boardEngine=engine;window.boardProject=p;window.boardImages=await engine.loadAssets(p,location.origin+'/');},project);
 for(let i=0;i<frames.length;i++){
  const b64=await page.evaluate(i=>{const c=document.createElement('canvas');c.width=1920;c.height=1080;boardEngine.render(c.getContext('2d'),boardProject,boardImages,i*6+3);return c.toDataURL('image/png').split(',')[1];},i);
  write(frames[i].image,Buffer.from(b64,'base64'));
 }
 const artwork={version:1,video:'004-living-alone',title:'Why Living Alone Has Become So Expensive',canvas:{width:1920,height:1080},status:'Artwork prepared; no narration received; storyboard timings are placeholders.',frames:frames.map(({elements,...f})=>f),sheets:spec.sheets};
 write('artwork.json',artwork);
 write('images/crop-map.json',{version:1,coordinateFormat:'[x, y, width, height], zero-based. sourceCrop/sourceArtCrop use sourceImage pixels; crop/artBounds use packed image pixels.',padding:32,sheets:spec.sheets});
 const catalogFile=path.join(ROOT,'library/props/catalog.json'),catalog=JSON.parse(fs.readFileSync(catalogFile));
 for(const s of spec.sheets)for(const it of s.items){const item={id:it.id,name:it.name,category:'Nhà ở · Collage',tags:['living alone','documentary collage','solo4',it.slug],src:REL+'/'+s.image,crop:it.crop};const old=catalog.items.findIndex(p=>p.id===item.id);if(old<0)catalog.items.push(item);else catalog.items[old]=item;}
 fs.writeFileSync(catalogFile,JSON.stringify(catalog,null,2)+'\n');
 console.log(`Built ${frames.length} editable frames, ${spec.sheets.length} atlases, ${spec.sheets.reduce((n,s)=>n+s.items.length,0)} new isolated PNGs plus ${spec.reuse.length} reused icons; shared library ${catalog.items.length} items.`);
}
main().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();});
