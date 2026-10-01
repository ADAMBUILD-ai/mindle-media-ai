import argparse
from pathlib import Path
from .contracts import MediaJob
from .router import route
from .runtime import MediaRuntime

def main():
    p=argparse.ArgumentParser(); p.add_argument("mode", choices=["photo","video"]); p.add_argument("--input", required=True); p.add_argument("--output", required=True); p.add_argument("--brightness", type=float, default=1); p.add_argument("--contrast", type=float, default=1); p.add_argument("--saturation", type=float, default=1); p.add_argument("--sharpness", type=float); p.add_argument("--denoise", action='store_true'); p.add_argument("--upscale", type=int); p.add_argument("--preset", choices=['web','sns','proposal']); p.add_argument("--width", type=int); p.add_argument('--auto-vertical', action='store_true'); p.add_argument('--mask'); p.add_argument('--object-remove', action='store_true'); p.add_argument('--background-remove', action='store_true'); p.add_argument('--background-replace'); p.add_argument("--aspect", default="16:9"); p.add_argument("--start"); p.add_argument("--duration"); p.add_argument('--subtitle'); p.add_argument('--mute', action='store_true'); p.add_argument('--volume', type=float); p.add_argument('--clips', nargs='*'); args=p.parse_args()
    source=Path(args.input); kind=route(args.mode, source); rt=MediaRuntime(Path(args.output).parent / "media_workspace")
    job=MediaJob(args.mode, source, kind, vars(args))
    job=rt.submit(job)
    if job.output_path and job.output_path != Path(args.output): Path(args.output).write_bytes(job.output_path.read_bytes())
    print(job.state, job.output_path or job.error)
if __name__ == '__main__': main()
