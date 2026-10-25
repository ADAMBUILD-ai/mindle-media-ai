(() => {
  const root=document.querySelector('[data-ai-core-status]');
  if(!root)return;
  const summary=root.querySelector('[data-ai-core-summary]');
  const label=(name,text,ok)=>{const node=root.querySelector(`[data-ai-engine="${name}"]`);node.textContent=text;node.dataset.ok=ok?'true':'false';};
  async function refresh(){
    root.dataset.state='checking';summary.textContent='실제 로컬 AI 엔진과 최근 실행 증거를 확인 중입니다.';
    try{
      const response=await fetch('/api/ai-core/status');const value=await response.json();
      if(!response.ok)throw new Error(value.error||'AI 코어 상태 확인 실패');
      const actual=value.actual_evidence||{},configured=value.configured||{};
      label('planner',actual.qwen_or_architecture_plan?'Qwen 실제 추론 PASS':configured.local_generative_planner?'Qwen 준비 · 새 추론 필요':'Qwen 사용 불가',actual.qwen_or_architecture_plan);
      label('tts',actual.neural_korean_voice?'한국어 신경망 음성 PASS':configured.neural_korean_tts?'신경망 음성 준비 · 새 합성 필요':'신경망 음성 사용 불가',actual.neural_korean_voice);
      label('mp4',actual.mp4_output?'AI 작업 MP4 PASS':'AI 작업 MP4 생성 필요',actual.mp4_output);
      label('sam',actual.sam_photo_segmentation||actual.sam_video_tracking?'SAM 실제 추론 PASS':'SAM 새 추론 필요',actual.sam_photo_segmentation||actual.sam_video_tracking);
      label('whisper',actual.whisper_korean_stt?'Whisper 한국어 STT PASS':'Whisper 새 추론 필요',actual.whisper_korean_stt);
      label('upscale',actual.photo_upscale_4x?'4× 업스케일 PASS':'4× 업스케일 새 추론 필요',actual.photo_upscale_4x);
      root.dataset.state=value.state;
      summary.textContent=value.state==='AI_RUNTIME_ACTUAL_CHAIN_VERIFIED'?'로컬 AI가 계획·음성·MP4를 실제 생성했습니다.':value.shell_only?'AI 엔진이 연결되지 않았습니다. 이 상태는 제품 PASS가 아닙니다.':'엔진은 준비됐습니다. 자연어 작업을 실행해야 실제 AI PASS가 됩니다.';
    }catch(error){root.dataset.state='AI_STATUS_UNAVAILABLE';summary.textContent=error.message;for(const name of ['planner','tts','mp4','sam','whisper','upscale'])label(name,'상태 확인 실패',false);}
  }
  root.querySelector('[data-ai-core-refresh]').addEventListener('click',refresh);
  window.addEventListener('focus',refresh);
  document.addEventListener('DOMContentLoaded',refresh,{once:true});
  window.mindleRefreshAiCore=refresh;
})();
