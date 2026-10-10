/* Existing navigation exposes real saved projects, storage and job records. */
(() => {
  const display=(title,items,projects=false)=>{
    const dialog=document.createElement('dialog');
    const heading=document.createElement('h2');heading.textContent=title;dialog.append(heading);
    for(const item of items) {
      const row=document.createElement(projects?'button':'p');
      row.textContent=projects?`${item.project_id} · ${item.saved_at} · ${item.job_count} 작업`:item;
      if(projects) row.addEventListener('click',async()=>{await window.mindleOpenProject(item.project_id);dialog.close();});
      dialog.append(row);
    }
    if(projects) {const fresh=document.createElement('button');fresh.textContent='새 프로젝트';fresh.addEventListener('click',()=>{window.mindleNewProject();dialog.close();});dialog.append(fresh);}
    const close=document.createElement('button');close.textContent='닫기';close.addEventListener('click',()=>dialog.close());dialog.append(close);
    dialog.addEventListener('close',()=>dialog.remove());document.body.append(dialog);dialog.showModal();
  };
  document.querySelectorAll('[data-shell]').forEach(button=>button.addEventListener('click',async()=>{
    try {
      const key=button.dataset.shell;
      if(key==='home') {window.scrollTo({top:0,behavior:'smooth'});return;}
      if(key==='help') {display('MINDLE MEDIA AI 도움말',['원본 불러오기 → 편집 도구 / AI 지시 → 프로젝트 저장 → 내보내기','내보내기는 프로젝트와 모든 결과 파일을 ZIP으로 보관합니다.','배경 제거·4배 업스케일·추적·한국어 STT는 준비된 모델 Runtime을 사용합니다.','광고 숏폼 외부 연동은 현재 별도 검증 대기입니다.','미구현 기능은 비활성화돼 있습니다.']);return;}
      if(key==='history') {const r=await fetch('/api/evidence');if(!r.ok) throw new Error('작업 내역을 읽을 수 없습니다.');const data=await r.json();display('실제 작업 내역',Object.values(data.jobs).map(job=>`${job.lane} · ${job.operation} · ${job.status} · ${job.job_id}`));return;}
      const r=await fetch('/api/projects');if(!r.ok) throw new Error('프로젝트를 읽을 수 없습니다.');const data=await r.json();
      if(key==='projects') display('저장된 프로젝트',data.projects,true);
      else display('저장소',[data.data_root,`저장된 프로젝트 ${data.projects.length}개`]);
    } catch(error) {display('오류',[error.message]);}
  }));
  document.querySelector('[data-photo-fullscreen]').addEventListener('click',()=>document.querySelector('[data-preview="photo"]').requestFullscreen().catch(error=>{document.querySelector('[data-photo-status]').textContent=error.message;}));
  for(const kind of ['photo','video']) {
    const editor=document.querySelector(`[data-editor="${kind}"]`);
    editor.querySelectorAll('.command-chips button:not(.send-button)').forEach(button=>button.addEventListener('click',()=>{
      const text=button.textContent.trim();
      if(text==='참고 이미지') {editor.querySelector('[data-reference-input]').click();return;}
      if(text==='길이') {editor.querySelector('[data-video-controls]').hidden=false;editor.querySelector('[data-video-option="duration"]').focus();return;}
      if(text==='비율') {editor.querySelector(kind==='photo'?'[data-photo-tool="resize"]':'[data-video-tool="shortform"]').click();return;}
      const command=editor.querySelector('[data-command]');command.focus();command.value=kind==='video'?'영상 효과 적용해줘':text==='톤 조정'?'따뜻하게 보정해줘':'흑백으로 보정해줘';command.dispatchEvent(new Event('input',{bubbles:true}));
    }));
  }
})();
