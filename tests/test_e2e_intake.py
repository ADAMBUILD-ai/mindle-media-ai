import hashlib
import subprocess
import pytest
from media_ai.e2e_intake import validate_intake


def test_missing_inputs_stay_blocked_without_invented_assets(tmp_path):
    result=validate_intake({},tmp_path)
    assert result['status']=='BLOCKED_ASSET_INTAKE'
    assert result['full_product_pass'] is False
    assert result['verified_assets']==[]


@pytest.fixture
def intake(tmp_path):
    video=tmp_path/'real-capture-placeholder-for-contract-test.mp4'
    bgm=tmp_path/'test-tone.wav'
    # Fixtures test the contract only, never serve as real architecture acceptance.
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=s=32x18:r=1','-t','30','-c:v','libx264',str(video)],check=True)
    subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=440:duration=1',str(bgm)],check=True)
    def entry(path):return {'path':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,
                           'rights_status':'CONFIRMED','source_or_owner':'test fixture','license_or_permission':'test-only',
                           'label':'fixture, not actual capture','duration_seconds':30 if path==video else 1}
    manifest={'duration_seconds':30,'aspect':'16:9','narration_script':'시험 원고','voice_length_policy':'reject',
              'volumes':{'narration':1,'original':0,'bgm':.2},'clips':[{**entry(video),'origin':'real_capture','width':32,'height':18}],
              'bgm':entry(bgm)}
    return manifest,tmp_path


def test_verified_manifest_is_technical_only_and_hash_drift_blocks(intake):
    manifest,base=intake
    result=validate_intake(manifest,base)
    assert result['status']=='PASS_INTAKE_TECHNICAL_ONLY'
    assert result['rights_review']=='DECLARATIONS_ONLY_REQUIRES_OWNER_CONFIRMATION'
    assert result['human_audio_review']=='NOT_EXECUTED'
    manifest['clips'][0]['sha256']='a'*64
    result=validate_intake(manifest,base)
    assert result['status']=='BLOCKED_ASSET_INTAKE'
    assert any('SHA-256 mismatch' in error for error in result['errors'])


@pytest.mark.parametrize('fault',['rights','duration','resolution','policy','volume','bgm'])
def test_incomplete_or_drifted_acceptance_contract_blocks(intake,fault):
    manifest,base=intake
    if fault=='rights':manifest['clips'][0]['rights_status']='UNCONFIRMED'
    elif fault=='duration':manifest['clips'][0]['duration_seconds']=31
    elif fault=='resolution':manifest['clips'][0]['width']=64
    elif fault=='policy':manifest['voice_length_policy']='trim'
    elif fault=='volume':manifest['volumes']['bgm']=True
    elif fault=='bgm':manifest['bgm']=None
    assert validate_intake(manifest,base)['status']=='BLOCKED_ASSET_INTAKE'
