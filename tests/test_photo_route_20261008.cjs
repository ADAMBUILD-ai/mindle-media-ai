const fs=require('fs'),vm=require('vm'),assert=require('assert');
const code=fs.readFileSync(require('path').join(__dirname,'../ui/photo_workspace.js'),'utf8');
const node={addEventListener(){},hidden:true,value:0,nextElementSibling:{value:0}};
const editor={querySelector(){return node},querySelectorAll(){return []}};
const context={document:{querySelector(){return editor}},window:{},photoCommand:{references:[]}};
vm.runInNewContext(code,context);
(async()=>{
 for(const command of ['왼쪽 인물을 실제로 분할해줘','배경을 제거해줘','사진을 실제 4배 업스케일해줘']) {
  assert.equal(await context.window.mindlePhotoCommand(command),false,command);
 }
 assert.equal(await context.window.mindlePhotoCommand('지원하지 않는 명령'),true);
 console.log('PASS: 3 model commands reach model router; unsupported command stays handled');
})().catch(e=>{console.error(e);process.exitCode=1});
