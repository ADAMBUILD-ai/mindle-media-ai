from pathlib import Path
from PIL import Image
from media_ai.contracts import MediaJob, MediaType, JobState
from media_ai.router import route
from media_ai.runtime import MediaRuntime

def test_photo_e2e_preserves_original_and_writes_evidence(tmp_path: Path):
    source=tmp_path/'original.jpg'; Image.new('RGB',(20,10),(100,100,100)).save(source)
    runtime=MediaRuntime(tmp_path/'workspace'); job=MediaJob('사진을 밝게 보정해줘', source, route('사진을 밝게 보정해줘',source), {'brightness':1.2,'width':10})
    result=runtime.submit(job)
    assert result.state == JobState.SUCCEEDED
    assert result.output_path and result.output_path.exists()
    assert list((tmp_path/'workspace'/'originals').iterdir())
    assert result.evidence['engine'].startswith('Pillow')
    assert (tmp_path/'workspace'/'logs'/f'{job.id}.json').exists()
    assert result.evidence['input_sha256'] and result.evidence['output_sha256']

def test_router_identifies_video(tmp_path: Path):
    assert route('쇼츠로 만들어줘', tmp_path/'a.mp4') == MediaType.VIDEO

def test_photo_preset_denoise_upscale_and_alpha(tmp_path: Path):
    source=tmp_path/'rgba.png'; Image.new('RGBA',(12,8),(100,100,100,120)).save(source)
    result=MediaRuntime(tmp_path/'workspace').submit(MediaJob('제안서용 이미지',source,MediaType.PHOTO,{'preset':'web','denoise':True,'upscale':2,'transparent':True}))
    assert result.state == JobState.SUCCEEDED and result.output_path.suffix == '.png'
    assert result.evidence['adapter'] == 'pillow_local_fallback'

def test_mask_object_remove_and_background_remove_are_real_outputs(tmp_path: Path):
    source=tmp_path/'a.jpg'; mask=tmp_path/'mask.png'
    Image.new('RGB',(32,32),(240,20,20)).save(source); Image.new('L',(32,32),255).save(mask)
    runtime=MediaRuntime(tmp_path/'workspace')
    removed=runtime.submit(MediaJob('객체 제거',source,MediaType.PHOTO,{'object_remove':True,'mask':str(mask)}))
    background=runtime.submit(MediaJob('배경 제거',source,MediaType.PHOTO,{'background_remove':True,'mask':str(mask)}))
    assert removed.state == JobState.SUCCEEDED and removed.evidence['adapter']=='opencv_quality_engine'
    assert background.state == JobState.SUCCEEDED and background.output_path.suffix == '.png'

def test_auto_vertical_keeps_conservative_fallback_evidence(tmp_path: Path):
    source=tmp_path/'a.jpg'; Image.new('RGB',(32,32)).save(source)
    result=MediaRuntime(tmp_path/'workspace').submit(MediaJob('수직 보정',source,MediaType.PHOTO,{'auto_vertical':True}))
    assert result.state == JobState.SUCCEEDED and result.evidence['perspective_mode'].startswith('cv_')

def test_quality_inpaint_and_grabcut_paths(tmp_path: Path):
    source=tmp_path/'building.jpg'; mask=tmp_path/'mask.png'
    image=Image.new('RGB',(100,80),'white'); image.paste('gray',(35,20,65,60)); image.save(source)
    mask_image=Image.new('L',(100,80),0); mask_image.paste(255,(35,20,65,60)); mask_image.save(mask)
    runtime=MediaRuntime(tmp_path/'workspace')
    fixed=runtime.submit(MediaJob('객체 제거',source,MediaType.PHOTO,{'object_remove':True,'mask':str(mask),'quality_engine':True}))
    cut=runtime.submit(MediaJob('배경 제거',source,MediaType.PHOTO,{'background_remove':True,'quality_engine':True}))
    assert fixed.state == JobState.SUCCEEDED and fixed.evidence['quality_mode']=='opencv_telea_inpaint'
    assert cut.state == JobState.SUCCEEDED and cut.evidence['quality_mode']=='opencv_grabcut'
