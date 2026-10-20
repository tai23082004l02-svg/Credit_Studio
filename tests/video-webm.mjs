import test from 'node:test';
import assert from 'node:assert/strict';
import {finalizeWebM} from '../video/webm.js';
const header=[0x1a,0x45,0xdf,0xa3,0x80,0x18,0x53,0x80,0x67,0x01,0xff,0xff,0xff,0xff,0xff,0xff,0xff];
const info=[0x15,0x49,0xa9,0x66,0x87,0x2a,0xd7,0xb1,0x83,0x0f,0x42,0x40];
const packets=[0x1f,0x43,0xb6,0x75,0x83,0x01,0x02,0x03];
test('adds a 2-second duration without changing media packets',async()=>{
 const before=new Blob([new Uint8Array([...header,...info,...packets])]);const out=new Uint8Array(await(await finalizeWebM(before,2000)).arrayBuffer());
 const position=out.findIndex((v,i)=>v===0x44&&out[i+1]===0x89&&out[i+2]===0x88);assert.ok(position>0);assert.equal(new DataView(out.buffer).getFloat64(position+3,false),2000);assert.deepEqual([...out.slice(-packets.length)],packets);
});
test('a finalized file can be updated without growing another duration tag',async()=>{
 const one=await finalizeWebM(new Blob([new Uint8Array([...header,...info,...packets])]),2000);const two=await finalizeWebM(one,5000);assert.equal(one.size,two.size);
 const bytes=new Uint8Array(await two.arrayBuffer());const position=bytes.findIndex((v,i)=>v===0x44&&bytes[i+1]===0x89);assert.equal(new DataView(bytes.buffer).getFloat64(position+3,false),5000);
});
test('preserves an indexed file layout instead of breaking seek offsets',async()=>{
 const input=new Blob([new Uint8Array([...header,0x11,0x4d,0x9b,0x74,0x80,...info,...packets])]);assert.equal(await finalizeWebM(input,2000),input);
});
