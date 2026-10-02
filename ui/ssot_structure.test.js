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

const videoStart = html.indexOf('<section data-editor="video"');
const photoStart = html.indexOf('<section data-editor="photo"');
assert.ok(videoStart >= 0 && photoStart > videoStart, "video/photo editor sections must be ordered");
const videoHtml = html.slice(videoStart, photoStart);
const videoButtons = [...videoHtml.matchAll(/<button[^>]*>([\s\S]*?)<\/button>/g)].map((match) => match[1].replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim());
const aiIndex = videoButtons.findIndex((label) => label.includes("AI 자동 편집"));
const shortformIndex = videoButtons.findIndex((label) => label.includes("광고 숏폼"));
const saveIndex = videoButtons.findIndex((label) => label.includes("프로젝트 저장"));
assert.equal(videoButtons.filter((label) => label.includes("AI 자동 편집")).length, 1);
assert.equal(videoButtons.filter((label) => label.includes("광고 숏폼")).length, 1);
assert.equal((videoHtml.match(/data-action="shortform-mode"/g) || []).length, 1);
assert.match(videoHtml, /<button[^>]*data-action="ai-auto-edit"[^>]*>[^<]*✦ AI 자동 편집/);
assert.match(videoHtml, /<button[^>]*data-action="shortform-mode"[^>]*>[^<]*✦ 광고 숏폼/);
assert.ok(aiIndex >= 0 && shortformIndex > aiIndex && shortformIndex < saveIndex, "video action order must be AI auto edit, ad shortform, save");
assert.equal((html.match(/data-editor="shortform"/g) || []).length, 0, "independent shortform editor is forbidden");

const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, "ssot_manifest.json"), "utf8"));
assert.equal(manifest.status, "APPROVED_PINNED");
assert.equal(manifest.approved_ui_asset, "assets/ssot/MINDLE_MEDIA_AI_APPROVED_FINAL_20260913.png");
assert.match(manifest.asset_sha256, /^[a-f0-9]{64}$/);
