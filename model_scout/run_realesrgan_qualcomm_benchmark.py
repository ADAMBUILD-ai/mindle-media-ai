"""Run Qualcomm's pinned Real-ESRGAN ONNX package against Lanczos4 on five fixtures."""
import hashlib, json, time
from pathlib import Path
import numpy as np, onnxruntime as ort
from PIL import Image
BASE=Path(__file__).parent/"artifacts"; FIX=BASE/"public_architecture_fixtures"; ROOT=BASE/"realesrgan_qualcomm"; MODEL=ROOT/"real_esrgan_x4plus-onnx-float"/"real_esrgan_x4plus.onnx"; OUT=ROOT/"benchmark"
REPO="qualcomm/Real-ESRGAN-x4plus"; REV="4022efb8b74eb88900724d9e05a468ac3673df4a"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True); fixtures=json.loads((FIX/"manifest.json").read_text())["fixtures"]; session=ort.InferenceSession(str(MODEL),providers=["CPUExecutionProvider"]); runs=[]
 for i,fixture in enumerate(fixtures,1):
  src=Image.open(FIX/fixture["file"]).convert("RGB"); src.thumbnail((128,128)); src=src.resize((128,128)); inp=OUT/f"{i:02d}_input_128.png"; src.save(inp); x=np.asarray(src,dtype=np.float32).transpose(2,0,1)[None]/255
  start=time.perf_counter(); y=session.run(None,{"image":x})[0]; ms=round((time.perf_counter()-start)*1000,2); model_out=OUT/f"{i:02d}_realesrgan_4x.png"; Image.fromarray(np.clip(y[0].transpose(1,2,0)*255,0,255).astype(np.uint8)).save(model_out)
  baseline=OUT/f"{i:02d}_lanczos4_4x.png"; src.resize((512,512),Image.Resampling.LANCZOS).save(baseline)
  runs.append({"fixture":fixture,"input_sha256":sha(inp),"output_sha256":sha(model_out),"lanczos4_sha256":sha(baseline),"latency_ms":ms,"human_review":{"status":"REVIEW_REQUIRED","defect_type":None,"reviewer_note":None}})
 e={"status":"ACTUAL_WEIGHT_INFERENCE_FIVE_FIXTURES_COMPLETE","repo_id":REPO,"revision":REV,"declared_license":"bsd-3-clause","provenance":"Qualcomm HF release_assets.json pinned to the ONNX float release URL","model_sha256":sha(MODEL),"data_sha256":sha(MODEL.with_suffix('.data')),"runtime":{"onnxruntime":ort.__version__,"provider":"CPUExecutionProvider"},"runs":runs,"quality_gate":"VERIFY_REQUIRED: five actual inferences and Lanczos4 A/B outputs exist; human review of straight lines, text, texture, halo/ringing and hallucinated detail is required before KEEP."}; (OUT/"result.json").write_text(json.dumps(e,indent=2)+"\n");print(json.dumps(e,indent=2))
if __name__=='__main__':main()
