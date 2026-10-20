import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validate,duration,locate,clipStart,safeSource,layerBox,clone} from '../video/engine.js';
const original=JSON.parse(fs.readFileSync(new URL('../videos/001-100k-salary/intro/project.json',import.meta.url)));
test('intro covers 40.5 seconds with correct boundary selection',()=>{
 const p=validate(clone(original));assert.equal(duration(p),40.5);assert.equal(locate(p,0).index,0);assert.equal(locate(p,4.249).index,0);assert.equal(locate(p,4.25).index,1);assert.equal(locate(p,40.5).index,7);assert.ok(Math.abs(locate(p,40.5).local-5.65)<1e-9);
 assert.equal(clipStart(p,4),18.45);
});
test('duration edits shift following scenes and retain a continuous timeline',()=>{
 const p=clone(original);p.clips[0].duration+=1.5;validate(p);assert.equal(duration(p),42);assert.equal(clipStart(p,1),5.75);assert.equal(locate(p,5).index,0);assert.equal(locate(p,5.75).index,1);
});
test('unsafe media, broken references and malformed numeric edits are rejected',()=>{
 for(const mutate of [p=>p.audio.src='https://example.com/audio.mp3',p=>p.assets.paycheck.src='videos/001-100k-salary/../../secret.png',p=>p.clips[0].duration=-1,p=>p.clips[0].layers[0].asset='missing',p=>p.clips[0].layers[0].x=NaN,p=>p.clips[0].layers[1].fill='url(javascript:bad)',p=>p.clips[1].id=p.clips[0].id]){const p=clone(original);mutate(p);assert.throws(()=>validate(p));}
 assert.equal(safeSource('data:audio/mpeg;base64,AAAA','audio'),true);assert.equal(safeSource('javascript:alert(1)'),false);
});
test('entrance animations hide layers until their cue and finish at the editable position',()=>{
 const l=original.clips[0].layers.find(l=>l.id==='job');assert.equal(layerBox(l,l.enter-.01).alpha,0);assert.equal(layerBox(l,l.enter+.6).alpha,1);assert.equal(layerBox(l,l.enter+.6).x,l.x);
 const p=original.clips[1].layers.find(l=>l.id==='salary');assert.ok(layerBox(p,p.enter+.15).w<p.w);assert.equal(layerBox(p,p.enter+1).w,p.w);
});
test('all captions are within the selected audio excerpt and scene IDs are unique',()=>{
 assert.equal(new Set(original.clips.map(c=>c.id)).size,8);assert.ok(original.captions.every(c=>c.start>=0&&c.end<=40.5));assert.equal(original.captions.at(-1).text,'Because the answer starts before you buy a single thing.');
});
