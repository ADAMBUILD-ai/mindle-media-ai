const {chromium}=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/playwright');const fs=require('node:fs');const path=require('node:path');
(async()=>{
 const out=process.argv[2],fix=process.argv[3];fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch({executablePath:path.resolve('browser-test-runtime/chromium'),headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 const results=[];
 for(const [w,h] of [[1536,1024],[1920,1080],[1366,768]]){
  const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('http://127.0.0.1:18987');await p.waitForFunction(()=>window.mindleRestoreReady===true);
  if(fix)await p.addStyleTag({content:fs.readFileSync(fix,'utf8')});
  await p.evaluate(()=>{
   for(const kind of ['video','photo']){
    const e=document.querySelector(`[data-editor=${kind}]`),g=e.querySelector('.asset-grid');g.replaceChildren();
    for(let i=0;i<(kind==='video'?14:12);i++){const s=document.createElement('span');s.textContent=kind==='video'?'video_original.mp4':'portrait_autofit.png';s.tabIndex=0;g.append(s);}
    const host=e.querySelector('[data-preview]');host.replaceChildren();const img=kind==='video'?document.createElement('video'):new Image();const c=document.createElement('canvas');c.width=kind==='photo'?480:672;c.height=kind==='photo'?960:384;const ctx=c.getContext('2d');ctx.fillStyle='#41698d';ctx.fillRect(0,0,c.width,c.height);ctx.strokeStyle='white';ctx.lineWidth=12;ctx.strokeRect(6,6,c.width-12,c.height-12);img.src=kind==='video'?'/files/probe.mp4':c.toDataURL();host.append(img);
    e.querySelector('.command-card').dataset.phase='expanded';e.querySelector('[data-command-error]').textContent='저장된 프로젝트를 다시 열었습니다 · '+('검수 결과 '.repeat(35));
    const list=e.querySelector('[data-reference-list]');for(let i=0;i<2;i++){const li=document.createElement('li');li.textContent='reference_photo.png';list.append(li);}
   }
  });
  await p.waitForFunction(()=>document.querySelector('[data-preview=video] video').videoWidth>0);
  const data=await p.evaluate(()=>({viewport:{width:innerWidth,height:innerHeight},documentHeight:document.documentElement.scrollHeight,lanes:[...document.querySelectorAll('[data-editor]')].map(e=>{const r=e.getBoundingClientRect(),a=e.querySelector('.asset-grid'),input=e.querySelector('[data-command]'),i=input.getBoundingClientRect(),host=e.querySelector('[data-preview]'),media=host.querySelector('img,video'),m=media.getBoundingClientRect(),s=host.getBoundingClientRect();return {kind:e.dataset.editor,cardHeight:r.height,bottom:r.bottom,commandBottom:i.bottom,assetClientHeight:a.clientHeight,assetScrollHeight:a.scrollHeight,assetOverflow:getComputedStyle(a).overflowY,preview:{width:s.width,height:s.height},media:{width:m.width,height:m.height,objectFit:getComputedStyle(media).objectFit},sevenSliders:e.querySelectorAll('[data-photo-adjust]').length}})}));
  for(const kind of ['video','photo']){const e=p.locator(`[data-editor=${kind}]`);await e.locator('[data-command]').scrollIntoViewIfNeeded();if(!await e.locator('[data-command]').isVisible())throw Error('command inaccessible');const a=e.locator('.asset-grid');await a.evaluate(el=>{el.scrollTop=el.scrollHeight});const last=a.locator('span').last();await last.scrollIntoViewIfNeeded();if(!await last.isVisible())throw Error('last asset inaccessible');const q=await last.boundingBox(),z=await a.boundingBox();if(q.y<z.y-1||q.y+q.height>z.y+z.height+1)throw Error('last asset clipped by library');}
  results.push(data);await p.screenshot({path:path.join(out,`${w}x${h}.png`),fullPage:true});await p.close();
 }
 await b.close();fs.writeFileSync(path.join(out,'GEOMETRY.json'),JSON.stringify({scope:'REAL_LINUX_CHROMIUM_PRODUCTION_HTML_CSS_SYNTHETIC_ASSET_DENSITY_NO_MODELS',browser:'138.0.7204.0',font:'NotoSansCJKkr-Regular; not Windows Malgun',results},null,2));console.log(JSON.stringify(results.map(x=>({viewport:x.viewport,lanes:x.lanes.map(l=>({kind:l.kind,bottom:l.bottom,commandBottom:l.commandBottom,assets:l.assetClientHeight,assetScroll:l.assetScrollHeight,overflow:l.assetOverflow}))}))));
})().catch(e=>{console.error(e);process.exit(1)});
