/* Workflow controls live inside the existing command/status region. */
(() => {
  const video=document.querySelector('[data-editor="video"]');
  const show=(text,error=false)=>{const node=video.querySelector('[data-command-error]');node.replaceChildren(document.createTextNode(text));node.style.display='block';node.dataset.result=error?'error':'ok';return node;};
  window.mindleShowNarrations=records=>{
    video.querySelector('[data-narration-results]')?.remove();
    const voices=records.filter(r=>r.operation==='narration');if(!voices.length)return;
    const host=document.createElement('div');host.dataset.narrationResults='';
    for(const record of voices){const row=document.createElement('div');const label=document.createElement('span');label.textContent='나레이션 · '+record.runtime_result.text;
      const audio=document.createElement('audio');audio.controls=true;audio.preload='metadata';
      // Reopen supplies the server-generated, contained preview URL.
      if(record.preview_url)audio.src=record.preview_url;
      const remove=document.createElement('button');remove.type='button';remove.textContent='음성 원본 목록에서 제외';remove.addEventListener('click',()=>{if(window.mindleEditPending('video'))return;if(!window.mindleRemoveNarration?.(record.job_id))return;row.remove();show('음성 원본을 목록에서 제외했습니다. 이미 합성된 영상의 소리는 원본 영상에서 다시 합성해야 변경됩니다.');});
      const volumeLabel=document.createElement('label');volumeLabel.textContent='합성할 나레이션 음량 ';const volume=document.createElement('input');volume.type='number';volume.min=0;volume.max=2;volume.step=.1;volume.value=1;volume.dataset.narrationVolume=record.job_id;volumeLabel.append(volume);
      const length=document.createElement('select');for(const [value,text] of [['reject','원본 길이 유지 · 음성 초과 시 중단'],['extend_video','음성 길이만큼 마지막 영상 연장']]){const option=document.createElement('option');option.value=value;option.textContent=text;length.append(option);}
      const remix=document.createElement('button');remix.type='button';remix.textContent='원본에서 이 음성으로 다시 합성';remix.dataset.narrationRemix=record.job_id;
      remix.addEventListener('click',()=>{if(window.mindleEditPending('video'))return;video.dispatchEvent(new CustomEvent('mindle:command',{detail:{command:'나레이션 다시 합성',input_job_id:record.runtime_result.base_video_job_id,steps:[{operation:'mix_narration',voice_job_id:record.job_id,volume:Number(volume.value),original_volume:1,length_policy:length.value}]}}));});
      row.append(label,audio,volumeLabel,length,remix,remove);host.append(row);}
    video.querySelector('[data-command-panel]').append(host);
  };
  window.mindleWorkflowCommand=async(editor,kind,detail)=>{
    if(kind!=='video')return false;
    let steps=detail.steps;
    if(!steps && /^계획 JSON\s*:/i.test(detail.command)){try{steps=JSON.parse(detail.command.replace(/^계획 JSON\s*:/i,'')).steps;}catch(_){show('실행 계획 JSON을 확인하세요.',true);return true;}}
    // Explicit toolbar actions retain their deterministic processing. Free-form
    // supported requests and unknown requests reach the model, never a silent
    // keyword fallback that executes only part of the user's instruction.
    const text=detail.command.trim();
    const architectureIntent=/건축.*(?:홍보|소개|영상)|(?:홍보|소개).*건축|장면.*(?:조립|구성)|클립.*(?:이어|조립|구성)/i.test(text);
    if(!steps && architectureIntent){
      window.mindleBeginEdit('video');let ownsPending=true;
      try{
        const context=await window.mindleWorkflowContext();
        if(!context.job_ids?.length)throw new Error('먼저 실제 영상 자료를 불러오고 저장하세요.');
        const planResponse=await fetch('/api/architecture-agent/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command:text,project_id:context.project_id,job_ids:context.job_ids})});
        const plan=await planResponse.json();if(!planResponse.ok)throw new Error(plan.error||'건축 영상 계획 생성 실패');
        show('건축 AI 계획 · '+(plan.model_id||'로컬 모델')+' · 실제 프레임 측정 기반 · '+plan.aspect+' · '+plan.scenes.map(s=>s.source_id+' '+s.start_seconds+'초부터 '+s.duration_seconds+'초').join(' → ')+' · 합계 '+plan.total_duration_seconds+'초');
        const response=await fetch('/api/architecture-agent/productions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({request_id:crypto.randomUUID(),plan_id:plan.plan_id})});
        let task=await response.json();if(!response.ok)throw new Error(task.error||'건축 영상 작업 등록 실패');
        while(!['SUCCEEDED','FAILED','CANCELLED','INTERRUPTED','BLOCKED_INPUT','BLOCKED_ASSET'].includes(task.state)){
          const node=show('건축 영상 AI · '+task.state+' · '+task.production_id);const cancel=document.createElement('button');cancel.type='button';cancel.textContent='작업 취소';
          cancel.addEventListener('click',async()=>{cancel.disabled=true;await fetch('/api/architecture-agent/productions/'+task.production_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});});node.append(cancel);
          await new Promise(r=>setTimeout(r,350));const status=await fetch('/api/architecture-agent/productions/'+task.production_id);if(!status.ok)throw new Error('건축 영상 작업 상태를 읽을 수 없습니다.');task=await status.json();
        }
        if(task.state!=='SUCCEEDED')throw new Error(task.state+' · '+(task.error||task.missing?.join(', ')||'기존 결과는 보존했습니다.'));
        const needsAudioFinish=/나레이션|내레이션|narration|tts|배경\s*음악|bgm/i.test(text);
        if(needsAudioFinish){
          const finishPlanResponse=await fetch('/api/workflows/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command:text})});
          const finishPlan=await finishPlanResponse.json();if(!finishPlanResponse.ok)throw new Error(finishPlan.error||'건축 영상 음성 계획 생성 실패');
          let background=null;const bgm=video.querySelector('[data-bgm-input]').files[0];
          if(finishPlan.steps.some(step=>Object.hasOwn(step.options||{},'backgroundVolume')||Object.hasOwn(step,'background_volume'))&&!bgm)throw new Error('건축 영상에 BGM을 넣으려면 우측 배경음악 버튼에서 오디오 파일을 먼저 선택하세요.');
          if(bgm)background={filename:bgm.name,content_base64:await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onerror=reject;reader.onload=()=>resolve(String(reader.result).split(',')[1]);reader.readAsDataURL(bgm);})};
          const context=await window.mindleWorkflowContext();
          const finishResponse=await fetch('/api/workflows',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({request_id:crypto.randomUUID(),plan_id:finishPlan.plan_id,input_job_id:task.receipt.job_id,project_id:task.receipt.project_id,job_ids:[...new Set([...(context.job_ids||[]),task.receipt.job_id])],workspace:context.workspace,steps:finishPlan.steps.map(({step_id,...step})=>step),background,export:true})});
          let finish=await finishResponse.json();if(!finishResponse.ok)throw new Error(finish.error||'건축 영상 음성 작업 등록 실패');
          while(!['SUCCEEDED','FAILED','CANCELLED','INTERRUPTED'].includes(finish.state)){
            const node=show(`건축 AI 음성·BGM 마감 · ${finish.state} · 단계 ${finish.current_step+1}/${finish.steps.length}`);const cancel=document.createElement('button');cancel.type='button';cancel.textContent='작업 취소';cancel.addEventListener('click',()=>fetch('/api/workflows/'+finish.workflow_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}));node.append(cancel);
            await new Promise(r=>setTimeout(r,350));const status=await fetch('/api/workflows/'+finish.workflow_id);if(!status.ok)throw new Error('건축 영상 음성 작업 상태를 읽을 수 없습니다.');finish=await status.json();
          }
          if(finish.state!=='SUCCEEDED')throw new Error(finish.state+' · '+(finish.error||'건축 영상 MP4는 보존했습니다.'));
          task={...task,receipt:{...task.receipt,project_id:finish.project_id},finish_workflow_id:finish.workflow_id};
        }
        window.mindleEndEdit('video');ownsPending=false;
        if(!await window.mindleWorkflowRestore(task.receipt.project_id))throw new Error('건축 영상은 완료됐지만 프로젝트를 다시 열지 못했습니다.');
        await window.mindleRefreshAiCore?.();
        show('건축 AI 장면 계획·MP4 조립'+(task.finish_workflow_id?'·신경망 나레이션·BGM 합성':'')+'·프로젝트 저장 완료 · '+task.production_id);
      }catch(error){show(error.message,true);}finally{if(ownsPending)window.mindleEndEdit('video');}
      return true;
    }
    const modelIntent=/밝기|밝게|대비|채도|자막|STT|받아쓰|나레이션|내레이션|narration|tts|속도|배속|자르|구간|trim|페이드|fade|배경\s*음악|bgm|9\s*:\s*16|16\s*:\s*9|순차|순서대로|실행 계획/i.test(text);
    const manualIntent=/추적|tracking|숏폼|속도|자르|전환|효과|오디오|배경음악|잔잔|자동.*편집|하이라이트/i.test(text);
    if(!steps && !modelIntent && manualIntent)return false;
    const input=detail.input_job_id||editor.querySelector('[data-preview]').dataset.jobId;
    if(!input){show('먼저 실제 원본 영상을 불러오세요.',true);return true;}
    window.mindleBeginEdit('video');let ownsPending=true;
    try{
      const planResponse=await fetch('/api/workflows/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command:detail.command,...(steps?{steps}:{})})});const plan=await planResponse.json();if(!planResponse.ok)throw new Error(plan.error||'계획 생성 실패');
      const labels={brightness:'밝기',contrast:'대비',saturation:'채도',speed:'속도',start:'시작',duration:'길이',aspect:'비율',fade:'페이드',backgroundVolume:'BGM 음량',volume:'나레이션 음량',original_volume:'원본 음량',length_policy:'영상 길이'};
      const applied=Object.entries(plan.validated_edit_values||{}).map(([key,value])=>{let shown=value;if(['brightness','contrast','saturation'].includes(key))shown=(value>=0?'+':'')+value+' 포인트';else if(key==='speed')shown=value+'배';else if(['start','duration'].includes(key))shown=value+'초';else if(['backgroundVolume','volume','original_volume'].includes(key))shown=Math.round(value*100)+'%';else if(key==='fade')shown=value?'적용':'미적용';else if(key==='length_policy')shown=value==='extend_video'?'음성에 맞춰 연장':'원본 유지';return (labels[key]||key)+' '+shown;}).join(' · ');
      show('실행 계획 · '+(plan.plan_source==='LOCAL_GENERATIVE_INFERENCE'?'로컬 생성형 계획 · '+(plan.model_id||'모델 정보 없음'):'사용자 지정 단계 · 생성형 추론 아님')+' · '+plan.steps.map(s=>({'video_edit':'영상 편집','transcribe':'한국어 받아쓰기','apply_subtitles':'자막 적용','narrate':'나레이션 생성','mix_narration':'나레이션 합성'}[s.operation])).join(' → ')+(applied?' · 검증된 적용값: '+applied:''));
      let background=null;const bgm=editor.querySelector('[data-bgm-input]').files[0];
      if(plan.steps.some(step=>Object.hasOwn(step.options||{},'backgroundVolume')||Object.hasOwn(step,'background_volume'))&&!bgm)throw new Error('BGM 작업을 실행하려면 우측 배경음악 버튼에서 오디오 파일을 먼저 선택하세요.');
      if(bgm){background={filename:bgm.name,content_base64:await new Promise((resolve,reject)=>{const reader=new FileReader();reader.onerror=reject;reader.onload=()=>resolve(String(reader.result).split(',')[1]);reader.readAsDataURL(bgm);})};}
      const response=await fetch('/api/workflows',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({request_id:crypto.randomUUID(),plan_id:plan.plan_id,input_job_id:input,...await window.mindleWorkflowContext(),steps:plan.steps.map(({step_id,...step})=>step),background,export:true})});let task=await response.json();if(!response.ok)throw new Error(task.error||'작업 요청 실패');
      while(!['SUCCEEDED','FAILED','CANCELLED','INTERRUPTED'].includes(task.state)){
        const node=show(`작업 ${task.workflow_id} · ${task.state} · 단계 ${task.current_step+1}/${task.steps.length} · 시도 ${task.attempts.length}`);
        const cancel=document.createElement('button');cancel.type='button';cancel.textContent='작업 취소';cancel.addEventListener('click',async()=>{cancel.disabled=true;try{const r=await fetch('/api/workflows/'+task.workflow_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});if(!r.ok)throw new Error('취소 요청 실패');}catch(error){show(error.message,true);cancel.disabled=false;}});node.append(cancel);
        await new Promise(r=>setTimeout(r,350));const status=await fetch('/api/workflows/'+task.workflow_id);if(!status.ok)throw new Error('작업 상태를 읽을 수 없습니다. 서버 작업 이력에서 확인하세요.');task=await status.json();
      }
      if(task.state!=='SUCCEEDED')throw new Error(task.state+' · '+(task.error||'기존 프로젝트는 보존했습니다.'));
      window.mindleEndEdit('video');ownsPending=false;
      if(!await window.mindleWorkflowRestore(task.project_id))throw new Error('작업은 완료됐지만 프로젝트 다시 열기에 실패했습니다. 작업 이력을 확인하세요.');
      await window.mindleRefreshAiCore?.();
      show('순차 작업·저장 완료 · '+task.workflow_id+' · MP4는 프로젝트 내보내기에 포함됩니다.');
    }catch(error){show(error.message,true);}finally{if(ownsPending)window.mindleEndEdit('video');}
    return true;
  };
  document.addEventListener('DOMContentLoaded',async()=>{
    window.mindleBeginEdit('video');let ownsReconnect=true;
    try{
      const architectureResponse=await fetch('/api/architecture-agent/productions');
      if(architectureResponse.ok){const {productions}=await architectureResponse.json();let production=productions.find(t=>['QUEUED','RUNNING','CANCEL_REQUESTED'].includes(t.state));
        if(production){while(!['SUCCEEDED','FAILED','CANCELLED','INTERRUPTED','BLOCKED_INPUT','BLOCKED_ASSET'].includes(production.state)){
          const node=show('건축 AI 작업 다시 연결 · '+production.production_id+' · '+production.state);const cancel=document.createElement('button');cancel.textContent='작업 취소';cancel.addEventListener('click',()=>fetch('/api/architecture-agent/productions/'+production.production_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}));node.append(cancel);
          await new Promise(r=>setTimeout(r,350));const status=await fetch('/api/architecture-agent/productions/'+production.production_id);if(!status.ok)throw new Error('건축 AI 작업 연결이 끊겼습니다.');production=await status.json();}
          window.mindleEndEdit('video');ownsReconnect=false;
          if(production.state==='SUCCEEDED'){if(!await window.mindleWorkflowRestore(production.receipt.project_id))throw new Error('완료된 건축 AI 프로젝트를 다시 열지 못했습니다.');show('건축 AI 작업 복원 완료 · '+production.production_id);}
          else show(production.state+' · '+(production.error||production.missing?.join(', ')||'기존 결과를 보존했습니다.'),true);
          return;
        }}
      const response=await fetch('/api/workflows');if(!response.ok)throw new Error('저장된 작업 이력을 읽을 수 없습니다.');
      const {workflows}=await response.json();let task=workflows.find(t=>['QUEUED','RUNNING','RETRY_WAIT','CANCEL_REQUESTED'].includes(t.state));
      if(!task)return;
      while(!['SUCCEEDED','FAILED','CANCELLED','INTERRUPTED'].includes(task.state)){
        const node=show('이전 작업 연결 · '+task.workflow_id+' · '+task.state);const cancel=document.createElement('button');cancel.textContent='작업 취소';cancel.addEventListener('click',()=>fetch('/api/workflows/'+task.workflow_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'}));node.append(cancel);
        await new Promise(r=>setTimeout(r,350));const status=await fetch('/api/workflows/'+task.workflow_id);if(!status.ok)throw new Error('작업 연결이 끊겼습니다. 작업 이력에서 확인하세요.');task=await status.json();
      }
      window.mindleEndEdit('video');ownsReconnect=false;
      if(task.state==='SUCCEEDED'){if(!await window.mindleWorkflowRestore(task.project_id))throw new Error('완료 프로젝트를 다시 열지 못했습니다.');show('이전 작업 복원 완료 · '+task.workflow_id);}
      else show(task.state+' · '+(task.error||'기존 저장 결과를 보존했습니다.'),true);
    }catch(error){show(error.message,true);}finally{if(ownsReconnect)window.mindleEndEdit('video');}
  });
})();
// The existing history action also exposes durable attempts after a browser/server restart.
window.mindleOpenWorkflowHistory=async()=>{
  const response=await fetch('/api/workflows');if(!response.ok)throw new Error('순차 작업 이력을 읽을 수 없습니다.');
  const {workflows}=await response.json();let productions=[];const architectureResponse=await fetch('/api/architecture-agent/productions');
  if(architectureResponse.ok)({productions=[]}=await architectureResponse.json());
  const dialog=document.createElement('dialog');const title=document.createElement('h2');title.textContent='AI 작업 이력';dialog.append(title);
  if(productions.length){const architectureTitle=document.createElement('h3');architectureTitle.textContent='건축 AI 영상';dialog.append(architectureTitle);}
  for(const task of productions){const row=document.createElement('div');const text=document.createElement('p');const planner=task.planner_receipt||{};const ranges=(planner.scenes||[]).map(scene=>scene.start_seconds+'초→'+scene.duration_seconds+'초').join(', ');
    text.textContent=`${task.production_id} · ${task.state} · ${planner.model_id||'모델 정보 없음'} · ${ranges||'측정 구간 없음'} · ${task.error||''}`;row.append(text);
    if(['QUEUED','RUNNING','CANCEL_REQUESTED'].includes(task.state)){const cancel=document.createElement('button');cancel.textContent='작업 취소';cancel.addEventListener('click',async()=>{const r=await fetch('/api/architecture-agent/productions/'+task.production_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});const value=await r.json();text.textContent=task.production_id+' · '+value.state;cancel.disabled=r.ok;});row.append(cancel);}
    if(task.state==='SUCCEEDED'&&task.receipt?.project_id){const reopen=document.createElement('button');reopen.textContent='완료 프로젝트 열기';reopen.addEventListener('click',async()=>{if(await window.mindleOpenProject(task.receipt.project_id))dialog.close();});row.append(reopen);}
    dialog.append(row);}
  if(workflows.length){const workflowTitle=document.createElement('h3');workflowTitle.textContent='편집·자막·나레이션';dialog.append(workflowTitle);}
  for(const task of workflows){const row=document.createElement('div');const text=document.createElement('p');text.textContent=`${task.workflow_id} · ${task.state} · ${task.attempts.length}회 시도 · ${task.error||''}`;row.append(text);
    if(['QUEUED','RUNNING','RETRY_WAIT','CANCEL_REQUESTED'].includes(task.state)){const cancel=document.createElement('button');cancel.textContent='작업 취소';cancel.addEventListener('click',async()=>{const r=await fetch('/api/workflows/'+task.workflow_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});const value=await r.json();text.textContent=task.workflow_id+' · '+value.state;cancel.disabled=r.ok;});row.append(cancel);}
    if(task.state==='SUCCEEDED'){const reopen=document.createElement('button');reopen.textContent='완료 프로젝트 열기';reopen.addEventListener('click',async()=>{if(await window.mindleOpenProject(task.project_id))dialog.close();});row.append(reopen);}
    dialog.append(row);}
  const close=document.createElement('button');close.textContent='닫기';close.addEventListener('click',()=>dialog.close());dialog.append(close);dialog.addEventListener('close',()=>dialog.remove());document.body.append(dialog);dialog.showModal();
};
