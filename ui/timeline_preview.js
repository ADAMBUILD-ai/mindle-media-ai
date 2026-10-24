/* Read-only timeline drawn only from the active decoded media, never demo clips. */
(() => {
  const editor=document.querySelector('[data-editor="video"]');
  if(!editor) return;
  const timeline=editor.querySelector('[data-timeline]');
  let generation=0, cleanup=()=>{};
  window.mindleClearTimeline=()=>{generation++;cleanup();cleanup=()=>{};timeline.querySelector('[data-media-timeline]')?.remove();};
  const clock=t=>new Date(Math.max(0,t)*1000).toISOString().slice(11,19);
  window.mindleRenderTimeline=(video,options={})=>{
    window.mindleClearTimeline();const token=generation;
    const current=()=>token===generation && editor.querySelector('[data-preview] video')===video;
    const root=document.createElement('div');root.dataset.mediaTimeline='';root.dataset.status='loading';
    root.setAttribute('aria-label','현재 영상 미리보기 타임라인 · 위치 탐색');
    const frames=document.createElement('div');frames.className='timeline-frames';
    const waveform=document.createElement('div');waveform.className='timeline-waveform';waveform.textContent='오디오 파형 확인 중';
    const subtitle=document.createElement('div');subtitle.className='timeline-caption';subtitle.textContent=options.subtitle||'자막 없음';
    const effect=document.createElement('div');effect.className='timeline-effect';effect.textContent=options.effect?'적용된 영상 효과':options.fade?'적용된 장면 전환':'효과 없음';
    const seek=document.createElement('input');seek.type='range';seek.min=0;seek.max=100;seek.step=.1;seek.value=0;seek.setAttribute('aria-label','타임라인 영상 위치');
    seek.addEventListener('input',()=>{if(current()&&Number.isFinite(video.duration))video.currentTime=video.duration*Number(seek.value)/100;});
    const playhead=document.createElement('div');playhead.className='timeline-playhead';playhead.setAttribute('aria-hidden','true');
    root.append(frames,waveform,subtitle,effect,seek,playhead);timeline.prepend(root);
    const update=()=>{if(current()){const percent=video.duration?video.currentTime/video.duration*100:0;seek.value=percent;playhead.style.left=percent+'%';}};
    const mediaError=()=>{if(current()){root.dataset.status='media-error';frames.textContent='영상 프레임 없음';waveform.textContent='오디오 파형 없음';waveform.dataset.status='unavailable';}};
    video.addEventListener('timeupdate',update);video.addEventListener('error',mediaError);
    const clone=document.createElement('video');clone.muted=true;clone.preload='auto';clone.src=video.currentSrc||video.src;
    let audioContext=null;const abort=new AbortController();
    cleanup=()=>{abort.abort();video.removeEventListener('timeupdate',update);video.removeEventListener('error',mediaError);video.removeEventListener('loadeddata',start);clone.pause();clone.removeAttribute('src');clone.load();audioContext?.close().catch(()=>{});};
    const ready=(event,action)=>new Promise((resolve,reject)=>{
      const done=()=>{clearTimeout(timer);clone.removeEventListener(event,ok);clone.removeEventListener('error',fail);abort.signal.removeEventListener('abort',fail);};
      const ok=()=>{done();resolve();},fail=()=>{done();reject(new Error('media unavailable'));};
      const timer=setTimeout(fail,10000);clone.addEventListener(event,ok,{once:true});clone.addEventListener('error',fail,{once:true});abort.signal.addEventListener('abort',fail,{once:true});if(abort.signal.aborted)fail();else action();
    });
    const drawFrames=async()=>{
      try {
        await ready('loadeddata',()=>clone.load());if(!current())return;
        for(let i=0;i<6;i++) {
          const time=Math.min(clone.duration*.98,clone.duration*(i+.5)/6);
          await ready('seeked',()=>{clone.currentTime=time;});if(!current())return;
          const canvas=document.createElement('canvas');canvas.width=144;canvas.height=81;
          const context=canvas.getContext('2d');context.fillStyle='#020913';context.fillRect(0,0,144,81);
          const scale=Math.min(144/clone.videoWidth,81/clone.videoHeight),w=clone.videoWidth*scale,h=clone.videoHeight*scale;
          context.drawImage(clone,(144-w)/2,(81-h)/2,w,h);
          const button=document.createElement('button');button.type='button';button.className='timeline-frame';button.dataset.seconds=String(time);button.setAttribute('aria-label',clock(time)+' 위치로 이동');button.title=clock(time);button.append(canvas);button.addEventListener('click',()=>{if(current())video.currentTime=time;});frames.append(button);
        }
        if(current())root.dataset.status='ready';
      }catch(_){if(current()){root.dataset.status='frame-unavailable';frames.textContent='영상 프레임을 읽을 수 없습니다.';}}
    };
    const drawWaveform=async()=>{
      try {
        const response=await fetch(video.currentSrc||video.src,{signal:abort.signal});if(!response.ok)throw new Error('HTTP');
        const size=Number(response.headers.get('Content-Length'));if(size>32*1024*1024){await response.body?.cancel();throw new Error('size');}
        const bytes=await response.arrayBuffer();if(bytes.byteLength>32*1024*1024)throw new Error('size');if(!current())return;
        const AudioContext=window.AudioContext||window.webkitAudioContext;if(!AudioContext)throw new Error('decoder');
        audioContext=new AudioContext();const audio=await audioContext.decodeAudioData(bytes);if(!current())return;
        const samples=audio.getChannelData(0);const canvas=document.createElement('canvas');canvas.width=600;canvas.height=40;const context=canvas.getContext('2d');context.fillStyle='#17d9d2';
        for(let x=0;x<600;x++){let peak=0;const start=Math.floor(x*samples.length/600),end=Math.floor((x+1)*samples.length/600);for(let n=start;n<end;n++)peak=Math.max(peak,Math.abs(samples[n]));context.fillRect(x,20-peak*19,1,Math.max(1,peak*38));}
        waveform.replaceChildren(canvas);waveform.dataset.status='decoded';await audioContext.close();audioContext=null;
      }catch(_){if(current()){waveform.textContent='오디오 파형 없음 · 디코딩되지 않은 파형은 표시하지 않습니다.';waveform.dataset.status='unavailable';}}
    };
    const start=()=>{if(!current()||!Number.isFinite(video.duration)||!video.videoWidth)return;drawFrames();if(video.duration<=120)drawWaveform();else{waveform.textContent='120초 초과 영상 · 파형 미생성';waveform.dataset.status='deferred';}};
    if(video.readyState>=2)start();else video.addEventListener('loadeddata',start,{once:true});
  };
})();
