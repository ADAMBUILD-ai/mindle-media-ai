"""Run pinned SAM 2.1 on five CC/PD Wikimedia architecture fixtures."""
import hashlib, json, os, time
from pathlib import Path
import torch
from PIL import Image
from transformers import AutoModelForMaskGeneration, AutoProcessor

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
BASE = Path(__file__).parent / "artifacts"
FIXTURES, OUT = BASE / "public_architecture_fixtures", BASE / "sam21_live"
REPO, REV = "facebook/sam2.1-hiera-base-plus", "b7320756a13354e7530a63935656d35b2f91a290"
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
  OUT.mkdir(parents=True, exist_ok=True); manifest=json.loads((FIXTURES / "manifest.json").read_text())
  processor=AutoProcessor.from_pretrained(REPO, revision=REV); model=AutoModelForMaskGeneration.from_pretrained(REPO, revision=REV).eval(); rows=[]
  for fixture in manifest["fixtures"]:
    image=Image.open(FIXTURES / fixture["file"]).convert("RGB"); image.thumbnail((768,768)); x,y=image.width//2,image.height//2
    inputs=processor(images=image,input_points=[[[[x,y]]]],return_tensors="pt"); start=time.perf_counter()
    with torch.no_grad(): result=model(**inputs)
    index=int(result.iou_scores[0,0].argmax().item()); raw=result.pred_masks[0,0,index][None,None]
    mask=torch.nn.functional.interpolate(raw,size=(image.height,image.width),mode="bilinear",align_corners=False)[0,0]
    out=OUT / fixture["file"].replace(".jpg","_mask.png"); Image.fromarray((mask.cpu().numpy()>0).astype("uint8")*255).save(out)
    rows.append({"fixture":fixture,"input_sha256":digest(FIXTURES/fixture["file"]),"mask_sha256":digest(out),"duration_ms":round((time.perf_counter()-start)*1000,2),"selected_mask_index":index})
  evidence={"status":"LIVE_FUNCTIONAL_BENCHMARK_COMPLETE","repo_id":REPO,"revision":REV,"runtime":{"torch":torch.__version__,"provider":"CPU"},"fixture_manifest":"../public_architecture_fixtures/manifest.json","runs":rows,"quality_gate":"VERIFY_REQUIRED: mask outputs and latency are recorded; object-level human quality review is still required before adapter enablement."}
  (OUT/"result.json").write_text(json.dumps(evidence,indent=2)+"\n"); print(json.dumps(evidence,indent=2))
if __name__=="__main__": main()
