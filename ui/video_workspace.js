/* Explicit video editing uses the package FFmpeg, with the original retained. */
(() => {
  const editor=document.querySelector('[data-editor="video"]');
  const media=()=>editor.querySelector('[data-preview] video');
  editor.querySelector('[data-video-play]').addEventListener('click',()=>{const v=media();if(v) {if(v.paused) v.play().catch(()=>{});else v.pause();}});
  editor.querySelector('[data-video-start]').addEventListener('click',()=>{const v=media();if(v) v.currentTime=0;});
  editor.querySelector('[data-video-end]').addEventListener('click',()=>{const v=media();if(v && Number.isFinite(v.duration)) v.currentTime=v.duration;});
  editor.querySelector('[data-video-mute]').addEventListener('click',()=>{const v=media();if(v) v.muted=!v.muted;});
  editor.querySelector('[data-video-fullscreen]').addEventListener('click',()=>media()?.requestFullscreen?.());
  editor.querySelector('[data-video-seek]').addEventListener('input',event=>{const v=media();if(v && Number.isFinite(v.duration)) v.currentTime=v.duration*Number(event.target.value)/100;});
  const value=key=>Number(editor.querySelector(`[data-video-option="${key}"]`).value);
  let busy=false, splitPending=false;
  async function apply(extra={}, label='영상 편집') {
    if(busy || window.mindleEditPending('video')) return;
    const file=window.mindleInputFor('video') || editor.querySelector('[data-primary-input]').files[0];
    const message=editor.querySelector('[data-command-error]');
    message.style.display='block';
    if(!file || !file.type.startsWith('video/')) {message.textContent='먼저 영상을 불러오세요.';return;}
    busy=true;window.mindleBeginEdit('video');message.textContent='영상 편집을 적용하고 있습니다.';
    try {
      const base64=await new Promise((resolve,reject)=>{const r=new FileReader();r.onerror=reject;r.onload=()=>resolve(String(r.result).split(',')[1]);r.readAsDataURL(file);});
      const toggles=Object.fromEntries([...editor.querySelectorAll('[data-video-toggle]')].map(input=>[input.dataset.videoToggle,input.checked]));
      const options={...toggles,split:splitPending,start:value('start'),duration:value('duration'),speed:value('speed'),volume:value('volume'),brightness:value('brightness'),contrast:value('contrast'),saturation:value('saturation'),...extra};
      const bgm=editor.querySelector('[data-bgm-input]').files[0];
      let background=null;
      if(bgm) background={filename:bgm.name,content_base64:await new Promise((resolve,reject)=>{const r=new FileReader();r.onerror=reject;r.onload=()=>resolve(String(r.result).split(',')[1]);r.readAsDataURL(bgm);})};
      const response=await fetch('/api/video-edits',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:file.name,content_base64:base64,command:label,options,background})});
      const result=await response.json();if(!response.ok) throw new Error(result.error||'영상 편집 실패');
      await window.mindleAcceptResult(result);editor.querySelectorAll('[data-video-option]').forEach(input=>{input.value=['speed','volume'].includes(input.dataset.videoOption)?1:0;if(input.nextElementSibling?.tagName==='OUTPUT') input.nextElementSibling.value=input.value;});splitPending=false;message.textContent=result.runtime_result.options.split?'분할 완료 · 두 클립을 프로젝트 내보내기에서 받을 수 있습니다.':'영상 편집 완료';
    } catch(error) {message.textContent=error.message;} finally {busy=false;window.mindleEndEdit('video');}
  }
  editor.querySelectorAll('[data-video-tool]').forEach(button=>button.addEventListener('click',()=>{
    const key=button.dataset.videoTool;
    if(key==='trim' || key==='split' || key==='speed') {splitPending=key==='split';editor.querySelector('[data-video-controls]').hidden=false;editor.querySelector('[data-video-option="'+(key==='speed'?'speed':'start')+'"]').focus();return;}
    if(key==='rotate') return apply({rotate:true},'회전');
    if(key==='shortform') return apply({aspect:'9:16',duration:30},'30초 숏폼 변환');
    if(key==='fade') return apply({fade:true},'장면 전환');
    if(key==='effect') return apply({effect:true},'영상 효과');
    if(key==='subtitle') {editor.querySelector('[data-subtitle-controls]').hidden=false;return;}
    if(key==='highlight') return apply({highlight:true},'장면 변화 기반 하이라이트 추출');
    if(key==='bgm') {editor.querySelector('[data-bgm-input]').click();return;}
    if(key==='auto-subtitle') {editor.dispatchEvent(new CustomEvent('mindle:command',{detail:{command:'자동으로 자막 넣어줘'}}));return;}
    apply();
  }));
  editor.querySelector('[data-video-apply]').addEventListener('click',()=>apply({subtitle:editor.querySelector('[data-video-subtitle]').value}));
  editor.querySelector('[data-bgm-input]').addEventListener('change',()=>apply({backgroundVolume:.35},'배경음악 추가'));
  editor.querySelectorAll('[data-video-option]').forEach(input=>input.addEventListener('input',()=>{if(input.nextElementSibling?.tagName==='OUTPUT') input.nextElementSibling.value=input.value;}));
  window.mindleApplyVideoSubtitle=text=>apply({subtitle:text},"자동 자막 적용");
  window.mindleVideoCommand=async text=>{
    if(/숏폼|초.*만들|속도|자르|전환|효과|밝게|오디오/.test(text)) {
      const extra={};if(/숏폼/.test(text)) extra.aspect='9:16';const sec=text.match(/(\d+)\s*초/);if(sec) extra.duration=Number(sec[1]);
      if(/전환/.test(text)) extra.fade=true;if(/효과/.test(text)) extra.effect=true;if(/밝게/.test(text)) extra.brightness=15;
      const speed=text.match(/([\d.]+)\s*배/);if(speed) extra.speed=Number(speed[1]);
      await apply(extra,'AI 대화 편집 · '+text);return true;
    }
    if(/배경음악|잔잔/.test(text)) {if(editor.querySelector('[data-bgm-input]').files[0]) await apply({backgroundVolume:.2},'잔잔한 배경음악');else {editor.querySelector('[data-command-error]').textContent='배경음악 추가 버튼에서 사용할 음악을 선택하세요.';editor.querySelector('[data-command-error]').style.display='block';}return true;}
    return false;
  };
})();

