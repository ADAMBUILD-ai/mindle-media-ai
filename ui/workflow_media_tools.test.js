const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8');
const source=fs.readFileSync(path.join(__dirname,'workflow_execution.js'),'utf8');

for(const word of ['자르기','속도','비율','BGM','자막','나레이션'])assert.ok(html.includes(word),`missing AI command hint: ${word}`);
for(const contract of ['backgroundVolume','BGM 작업을 실행하려면','validated_edit_values','로컬 생성형 계획'])assert.ok(source.includes(contract),`missing workflow contract: ${contract}`);
for(const contract of ['needsAudioFinish','finish_workflow_id','건축 AI 음성·BGM 마감','task.receipt.job_id'])assert.ok(source.includes(contract),`missing architecture finish chain: ${contract}`);
