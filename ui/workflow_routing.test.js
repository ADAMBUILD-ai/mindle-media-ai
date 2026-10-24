const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
function setup(){
 const status={style:{},dataset:{},replaceChildren(){}};
 const editor={querySelector:()=>status};const calls=[];
 const document={querySelector:()=>editor,createTextNode:x=>x,addEventListener(){}};
 const window={mindleBeginEdit(){},mindleEndEdit(){}};
 vm.runInNewContext(fs.readFileSync(__dirname+'/workflow_execution.js','utf8'),{window,document,fetch:async(url,opts)=>{calls.push({url,body:JSON.parse(opts.body)});return {ok:false,json:async()=>({error:'fixture boundary: inference not executed'})};}});
 return {window,calls,editor:{querySelector:()=>({dataset:{jobId:'imported-video'}})}};
}
for(const command of ['대비를 13 높여 줘','밝기를 7 낮추고 자막을 넣어줘','"안녕하세요" 나레이션 추가','내레이션을 넣어 줘','할 수 없는 요청을 정직하게 거절해 줘']){
 test(command+' reaches plan API without injected steps',async()=>{const s=setup();assert.equal(await s.window.mindleWorkflowCommand(s.editor,'video',{command}),true);assert.equal(s.calls[0].url,'/api/workflows/plan');assert.equal('steps' in s.calls[0].body,false);});
}
test('manual scene analysis and tracking stay in existing path',async()=>{for(const command of ['자동 편집','객체 추적','속도 2배']){const s=setup();assert.equal(await s.window.mindleWorkflowCommand(s.editor,'video',{command}),false);assert.equal(s.calls.length,0);}});
test('PHOTO does not silently enter VIDEO model plan',async()=>{const s=setup();assert.equal(await s.window.mindleWorkflowCommand(s.editor,'photo',{command:'사진 분할'}),false);assert.equal(s.calls.length,0);});
test('architecture promotion uses the bound architecture agent instead of fixed edit routing',async()=>{
 const status={style:{},dataset:{},replaceChildren(){}};const editor={querySelector:()=>status};const calls=[];
 const document={querySelector:()=>editor,createTextNode:x=>x,addEventListener(){}};
 const window={mindleBeginEdit(){},mindleEndEdit(){},mindleWorkflowContext:async()=>({project_id:'project',job_ids:['video-1','video-2']})};
 const fetch=async(url,opts)=>{calls.push({url,body:JSON.parse(opts.body)});return {ok:false,json:async()=>({error:'fixture: model not executed'})};};
 vm.runInNewContext(fs.readFileSync(__dirname+'/workflow_execution.js','utf8'),{window,document,fetch,crypto:{randomUUID:()=> 'request'}});
 assert.equal(await window.mindleWorkflowCommand(editor,'video',{command:'두 장면으로 16:9 건축 홍보 영상을 구성해 줘'}),true);
 assert.equal(calls[0].url,'/api/architecture-agent/plan');assert.deepEqual(calls[0].body.job_ids,['video-1','video-2']);
});
test('verified values and model provenance are shown before queue submission',async()=>{
 const messages=[],status={style:{},dataset:{},replaceChildren(text){messages.push(text);}};
 const editor={querySelector:selector=>selector==='[data-bgm-input]'?{files:[]}:selector==='[data-preview]'?{dataset:{jobId:'video'}}:status};
 const document={querySelector:()=>editor,createTextNode:x=>x,addEventListener(){}};
 const window={mindleBeginEdit(){},mindleEndEdit(){},mindleWorkflowContext:async()=>({})};
 let submitted=false;
 const fetch=async url=>{
  if(url==='/api/workflows/plan')return {ok:true,json:async()=>({plan_source:'LOCAL_GENERATIVE_INFERENCE',model_id:'fixture-model',plan_id:'fixture-plan',steps:[{operation:'video_edit',options:{brightness:-3}}],validated_edit_values:{brightness:-3}})};
  assert.ok(messages.some(x=>x.includes('fixture-model')&&x.includes('밝기 -3 포인트')));
  submitted=true;return {ok:false,json:async()=>({error:'fixture: stop before execution'})};
 };
 vm.runInNewContext(fs.readFileSync(__dirname+'/workflow_execution.js','utf8'),{window,document,fetch,crypto:{randomUUID:()=> 'fixture-request'}});
 await window.mindleWorkflowCommand(editor,'video',{command:'밝기 3 낮춰 줘'});
 assert.equal(submitted,true);
});
test('browser refresh reconnects the same architecture production and restores its project',async()=>{
 const messages=[],listeners={},status={style:{},dataset:{},replaceChildren(value){messages.push(value);},append(){}};
 const editor={querySelector:()=>status};
 const document={querySelector:()=>editor,createTextNode:x=>x,createElement:()=>({addEventListener(){},append(){}}),addEventListener:(name,callback)=>{listeners[name]=callback;}};
 const edits=[];let restored=null;
 const window={mindleBeginEdit:kind=>edits.push('begin:'+kind),mindleEndEdit:kind=>edits.push('end:'+kind),mindleWorkflowRestore:async project=>{restored=project;return true;}};
 const calls=[];const fetch=async(url,opts)=>{calls.push({url,method:opts?.method||'GET'});
  if(url==='/api/architecture-agent/productions')return {ok:true,json:async()=>({productions:[{production_id:'production-1',state:'RUNNING'}]})};
  if(url==='/api/architecture-agent/productions/production-1')return {ok:true,json:async()=>({production_id:'production-1',state:'SUCCEEDED',receipt:{project_id:'project-1'}})};
  throw new Error('unexpected '+url);
 };
 vm.runInNewContext(fs.readFileSync(__dirname+'/workflow_execution.js','utf8'),{window,document,fetch,setTimeout:callback=>callback(),crypto:{randomUUID:()=> 'request'}});
 await listeners.DOMContentLoaded();
 assert.equal(restored,'project-1');
 assert.deepEqual(calls.map(x=>x.url),['/api/architecture-agent/productions','/api/architecture-agent/productions/production-1']);
 assert.equal(calls.some(x=>x.method==='POST'),false);
 assert.ok(messages.some(x=>String(x).includes('건축 AI 작업 복원 완료')));
 assert.deepEqual(edits,['begin:video','end:video']);
});
test('AI history exposes a completed architecture production without creating new work',async()=>{
 const listeners={};const created=[];const makeElement=tag=>{const node={tag,children:[],listeners:{},append(...items){this.children.push(...items);},addEventListener(name,callback){this.listeners[name]=callback;},showModal(){this.open=true;},close(){this.open=false;this.listeners.close?.();},remove(){this.removed=true;}};created.push(node);return node;};
 const status={style:{},dataset:{},replaceChildren(){}};const document={querySelector:()=>({querySelector:()=>status}),createTextNode:x=>x,createElement:makeElement,addEventListener:(name,callback)=>{listeners[name]=callback;},body:{append(){}}};
 let opened=null;const window={mindleBeginEdit(){},mindleEndEdit(){},mindleOpenProject:async project=>{opened=project;return true;}};const calls=[];
 const fetch=async(url,opts)=>{calls.push({url,method:opts?.method||'GET'});
  if(url==='/api/workflows')return {ok:true,json:async()=>({workflows:[]})};
  if(url==='/api/architecture-agent/productions')return {ok:true,json:async()=>({productions:[{production_id:'production-2',state:'SUCCEEDED',planner_receipt:{model_id:'qwen-fixture',scenes:[{start_seconds:.5,duration_seconds:1}]},receipt:{project_id:'project-2'}}]})};
  throw new Error('unexpected '+url);
 };
 vm.runInNewContext(fs.readFileSync(__dirname+'/workflow_execution.js','utf8'),{window,document,fetch,crypto:{randomUUID:()=> 'request'}});
 await window.mindleOpenWorkflowHistory();
 const reopen=created.find(node=>node.tag==='button'&&node.textContent==='완료 프로젝트 열기');assert.ok(reopen);await reopen.listeners.click();
 assert.equal(opened,'project-2');assert.equal(calls.some(call=>call.method==='POST'),false);
 assert.ok(created.some(node=>node.tag==='p'&&node.textContent.includes('qwen-fixture')&&node.textContent.includes('0.5초→1초')));
});
