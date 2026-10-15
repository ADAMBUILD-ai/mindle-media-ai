// Runtime routing regression; isolated DOM harness, no browser or product PASS.
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, 'workspace_shell.js'), 'utf8');

function harness(key) {
  const dialogs = [], requests = [];
  let click;
  const button = {dataset:{shell:key},addEventListener:(_, fn)=>{click=fn;}};
  const node = () => ({children:[],append(...values){this.children.push(...values);},
    addEventListener(){},showModal(){dialogs.push(this);},close(){},remove(){}});
  const document = {
    createElement:node,body:node(),
    querySelectorAll:()=>[button],
    querySelector:()=>({addEventListener(){},querySelectorAll:()=>[]})
  };
  vm.runInNewContext(source,{document,window:{},fetch:async url=>{
    requests.push(url);return {ok:true,json:async()=>({data_root:'LOCAL_TEST',projects:[]})};
  }});
  return {click:()=>click(),dialogs,requests};
}

test('cloud reports absent external integration without requesting local projects',async()=>{
  const h=harness('cloud');await h.click();
  assert.deepEqual(h.requests,[]);
  assert.equal(h.dialogs[0].children[0].textContent,'클라우드 연동 미완료');
});
test('local storage keeps its original project API route',async()=>{
  const h=harness('storage');await h.click();
  assert.deepEqual(h.requests,['/api/projects']);
  assert.equal(h.dialogs[0].children[0].textContent,'저장소');
});
test('approved cloud label remains and is routed separately from settings',()=>{
  const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
  assert.match(html,/data-shell="cloud">☁ 클라우드/);
  assert.match(html,/data-shell="storage">⚙/);
});
