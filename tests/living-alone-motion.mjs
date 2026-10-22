import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {validate,duration,layerText,layerBox,animatedValue} from '../video/engine.js';
const folder=new URL('../videos/004-living-alone/',import.meta.url),p=JSON.parse(fs.readFileSync(new URL('review/project.json',folder))),shots=JSON.parse(fs.readFileSync(new URL('review/shot-plan.json',folder)));
const clip=(mode,section)=>p.clips[shots.findIndex(s=>s.layout===mode&&(!section||s.section===section))];
test('full Living Alone narration preserves uploaded WAV and original silent board',()=>{
 validate(p);assert.equal(p.clips.length,91);assert.equal(duration(p),577.5);
 assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL('audio/tts_20261022_133142_ba54ee.wav',folder))).digest('hex'),'10a7d8bbb78bcab9411979954c4409e9e8a70344bf527d3316258189c5c5194d');
 const old=JSON.parse(fs.readFileSync(new URL('storyboard/project.json',folder)));assert.equal(duration(old),96);assert.equal(old.audio.src,'');assert.equal(p.showCaptions,false);
});
test('per-person rent and internet counters agree with bars throughout all motion',()=>{
 for(let i=0;i<shots.length;i++)for(const j of [0,1]){
  const c=p.clips[i],value=c.layers.find(l=>l.id===`cost-value-${j}`),bar=c.layers.find(l=>l.id===`cost-meter-${j}`);if(!value)continue;
  const maxValue=Math.max(...c.layers.filter(l=>/^cost-value-/.test(l.id)).map(l=>l.animation.keys.at(-1).value));
  for(let t=0;t<c.duration;t+=.031)assert.ok(Math.abs(layerBox(bar,t).w/660*maxValue-animatedValue(value.animation,t))<1e-4);
 }
 for(const[mode,amounts]of[['rent-solo',[1800]],['rent-shared',[2400,1200]],['internet-split',[60,30]],['monthly-total',[1860,1230]]]){
  const c=clip(mode,2);for(const[j,amount]of amounts.entries())assert.equal(layerText(c.layers.find(l=>l.id===`cost-value-${j}`),120),'$'+amount.toLocaleString('en-US'));
 }
});
test('shared amounts wait for their narration cues and the monthly gap is scoped correctly',()=>{
 for(const mode of ['rent-shared','internet-split','monthly-total']){
  const c=clip(mode,2),card=c.layers.find(l=>l.id==='cost-card-1'),value=c.layers.find(l=>l.id==='cost-value-1');assert.ok(card.enter>1);assert.equal(layerBox(card,card.enter-.01).alpha,0);assert.equal(value.animation.keys[0].time,card.enter);
 }
 const c=clip('monthly-gap');assert.equal(layerText(c.layers.find(l=>l.id==='monthly-gap'),120),'$630');assert.match(JSON.stringify(c),/RENT \+ INTERNET/);assert.match(JSON.stringify(c),/not national averages/);
});
test('annual difference increments by exactly $630 for twelve synchronized months',()=>{
 const c=clip('annual-gap'),counter=c.layers.find(l=>l.id==='annual-gap');assert.equal(counter.animation.easing,'step');assert.deepEqual(counter.animation.keys.map(k=>k.value),Array.from({length:13},(_,i)=>630*i));
 for(let i=1;i<=12;i++){const t=counter.animation.keys[i].time,cell=c.layers.find(l=>l.id===`month-${i}`);assert.equal(cell.enter,Number(t.toFixed(4)));assert.equal(layerText(counter,t),'$'+(630*i).toLocaleString('en-US'));}
 assert.equal(layerText(counter,120),'$7,560');assert.ok(c.duration-counter.animation.keys.at(-1).time>=1.39);
});
test('two-month exposure is $3,720 for rent and internet only, not a complete reserve',()=>{
 const c=clip('two-months'),counter=c.layers.find(l=>l.id==='two-month-total');assert.deepEqual(counter.animation.keys.map(k=>k.value),[0,1860,3720]);assert.equal(layerText(counter,120),'$3,720');assert.match(JSON.stringify(c),/Rent \+ internet only; not a complete emergency-fund target/);
 assert.match(JSON.stringify(clip('excluded-costs')),/excludes these and other obligations/);
});
test('historical statistics keep their date, unit and household denominator',()=>{
 const rent=JSON.stringify(clip('rent-stat'));assert.match(rent,/\+4.3%/);assert.match(rent,/12 months ending December 2024/);assert.match(rent,/Bureau of Labor Statistics/);
 const households=clip('household-stat');assert.match(JSON.stringify(households),/38.5 MILLION/);assert.match(JSON.stringify(households),/2024/);assert.match(JSON.stringify(households),/HOUSEHOLDS — NOT PEOPLE/);assert.equal(layerText(households.layers.find(l=>l.id==='household-share'),120),'29%');
});
