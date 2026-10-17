const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

// Execute the production controller. Only DOM/network boundaries are fixtures;
// no model, browser decoding, Windows execution or hearing is claimed here.
function deferred() {
  let resolve;
  const promise = new Promise(r => { resolve = r; });
  return {promise, resolve};
}
class Element {
  constructor() { this.dataset = {}; this.style = {}; this.listeners = {}; this.nodes = new Map(); }
  querySelector(selector) {
    if (!this.nodes.has(selector)) this.nodes.set(selector, new Element());
    return this.nodes.get(selector);
  }
  addEventListener(name, callback) { this.listeners[name] = callback; }
  dispatchEvent(event) { return this.listeners[event.type]?.(event); }
  replaceChildren(...children) { this.children = children; }
  append(...children) { (this.children ||= []).push(...children); }
  click() {}
  remove() {}
}
async function setup(routes = {}) {
  const editors = {video: new Element(), photo: new Element()};
  const calls = [];
  const pendingSave = deferred();
  const pendingRestore = deferred();
  const pendingExport = deferred();
  let delaySave = false;
  let delayRestore = false;
  let delayExport = false;
  const document = new Element();
  document.body = new Element();
  document.querySelector = selector => editors[selector.includes('photo') ? 'photo' : 'video'];
  document.querySelectorAll = selector => selector === '[data-editor]' ? Object.values(editors)
    : selector === '[data-preview]' ? Object.values(editors).map(e => e.querySelector('[data-preview]')) : [];
  document.createElement = () => new Element();
  const response = data => ({ok: true, json: async () => data, blob: async () => new Blob(['photo'], {type: 'image/png'})});
  const window = {};
  const context = vm.createContext({window, document, File, Blob, Set, FileReader: class { readAsDataURL() { this.result="data:image/png;base64,cGhvdG8=";this.onload(); } },
    CustomEvent: class { constructor(type, options) { this.type = type; this.detail = options?.detail; } },
    fetch: async (url, options) => {
      calls.push({url, options});
      if(routes[url]) return routes[url];
      if (url === '/api/projects/latest') return response({project: null});
      if (url === '/api/assets') return response({assets: []});
      if (url === '/api/projects/save') {
        if (delaySave) await pendingSave.promise;
        return response({project_id: 'saved-project', status: 'SAVED'});
      }
      if (url.endsWith('/export')) {
        if (delayExport) await pendingExport.promise;
        return response({download_url: '/bundle.zip', export: {file_name: 'bundle.zip', sha256: 'fixture'}});
      }
      if (url.startsWith('/api/projects/')) {
        if (delayRestore) await pendingRestore.promise;
        return response({project: null});
      }
      return response({});
    }});
  vm.runInContext(fs.readFileSync(__dirname + '/product_integration.js', 'utf8'), context);
  await new Promise(setImmediate);
  const job = {job_id: 'existing-photo', lane: 'photo', operation: 'import', preview_url: '/photo.png',
    primary_output: {file_name: 'photo.png', sha256: 'fixture'}, runtime_result: {options: {}}};
  await window.mindleAcceptResult(job);
  return {window, editors, calls, pendingSave, pendingRestore, pendingExport,
    startSave: () => { delaySave = true; return editors.photo.dispatchEvent({type: 'mindle:save'}); },
    startRestore: () => { delayRestore = true; return window.mindleOpenProject('first-project'); },
    startExport: () => { delayExport = true; return editors.photo.dispatchEvent({type: 'mindle:export'}); }};
}

test('new/open project cannot clear an edit in progress or start a competing restore', async () => {
  const {window, calls} = await setup();
  const photo = window.mindleInputFor('photo');
  window.mindleBeginEdit('photo');
  window.mindleNewProject();
  assert.equal(window.mindleInputFor('photo'), photo, 'pending photo must stay in its project');
  const before = calls.length;
  await window.mindleOpenProject('another-project');
  assert.equal(calls.length, before, 'no project fetch may race the active edit');
  window.mindleEndEdit('photo');
  window.mindleNewProject();
  assert.equal(window.mindleInputFor('photo'), null);
});

test('save response cannot attach the old project to a new project', async () => {
  const {window, editors, calls, pendingSave, startSave} = await setup();
  const photo = window.mindleInputFor('photo');
  const saving = startSave();
  await new Promise(setImmediate);
  window.mindleNewProject();
  assert.equal(window.mindleInputFor('photo'), photo, 'new project must wait for the save response');
  pendingSave.resolve();
  await saving;
  window.mindleNewProject();
  await editors.photo.dispatchEvent({type: 'mindle:save'});
  const saves = calls.filter(c => c.url === '/api/projects/save');
  assert.equal(JSON.parse(saves.at(-1).options.body).project_id, null);
});

