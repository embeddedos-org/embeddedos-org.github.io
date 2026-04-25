#!/usr/bin/env python3
"""
Generate professional book cover PNGs for all EmbeddedOS products.
Uses Pillow to create 1600x2400px covers with gradient backgrounds,
product branding, decorative patterns, and author info.
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

# ─── Configuration ───────────────────────────────────────────────────────────

WIDTH, HEIGHT = 1600, 2400
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORG_DIR = os.path.dirname(BASE_DIR)

PRODUCTS = [
    {
        "name": "EoS",
        "full_name": "EmbeddedOS (EoS)",
        "subtitle": "Real-Time Operating System",
        "color": "#58a6ff",
        "accent": "#1158a6",
        "repo": "eos",
        "icon": "chip",
    },
    {
        "name": "eBoot",
        "full_name": "eBoot",
        "subtitle": "Secure Bootloader Platform",
        "color": "#3fb950",
        "accent": "#1a6b2a",
        "repo": "eBoot",
        "icon": "lightning",
    },
    {
        "name": "ebuild",
        "full_name": "ebuild",
        "subtitle": "Build System & Toolchain",
        "color": "#f0883e",
        "accent": "#a05020",
        "repo": "ebuild",
        "icon": "gear",
    },
    {
        "name": "eIPC",
        "full_name": "eIPC",
        "subtitle": "Inter-Process Communication",
        "color": "#79c0ff",
        "accent": "#2a6090",
        "repo": "eIPC",
        "icon": "network",
    },
    {
        "name": "eAI",
        "full_name": "eAI",
        "subtitle": "Embedded AI & TinyML",
        "color": "#bc8cff",
        "accent": "#6e40aa",
        "repo": "eAI",
        "icon": "brain",
    },
    {
        "name": "eNI",
        "full_name": "eNI",
        "subtitle": "Neural Interface Platform",
        "color": "#f778ba",
        "accent": "#a03070",
        "repo": "eNI",
        "icon": "waves",
    },
    {
        "name": "EoSim",
        "full_name": "EoSim",
        "subtitle": "Hardware Simulation Engine",
        "color": "#f85149",
        "accent": "#a02020",
        "repo": "EoSim",
        "icon": "monitor",
    },
    {
        "name": "EoStudio",
        "full_name": "EoStudio",
        "subtitle": "Integrated Development Environment",
        "color": "#bc8cff",
        "accent": "#6e40aa",
        "repo": "EoStudio",
        "icon": "palette",
    },
    {
        "name": "eApps",
        "full_name": "eApps",
        "subtitle": "Application Framework",
        "color": "#e3b341",
        "accent": "#8a6a10",
        "repo": "eApps",
        "icon": "grid",
    },
    {
        "name": "eDB",
        "full_name": "eDB",
        "subtitle": "Embedded Database Engine",
        "color": "#3fb950",
        "accent": "#1a6b2a",
        "repo": "eDB",
        "icon": "database",
    },
    {
        "name": "eBrowser",
        "full_name": "eBrowser",
        "subtitle": "Embedded Web Browser",
        "color": "#79c0ff",
        "accent": "#2a6090",
        "repo": "eBrowser",
        "icon": "globe",
    },
    {
        "name": "eOffice",
        "full_name": "eOffice",
        "subtitle": "Office Productivity Suite",
        "color": "#f0883e",
        "accent": "#a05020",
        "repo": "eOffice",
        "icon": "document",
    },
    {
        "name": "eVera",
        "full_name": "eVera",
        "subtitle": "AI Assistant & 3D Avatar",
        "color": "#f778ba",
        "accent": "#a03070",
        "repo": "eVera",
        "icon": "avatar",
    },
    {
        "name": "eStocks",
        "full_name": "eStocks Trading Scripts",
        "subtitle": "Algorithmic Trading Platform",
        "color": "#58a6ff",
        "accent": "#6e7681",
        "repo": "eStocks_Trading_Scripts",
        "icon": "chart",
    },
    {
        "name": "eHardware",
        "full_name": "eHardware Designs",
        "subtitle": "Hardware Design & Products",
        "color": "#3fb950",
        "accent": "#1a6b2a",
        "repo": "eHardware-Designs-Products",
        "icon": "pcb",
    },
    {
        "name": "EmbeddedOS\nEcosystem",
        "full_name": "EmbeddedOS Ecosystem",
        "subtitle": "The Complete Platform Guide",
        "color": "#bc8cff",
        "accent": "#58a6ff",
        "repo": "embeddedos-org.github.io",
        "icon": "ecosystem",
    },
]


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def darken(rgb, factor=0.4):
    return tuple(max(0, int(c * factor)) for c in rgb)


def lighten(rgb, factor=0.3):
    return tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)


def create_gradient(draw, width, height, color_top, color_bottom):
    """Create a smooth vertical gradient."""
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))


def draw_circuit_pattern(draw, width, height, color, icon_type):
    """Draw decorative tech patterns based on icon type."""
    random.seed(hash(icon_type))
    alpha_color = (*color, 30)

    # Draw subtle grid lines
    for x in range(0, width, 80):
        if random.random() > 0.5:
            draw.line([(x, 600), (x, 1800)], fill=(*color, 15), width=1)
    for y in range(600, 1800, 80):
        if random.random() > 0.5:
            draw.line([(0, y), (width, y)], fill=(*color, 15), width=1)

    # Draw icon-specific decorative elements
    if icon_type == "chip":
        # SoC chip pattern
        cx, cy = width // 2, 1200
        draw.rectangle([cx - 150, cy - 150, cx + 150, cy + 150], outline=(*color, 50), width=4)
        draw.rectangle([cx - 120, cy - 120, cx + 120, cy + 120], outline=(*color, 35), width=2)
        for i in range(-3, 4):
            draw.line([(cx + i * 40, cy - 150), (cx + i * 40, cy - 200)], fill=(*color, 40), width=3)
            draw.line([(cx + i * 40, cy + 150), (cx + i * 40, cy + 200)], fill=(*color, 40), width=3)
            draw.line([(cx - 150, cy + i * 40), (cx - 200, cy + i * 40)], fill=(*color, 40), width=3)
            draw.line([(cx + 150, cy + i * 40), (cx + 200, cy + i * 40)], fill=(*color, 40), width=3)
    elif icon_type == "lightning":
        # Lightning bolt shapes
        for _ in range(8):
            x = random.randint(100, width - 100)
            y = random.randint(700, 1700)
            pts = [(x, y), (x - 20, y + 60), (x + 10, y + 55), (x - 10, y + 120)]
            draw.line(pts, fill=(*color, 25), width=3)
    elif icon_type == "gear":
        # Gear teeth pattern
        cx, cy = width // 2, 1200
        r = 140
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x1 = cx + int(r * math.cos(rad))
            y1 = cy + int(r * math.sin(rad))
            x2 = cx + int((r + 40) * math.cos(rad))
            y2 = cy + int((r + 40) * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=(*color, 40), width=6)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*color, 40), width=3)
        draw.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], outline=(*color, 30), width=2)
    elif icon_type == "network":
        # Network node connections
        nodes = [(random.randint(200, width - 200), random.randint(800, 1600)) for _ in range(12)]
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i + 1 :]:
                dist = math.sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2)
                if dist < 400:
                    draw.line([n1, n2], fill=(*color, 20), width=2)
            draw.ellipse([n1[0] - 8, n1[1] - 8, n1[0] + 8, n1[1] + 8], fill=(*color, 40))
    elif icon_type == "brain":
        # Neural network pattern
        layers = [4, 6, 8, 6, 4]
        layer_x = [300, 500, 800, 1100, 1300]
        layer_nodes = []
        for li, (lx, count) in enumerate(zip(layer_x, layers)):
            nodes = []
            for ni in range(count):
                ny = 900 + (ni - count / 2) * 100
                nodes.append((lx, int(ny)))
                draw.ellipse([lx - 6, int(ny) - 6, lx + 6, int(ny) + 6], fill=(*color, 40))
            layer_nodes.append(nodes)
        for li in range(len(layer_nodes) - 1):
            for n1 in layer_nodes[li]:
                for n2 in layer_nodes[li + 1]:
                    draw.line([n1, n2], fill=(*color, 12), width=1)
    elif icon_type == "waves":
        # Brain wave patterns
        for wave_y in range(800, 1600, 80):
            pts = []
            for x in range(0, width, 4):
                y = wave_y + int(30 * math.sin(x * 0.02 + wave_y * 0.1))
                pts.append((x, y))
            if len(pts) > 1:
                draw.line(pts, fill=(*color, 20), width=2)
    elif icon_type == "monitor":
        # Monitor/simulation display
        cx, cy = width // 2, 1200
        draw.rectangle([cx - 200, cy - 140, cx + 200, cy + 100], outline=(*color, 40), width=3)
        draw.rectangle([cx - 180, cy - 120, cx + 180, cy + 80], outline=(*color, 25), width=1)
        draw.line([(cx - 40, cy + 100), (cx - 60, cy + 160)], fill=(*color, 35), width=3)
        draw.line([(cx + 40, cy + 100), (cx + 60, cy + 160)], fill=(*color, 35), width=3)
        draw.line([(cx - 80, cy + 160), (cx + 80, cy + 160)], fill=(*color, 35), width=3)
        # Sine wave on screen
        pts = []
        for x in range(cx - 170, cx + 170, 3):
            y = cy - 20 + int(40 * math.sin((x - cx) * 0.05))
            pts.append((x, y))
        if pts:
            draw.line(pts, fill=(*color, 35), width=2)
    elif icon_type == "palette":
        # Code editor/palette
        cx, cy = width // 2, 1200
        for i in range(6):
            y = cy - 100 + i * 40
            w = random.randint(100, 300)
            draw.rectangle([cx - 200, y, cx - 200 + w, y + 25], fill=(*color, 20))
    elif icon_type == "grid":
        # App grid
        cx, cy = width // 2, 1200
        for r in range(3):
            for c in range(3):
                x = cx - 150 + c * 120
                y = cy - 150 + r * 120
                draw.rounded_rectangle([x, y, x + 90, y + 90], radius=10, outline=(*color, 40), width=2)
    elif icon_type == "database":
        # Database cylinder
        cx, cy = width // 2, 1200
        for i in range(4):
            y = cy - 120 + i * 80
            draw.ellipse([cx - 120, y - 25, cx + 120, y + 25], outline=(*color, 35), width=2)
        draw.line([(cx - 120, cy - 120), (cx - 120, cy + 120)], fill=(*color, 35), width=2)
        draw.line([(cx + 120, cy - 120), (cx + 120, cy + 120)], fill=(*color, 35), width=2)
    elif icon_type == "globe":
        # Globe/web
        cx, cy = width // 2, 1200
        r = 140
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*color, 40), width=2)
        draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(*color, 25), width=1)
        draw.line([(cx - r, cy), (cx + r, cy)], fill=(*color, 30), width=1)
        draw.line([(cx, cy - r), (cx, cy + r)], fill=(*color, 30), width=1)
        for lat in [-70, -35, 35, 70]:
            yr = cy + int(r * math.sin(math.radians(lat)))
            xr = int(r * math.cos(math.radians(lat)))
            draw.line([(cx - xr, yr), (cx + xr, yr)], fill=(*color, 20), width=1)
    elif icon_type == "document":
        # Document stack
        cx, cy = width // 2, 1200
        for i in range(3):
            offset = i * 20
            draw.rectangle(
                [cx - 120 + offset, cy - 160 + offset, cx + 120 + offset, cy + 120 + offset],
                outline=(*color, 30 + i * 10),
                width=2,
            )
        for i in range(5):
            draw.line([(cx - 60, cy - 80 + i * 35), (cx + 80, cy - 80 + i * 35)], fill=(*color, 25), width=2)
    elif icon_type == "avatar":
        # AI avatar face outline
        cx, cy = width // 2, 1200
        draw.ellipse([cx - 100, cy - 130, cx + 100, cy + 100], outline=(*color, 40), width=3)
        draw.ellipse([cx - 50, cy - 60, cx - 20, cy - 30], fill=(*color, 35))
        draw.ellipse([cx + 20, cy - 60, cx + 50, cy - 30], fill=(*color, 35))
        draw.arc([cx - 40, cy + 10, cx + 40, cy + 50], 0, 180, fill=(*color, 35), width=2)
    elif icon_type == "chart":
        # Candlestick chart
        cx, cy = width // 2, 1200
        candles = [80, -40, 60, -30, 90, -50, 70, 20, -60, 40]
        for i, h in enumerate(candles):
            x = cx - 200 + i * 45
            if h > 0:
                draw.rectangle([x, cy - h, x + 30, cy], fill=(*color, 30))
            else:
                draw.rectangle([x, cy, x + 30, cy - h], fill=(*color, 20))
            draw.line([(x + 15, cy - h - 20), (x + 15, cy - h)], fill=(*color, 25), width=1)
    elif icon_type == "pcb":
        # PCB traces
        for _ in range(15):
            x = random.randint(200, width - 200)
            y = random.randint(800, 1600)
            length = random.randint(50, 200)
            if random.random() > 0.5:
                draw.line([(x, y), (x + length, y)], fill=(*color, 25), width=3)
            else:
                draw.line([(x, y), (x, y + length)], fill=(*color, 25), width=3)
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(*color, 35))
    elif icon_type == "ecosystem":
        # All icons combined - hexagonal arrangement
        cx, cy = width // 2, 1200
        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = cx + int(180 * math.cos(angle))
            y = cy + int(180 * math.sin(angle))
            draw.regular_polygon((x, y, 40), 6, rotation=30, outline=(*color, 35), fill=(*color, 10))
        draw.regular_polygon((cx, cy, 50), 6, rotation=30, outline=(*color, 45), fill=(*color, 15))


def try_load_font(size):
    """Try to load a TrueType font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def try_load_font_regular(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Regular.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def generate_cover(product):
    """Generate a single book cover PNG."""
    primary = hex_to_rgb(product["color"])
    accent = hex_to_rgb(product["accent"])

    # Create RGBA image for alpha support in patterns
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    # Background gradient: dark accent at top -> darker at bottom
    dark_top = darken(accent, 0.6)
    dark_bottom = darken(accent, 0.2)
    create_gradient(draw, WIDTH, HEIGHT, dark_top, dark_bottom)

    # Decorative tech pattern in the middle area
    pattern_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pattern_draw = ImageDraw.Draw(pattern_layer)
    draw_circuit_pattern(pattern_draw, WIDTH, HEIGHT, primary, product["icon"])
    img = Image.alpha_composite(img, pattern_layer)
    draw = ImageDraw.Draw(img)

    # Top color band
    band_color = (*primary, 180)
    for y in range(0, 120):
        alpha = int(180 * (1 - y / 120))
        draw.line([(0, y), (WIDTH, y)], fill=(*primary, alpha))

    # "EMBEDDEDOS" branding at top
    font_brand = try_load_font(48)
    draw.text((80, 40), "EMBEDDEDOS", fill=(255, 255, 255, 220), font=font_brand)

    # Thin accent line under brand
    draw.line([(80, 110), (WIDTH - 80, 110)], fill=(*primary, 150), width=3)

    # "Official Reference Guide" subtitle line
    font_subtitle_small = try_load_font_regular(32)
    draw.text((80, 130), "Official Reference Guide", fill=(255, 255, 255, 160), font=font_subtitle_small)

    # ─── Main product name (large) ──────────────────────────────────
    font_title = try_load_font(140)
    font_title_med = try_load_font(100)
    name = product["name"]

    # Position the product name prominently
    title_y = 350

    if "\n" in name:
        # Multi-line name (Ecosystem)
        lines = name.split("\n")
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font_title_med)
            tw = bbox[2] - bbox[0]
            draw.text(((WIDTH - tw) // 2, title_y + i * 120), line, fill=(255, 255, 255, 255), font=font_title_med)
    else:
        bbox = draw.textbbox((0, 0), name, font=font_title)
        tw = bbox[2] - bbox[0]
        x = (WIDTH - tw) // 2
        # Drop shadow
        draw.text((x + 4, title_y + 4), name, fill=(0, 0, 0, 100), font=font_title)
        draw.text((x, title_y), name, fill=(255, 255, 255, 255), font=font_title)

    # ─── Subtitle ───────────────────────────────────────────────────
    font_sub = try_load_font_regular(44)
    sub = product["subtitle"]
    bbox = draw.textbbox((0, 0), sub, font=font_sub)
    sw = bbox[2] - bbox[0]
    draw.text(((WIDTH - sw) // 2, title_y + 180), sub, fill=(*lighten(primary, 0.5), 220), font=font_sub)

    # ─── Version badge ──────────────────────────────────────────────
    font_ver = try_load_font(36)
    ver_text = "v1.0.0"
    bbox = draw.textbbox((0, 0), ver_text, font=font_ver)
    vw = bbox[2] - bbox[0]
    vh = bbox[3] - bbox[1]
    vx = (WIDTH - vw) // 2 - 20
    vy = title_y + 260
    draw.rounded_rectangle([vx, vy, vx + vw + 40, vy + vh + 20], radius=8, fill=(*primary, 150))
    draw.text((vx + 20, vy + 8), ver_text, fill=(255, 255, 255, 240), font=font_ver)

    # ─── Bottom section ─────────────────────────────────────────────
    # Bottom gradient band
    for y in range(HEIGHT - 300, HEIGHT):
        alpha = int(200 * ((y - (HEIGHT - 300)) / 300))
        draw.line([(0, y), (WIDTH, y)], fill=(*darken(primary, 0.3), alpha))

    # Divider line
    draw.line([(80, HEIGHT - 250), (WIDTH - 80, HEIGHT - 250)], fill=(*primary, 100), width=2)

    # Author
    font_author = try_load_font_regular(38)
    author = "Srikanth Patchava"
    bbox = draw.textbbox((0, 0), author, font=font_author)
    aw = bbox[2] - bbox[0]
    draw.text(((WIDTH - aw) // 2, HEIGHT - 220), author, fill=(255, 255, 255, 200), font=font_author)

    # Contributors line
    font_contrib = try_load_font_regular(28)
    contrib = "& EmbeddedOS Contributors"
    bbox = draw.textbbox((0, 0), contrib, font=font_contrib)
    cw = bbox[2] - bbox[0]
    draw.text(((WIDTH - cw) // 2, HEIGHT - 170), contrib, fill=(255, 255, 255, 140), font=font_contrib)

    # Date
    font_date = try_load_font_regular(30)
    draw.text(((WIDTH - 200) // 2, HEIGHT - 110), "April 2026", fill=(255, 255, 255, 120), font=font_date)

    # Bottom accent line
    draw.line([(80, HEIGHT - 60), (WIDTH - 80, HEIGHT - 60)], fill=(*primary, 120), width=3)

    # Convert to RGB for PNG saving
    final = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    final.paste(img, mask=img.split()[3])

    return final


def main():
    for product in PRODUCTS:
        repo_dir = os.path.join(ORG_DIR, product["repo"])
        book_dir = os.path.join(repo_dir, "docs", "book")

        if not os.path.isdir(repo_dir):
            print(f"SKIP: {product['repo']} — repo not found at {repo_dir}")
            continue

        os.makedirs(book_dir, exist_ok=True)
        output_path = os.path.join(book_dir, "cover.png")

        print(f"Generating cover for {product['name']} -> {output_path}")
        cover = generate_cover(product)
        cover.save(output_path, "PNG", optimize=True)
        print(f"  Saved: {os.path.getsize(output_path)} bytes")

    print("\nDone! Generated all covers.")


if __name__ == "__main__":
    main()
