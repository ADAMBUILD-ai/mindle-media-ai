"""Source-only Chrome geometry comparison, no server/model/Windows PASS."""
import base64
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/r9-source-regression'
CANDIDATE='[data-preview="photo"] > img { position:absolute; inset:0; width:100%; height:100%; min-width:0; min-height:0; max-width:100%; max-height:100%; object-fit:contain; object-position:center; }'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    html=(ROOT/'ui/index.html').read_text()
    html=re.sub(r'<script\b[^>]*>.*?</script>','',html,flags=re.S)
    html=re.sub(r'<link\b[^>]*>','',html)
    css='\n'.join((ROOT/'ui'/p).read_text() for p in ('approved_visual.css','interaction.css'))
    rows=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='chrome',headless=True)
        for width in (1280,1536):
            for shape,w,h in (('portrait',900,1600),('landscape',1600,900),('square',1000,1000)):
                for variant in ('baseline','candidate'):
                    page=browser.new_page(viewport={'width':width,'height':1024})
                    page.set_content(html)
                    page.add_style_tag(content=css)
                    if variant=='candidate':page.add_style_tag(content=CANDIDATE)
                    host=page.locator('[data-preview="photo"]')
                    empty=host.bounding_box()
                    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="orange"/><rect x="2" y="2" width="{w-4}" height="{h-4}" fill="none" stroke="lime" stroke-width="8"/></svg>'
                    src='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
                    host.evaluate('(host,src)=>{const img=new Image();img.src=src;host.replaceChildren(img)}',src)
                    page.locator('[data-preview="photo"] img').evaluate('img=>img.decode()')
                    measure=host.evaluate('''host=>{const img=host.querySelector('img'),a=host.getBoundingClientRect(),b=img.getBoundingClientRect(),s=getComputedStyle(img);
                        const scale=Math.min(img.clientWidth/img.naturalWidth,img.clientHeight/img.naturalHeight);
                        const iw=img.naturalWidth*scale,ih=img.naturalHeight*scale;
                        return {host:{x:a.x,y:a.y,width:a.width,height:a.height},image:{x:b.x,y:b.y,width:b.width,height:b.height},
                          fit:s.objectFit,position:s.objectPosition,natural:[img.naturalWidth,img.naturalHeight],
                          artwork:{x:b.x+(b.width-iw)/2,y:b.y+(b.height-ih)/2,width:iw,height:ih}}}''')
                    a=measure['host'];art=measure['artwork']
                    stable=abs(a['height']-empty['height'])<1 and abs(a['width']-empty['width'])<1
                    contained=art['x']>=a['x']-1 and art['y']>=a['y']-1 and art['x']+art['width']<=a['x']+a['width']+1 and art['y']+art['height']<=a['y']+a['height']+1
                    row={'viewport':width,'shape':shape,'variant':variant,'empty':empty,**measure,'stable_stage':stable,'contained':contained,'pass':stable and contained and measure['fit']=='contain'}
                    rows.append(row)
                    page.screenshot(path=str(OUT/f'{width}-{shape}-{variant}.png'),full_page=True)
                    page.close()
        browser_version=browser.version
        browser.close()
    result={'scope':'LINUX_CHROME_SOURCE_GEOMETRY_ONLY','browser':browser_version,'rows':rows,
            'baseline_failures':sum(not r['pass'] for r in rows if r['variant']=='baseline'),
            'candidate_failures':sum(not r['pass'] for r in rows if r['variant']=='candidate'),
            'candidate_css':CANDIDATE,'owner_pc_pass':False,'full_product_pass':False}
    (OUT/'PHOTO_GEOMETRY_MATRIX.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    return int(result['candidate_failures']>0)


if __name__=='__main__':raise SystemExit(main())
