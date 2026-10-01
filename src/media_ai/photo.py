from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from .photo_adapters import select_adapter
from .quality_engine import straighten, denoise_upscale, inpaint, foreground

PRESETS = {
    "web": {"width": 1920, "quality": 85},
    "sns": {"width": 1080, "quality": 88},
    "proposal": {"width": 2560, "quality": 92},
}

def process_photo(source: Path, destination: Path, options: dict) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    options = {**PRESETS.get(options.get("preset"), {}), **options}
    with Image.open(source) as raw:
        image = ImageOps.exif_transpose(raw)
        alpha = "A" in image.getbands()
        image = image.convert("RGBA" if alpha or options.get("transparent") else "RGB")
        original_size = image.size
        # Conservative architecture correction: user override only; auto is intentionally neutral.
        correction = "none"
        quality = {}
        if options.get("perspective"):
            coeffs = tuple(float(x) for x in options["perspective"])
            if len(coeffs) != 8: raise ValueError("perspective requires 8 coefficients")
            image = image.transform(image.size, Image.Transform.PERSPECTIVE, coeffs, Image.Resampling.BICUBIC)
            correction = "manual_perspective"
        elif options.get("auto_vertical"):
            image, quality = straighten(image, bool(options.get('conservative', True))); correction=quality['quality_mode']
        image = ImageEnhance.Brightness(image).enhance(float(options.get("brightness", 1.0)))
        image = ImageEnhance.Contrast(image).enhance(float(options.get("contrast", 1.0)))
        image = ImageEnhance.Color(image).enhance(float(options.get("saturation", 1.0)))
        if options.get("sharpness"): image = ImageEnhance.Sharpness(image).enhance(float(options["sharpness"]))
        if options.get('quality_engine') and (options.get('denoise') or options.get('upscale')):
            image, detail = denoise_upscale(image, options); quality.update(detail); adapter_name='opencv_quality_engine'
        elif options.get('object_remove') and options.get('mask'):
            image, detail = inpaint(image, options['mask']); quality.update(detail); adapter_name='opencv_quality_engine'
        elif options.get('background_remove') or options.get('background_replace'):
            image, detail = foreground(image, options.get('background_replace')); quality.update(detail); adapter_name='opencv_quality_engine'
        else:
            adapter = select_adapter(options); image = adapter.apply(image, options); adapter_name=adapter.name
        if options.get("width"):
            width = int(options["width"]); height = round(image.height * width / image.width)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        if options.get("crop"):
            left, top, right, bottom = map(int, options["crop"]); image = image.crop((left, top, right, bottom))
        if options.get("transparent") or options.get("background_remove"):
            destination = destination.with_suffix('.png')
            image.save(destination, optimize=True)
        else: image.convert('RGB').save(destination, quality=int(options.get("quality", 92)), optimize=True)
    return {"original_size": original_size, "result_size": image.size, "engine": "Pillow OpenCV", "adapter": adapter_name, "alpha_input": alpha, "perspective_mode": correction, "actual_output": str(destination), **quality}
