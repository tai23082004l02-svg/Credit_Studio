import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {validateStorage,initStorage,mediaURL} from '../assets/js/media-storage.js';
const fixture=JSON.parse(fs.readFileSync(new URL('../storage/manifest.json',import.meta.url)));fixture.enabled=true;
fixture.assets['videos/test/pinned.png']={...Object.values(fixture.assets)[0],local:true};
test('media manifest permits only registered public HTTPS media, never credentials or traversal',()=>{
 assert.equal(validateStorage(fixture),fixture);
 for(const publicBaseURL of ['http://media.example/','https://user:pass@media.example/','https://media.example/?token=x','https://media.example/path'])assert.throws(()=>validateStorage({...fixture,publicBaseURL}));
 const sample=Object.values(fixture.assets)[0];assert.throws(()=>validateStorage({...fixture,assets:{'../private.env':sample}}));assert.throws(()=>validateStorage({...fixture,assets:{'videos/a/../../private.env':sample}}));assert.throws(()=>validateStorage({...fixture,assets:{'videos/a/a.png':{...sample,key:'../private'}}}));
 assert.throws(()=>validateStorage({...fixture,assets:{'videos/a/a.png':{...sample,local:'yes'}}}));
});
test('logical paths map to content-addressed media; project JSON, inline media and other origins stay unchanged',async()=>{
 const saved=globalThis.fetch;globalThis.fetch=async()=>({ok:true,json:async()=>fixture});try{await initStorage();}finally{globalThis.fetch=saved;}
 const base=new URL('../',import.meta.url);const logical=Object.keys(fixture.assets)[0];assert.equal(mediaURL(logical,base),fixture.publicBaseURL+fixture.assets[logical].key);
 assert.equal(mediaURL('videos/test/pinned.png',base),new URL('videos/test/pinned.png',base).href,'a retained GitHub asset stays local even with R2 enabled');
 assert.equal(mediaURL('projects.json',base),new URL('projects.json',base).href);assert.equal(mediaURL('data:image/png;base64,AAAA',base),'data:image/png;base64,AAAA');assert.equal(mediaURL('https://other.example/asset.png',base),'https://other.example/asset.png');
});
