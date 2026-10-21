// Package the four v02 illustrations as editable image designs; preserve the original 16.
const fs=require('node:fs'),path=require('node:path'),{chromium}=require('playwright');
const folder='videos/001-100k-salary',force=process.argv.includes('--force');
const metadata=JSON.parse(fs.readFileSync(folder+'/review-v02/new-scenes.json'));
const titles={cashflow:['GIVE THE PAYCHECK','SOMEWHERE TO GO.'],'annual-funds':['PREDICTABLE COSTS','DESERVE A PLAN.'],'social-context':['A PHOTO DOESN’T','SHOW THE FUNDING.'],'raise-plan':['PLAN THE RAISE','BEFORE IT BECOMES ROUTINE.']};
const sections={cashflow:3,'annual-funds':4,'social-context':6,'raise-plan':7};
const cues={cashflow:"Now let's give that six thousand dollars somewhere to go.",'annual-funds':'Then real life walks in.','social-context':'Then Alex opens social media.','raise-plan':'And when the next raise comes'};
(async()=>{const browser=await chromium.launch();try{const page=await browser.newPage();await page.goto((process.env.CREDIT_STUDIO_URL||'http://127.0.0.1:8000')+'/work/salary-v02/contact.html');
 const artwork=JSON.parse(fs.readFileSync(folder+'/artwork.json'));
 for(const scene of metadata.scenes){
  const id='v02-'+scene.id,target=folder+'/projects/'+id+'.json';if(fs.existsSync(target)&&!force)throw Error('Already exists: '+target);
  const src='data:image/png;base64,'+fs.readFileSync(folder+'/review-v02/'+scene.image).toString('base64');
  const result=await page.evaluate(async({scene,src,titles,section})=>{
   const img=new Image();img.src=src;await img.decode();await document.fonts.ready;const canvas=document.createElement('canvas');canvas.width=1920;canvas.height=1080;const ctx=canvas.getContext('2d');
   const k=Math.min(1760/img.naturalWidth,650/img.naturalHeight),w=img.naturalWidth*k,h=img.naturalHeight*k;
   const elements=[{id:'illustration',type:'image',x:80+(1760-w)/2,y:285+(650-h)/2,w,h,src,opacity:100,fill:'#ffffff'}];
   const add=(id,text,y,size,fill,center)=>{ctx.font=`700 ${size}px "Times New Roman"`;const w=ctx.measureText(text).width;elements.push({id,type:'text',text,x:center?(1920-w)/2:80,y,w:Math.ceil(w)+2,h:size*1.2,size,font:'Times New Roman',weight:700,fill,opacity:100});};
   add('chapter',`0${section}  /  SALARY REVIEW V02`,35,24,'#286a52',false);titles.forEach((text,i)=>add('title-'+i,text,100+i*79.2,66,'#27332f',true));
   ctx.fillStyle='#faf6ec';ctx.fillRect(0,0,1920,1080);for(const e of elements){if(e.type==='image')ctx.drawImage(img,e.x,e.y,e.w,e.h);else{ctx.font=`700 ${e.size}px "Times New Roman"`;ctx.fillStyle=e.fill;ctx.textBaseline='alphabetic';ctx.fillText(e.text,e.x,e.y+e.size);}}
   return {design:{version:1,name:'v02 — '+scene.title,width:1920,height:1080,bg:'#faf6ec',elements},png:canvas.toDataURL('image/png').split(',')[1]};
  },{scene,src,titles:titles[scene.id],section:sections[scene.id]});
  fs.writeFileSync(target,JSON.stringify(result.design));fs.writeFileSync(folder+'/review-v02/images/'+scene.id+'-board.png',Buffer.from(result.png,'base64'));
  const frame={id,section:sections[scene.id],slug:id,title:scene.title,caption:titles[scene.id].join('\n'),cue:cues[scene.id],scene:scene.scene,image:'review-v02/images/'+scene.id+'-board.png',project:'projects/'+id+'.json',overlays:[],motion:'Minh họa bổ sung v02. Chữ là lớp riêng trong thiết kế; toàn bộ minh họa là một lớp ảnh, chưa rig khớp. Timecode: review-v02/README.md.'};
  const previous=artwork.frames.findIndex(f=>f.id===id);if(previous<0)artwork.frames.push(frame);else artwork.frames[previous]=frame;
 }
 artwork.status='Full editable review v02: 88 shots, 486.75 seconds; 16 original designs preserved, four new illustrations.';fs.writeFileSync(folder+'/artwork.json',JSON.stringify(artwork,null,2)+'\n');console.log('Packaged 4 editable designs; gallery has '+artwork.frames.length+' frames.');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
