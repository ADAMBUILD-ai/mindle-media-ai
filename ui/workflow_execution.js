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
    const modelIntent=/밝기|밝게|대비|채도|자막|STT|받아쓰|나레이션|내레이션|narration|tts|순차|순서대로|실행 계획/i.test(text);
    const manualIntent=/추적|tracking|숏폼|속도|자르|전환|효과|오디오|배경음악|잔잔|자동.*편집|하이라이트/i.test(text);
    if(!steps && !modelIntent && manualIntent)return false;
    const input=detail.input_job_id||editor.querySelector('[data-preview]').dataset.jobId;
    if(!input){show('먼저 실제 원본 영상을 불러오세요.',true);return true;}
    window.mindleBeginEdit('video');let ownsPending=true;
    try{
      const planResponse=await fetch('/api/workflows/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command:detail.command,...(steps?{steps}:{})})});const plan=await planResponse.json();if(!planResponse.ok)throw new Error(plan.error||'계획 생성 실패');
      show('실행 계획 · '+(plan.plan_source==='LOCAL_GENERATIVE_INFERENCE'?'로컬 생성형 계획 · '+(plan.model_id||'모델 정보 없음'):'사용자 지정 단계 · 생성형 추론 아님')+' · '+plan.steps.map(s=>({'video_edit':'영상 편집','transcribe':'한국어 받아쓰기','apply_subtitles':'자막 적용','narrate':'나레이션 생성','mix_narration':'나레이션 합성'}[s.operation])).join(' → '));
      let background=null;const bgm=editor.querySelector('[data-bgm-input]').files[0];
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
      show('순차 작업·저장 완료 · '+task.workflow_id+' · MP4는 프로젝트 내보내기에 포함됩니다.');
    }catch(error){show(error.message,true);}finally{if(ownsPending)window.mindleEndEdit('video');}
    return true;
  };
  document.addEventListener('DOMContentLoaded',async()=>{
    window.mindleBeginEdit('video');let ownsReconnect=true;
    try{
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
  const {workflows}=await response.json();const dialog=document.createElement('dialog');const title=document.createElement('h2');title.textContent='순차 작업 이력';dialog.append(title);
  for(const task of workflows){const row=document.createElement('div');const text=document.createElement('p');text.textContent=`${task.workflow_id} · ${task.state} · ${task.attempts.length}회 시도 · ${task.error||''}`;row.append(text);
    if(['QUEUED','RUNNING','RETRY_WAIT','CANCEL_REQUESTED'].includes(task.state)){const cancel=document.createElement('button');cancel.textContent='작업 취소';cancel.addEventListener('click',async()=>{const r=await fetch('/api/workflows/'+task.workflow_id+'/cancel',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});const value=await r.json();text.textContent=task.workflow_id+' · '+value.state;cancel.disabled=r.ok;});row.append(cancel);}
    if(task.state==='SUCCEEDED'){const reopen=document.createElement('button');reopen.textContent='완료 프로젝트 열기';reopen.addEventListener('click',async()=>{if(await window.mindleOpenProject(task.project_id))dialog.close();});row.append(reopen);}
    dialog.append(row);}
  const close=document.createElement('button');close.textContent='닫기';close.addEventListener('click',()=>dialog.close());dialog.append(close);dialog.addEventListener('close',()=>dialog.remove());document.body.append(dialog);dialog.showModal();
};
