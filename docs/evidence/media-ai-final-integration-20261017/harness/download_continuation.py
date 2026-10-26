import sys,asyncio,threading,json,zipfile,hashlib
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[2];repo=Path(__file__).parent/'source';out=R/'outputs/FINAL_INTEGRATION_20261017_R1/DOWNLOAD_CONTROL_DIAG';out.mkdir(exist_ok=False)
sys.path.insert(0,str(repo/'src'));sys.path.append(str(R/'work/site-packages'))
from media_ai.product_server import create_server
s=create_server(repo,R/'outputs/FINAL_BOUNDARIES_20261017_AFTER_R1/data','',0);th=threading.Thread(target=s.serve_forever,daemon=True);th.start()
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(channel='chrome',headless=False,downloads_path=str(out/'browser_downloads'))
  p=await browser.new_page(accept_downloads=True,viewport={'width':1536,'height':1024});await p.goto(f'http://127.0.0.1:{s.server_port}');await p.wait_for_function('window.mindleRestoreReady')
  async with p.expect_download() as dd:await p.locator('[data-editor="photo"] [data-action="export"]').click()
  dl=await dd.value;path=out/'ACTUAL_UI_EXPORT.zip'
  result={'browser':browser.version,'scope':'SAME_SAVED_SOURCE_PROJECT_CONTINUATION_NOT_PC_PACKAGE','changed_test_condition':'Playwright downloads_path explicitly set to permitted evidence workspace; product unmodified','identity':s.runtime_identity(),'url':dl.url,'suggested_filename':dl.suggested_filename}
  try:
   await dl.save_as(path)
   with zipfile.ZipFile(path) as z:assert z.testzip() is None
   result.update(status='PASS',bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),crc='PASS')
  except Exception as e:result.update(status='BLOCKED',error=str(e),failure=await dl.failure())
  (s.data_dir/'download_control.txt').write_text('Acceptance download control; no media engine',encoding='utf-8')
  async with p.expect_download() as dd:
   await p.evaluate("()=>{const a=document.createElement('a');a.href='/files/download_control.txt';a.download='download_control.txt';document.body.append(a);a.click();a.remove()}")
  control=await dd.value
  try:await control.save_as(out/'download_control.txt');result['plain_text_control']={'status':'PASS'}
  except Exception as e:result['plain_text_control']={'status':'BLOCKED','failure':await control.failure(),'error':str(e)}
  (out/'RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':result['status'],'error':result.get('error'),'control':result['plain_text_control']}));await browser.close()
try:asyncio.run(main())
finally:s.shutdown();s.server_close();th.join(5)
