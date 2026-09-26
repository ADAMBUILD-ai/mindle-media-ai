from pathlib import Path
from subprocess import run, CalledProcessError

ASPECTS = {"16:9": "1920:1080", "9:16": "1080:1920", "1:1": "1080:1080"}

def process_video(source: Path, destination: Path, options: dict) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    aspect = options.get("aspect", "16:9")
    canvas = ASPECTS.get(aspect, ASPECTS["16:9"])
    vf = f"scale={canvas}:force_original_aspect_ratio=decrease,pad={canvas}:(ow-iw)/2:(oh-ih)/2"
    input_source = source
    concat_file = None
    if options.get("clips"):
        concat_file = destination.with_suffix('.concat.txt')
        clips = [source, *map(Path, options['clips'])]
        concat_file.write_text(''.join(f"file '{clip.resolve()}'\\n" for clip in clips), encoding='utf-8')
        input_source = concat_file
    command = ["ffmpeg", "-y"]
    if concat_file: command += ["-f", "concat", "-safe", "0"]
    command += ["-i", str(input_source)]
    if options.get("start"): command += ["-ss", str(options["start"])]
    if options.get("duration"): command += ["-t", str(options["duration"])]
    if options.get("subtitle"):
        subtitle = str(Path(options['subtitle']).resolve()).replace('\\', '\\\\').replace(':', '\\:')
        vf += f",subtitles='{subtitle}'"
    command += ["-vf", vf, "-c:v", "libx264", "-crf", str(options.get("crf", 23))]
    if options.get("mute"): command += ["-an"]
    else:
        if options.get("volume") is not None: command += ["-af", f"volume={float(options['volume'])}"]
        command += ["-c:a", "aac"]
    command += [str(destination)]
    try: run(command, check=True, capture_output=True, text=True)
    except CalledProcessError as error: raise RuntimeError(error.stderr[-1000:]) from error
    if concat_file: concat_file.unlink(missing_ok=True)
    return {"engine": "ffmpeg", "aspect": aspect, "command": command[:-1] + ["<output>"]}
