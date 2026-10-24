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
