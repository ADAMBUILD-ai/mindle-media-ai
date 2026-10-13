"""Full-frame SAM2 video memory engine; preserves source duration, FPS and audio."""
import time
import json
import os
import subprocess
from pathlib import Path
import cv2
import numpy as np
from .verified_model_adapters import sha256_file

class ContinuousSamTracking:
    adapter_id='mindle.sam21.video.memory.cpu'
    adapter_version='1.0.0'
    runtime_backend='transformers-sam2-video-pytorch'
    device_requirement='cpu'
    def __init__(self,snapshot,identity):
        import torch
        from transformers import Sam2VideoModel,Sam2VideoProcessor,Sam2VideoConfig,Sam2ImageProcessorFast,Sam2VideoVideoProcessor
        self.identity=identity;self.weight=identity.verify_snapshot(Path(snapshot),{'config.json','model.safetensors','preprocessor_config.json','processor_config.json'})
        self.torch=torch
        config=Sam2VideoConfig.from_pretrained(snapshot,local_files_only=True)
        config.image_size=512;config.prompt_encoder_config.image_size=512;config.vision_config.image_size=512
        self.model,loading=Sam2VideoModel.from_pretrained(snapshot,config=config,local_files_only=True,trust_remote_code=False,output_loading_info=True)
        if loading.get('missing_keys') or loading.get('mismatched_keys'):
            raise RuntimeError('Pinned checkpoint does not contain the complete video memory engine')
        self.model=self.model.to('cpu').eval();self.processor=Sam2VideoProcessor(image_processor=Sam2ImageProcessorFast.from_pretrained(snapshot,local_files_only=True,size={'height':512,'width':512}),video_processor=Sam2VideoVideoProcessor(size={'height':512,'width':512}),target_size=512)
    def track_video(self,source,directory,command=''):
        directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
        capture=cv2.VideoCapture(str(source));fps=capture.get(cv2.CAP_PROP_FPS)
        if not capture.isOpened() or fps<=0:raise RuntimeError('영상 원본을 읽을 수 없습니다.')
        width=int(capture.get(cv2.CAP_PROP_FRAME_WIDTH));height=int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        session=self.processor.init_video_session(inference_device='cpu',dtype=self.torch.float32)
        raw=directory/'tracking_frames.mp4';writer=cv2.VideoWriter(str(raw),cv2.VideoWriter_fourcc(*'mp4v'),fps,(width,height))
        if not writer.isOpened():raise RuntimeError('영상 출력기를 열 수 없습니다.')
        started=time.perf_counter();rows=[]
        try:
            with self.torch.inference_mode():
                while True:
                    ok,frame=capture.read()
                    if not ok:break
                    index=len(rows)
                    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    inputs=self.processor(images=rgb,device='cpu',return_tensors='pt')
                    if index==0:
                        x=width*.74 if '오른쪽' in command else width*.26 if '왼쪽' in command else width*.5
                        self.processor.add_inputs_to_inference_session(inference_session=session,frame_idx=0,obj_ids=1,input_points=[[[[round(x),height//2]]]],input_labels=[[[1]]],original_size=inputs.original_sizes[0])
                    result=self.model(inference_session=session,frame=inputs.pixel_values[0])
                    mask=self.processor.post_process_masks([result.pred_masks],original_sizes=inputs.original_sizes,binarize=False)[0].squeeze().cpu().numpy()>0
                    if mask.shape!=(height,width):raise RuntimeError('영상 mask 비율이 원본과 다릅니다.')
                    overlay=frame.copy();overlay[mask]=(.55*frame[mask]+.45*np.array([32,32,255])).astype(np.uint8)
                    writer.write(overlay);rows.append({'frame_index':index,'foreground_fraction':float(mask.mean())})
        finally:capture.release();writer.release()
        if not rows or not any(r['foreground_fraction']>0 for r in rows):raise RuntimeError('추적 대상 결과가 없습니다.')
        output=directory/'track_1_overlays.mp4';package=os.environ.get('MINDLE_LOCAL_VERIFIED_RUNTIME_ROOT')
        ffmpeg=str(Path(package)/'tools/ffmpeg/ffmpeg.exe') if package else 'ffmpeg'
        encoder='h264_mf' if package and os.name=='nt' else 'libx264'
        subprocess.run([ffmpeg,'-y','-i',str(raw),'-i',str(source),'-map','0:v:0','-map','1:a?','-c:v',encoder,'-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(output)],check=True,capture_output=True)
        manifest=directory/'tracking.json';manifest.write_text(json.dumps({'engine':'SAM2_VIDEO_MEMORY','all_frames':True,'fps':fps,'width':width,'height':height,'frames':rows})+'\n')
        return {'status':'TESTED_PASS','tracking_mode':'continuous_video_memory','sampled_frames':len(rows),'tracked_frames':len(rows),'fps':fps,'elapsed_ms':(time.perf_counter()-started)*1000,'task_quality':'NOT_BENCHMARKED','outputs':[{'path':str(output),'sha256':sha256_file(output),'bytes':output.stat().st_size},{'path':str(manifest),'sha256':sha256_file(manifest),'bytes':manifest.stat().st_size}]}
    def close(self):self.model=None
