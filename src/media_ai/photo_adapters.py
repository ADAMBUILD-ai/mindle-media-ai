from abc import ABC, abstractmethod
from pathlib import Path
from PIL import Image, ImageFilter, ImageChops

class PhotoAdapter(ABC):
    name = "local_adapter"
    @abstractmethod
    def apply(self, image: Image.Image, options: dict) -> Image.Image: ...

class LocalEnhancementAdapter(PhotoAdapter):
    name = "pillow_local_fallback"
    def apply(self, image: Image.Image, options: dict) -> Image.Image:
        if options.get("denoise"):
            image = image.filter(ImageFilter.MedianFilter(size=3))
        if options.get("upscale"):
            factor = max(1, int(options["upscale"]))
            image = image.resize((image.width * factor, image.height * factor), Image.Resampling.LANCZOS)
        return image

class LocalMaskAdapter(PhotoAdapter):
    """Mask-based local fallback; high-quality model adapters can replace it later."""
    name = "pillow_mask_fallback"
    def apply(self, image: Image.Image, options: dict) -> Image.Image:
        mask_path = options.get("mask")
        if mask_path:
            mask = Image.open(mask_path).convert('L').resize(image.size)
        else:
            # Neutral automatic foreground heuristic for simple bright-background assets.
            gray = image.convert('L')
            mask = gray.point(lambda px: 255 if px < int(options.get('threshold', 245)) else 0)
        if options.get('object_remove'):
            # Simple inpaint fallback: blur surrounding image and composite only masked region.
            return Image.composite(image.filter(ImageFilter.GaussianBlur(radius=12)), image, mask)
        if options.get('background_remove'):
            out=image.convert('RGBA'); out.putalpha(mask); return out
        if options.get('background_replace'):
            bg=options['background_replace']
            if isinstance(bg, str) and bg.startswith('#'):
                background=Image.new('RGBA',image.size,bg)
            else: background=Image.open(bg).convert('RGBA').resize(image.size)
            background.alpha_composite(image.convert('RGBA'), (0,0))
            return Image.composite(image.convert('RGBA'), background, mask)
        return image

def select_adapter(options: dict) -> PhotoAdapter:
    if options.get("object_remove") or options.get("background_remove") or options.get("background_replace"):
        return LocalMaskAdapter()
    return LocalEnhancementAdapter()
