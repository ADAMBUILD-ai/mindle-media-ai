const assert = require("node:assert/strict");
const { CommandPanelState, ShortformModeState, EditorActionState, AdapterFeatureState, MAX_REFERENCES } = require("./interaction.js");

const command = new CommandPanelState("video");
command.focus();
command.text = "창문 반사를 줄여줘";
command.attach({ name: "reference.png", type: "image/png" });
assert.deepEqual(command.submit(), { kind: "video", command: "창문 반사를 줄여줘", references: [{ name: "reference.png", type: "image/png" }] });
assert.equal(command.phase, "executing");
command.fail();
assert.equal(command.phase, "expanded");
assert.equal(command.text, "창문 반사를 줄여줘");
command.complete();
assert.equal(command.phase, "collapsed");
assert.deepEqual(command.references, []);

const photo = new CommandPanelState("photo", 2);
assert.equal(photo.phase, "collapsed");
assert.equal(photo.attach({ name: "a.jpg", type: "image/jpeg" }), true);
assert.equal(photo.attach({ name: "not-image.pdf", type: "application/pdf" }), false);
assert.match(photo.error, /이미지/);
assert.equal(photo.attach({ name: "b.jpg", type: "image/jpeg" }), true);
assert.equal(photo.attach({ name: "c.jpg", type: "image/jpeg" }), false);
assert.match(photo.error, /최대 2개/);
photo.remove(0); assert.equal(photo.references.length, 1);
assert.equal(photo.attach({ name: "B.JPG", type: "image/jpeg" }), false);
assert.match(photo.error, /한 번만/);
assert.equal(photo.attach({ name: "animation.gif", type: "image/gif" }), false);
assert.match(photo.error, /JPG, PNG, WEBP, TIFF/);
assert.equal(MAX_REFERENCES, 5);

const actions = new EditorActionState("photo");
assert.deepEqual(actions.save(), { action: "save", kind: "photo", result: "edit-state-saved" });
assert.deepEqual(actions.export(), { action: "export", kind: "photo", result: "result-file-requested", sequence: 1 });

const upscale = new AdapterFeatureState("high resolution", "OpenCV Lanczos4");
assert.deepEqual(upscale.requestExecution(), { capability: "high resolution", executed: false, fallback_used: "OpenCV Lanczos4", status: "VERIFY_REQUIRED" });
assert.equal(upscale.adapterEnabled, false);
assert.deepEqual(upscale.fail("timeout", "timeout"), { capability: "high resolution", executed: false, error: "timeout", fallback_used: "OpenCV Lanczos4", status: "VERIFY_REQUIRED" });


const shortform = new ShortformModeState();
assert.equal(shortform.mode, "general");
assert.equal(shortform.toggle(), "ad_shortform");
assert.equal(shortform.isShortform(), true);
assert.equal(shortform.toggle(), "general");
