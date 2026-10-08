/* Behaviour layer for the approved layout.  It never selects or substitutes a model. */
(() => {
  const state = { video: null, photo: null, jobs: [], projectId: null, videoMode: "general", shortformContract: null };
  window.mindleInputFor = kind => state[kind];
  const readFile = (file) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("파일을 읽을 수 없습니다."));
    reader.onload = () => resolve(String(reader.result).split(",", 2)[1]);
    reader.readAsDataURL(file);
  });
  const operationFor = (kind, file, command) => {
    if (file.type.startsWith("audio/")) return { lane: "korean_audio", operation: "transcribe" };
    if (kind === "video" && /자막|STT|받아쓰기/.test(command)) return {lane:"korean_audio",operation:"transcribe"};
    if (kind === "video") return { lane: "video", operation: "tracking" };
    return { lane: "photo", operation: /업스케일|고화질|해상도|4x|4배|upscale/i.test(command) ? "upscale" : "segment" };
  };
  const message = (editor, text, error = false) => {
    const node = editor.querySelector("[data-command-error]");
    node.textContent = text; node.dataset.result = error ? "error" : "ok";
    node.style.display = text ? "block" : "none";
  };
  const rememberResult = async result => {
    if(result.lane!=='photo' && result.lane!=='video') return;
    const response=await fetch(result.preview_url);
    if(response.ok) {const blob=await response.blob();state[result.lane]=new File([blob],result.primary_output.file_name||result.primary_output.path.split(/[\\/]/).pop(),{type:blob.type});}
  };
  const preview = (editor, result) => {
    const host = editor.querySelector("[data-preview]"); host.replaceChildren();
    const output = result.preview_output || result.primary_output;
    let element;
    if (result.lane === "photo") { element = document.createElement("img"); element.alt = result.operation === "photo_edit" ? "보정 결과" : result.operation === "import" ? "원본 사진" : "AI 편집 결과"; element.src = result.preview_url; }
    else if (result.lane === "video") { element = document.createElement("video"); element.controls = false; element.src = result.preview_url; }
    else { element = document.createElement("pre"); element.textContent = result.runtime_result.text; }
    element.dataset.jobId = result.job_id; element.dataset.outputSha256 = output.sha256; host.append(element);
    if(result.lane==='video') {
      const clock=seconds=>new Date(Math.max(0,seconds||0)*1000).toISOString().slice(11,19);
      element.addEventListener('error',()=>{ host.dataset.previewStatus='media-error'; message(editor, '영상 미리보기를 재생할 수 없습니다 · MediaError '+(element.error?.code || 0), true); });
      element.addEventListener('loadedmetadata',()=>{
        editor.querySelector('[data-video-duration]').textContent='/ '+clock(element.duration);
        editor.querySelector('.timeline-ruler').textContent=Array.from({length:6},(_,i)=>clock(element.duration*i/5)).join('　');
      });
      element.addEventListener('timeupdate',()=>{
        editor.querySelector('[data-video-time]').textContent=clock(element.currentTime);
        editor.querySelector('[data-video-seek]').value=element.duration?element.currentTime/element.duration*100:0;
      });
      const options=result.runtime_result.options||{};
      if(options.subtitle) editor.querySelector('.track.purple').textContent='Subtitle Track · '+options.subtitle;
      editor.querySelector('.track.cyan').textContent='Effect Track · '+(options.effect?'영상 효과':options.fade?'장면 전환':'효과 없음');
      editor.querySelector('.track.green').textContent='Audio Track · '+(options.backgroundVolume!=null?'추가한 배경음악':'원본 오디오');
    }
    host.dataset.operation = result.operation; host.dataset.jobId = result.job_id; host.dataset.previewStatus = "actual-output";
    if (result.lane === "video") { const track = editor.querySelector(".track.film"); if (track) track.textContent = result.operation === "tracking" ? `영상 Track · SAM tracking · ${result.runtime_result.sampled_frames} samples` : "영상 Track · "+(result.operation === "import" ? "원본 영상" : "편집 결과"); }
  };
  async function executeShortform(editor, detail) {
    try {
      message(editor, "Marketing AI에 광고 기획을 요청 중입니다.");
      const response = await fetch("/api/integrations/marketing/shortform", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: detail.command, entrypoint: "media_ai", project_id: state.projectId })
      });
      const result = await response.json();
      if (!response.ok || result.status !== "bridge_contract_ready") throw new Error(result.error || "광고 제작지시 수신 실패");
      state.shortformContract = result.contract;
      const timeline = editor.querySelector("[data-timeline]");
      timeline.replaceChildren(...result.contract.scenes.map((scene) => {
        const item = document.createElement("span");
        item.dataset.sceneId = scene.id;
        item.dataset.startSec = String(scene.start_sec);
        item.dataset.endSec = String(scene.end_sec);
        item.textContent = `${scene.start_sec}–${scene.end_sec}초 · ${scene.subtitle}`;
        return item;
      }));
      editor.dataset.shortformStatus = "contract-ready";
      editor.dataset.aspectRatio = result.contract.aspect_ratio;
      message(editor, `광고 제작지시 준비 완료 · ${result.contract.duration}초 · Preview 전 검수 필요`);
    } catch (error) { message(editor, error.message, true); }
  }
  async function execute(editor, kind, detail) {
    if (kind === "video" && state.videoMode === "ad_shortform") return executeShortform(editor, detail);
    const file = state[kind];
    if (!file) { message(editor, "먼저 실제 원본 파일을 불러오세요.", true); return; }
    try {
      const command = detail.command;
      if (kind === "video" && window.mindleVideoCommand && await window.mindleVideoCommand(command)) return;
      if (kind === "photo" && window.mindlePhotoCommand && await window.mindlePhotoCommand(command)) return;
      message(editor, "AI 편집을 실행하고 있습니다.");
      const choice = operationFor(kind, file, command);
      const body = { ...choice, command, filename: file.name, content_base64: await readFile(file), project_id: state.projectId };
      if (file.datasetReference) body.reference = file.datasetReference;
      const response = await fetch("/api/jobs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const result = await response.json(); if (!response.ok || result.status !== "TESTED_PASS") throw new Error(result.error || "실제 모델 Job 실패");
      if (!state.jobs.includes(result.job_id)) state.jobs.push(result.job_id);
      if(result.lane==='korean_audio' && editor.querySelector('[data-preview] video')) {
        editor.querySelector('.track.purple').textContent='Subtitle Track · '+result.runtime_result.text;
        message(editor,result.runtime_result.text);
        if(/자막/.test(command) && window.mindleApplyVideoSubtitle) await window.mindleApplyVideoSubtitle(result.runtime_result.text);
        return;
      } else {preview(editor, result);await rememberResult(result);}
      message(editor, "편집 완료");
    } catch (error) { message(editor, error.message, true); }
  }
  async function save(editor) {
    try {
      const response = await fetch("/api/projects/save", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ project_id: state.projectId, job_ids: state.jobs }) });
      const result = await response.json(); if (!response.ok) throw new Error(result.error || "저장 실패");
      state.projectId = result.project_id; editor.dataset.projectStatus = "saved"; message(editor, `프로젝트 저장 완료 · ${result.project_id}`);
    } catch (error) { message(editor, error.message, true); }
  }
  async function exportProject(editor) {
    try {
      await save(editor);
      if (!state.projectId) return;
      const response = await fetch(`/api/projects/${state.projectId}/export`, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
      const result = await response.json(); if (!response.ok) throw new Error(result.error || "내보내기 실패");
      const link = document.createElement("a"); link.href = result.download_url; link.download = result.export.file_name; link.dataset.exportSha256 = result.export.sha256; document.body.append(link); link.click(); link.remove();
      editor.dataset.exportStatus = "exported"; editor.dataset.exportSha256 = result.export.sha256; message(editor, `내보내기 완료 · ${result.export.file_name}`);
    } catch (error) { message(editor, error.message, true); }
  }
  document.addEventListener('mindle:video-result', async (event) => { if (!state.jobs.includes(event.detail.job_id)) state.jobs.push(event.detail.job_id);preview(document.querySelector('[data-editor="video"]'),event.detail);await rememberResult(event.detail); });
  document.addEventListener('mindle:photo-result', async (event) => {
    const result = event.detail; if (!state.jobs.includes(result.job_id)) state.jobs.push(result.job_id);
    preview(document.querySelector('[data-editor="photo"]'), result);await rememberResult(result);
  });
  ["video", "photo"].forEach((kind) => {
    const editor = document.querySelector(`[data-editor="${kind}"]`); if (!editor) return;
    const input = editor.querySelector("[data-primary-input]");
    editor.querySelector("[data-action='load']").addEventListener("click", () => input.click());
    input.addEventListener("change", async () => {
      state[kind] = input.files[0] || null;
      if (!state[kind]) return;
      message(editor, `입력 준비 · ${state[kind].name}`);
      const host = editor.querySelector('[data-preview]');
      const previous = host.dataset.objectUrl; if (previous) URL.revokeObjectURL(previous);
      if (state[kind].type.startsWith('audio/')) return;
      const element = document.createElement(kind === 'photo' ? 'img' : 'video');
      element.src = URL.createObjectURL(state[kind]); host.dataset.objectUrl = element.src;
      if (kind === 'video') element.controls = true; else element.alt = state[kind].name;
      host.replaceChildren(element); host.dataset.previewStatus = 'original';
      try {
        message(editor,'원본을 불러오고 있습니다.');
        const response=await fetch('/api/media/import',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({kind,filename:state[kind].name,content_base64:await readFile(state[kind])})});
        const result=await response.json();if(!response.ok) throw new Error(result.error||'원본 불러오기 실패');
        if (!state.jobs.includes(result.job_id)) state.jobs.push(result.job_id);preview(editor,result);message(editor,'원본 불러오기 완료');
      } catch(error) {message(editor,error.message,true);}

    });
    editor.addEventListener("mindle:mode", (event) => { state.videoMode = event.detail.mode; message(editor, state.videoMode === "ad_shortform" ? "광고 숏폼 모드 · 자연어로 제품·대상·길이를 지시하세요." : "일반 영상 편집 모드"); });
    editor.querySelector("[data-action='ai-auto-edit']")?.addEventListener("click", () => execute(editor, kind, {command:"대상을 추적해줘"}));
    editor.addEventListener("mindle:command", (event) => execute(editor, kind, event.detail));
    editor.addEventListener("mindle:save", () => save(editor));
    editor.addEventListener("mindle:export", () => exportProject(editor));
  });
  async function restoreSavedProject() {
    try {
      const response = await fetch('/api/projects/latest');
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || '저장된 프로젝트를 불러올 수 없습니다.');
      if (!result.project) return;
      state.projectId = result.project.project_id;
      state.jobs = result.project.job_ids;
      for (const job of result.project.jobs) {
        // A saved transcript must not replace an available VIDEO result preview.
        if (job.lane === 'korean_audio' && result.project.jobs.some((item) => item.lane === 'video')) continue;
        const kind = job.lane === 'photo' ? 'photo' : 'video';
        const editor = document.querySelector(`[data-editor="${kind}"]`);
        if (editor) {
          preview(editor, job);
          if(job.preview_url && job.lane!=='korean_audio') {
            const inputResponse=await fetch(job.preview_url);
            if(inputResponse.ok) {const blob=await inputResponse.blob();state[kind]=new File([blob],job.input.file_name||job.input.path.split(/[\\/]/).pop(),{type:blob.type});}
          }
          editor.dataset.projectStatus = 'reopened';
          message(editor, `저장된 프로젝트를 다시 열었습니다 · ${state.projectId}`);
        }
      }
      const transcript = [...result.project.jobs].reverse().find((job) => job.lane === 'korean_audio');
      if (transcript) {
        const editor = document.querySelector('[data-editor="video"]');
        if (editor) {
          editor.querySelector('.track.purple').textContent='Subtitle Track · '+transcript.runtime_result.text;
          message(editor, `저장된 프로젝트를 다시 열었습니다 · ${state.projectId} · 한국어 자막: ${transcript.runtime_result.text}`);
        }
      }
    } catch (error) {
      const editor = document.querySelector('[data-editor="video"]');
      if (editor) message(editor, error.message, true);
    }
  }
  restoreSavedProject();
})();


