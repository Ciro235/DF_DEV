import { test } from 'node:test';
import assert from 'node:assert/strict';
import { onRequestPost, onRequestGet } from '../functions/api/contact.js';
const origin='https://readytoprod.pages.dev';
const valid={service:'web',email:'test@example.org',name:'Test',message:'A test inquiry with enough detail.',website:'',turnstileToken:'test'};
const configured={LEGAL_REVIEWED:'true',RESEND_API_KEY:'test-only',CONTACT_FROM:'Test <test@example.org>',TURNSTILE_SECRET:'test-only'};
const request=(data,headers={})=>new Request(origin+'/api/contact',{method:'POST',headers:{Origin:origin,'Content-Type':'application/json','Idempotency-Key':'00000000-0000-4000-8000-000000000000',...headers},body:typeof data==='string'?data:JSON.stringify(data)});
test('mock default refuses real collection',async()=>assert.equal((await onRequestPost({request:request(valid),env:{}})).status,503));
test('wrong origin is rejected',async()=>assert.equal((await onRequestPost({request:request(valid,{Origin:'https://example.org'}),env:configured})).status,403));
test('invalid email is rejected',async()=>assert.equal((await onRequestPost({request:request({...valid,email:'bad'}),env:configured})).status,422));
test('honeypot is rejected without pretending success',async()=>assert.equal((await onRequestPost({request:request({...valid,website:'spam'}),env:configured})).status,422));
test('invalid JSON is rejected',async()=>assert.equal((await onRequestPost({request:request('{broken'),env:configured})).status,400));
test('oversized payload is rejected',async()=>assert.equal((await onRequestPost({request:request('x'.repeat(9000)),env:configured})).status,413));
test('GET cannot send',()=>assert.equal(onRequestGet().status,405));
test('verified provider acceptance is necessary for success',async()=>{
  const old=globalThis.fetch;let calls=[];
  globalThis.fetch=async(url,init)=>{
    calls.push({url,init});
    return url.includes('siteverify')?Response.json({success:true,hostname:'readytoprod.pages.dev'}):Response.json({id:'test-only'});
  };
  try{
    assert.equal((await onRequestPost({request:request(valid),env:configured})).status,200);
    assert.equal(calls.length,2);
    assert.equal(calls[1].init.headers['Idempotency-Key'],'00000000-0000-4000-8000-000000000000');
    const body=JSON.parse(calls[1].init.body);
    assert.equal(body.reply_to,'test@example.org');
    assert.equal(body.to.length,2);
  }finally{globalThis.fetch=old;}
});
test('provider error cannot produce false success',async()=>{
  const old=globalThis.fetch;
  globalThis.fetch=async url=>url.includes('siteverify')?Response.json({success:true,hostname:'readytoprod.pages.dev'}):new Response('',{status:503});
  try{assert.equal((await onRequestPost({request:request(valid),env:configured})).status,502);}
  finally{globalThis.fetch=old;}
});
test('failed challenge never calls email provider',async()=>{
  const old=globalThis.fetch;let calls=0;
  globalThis.fetch=async()=>{calls++;return Response.json({success:false});};
  try{assert.equal((await onRequestPost({request:request(valid),env:configured})).status,422);assert.equal(calls,1);}
  finally{globalThis.fetch=old;}
});
