// MediaRecorder produces a streaming WebM without Duration. Add that metadata
// for the unknown-size Segment layout used by Chromium, without changing packets.
function element(bytes,offset){
 const first=bytes[offset];if(!first)throw Error('Invalid EBML');
 let idLength=1,mask=0x80;while(!(first&mask)){mask>>=1;idLength++;}
 let id=0;for(let i=0;i<idLength;i++)id=id*256+bytes[offset+i];
 const sizeAt=offset+idLength,lead=bytes[sizeAt];let sizeLength=1,bit=0x80;while(bit&&!(lead&bit)){bit>>=1;sizeLength++;}
 if(!bit||sizeLength>8)throw Error('Invalid EBML size');
 let size=lead&(bit-1),unknown=size===bit-1;
 for(let i=1;i<sizeLength;i++){size=size*256+bytes[sizeAt+i];unknown=unknown&&bytes[sizeAt+i]===255;}
 const start=sizeAt+sizeLength;
 return{id,size:unknown?Infinity:size,offset,sizeAt,sizeLength,start,end:unknown?bytes.length:start+size};
}
function sizeBytes(value){
 let length=1;while(value>=Math.pow(2,7*length)-1)length++;
 const out=new Uint8Array(length);let n=value;
 for(let i=length-1;i>=0;i--){out[i]=n%256;n=Math.floor(n/256);}out[0]|=1<<(8-length);return out;
}
export async function finalizeWebM(blob,milliseconds){
 const bytes=new Uint8Array(await blob.arrayBuffer());const header=element(bytes,0),segment=element(bytes,header.end);
 if(header.id!==0x1a45dfa3||segment.id!==0x18538067||segment.size!==Infinity)return blob;
 let at=segment.start,info;
 while(at<bytes.length){const e=element(bytes,at);if(e.id===0x114d9b74)return blob; // Do not invalidate indexed offsets in another muxer's layout.
  if(e.id===0x1549a966){info=e;break;}if(e.end<=at||e.end>bytes.length)return blob;at=e.end;
 }
 if(!info||!Number.isFinite(info.size))return blob;
 let scale=1000000,existing;
 for(at=info.start;at<info.end;){const e=element(bytes,at);if(e.id===0x2ad7b1){scale=0;for(let i=e.start;i<e.end;i++)scale=scale*256+bytes[i];}if(e.id===0x4489)existing=e;if(e.end<=at||e.end>info.end)throw Error('Invalid WebM metadata');at=e.end;}
 const duration=milliseconds*1000000/scale;
 if(existing){const copy=bytes.slice(),view=new DataView(copy.buffer);if(existing.size===8)view.setFloat64(existing.start,duration,false);else if(existing.size===4)view.setFloat32(existing.start,duration,false);return new Blob([copy],{type:'video/webm'});}
 const addition=new Uint8Array(11);addition.set([0x44,0x89,0x88]);new DataView(addition.buffer).setFloat64(3,duration,false);
 return new Blob([bytes.slice(0,info.sizeAt),sizeBytes(info.size+addition.length),bytes.slice(info.start,info.end),addition,bytes.slice(info.end)],{type:'video/webm'});
}