test('rejected duplicate save/export does not unlock the active save', async () => {
  const {window, editors, calls, pendingSave, startSave} = await setup();
  const saving = startSave();
  await new Promise(setImmediate);
  await editors.video.dispatchEvent({type: 'mindle:save'});
  await editors.video.dispatchEvent({type: 'mindle:export'});
  assert.equal(window.mindleNewProject(), false);
  assert.equal(calls.filter(c => c.url === '/api/projects/save').length, 1);
  pendingSave.resolve();
  await saving;
  assert.equal(window.mindleNewProject(), true);
});

test('in-flight restore excludes new/open/save and releases its guard when no project exists', async () => {
  const {window, editors, calls, pendingRestore, startRestore} = await setup();
  const restoring = startRestore();
  const before = calls.length;
  assert.equal(window.mindleNewProject(), false);
  assert.equal(await window.mindleOpenProject('second-project'), false);
  await editors.photo.dispatchEvent({type: 'mindle:save'});
  assert.equal(calls.length, before);
  pendingRestore.resolve();
  assert.equal(await restoring, false);
  assert.equal(window.mindleNewProject(), true);
});

test('rejected duplicate export cannot release the first export transition guard', async () => {
  const {window, editors, calls, pendingExport, startExport} = await setup();
  const exporting = startExport();
  await new Promise(setImmediate);
  await editors.video.dispatchEvent({type: 'mindle:export'});
  assert.equal(window.mindleNewProject(), false);
  assert.equal(calls.filter(c => c.url.endsWith('/export')).length, 1);
  pendingExport.resolve();
  await exporting;
  assert.equal(window.mindleNewProject(), true);
});

for(const dependency of ['preview','reference','audio']) {
  test(`failed ${dependency} restore preserves the previous input, preview, project and jobs`, async () => {
    const job={job_id:'replacement',lane:'photo',operation:'import',preview_url:'/replacement.png',
      primary_output:{file_name:'replacement.png',sha256:'new'},runtime_result:{options:{}}};
    const routes={
      '/api/projects/broken':{ok:true,json:async()=>({project:{project_id:'broken',job_ids:['replacement'],jobs:[job],
        workspace:{references:{photo:dependency==='reference'?[{url:'/missing',name:'ref.png'}]:[],video:[]},
          audio:dependency==='audio'?{url:'/missing',original_filename:'voice.wav'}:null}}})},
      '/missing':{ok:false},
    };
    if(dependency==='preview') routes['/replacement.png']={ok:false};
    const {window,editors,calls}=await setup(routes);
    await editors.photo.dispatchEvent({type:'mindle:save'});
    const input=window.mindleInputFor('photo');
    const preview=editors.photo.querySelector('[data-preview]').children[0];
    assert.equal(await window.mindleOpenProject('broken'),false);
    assert.equal(window.mindleInputFor('photo'),input);
    assert.equal(editors.photo.querySelector('[data-preview]').children[0],preview);
    await editors.photo.dispatchEvent({type:'mindle:save'});
    const body=JSON.parse(calls.filter(c=>c.url==='/api/projects/save').at(-1).options.body);
    assert.equal(body.project_id,'saved-project');
    assert.deepEqual(body.job_ids,['existing-photo']);
    assert.equal(window.mindleNewProject(),true,'failure releases transition guard');
  });
}

test('successful staged restore uses the actual output filename', async () => {
  const job={job_id:'replacement',lane:'photo',operation:'photo_edit',preview_url:'/output.png',
    input:{file_name:'original.jpg'},primary_output:{file_name:'edited.png',sha256:'output'},runtime_result:{options:{}}};
  const {window,editors}=await setup({'/api/projects/complete':{ok:true,json:async()=>({project:{
    project_id:'complete',job_ids:['replacement'],jobs:[job],workspace:{references:{photo:[],video:[]},audio:null}}})}});
  assert.equal(await window.mindleOpenProject('complete'),true);
  assert.equal(window.mindleInputFor('photo').name,'edited.png');
  assert.equal(window.mindleInputFor('video'),null);
  assert.equal(editors.photo.dataset.projectStatus,'reopened');
});
