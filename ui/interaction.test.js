const test = require("node:test");
const assert = require("node:assert/strict");
const { ShortformModeState } = require("./interaction.js");

test("shortform mode is additive and toggles without changing editor state", () => {
  const mode = new ShortformModeState();
  assert.equal(mode.mode, "general");
  assert.equal(mode.toggle(), "ad_shortform");
  assert.equal(mode.isShortform(), true);
  assert.equal(mode.toggle(), "general");
});
