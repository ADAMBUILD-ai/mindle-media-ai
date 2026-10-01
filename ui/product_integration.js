/* Behaviour layer for the approved layout.  It never selects or substitutes a model. */
(() => {
  const state = { video: null, photo: null, jobs: [], projectId: null };
  const readFile = (file) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("파일을 읽을 수 없습니다."));
    reader.onload = () => resolve(String(reader.result).split(",", 2)[1]);
    reader.readAsDataURL(file);
  });
  const operationFor = (kind, file, command) => {
    if (file.type.startsWith("audio/")) return { lane: "korean_audio", operation: "transcribe" };
    if (kind === "video") return { lane: "video", operation: "tracking" };
    return { lane: "photo", operation: /업스케일|4x|4배|upscale/i.test(command) ? "upscale" : "segment" };
  };
  const message = (editor, text, error = false) => {
    const node = editor.querySelector("[data-command-error]");
    node.textContent = text; node.dataset.result = error ? "error" : "ok";
  };
  const preview = (editor, result) => {
    const host = editor.querySelector("[data-preview]"); host.replaceChildren();
    const output = result.primary_output;
    let element;
    if (result.lane === "photo") { element = document.createElement("img"); element.alt = "실제 AI 결과"; element.src = result.preview_url; }
    else if (result.lane === "video") { element = document.createElement("video"); element.controls = true; element.src = result.preview_url; }
    else { element = document.createElement("pre"); element.textContent = result.runtime_result.text; }
    element.dataset.jobId = result.job_id; element.dataset.outputSha256 = output.sha256; host.append(element);
    host.dataset.jobId = result.job_id; host.dataset.previewStatus = "actual-output";
    if (result.lane === "video") editor.querySelector("[data-timeline]").textContent = `SAM tracking · Job ${result.job_id} · ${result.runtime_result.sampled_frames} samples`;
  };
  async function execute(editor, kind, detail) {
    const file = state[kind];
    if (!file) { message(editor, "먼저 실제 원본 파일을 불러오세요.", true); return; }
    try {
      message(editor, "실제 검증 모델을 CPU에서 실행 중입니다.");
      const command = detail.command;
      const choice = operationFor(kind, file, command);
      const body = { ...choice, command, filename: file.name, content_base64: await readFile(file), project_id: state.projectId };
      if (file.datasetReference) body.reference = file.datasetReference;
      const response = await fetch("/api/jobs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const result = await response.json(); if (!response.ok || result.status !== "TESTED_PASS") throw new Error(result.error || "실제 모델 Job 실패");
      state.jobs.push(result.job_id); preview(editor, result);
      message(editor, `완료 · Job ${result.job_id} · 실제 출력 SHA-256 ${result.primary_output.sha256}`);
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
      if (!state.projectId) await save(editor);
      const response = await fetch(`/api/projects/${state.projectId}/export`, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
      const result = await response.json(); if (!response.ok) throw new Error(result.error || "내보내기 실패");
      const link = document.createElement("a"); link.href = result.download_url; link.download = result.export.file_name; link.dataset.exportSha256 = result.export.sha256; document.body.append(link); link.click(); link.remove();
      editor.dataset.exportStatus = "exported"; editor.dataset.exportSha256 = result.export.sha256; message(editor, `내보내기 완료 · ${result.export.file_name}`);
    } catch (error) { message(editor, error.message, true); }
  }
  ["video", "photo"].forEach((kind) => {
    const editor = document.querySelector(`[data-editor="${kind}"]`); if (!editor) return;
    const input = editor.querySelector("[data-primary-input]");
    editor.querySelector("[data-action='load']").addEventListener("click", () => input.click());
    input.addEventListener("change", () => { state[kind] = input.files[0] || null; if (state[kind]) message(editor, `실제 입력 준비 · ${state[kind].name}`); });
    editor.addEventListener("mindle:command", (event) => execute(editor, kind, event.detail));
    editor.addEventListener("mindle:save", () => save(editor));
    editor.addEventListener("mindle:export", () => exportProject(editor));
  });
})();
