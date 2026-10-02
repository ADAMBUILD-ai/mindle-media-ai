from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'ui' / 'assets' / 'brand'
OUT.mkdir(parents=True, exist_ok=True)

def build(size: int) -> Image.Image:
    scale = size / 1024
    def s(value): return int(round(value * scale))
    image = Image.new('RGBA', (size, size), '#061522')
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((s(24), s(24), s(1000), s(1000)), radius=s(220), fill='#0b1830')
    draw.rounded_rectangle((s(86), s(86), s(938), s(938)), radius=s(178), outline='#1e4b73', width=max(1, s(18)))
    draw.rounded_rectangle((s(184), s(226), s(840), s(724)), radius=s(78), outline='#397dff', width=max(1, s(46)))
    draw.line([(s(232),s(650)),(s(378),s(480)),(s(494),s(585)),(s(590),s(483)),(s(792),s(650))], fill='#61e4ff', width=max(1,s(42)), joint='curve')
    draw.ellipse((s(632),s(304),s(728),s(400)), fill='#25d7ff')
    draw.polygon([(s(438),s(326)),(s(628),s(432)),(s(438),s(538))], fill='#f8fbff')
    draw.line([(s(780),s(142)),(s(780),s(258))], fill='#c04dff', width=max(1,s(30)))
    draw.line([(s(722),s(200)),(s(838),s(200))], fill='#ff3eb8', width=max(1,s(30)))
    draw.line([(s(844),s(292)),(s(844),s(368))], fill='#ff55c8', width=max(1,s(18)))
    draw.line([(s(806),s(330)),(s(882),s(330))], fill='#ff55c8', width=max(1,s(18)))
    return image

for size in (1024, 512, 256, 128, 64, 48, 32, 16):
    build(size).save(OUT / f'MINDLE_MEDIA_AI_APP_ICON_{size}.png', optimize=True)
build(1024).save(OUT / 'MINDLE_MEDIA_AI_APP_ICON.ico', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
