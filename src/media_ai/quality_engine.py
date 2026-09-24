"""OpenCV quality path. It is separate from Pillow fallback and always records its mode."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

def _cv(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(image.convert('RGB')), cv2.COLOR_RGB2BGR)
def _pil(array: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(array, cv2.COLOR_BGR2RGB))

def straighten(image: Image.Image, conservative: bool = True) -> tuple[Image.Image, dict]:
    frame=_cv(image); edges=cv2.Canny(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),60,160)
    lines=cv2.HoughLinesP(edges,1,np.pi/180,threshold=60,minLineLength=max(30,frame.shape[0]//5),maxLineGap=12)
    if lines is None: return image,{"quality_mode":"cv_no_lines_original_kept","confidence":0.0}
    angles=[]
    for x1,y1,x2,y2 in lines[:,0]:
        angle=np.degrees(np.arctan2(y2-y1,x2-x1)); folded=((angle+45)%90)-45
        if abs(folded) < 12: angles.append(folded)
    if len(angles)<2: return image,{"quality_mode":"cv_low_confidence_original_kept","confidence":len(angles)/10}
    correction=float(np.median(angles))
    if conservative and abs(correction)>4: return image,{"quality_mode":"cv_conservative_original_kept","confidence":min(1,len(angles)/20),"angle":correction}
    mat=cv2.getRotationMatrix2D((frame.shape[1]/2,frame.shape[0]/2),correction,1)
    result=cv2.warpAffine(frame,mat,(frame.shape[1],frame.shape[0]),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    return _pil(result),{"quality_mode":"cv_hough_straighten","confidence":min(1,len(angles)/20),"angle":correction}

def denoise_upscale(image: Image.Image, options: dict) -> tuple[Image.Image, dict]:
    frame=_cv(image); level=int(options.get('denoise_strength',7))
    if options.get('denoise'): frame=cv2.fastNlMeansDenoisingColored(frame,None,level,level,7,21)
    scale=int(options.get('upscale',1) or 1)
    if scale>1: frame=cv2.resize(frame,None,fx=scale,fy=scale,interpolation=cv2.INTER_LANCZOS4)
    return _pil(frame),{"quality_mode":"opencv_quality","denoise_strength":level if options.get('denoise') else 0,"upscale":scale}

def inpaint(image: Image.Image, mask_path: str) -> tuple[Image.Image, dict]:
    mask=np.array(Image.open(mask_path).convert('L').resize(image.size))
    frame=_cv(image); result=cv2.inpaint(frame,mask,3,cv2.INPAINT_TELEA)
    return _pil(result),{"quality_mode":"opencv_telea_inpaint","mask_path":mask_path}

def foreground(image: Image.Image, background: str | None = None) -> tuple[Image.Image, dict]:
    frame=_cv(image); mask=np.zeros(frame.shape[:2],np.uint8)
    rect=(max(1,frame.shape[1]//20),max(1,frame.shape[0]//20),frame.shape[1]*9//10,frame.shape[0]*9//10)
    bgd=np.zeros((1,65),np.float64); fgd=np.zeros((1,65),np.float64)
    cv2.grabCut(frame,mask,rect,bgd,fgd,3,cv2.GC_INIT_WITH_RECT)
    alpha=np.where((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD),255,0).astype('uint8')
    rgba=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA); rgba[:,:,3]=alpha
    result=Image.fromarray(rgba)
    if background:
        bg=Image.new('RGBA',result.size,background) if background.startswith('#') else Image.open(background).convert('RGBA').resize(result.size)
        bg.alpha_composite(result); result=bg
    return result,{"quality_mode":"opencv_grabcut","foreground_pixels":int((alpha>0).sum())}
