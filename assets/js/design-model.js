export function validateDesign(data){
 const bounded=(n,min,max)=>typeof n==='number'&&Number.isFinite(n)&&n>=min&&n<=max;
 const color=s=>typeof s==='string'&&/^#[0-9a-f]{6}$/i.test(s);
 if(!data||data.version!==1||typeof data.name!=='string'||data.name.length>100||!bounded(data.width,100,4096)||!bounded(data.height,100,4096)||!color(data.bg)||!Array.isArray(data.elements)||data.elements.length>500)throw Error('Invalid project');
 const ids=new Set();
 for(const e of data.elements){
  if(!e||typeof e.id!=='string'||ids.has(e.id)||!['rect','circle','text','image'].includes(e.type)||!bounded(e.x,-4096,8192)||!bounded(e.y,-4096,8192)||!bounded(e.w,1,8192)||!bounded(e.h,1,8192)||!bounded(e.opacity,0,100)||!color(e.fill))throw Error('Invalid element');ids.add(e.id);
  if(e.type==='text'&&(typeof e.text!=='string'||e.text.length>5000||!bounded(e.size,8,500)||!['Times New Roman','Arial','Georgia','Verdana','monospace'].includes(e.font)||!['400','700'].includes(String(e.weight))))throw Error('Invalid text');
  if(e.type==='image'&&(typeof e.src!=='string'||!/^data:image\/(png|jpeg|webp|gif);base64,[A-Za-z0-9+/=]+$/.test(e.src)))throw Error('Invalid image');
 }
 return data;
}
