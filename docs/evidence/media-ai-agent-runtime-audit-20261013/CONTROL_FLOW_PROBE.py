"""Control-flow repro only. Injected adapter is NOT a model or inference evidence."""
import base64
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from PIL import Image
from media_ai.product_runtime import ProductJobService

def main():
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder);source=root/'source.png'
        Image.new('RGB',(100,60),(80,100,120)).save(source)
        service=ProductJobService(root/'data','')
        events=[]
        class InjectedAdapter:
            weight=source
            def segment_photo(self, source, directory, point):
                events.append('injected_adapter_called')
                directory.mkdir(parents=True,exist_ok=True)
                output=directory/'injected.png';Image.new('RGB',(100,60)).save(output)
                return {'outputs':[{'path':str(output)}]}
            def close(self):events.append('adapter_closed')
        adapter=InjectedAdapter()
        def handoff(*args):
            events.append('handoff_gate_rejected');raise RuntimeError('AUDIT_GATE_REJECTION')
        with patch.object(service.vault,'sam',return_value=(adapter,{})),patch.object(service,'_handoff',side_effect=handoff):
            try:
                service.execute({'lane':'photo','operation':'segment','command':'분할',
                                 'filename':'source.png','content_base64':base64.b64encode(source.read_bytes()).decode()})
            except RuntimeError as error:
                assert str(error)=='AUDIT_GATE_REJECTION'
        assert events==['injected_adapter_called','handoff_gate_rejected','adapter_closed']
        failed=next(iter(service.records.values()))
        assert failed['status']=='FAILED' and failed['state']=='queued'
        point=service._photo_target_point('오른쪽 인물을 분리해줘',source)
        assert point[0]==26 and point[0]<50
        source_code=Path(__import__('media_ai.product_runtime',fromlist=['x']).__file__).read_text()
        ui=Path(__file__).resolve().parents[3]/'ui/product_integration.js'
        assert 'detail.references' not in ui.read_text()
        result={'probe_type':'INJECTED_ADAPTER_CONTROL_FLOW_ONLY','real_model_calls':0,
                'events':events,'inference_entry_precedes_handoff_and_preflight':True,
                'failed_job_status':failed['status'],'failed_job_state':failed['state'],
                'right_person_command_actual_point':list(point),'right_person_selected_left':True,
                'ui_attached_references_forwarded_to_model_job':False,
                'limitations':'No SAM/SISR/Whisper inference was run; probe proves code order and command routing only.'}
        Path(__file__).with_name('CONTROL_FLOW_PROBE.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result))
if __name__=='__main__':main()
