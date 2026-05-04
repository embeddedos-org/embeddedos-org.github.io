"""Generate og-image.png for the EmbeddedOS site (1200x630, brand-coloured)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), '..', 'og-image.png')

BG_TOP    = (13, 17, 23)
BG_BOTTOM = (22, 27, 64)
BLUE      = (88, 166, 255)
GREEN     = (63, 185, 80)
PURPLE    = (188, 140, 255)
ORANGE    = (240, 136, 62)
CYAN      = (121, 192, 255)
PINK      = (247, 120, 186)
YELLOW    = (227, 179, 65)
RED       = (248, 81, 73)
WHITE     = (230, 237, 243)
MUTED     = (139, 148, 158)

ACCENTS = [BLUE, GREEN, PURPLE, ORANGE, CYAN, PINK, YELLOW, RED]

img = Image.new('RGB', (W, H), BG_TOP)
draw = ImageDraw.Draw(img)

# Vertical gradient background
for y in range(H):
    t = y / H
    r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t)
    g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t)
    b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Top rainbow strip (8px)
strip_h = 10
seg = W // len(ACCENTS)
for i, c in enumerate(ACCENTS):
    draw.rectangle([(i * seg, 0), ((i + 1) * seg, strip_h)], fill=c)

# Bottom rainbow strip
for i, c in enumerate(ACCENTS):
    draw.rectangle([(i * seg, H - strip_h), ((i + 1) * seg, H)], fill=c)

def get_font(size, bold=False):
    candidates = [
        r'C:\Windows\Fonts\segoeuib.ttf' if bold else r'C:\Windows\Fonts\segoeui.ttf',
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

font_brand   = get_font(38, True)
font_title   = get_font(78, True)
font_subtitle = get_font(34, False)
font_stats   = get_font(26, True)
font_url     = get_font(28, False)

# Brand mark (top-left): 🚀 EmbeddedOS
mark_x, mark_y = 70, 60
draw.rectangle([(mark_x, mark_y), (mark_x + 56, mark_y + 56)],
               fill=BLUE, outline=PURPLE, width=2)
draw.text((mark_x + 28, mark_y + 26), 'E', fill=WHITE, anchor='mm', font=get_font(36, True))
draw.text((mark_x + 76, mark_y + 28), 'EmbeddedOS', fill=WHITE, anchor='lm', font=font_brand)

# Title (centered)
title = 'The Open-Source\nEmbedded OS'
draw.text((W // 2, 240), title, fill=WHITE, anchor='mm',
          font=font_title, align='center', spacing=10)

# Subtitle (centered, multi-colour gradient effect via segments)
subtitle = '15 Products  ·  83 Boards  ·  16 Books  ·  60+ Apps'
draw.text((W // 2, 380), subtitle, fill=MUTED, anchor='mm', font=font_subtitle)

# Stat pills (4 colourful badges)
pills = [
    ('Kernel + AI', BLUE),
    ('IPC + Apps', GREEN),
    ('Simulator', PURPLE),
    ('IDE + HW', ORANGE),
]
pill_w, pill_h, gap = 200, 50, 22
total_w = len(pills) * pill_w + (len(pills) - 1) * gap
start_x = (W - total_w) // 2
y = 450
for i, (label, c) in enumerate(pills):
    x0 = start_x + i * (pill_w + gap)
    draw.rounded_rectangle([(x0, y), (x0 + pill_w, y + pill_h)], radius=25,
                           fill=(c[0], c[1], c[2], 60), outline=c, width=2)
    draw.text((x0 + pill_w // 2, y + pill_h // 2), label, fill=c,
              anchor='mm', font=font_stats)

# Bottom URL
draw.text((W // 2, H - 60), 'embeddedos-org.github.io',
          fill=WHITE, anchor='mm', font=font_url)

img.save(OUT, 'PNG', optimize=True)
print('Wrote', os.path.abspath(OUT), 'size:', os.path.getsize(OUT))
