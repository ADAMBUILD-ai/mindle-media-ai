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
