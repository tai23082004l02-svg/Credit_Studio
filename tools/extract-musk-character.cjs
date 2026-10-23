#!/usr/bin/env node
// Extract only the four approved-production character groups. Preserve source pixels.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require('playwright');
const ROOT=path.resolve(__dirname,'..'),source=path.join(ROOT,'videos/006-musk-buy-a-country/images/generated/musk-sheet-v01.png');
const out=path.join(ROOT,'videos/006-musk-buy-a-country/images/cutouts'),mapPath=path.join(ROOT,'videos/006-musk-buy-a-country/images/musk-crop-map.json');
const ids=['musk-standing','musk-palm','musk-thinking','musk-folder'];
(async()=>{
 for(const id of ids)if(fs.existsSync(path.join(out,id+'.png')))throw Error('Existing prop: preserve edits; choose a new version.');
 if(fs.existsSync(mapPath))throw Error('Crop map already exists.');
 const browser=await chromium.launch();let result;
 try{const page=await browser.newPage();result=await page.evaluate(async({url,ids})=>{
  const image=new Image();image.src=url;await image.decode();const c=document.createElement('canvas');c.width=image.width;c.height=image.height;const ctx=c.getContext('2d');ctx.drawImage(image,0,0);const pixels=ctx.getImageData(0,0,c.width,c.height).data,cellW=c.width/2,cellH=c.height/2;
  if(!Number.isInteger(cellW)||!Number.isInteger(cellH))throw Error('Source must have equal integer cells.');
  const items=[];
  for(let i=0;i<4;i++){
   const sx=i%2*cellW,sy=Math.floor(i/2)*cellH;let left=cellW,top=cellH,right=-1,bottom=-1,count=0;
   // Generation leaves alpha 1–3 speckles in empty gutters. Find visible art at
   // alpha>=4, retain another 8px of its original feather, then pad transparently.
   for(let y=0;y<cellH;y++)for(let x=0;x<cellW;x++)if(pixels[((sy+y)*c.width+sx+x)*4+3]>=4){left=Math.min(left,x);top=Math.min(top,y);right=Math.max(right,x);bottom=Math.max(bottom,y);count++;}
   if(!count)throw Error('Empty group '+ids[i]);
   const margins=[left,top,cellW-1-right,cellH-1-bottom];if(Math.min(...margins)<4)throw Error('Artwork too close to quadrant edge: '+ids[i]+' '+margins);
   const art=[sx+left,sy+top,right-left+1,bottom-top+1],fx=Math.min(8,left,cellW-1-right),fy=Math.min(8,top,cellH-1-bottom),crop=[art[0]-fx,art[1]-fy,art[2]+2*fx,art[3]+2*fy],pad=40,cut=document.createElement('canvas');cut.width=crop[2]+2*pad;cut.height=crop[3]+2*pad;cut.getContext('2d').drawImage(image,...crop,pad,pad,crop[2],crop[3]);
   const result=cut.getContext('2d').getImageData(0,0,cut.width,cut.height).data;let actual=0;for(let p=3;p<result.length;p+=4)if(result[p]>=4)actual++;if(actual!==count)throw Error('Extraction lost visible pixels: '+ids[i]);
   items.push({id:ids[i],cell:[sx,sy,cellW,cellH],sourceArtCrop:art,sourceCrop:crop,sourceMargins:margins,featherPixels:[fx,fy],transparentPadding:pad,width:cut.width,height:cut.height,visiblePixelsPreserved:count,alphaThreshold:4,output:'videos/006-musk-buy-a-country/images/cutouts/'+ids[i]+'.png',png:cut.toDataURL('image/png').split(',')[1]});
  }
  return{width:c.width,height:c.height,items};
 },{url:'data:image/png;base64,'+fs.readFileSync(source).toString('base64'),ids});}finally{await browser.close();}
 fs.mkdirSync(out,{recursive:true});
 for(const item of result.items){fs.writeFileSync(path.join(ROOT,item.output),Buffer.from(item.png,'base64'));delete item.png;}
 fs.writeFileSync(mapPath,JSON.stringify({source:'videos/006-musk-buy-a-country/images/generated/musk-sheet-v01.png',...result,validation:'All source pixels at alpha>=4 preserved; original feather retained for 8px, then 32px transparent padding. No scaling. Only alpha 1–3 gutter speckles outside this region are omitted; original sheet is unchanged. Source quadrants do not overlap.'},null,2)+'\n');
 console.log(JSON.stringify(result,null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
