/* Local photo controls: adjustments are rendered to actual pixels before persistence. */
(() => {
  const editor = document.querySelector('[data-editor="photo"]');
  const status = editor.querySelector('[data-photo-status]');
  let rotation = 0, flipH = false, flipV = false, style = 'neutral';
  let busy = false;
  const say = text => { status.textContent = text; };
  const controls = () => Object.fromEntries([...editor.querySelectorAll('[data-photo-adjust]')].map(input => [input.dataset.photoAdjust, Number(input.value)]));
  editor.querySelectorAll('[data-photo-adjust]').forEach(input => input.addEventListener('input', () => {
    input.nextElementSibling.value = input.value;
    const image = editor.querySelector('[data-preview] img');
    const v = controls();
    if (image) image.style.filter = `brightness(${1+v.brightness/100}) contrast(${1+v.contrast/100}) saturate(${1+v.saturation/100})`;
    say('보정 미리보기 · 적용하기를 누르면 실제 결과가 저장됩니다.');
  }));
  async function renderPhoto() {
    const image = editor.querySelector('[data-preview] img');
    if (!image || !image.complete || !image.naturalWidth) throw new Error('먼저 사진을 불러오세요.');
    const canvas = document.createElement('canvas');
    const cropVisible = !editor.querySelector('[data-crop-controls]').hidden;
    const crop = Object.fromEntries([...editor.querySelectorAll('[data-crop]')].map(input => [input.dataset.crop, Number(input.value)]));
    if (cropVisible && (crop.left < 0 || crop.top < 0 || crop.right > 100 || crop.bottom > 100 || crop.left >= crop.right || crop.top >= crop.bottom)) throw new Error('크롭 범위를 확인하세요.');
    const x = cropVisible ? Math.round(image.naturalWidth * crop.left / 100) : 0;
    const y = cropVisible ? Math.round(image.naturalHeight * crop.top / 100) : 0;
    const w = cropVisible ? Math.round(image.naturalWidth * (crop.right-crop.left)/100) : image.naturalWidth;
    const h = cropVisible ? Math.round(image.naturalHeight * (crop.bottom-crop.top)/100) : image.naturalHeight;
    if (!w || !h) throw new Error('크롭 결과가 너무 작습니다.');
    canvas.width = rotation % 180 ? h : w; canvas.height = rotation % 180 ? w : h;
    const ctx = canvas.getContext('2d');
    ctx.translate(canvas.width/2, canvas.height/2); ctx.rotate(rotation*Math.PI/180); ctx.scale(flipH?-1:1,flipV?-1:1);
    ctx.drawImage(image,x,y,w,h,-w/2,-h/2,w,h); ctx.setTransform(1,0,0,1,0,0);
    const v = controls(), pixels = ctx.getImageData(0,0,canvas.width,canvas.height), d = pixels.data;
    const contrast = Math.max(0,1+v.contrast/100), saturation = Math.max(0,1+v.saturation/100);
    for (let i=0;i<d.length;i+=4) {
      let r=d[i],g=d[i+1],b=d[i+2], l=.2126*r+.7152*g+.0722*b;
      const tone = v.shadows*.6*(1-l/255)**2 + v.highlights*.6*(l/255)**2;
      r=(r-128)*contrast+128+v.brightness*.7+tone+v.temperature*.3;
      g=(g-128)*contrast+128+v.brightness*.7+tone;
      b=(b-128)*contrast+128+v.brightness*.7+tone-v.temperature*.3;
      l=.2126*r+.7152*g+.0722*b;
      r=l+(r-l)*saturation;g=l+(g-l)*saturation;b=l+(b-l)*saturation;
      if(style==='mono') r=g=b=l;
      if(style==='warm') { r+=12;b-=10; }
      d[i]=r;d[i+1]=g;d[i+2]=b;
    }
    if(v.sharpness) {
      const source=new Uint8ClampedArray(d), stride=canvas.width*4, amount=v.sharpness/100;
      for(let y=1;y<canvas.height-1;y++) for(let x=1;x<canvas.width-1;x++) {
        const p=y*stride+x*4;
        for(let c=0;c<3;c++) d[p+c]=source[p+c]+amount*(source[p+c]-(source[p-stride+c]+source[p+stride+c]+source[p-4+c]+source[p+4+c])/4);
      }
    }
    ctx.putImageData(pixels,0,0);
    let output=canvas;
    let resizeWidth=null;
    if(!editor.querySelector('[data-photo-resize-controls]').hidden) {
      resizeWidth=Number(editor.querySelector('[data-photo-resize]').value);
      if(!Number.isInteger(resizeWidth)||resizeWidth<1||resizeWidth>8000) throw new Error('사진 폭은 1~8000 px 범위입니다.');
      output=document.createElement('canvas');output.width=resizeWidth;output.height=Math.max(1,Math.round(canvas.height*resizeWidth/canvas.width));output.getContext('2d').drawImage(canvas,0,0,output.width,output.height);
    }
    return {base64:output.toDataURL('image/png').split(',')[1], options:{...v,rotation,flipH,flipV,style,resizeWidth,crop:cropVisible?crop:null}};
  }
  function reset() {
    editor.querySelectorAll('[data-photo-adjust]').forEach(input => { input.value=0;input.nextElementSibling.value=0; });
    rotation=0;flipH=flipV=false;style='neutral';editor.querySelector('[data-crop-controls]').hidden=true;editor.querySelector('[data-photo-resize-controls]').hidden=true;
    const image=editor.querySelector('[data-preview] img');if(image) image.style.filter='';
  }
  async function apply(label='사진 보정') {
    if(busy) return;busy=true;say('보정을 적용하고 있습니다.');
    try {
      const rendered=await renderPhoto();
      const response=await fetch('/api/photo-edits',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:'photo_edit.png',content_base64:rendered.base64,command:label,options:rendered.options})});
      const result=await response.json();if(!response.ok) throw new Error(result.error||'사진 보정 저장 실패');
      document.dispatchEvent(new CustomEvent('mindle:photo-result',{detail:result}));reset();say('보정 적용 완료 · 프로젝트 저장으로 보관할 수 있습니다.');
    } catch(error) {say(error.message);} finally {busy=false;}
  }
  const adjust=(key,value)=>{const input=editor.querySelector(`[data-photo-adjust="${key}"]`);input.value=value;input.nextElementSibling.value=value;};
  editor.querySelector('[data-photo-apply]').addEventListener('click',()=>apply());
  editor.querySelector('[data-photo-reset]').addEventListener('click',()=>{reset();say('보정 설정을 초기화했습니다.');});
  function command(text) {
    editor.dispatchEvent(new CustomEvent('mindle:command',{detail:{command:text}}));
  }
  async function tool(key) {
    if(key==='crop') {editor.querySelector('[data-crop-controls]').hidden=false;say('크롭 범위를 지정한 뒤 적용하기를 누르세요.');return;}
    if(key==='resize') {const image=editor.querySelector('[data-preview] img');if(!image?.naturalWidth) {say('먼저 사진을 불러오세요.');return;}editor.querySelector('[data-photo-resize-controls]').hidden=false;editor.querySelector('[data-photo-resize]').value=image.naturalWidth;say('원하는 폭을 입력하고 적용하기를 누르세요.');return;}
    if(key==='rotate') rotation=(rotation+90)%360;
    if(key==='flip-h') flipH=!flipH;
    if(key==='flip-v') flipV=!flipV;
    if(key==='auto') {adjust('contrast',8);adjust('saturation',8);adjust('shadows',12);}
    if(key==='color') {adjust('temperature',15);adjust('saturation',10);}
    if(key==='style') style=style==='mono'?'warm':'mono';
    if(key==='portrait') {adjust('shadows',10);adjust('sharpness',-25);say('인물 보정은 그림자 완화와 전체 사진의 부드럽게 보정을 적용합니다.');}
    if(key==='segment') {command('배경을 제거해줘');return;}
    if(key==='upscale') {command('4배 업스케일해줘');return;}
    if(key==='similar') {
      const image=editor.querySelector('[data-preview] img');
      if(!image?.naturalWidth) {say('먼저 사진을 불러오세요.');return;}
      if(!photoCommand.references.length) {say('참고 이미지를 첨부하면 현재 사진과 색감이 유사한 순서로 검색합니다.');return;}
      const signature=img=>{const c=document.createElement('canvas');c.width=c.height=16;const ctx=c.getContext('2d');ctx.drawImage(img,0,0,16,16);const pixels=ctx.getImageData(0,0,16,16).data;const bins=new Array(24).fill(0);for(let i=0;i<pixels.length;i+=4) for(let k=0;k<3;k++) bins[k*8+Math.min(7,pixels[i+k]>>5)]++;return bins;};
      const target=signature(image), matches=[];
      for(const ref of photoCommand.references) {
        const img=new Image();img.src=ref.preview;try {await img.decode();const bins=signature(img);matches.push({name:ref.name,distance:bins.reduce((sum,v,i)=>sum+(v-target[i])**2,0)});} catch(_) {}
      }
      matches.sort((a,b)=>a.distance-b.distance);
      say('첨부 참고 이미지 색감 유사도 순서: '+matches.map(item=>item.name).join(' → '));return;
    }
    await apply(key==='auto'?'자동 사진 보정':key);
  }
  editor.querySelectorAll('[data-photo-tool]').forEach(button=>button.addEventListener('click',()=>tool(button.dataset.photoTool)));
  editor.querySelector('[data-action="photo-generate"]').addEventListener('click',()=>say('현재 패키지에는 이미지 생성 모델이 포함돼 있지 않습니다. 사진 보정과 배경 제거는 계속 사용할 수 있습니다.'));
  editor.querySelectorAll('[data-action="photo-auto"]').forEach(button=>button.addEventListener('click',()=>tool('auto')));
  window.mindlePhotoCommand=async text=>{
    if(/배경|분리|세그먼트|업스케일|고화질|해상도|4배|4x/i.test(text)) return false;
    let known=false;
    if(/따뜻|노을/.test(text)) {adjust('temperature',20);known=true;}
    if(/차갑/.test(text)) {adjust('temperature',-20);known=true;}
    if(/밝게|밝기/.test(text)) {adjust('brightness',15);known=true;}
    if(/어둡/.test(text)) {adjust('brightness',-15);known=true;}
    if(/선명/.test(text)) {adjust('sharpness',25);known=true;}
    if(/흑백/.test(text)) {style='mono';known=true;}
    if(/보정/.test(text) && !known) {adjust('contrast',8);adjust('shadows',12);known=true;}
    if(known) await apply('AI 대화 편집 · '+text);
    else say('지원하는 사진 지시: 따뜻하게·차갑게·밝게·어둡게·선명하게·흑백·배경 제거·4배 업스케일');
    return true;
  };
})();
