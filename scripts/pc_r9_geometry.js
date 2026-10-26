/* Evaluate this expression in the already controlled PC product page.
   Read-only: no styles, media, project, server or model state is changed. */
(() => {
  const box = el => {
    if (!el) return null;
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return {x:r.x,y:r.y,width:r.width,height:r.height,clientWidth:el.clientWidth,
      clientHeight:el.clientHeight,scrollWidth:el.scrollWidth,scrollHeight:el.scrollHeight,
      css:Object.fromEntries(['display','width','height','min-width','min-height','max-width',
        'max-height','object-fit','object-position','overflow','grid-template-rows',
        'align-items','justify-items','transform','zoom'].map(k=>[k,s.getPropertyValue(k)]))};
  };
  const host=document.querySelector('[data-preview="photo"]'), image=host?.querySelector('img');
  const video=document.querySelector('[data-preview="video"] video');
  return {scope:'PC_R9_READ_ONLY_DOM_GEOMETRY',captured_at:new Date().toISOString(),
    url:location.href,title:document.title,viewport:{width:innerWidth,height:innerHeight,
      dpr:devicePixelRatio,visualScale:visualViewport?.scale},
    stylesheets:[...document.querySelectorAll('link[rel="stylesheet"]')].map(x=>x.href),
    ui_contract:document.body.dataset.uiContract,photo_host:box(host),photo_image:box(image),
    photo_source:image?{naturalWidth:image.naturalWidth,naturalHeight:image.naturalHeight,
      complete:image.complete,currentSrc:image.currentSrc}:null,
    video:video?{MediaError_code:video.error?.code??null,readyState:video.readyState,
      videoWidth:video.videoWidth,currentSrc:video.currentSrc,currentTime:video.currentTime}:null,
    owner_pc_pass:false,full_product_pass:false};
})()
