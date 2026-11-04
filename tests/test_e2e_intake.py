import hashlib
import json
import pytest
from media_ai.e2e_intake import validate_intake


def test_missing_inputs_stay_blocked_without_invented_assets(tmp_path):
    result=validate_intake({},tmp_path)
    assert result['status']=='BLOCKED_ASSET_INTAKE'
    assert result['full_product_pass'] is False
    assert result['verified_assets']==[]


@pytest.fixture
def intake(tmp_path,monkeypatch):
    video=tmp_path/'real-capture-placeholder-for-contract-test.mp4'
    bgm=tmp_path/'test-tone.wav'
    # Fixtures test the contract only, never serve as real architecture acceptance.
    video.write_bytes(b'contract-video-fixture')
    bgm.write_bytes(b'contract-audio-fixture')
    def fake_ffprobe(args,**_kwargs):
        assert _kwargs.get('encoding')=='utf-8'  # Windows CP949 must not decode FFprobe JSON.
        target=args[-1]
        if target==str(video):
            return json.dumps({'streams':[{'codec_type':'video','codec_name':'h264','width':32,'height':18}],
                               'format':{'duration':'30.0'}}).encode()
        return json.dumps({'streams':[{'codec_type':'audio','codec_name':'pcm_s16le'}],
                           'format':{'duration':'1.0'}}).encode()
    monkeypatch.setattr('media_ai.e2e_intake.subprocess.check_output',fake_ffprobe)
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


@pytest.mark.parametrize('fault',['rights','duration','resolution','policy','volume','bgm','bgm_over_product_limit'])
def test_incomplete_or_drifted_acceptance_contract_blocks(intake,fault):
    manifest,base=intake
    if fault=='rights':manifest['clips'][0]['rights_status']='UNCONFIRMED'
    elif fault=='duration':manifest['clips'][0]['duration_seconds']=31
    elif fault=='resolution':manifest['clips'][0]['width']=64
    elif fault=='policy':manifest['voice_length_policy']='trim'
    elif fault=='volume':manifest['volumes']['bgm']=True
    elif fault=='bgm':manifest['bgm']=None
    elif fault=='bgm_over_product_limit':manifest['volumes']['bgm']=1.01
    assert validate_intake(manifest,base)['status']=='BLOCKED_ASSET_INTAKE'

def test_usable_ranges_not_whole_file_duration_determine_coverage(intake):
    manifest,base=intake
    manifest['clips'][0].update(usable_start_seconds=10,usable_end_seconds=20)
    result=validate_intake(manifest,base)
    assert result['status']=='BLOCKED_ASSET_INTAKE'
    assert 'source coverage below 30 seconds' in result['errors']


@pytest.mark.parametrize('start,end',[(20,10),(-1,30),(0,31),(True,30)])
def test_invalid_usable_ranges_fail_closed(intake,start,end):
    manifest,base=intake;manifest['clips'][0].update(usable_start_seconds=start,usable_end_seconds=end)
    assert validate_intake(manifest,base)['status']=='BLOCKED_ASSET_INTAKE'


def test_r2_requires_rights_reference_and_product_supported_bgm_volume(intake):
    manifest,base=intake;manifest['require_rights_evidence']=True
    assert validate_intake(manifest,base)['status']=='BLOCKED_ASSET_INTAKE'
    manifest['clips'][0]['rights_evidence']='test contract only'
    manifest['bgm']['rights_evidence']='test license only'
    assert validate_intake(manifest,base)['status']=='PASS_INTAKE_TECHNICAL_ONLY'
    manifest['volumes']['bgm']=1.5
    assert validate_intake(manifest,base)['status']=='BLOCKED_ASSET_INTAKE'


def test_original_sound_request_requires_actual_source_audio(intake):
    manifest,base=intake;manifest['volumes']['original']=.2
    assert validate_intake(manifest,base)['status']=='BLOCKED_ASSET_INTAKE'
