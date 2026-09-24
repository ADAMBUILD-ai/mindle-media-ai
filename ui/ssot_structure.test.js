const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
for (const required of [
  'data-editor="video"',
  'data-editor="photo"',
  'data-layout="left-center-right"',
  'data-preview="video"',
  'data-timeline="video"',
  'data-preview="photo"',
  'data-command="video"',
  'data-command="photo"',
  '참고 이미지 추가',
  '프로젝트 저장',
  '내보내기',
]) assert.ok(html.includes(required), `missing SSOT structure: ${required}`);

const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, "ssot_manifest.json"), "utf8"));
assert.equal(manifest.status, "APPROVED_PINNED");
assert.equal(manifest.approved_ui_asset, "assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png");
assert.match(manifest.asset_sha256, /^[a-f0-9]{64}$/);
