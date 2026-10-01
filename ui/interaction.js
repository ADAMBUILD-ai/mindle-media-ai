const MAX_REFERENCES = 5;
const REFERENCE_IMAGE_EXTENSIONS = new Set([".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"]);

function normalizeReferenceName(name) {
  return String(name || "").trim().replace(/^.*[\\/]/, "");
}

class CommandPanelState {
  constructor(kind, maxReferences = MAX_REFERENCES) {
    this.kind = kind; this.maxReferences = maxReferences; this.phase = "collapsed";
    this.text = ""; this.references = []; this.error = null;
  }
  focus() { if (this.phase !== "executing") this.phase = "expanded"; }
  setText(text) { this.text = String(text); }
  attach(file) {
    this.focus();
    if (!file || !file.name) { this.error = "파일을 읽을 수 없습니다."; return false; }
    if (!String(file.type || "").startsWith("image/")) { this.error = "이미지 파일만 첨부할 수 있습니다."; return false; }
    const name = normalizeReferenceName(file.name);
    const extension = name.slice(name.lastIndexOf(".")).toLowerCase();
    if (!REFERENCE_IMAGE_EXTENSIONS.has(extension)) { this.error = "JPG, PNG, WEBP, TIFF 이미지만 첨부할 수 있습니다."; return false; }
    if (this.references.length >= this.maxReferences) { this.error = `참고 이미지는 최대 ${this.maxReferences}개까지 첨부할 수 있습니다.`; return false; }
    if (this.references.some((reference) => reference.name.toLowerCase() === name.toLowerCase())) { this.error = "같은 참고 이미지는 한 번만 첨부할 수 있습니다."; return false; }
    this.references.push({ name, type: file.type, preview: file.preview || null }); this.error = null; return true;
  }
  remove(index) { this.references.splice(index, 1); this.error = null; }
  submit() {
    if (!this.text.trim()) { this.error = "AI 지시를 입력하세요."; this.phase = "expanded"; throw new Error("command required"); }
    this.error = null; this.phase = "executing";
    return { kind: this.kind, command: this.text.trim(), references: this.references.map(({ name, type }) => ({ name, type })) };
  }
  complete() { this.phase = "collapsed"; this.text = ""; this.references = []; this.error = null; }
  fail(message = "작업을 완료하지 못했습니다. 지시 내용을 확인해 주세요.") { this.phase = "expanded"; this.error = message; }
}

class EditorActionState {
  constructor(kind) { this.kind = kind; this.saved = false; this.exports = 0; }
  save() { this.saved = true; return { action: "save", kind: this.kind, result: "edit-state-saved" }; }
  export() { this.exports += 1; return { action: "export", kind: this.kind, result: "result-file-requested", sequence: this.exports }; }
}

class AdapterFeatureState {
  constructor(capability, fallback) {
    this.capability = capability; this.fallback = fallback; this.adapterEnabled = false;
    this.status = "VERIFY_REQUIRED"; this.fallbackUsed = false; this.error = null;
  }
  requestExecution() {
    if (!this.adapterEnabled) {
      this.fallbackUsed = true; this.status = "VERIFY_REQUIRED";
      return { capability: this.capability, executed: false, fallback_used: this.fallback, status: this.status };
    }
    return { capability: this.capability, executed: true, fallback_used: null, status: "EXECUTING" };
  }
  fail(message, reason = "runtime_failure") {
    this.error = message; this.fallbackUsed = true; this.status = "VERIFY_REQUIRED";
    return { capability: this.capability, executed: false, error: reason, fallback_used: this.fallback, status: this.status };
  }
}

const videoCommand = new CommandPanelState("video");
const photoCommand = new CommandPanelState("photo");

function renderPanel(root, state) {
  root.dataset.phase = state.phase;
  root.querySelector("[data-command]").value = state.text;
  root.querySelector("[data-command-error]").textContent = state.error || "";
  const list = root.querySelector("[data-reference-list]");
  list.replaceChildren(...state.references.map((ref, index) => {
    const item = document.createElement("li"); item.className = "reference-thumbnail"; item.textContent = ref.name;
    const remove = document.createElement("button"); remove.type = "button"; remove.textContent = "제거"; remove.dataset.referenceRemove = String(index);
    item.append(" ", remove); return item;
  }));
}

function bindEditor(kind) {
  const editor = document.querySelector(`[data-editor="${kind}"]`); if (!editor) return;
  const state = kind === "video" ? videoCommand : photoCommand; const actions = new EditorActionState(kind);
  const command = editor.querySelector("[data-command]"); const fileInput = editor.querySelector("[data-reference-input]"); const panel = editor.querySelector("[data-command-panel]");
  const sync = () => renderPanel(panel, state);
  command.addEventListener("focus", () => { state.focus(); sync(); });
  command.addEventListener("input", (event) => { state.setText(event.target.value); sync(); });
  command.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.shiftKey) return; event.preventDefault();
    try { editor.dispatchEvent(new CustomEvent("mindle:command", { detail: state.submit() })); state.complete(); } catch (_) {} sync();
  });
  editor.querySelector("[data-action$='reference']").addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", (event) => {
    [...event.target.files].forEach((file) => state.attach({ name: file.name, type: file.type, preview: URL.createObjectURL(file) })); fileInput.value = ""; sync();
  });
  panel.addEventListener("click", (event) => { const index = event.target.dataset.referenceRemove; if (index !== undefined) { state.remove(Number(index)); sync(); } });
  editor.querySelector("[data-action='save']").addEventListener("click", () => editor.dispatchEvent(new CustomEvent("mindle:save", { detail: actions.save() })));
  editor.querySelector("[data-action='export']").addEventListener("click", () => editor.dispatchEvent(new CustomEvent("mindle:export", { detail: actions.export() })));
  sync();
}

if (typeof document !== "undefined") ["video", "photo"].forEach(bindEditor);
if (typeof module !== "undefined") module.exports = { CommandPanelState, EditorActionState, AdapterFeatureState, MAX_REFERENCES, REFERENCE_IMAGE_EXTENSIONS, videoCommand, photoCommand };
