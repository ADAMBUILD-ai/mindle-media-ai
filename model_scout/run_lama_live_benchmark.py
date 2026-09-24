"""Pinned LaMa ONNX vs TELEA A/B on CC/PD architecture fixtures."""
import hashlib, json, time
from pathlib import Path
import cv2, numpy as np, onnxruntime as ort
from PIL import Image, ImageDraw

BASE=Path(__file__).parent/"artifacts"; FIX=BASE/"public_architecture_fixtures"; OUT=BASE/"lama_live"; MODEL=BASE/"lama"/"inpainting_lama_2025jan.onnx"
REPO="opencv/inpainting_lama"; REV="aee6d22f0a13e5e35af1c9a1c3afd62841fc6f3f"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
  OUT.mkdir(parents=True,exist_ok=True); manifest=json.loads((FIX/"manifest.json").read_text()); session=ort.InferenceSession(str(MODEL),providers=["CPUExecutionProvider"]); rows=[]
  for i, fixture in enumerate(manifest["fixtures"]):
    image=Image.open(FIX/fixture["file"]).convert("RGB").resize((512,512)); mask=Image.new("L",(512,512),0); x=184+(i%2)*20; ImageDraw.Draw(mask).rectangle((x,210,x+120,300),fill=255)
    input_path=OUT/f"{i+1:02d}_input.png"; mask_path=OUT/f"{i+1:02d}_mask.png"; lama_path=OUT/f"{i+1:02d}_lama.png"; telea_path=OUT/f"{i+1:02d}_telea.png"; image.save(input_path); mask.save(mask_path)
    it=np.asarray(image,dtype=np.float32).transpose(2,0,1)[None]/127.5-1; mt=np.asarray(mask,dtype=np.float32)[None,None]/255
    start=time.perf_counter(); result=session.run(None,{"image":it,"mask":mt})[0]; lama_ms=round((time.perf_counter()-start)*1000,2)
    Image.fromarray(np.clip((result[0].transpose(1,2,0)+1)*127.5,0,255).astype(np.uint8)).save(lama_path)
    start=time.perf_counter(); telea=cv2.inpaint(cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR),np.asarray(mask),3,cv2.INPAINT_TELEA); telea_ms=round((time.perf_counter()-start)*1000,2); Image.fromarray(cv2.cvtColor(telea,cv2.COLOR_BGR2RGB)).save(telea_path)
    rows.append({"fixture":fixture,"input_sha256":sha(input_path),"mask_sha256":sha(mask_path),"lama_output_sha256":sha(lama_path),"telea_output_sha256":sha(telea_path),"lama_ms":lama_ms,"telea_ms":telea_ms,"note":"Fixed central rectangle mask; human review of architectural lines, texture and artifacts is still required."})
  e={"status":"LIVE_FUNCTIONAL_BENCHMARK_COMPLETE","repo_id":REPO,"revision":REV,"model_sha256":sha(MODEL),"runtime":{"onnxruntime":ort.__version__,"provider":"CPUExecutionProvider"},"fixture_manifest":"../public_architecture_fixtures/manifest.json","runs":rows,"quality_gate":"VERIFY_REQUIRED: 5 real-image A/B outputs and runtimes are recorded; no human architecture-quality approval has been given."}; (OUT/"result.json").write_text(json.dumps(e,indent=2)+"\n"); print(json.dumps(e,indent=2))
if __name__=="__main__": main()
