#!/usr/bin/env python3
"""
Professional Book Cover Generator for EmbeddedOS
Hybrid: PyCairo (vector graphics) + Pillow (text rendering)

Creates publisher-quality covers inspired by O'Reilly, Apress, Manning, Packt.
- Rich multi-stop gradient backgrounds
- Unique geometric/tech artwork per product
- Professional typography with Lato Black/Heavy
- Publisher branding "EmbeddedOS Press"
- Spine accent stripe, ISBN placeholder, edition badges
"""

import cairo
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

ORG_DIR = "/home/spatchava/embeddedos-org"
W, H = 1600, 2400

# ─── Font loading ────────────────────────────────────────────────────────────

def load_font(name, size):
    paths = {
        "black":     "/usr/share/fonts/truetype/lato/Lato-Black.ttf",
        "heavy":     "/usr/share/fonts/truetype/lato/Lato-Heavy.ttf",
        "bold":      "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
        "semibold":  "/usr/share/fonts/truetype/lato/Lato-Semibold.ttf",
        "medium":    "/usr/share/fonts/truetype/lato/Lato-Medium.ttf",
        "regular":   "/usr/share/fonts/truetype/lato/Lato-Regular.ttf",
        "light":     "/usr/share/fonts/truetype/lato/Lato-Light.ttf",
        "mono":      "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf",
        "mono_r":    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "dejavu":    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "dejavu_r":  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "ubuntu":    "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    }
    try:
        return ImageFont.truetype(paths.get(name, paths["bold"]), size)
    except:
        return ImageFont.load_default()


# ─── Product definitions ─────────────────────────────────────────────────────

PRODUCTS = [
    {"name": "EoS", "full": "EmbeddedOS", "sub": "Real-Time Operating System\nfor Embedded Devices",
     "tagline": "From microcontrollers to multi-core SoCs",
     "c1": (0.345,0.651,1.0), "c2": (0.067,0.345,0.651), "c3": (0.02,0.10,0.30),
     "repo": "eos", "icon": "chip", "edition": "Complete Reference"},
    {"name": "eBoot", "full": "eBoot", "sub": "Secure Bootloader Platform\nfor Embedded Systems",
     "tagline": "Multi-platform secure boot & firmware updates",
     "c1": (0.247,0.725,0.314), "c2": (0.102,0.420,0.165), "c3": (0.02,0.15,0.05),
     "repo": "eBoot", "icon": "lightning", "edition": "Definitive Guide"},
    {"name": "ebuild", "full": "ebuild", "sub": "Cross-Platform Build System\n& Toolchain Manager",
     "tagline": "CMake \u00b7 Meson \u00b7 Yocto \u00b7 Ninja",
     "c1": (0.941,0.533,0.243), "c2": (0.627,0.314,0.125), "c3": (0.20,0.08,0.02),
     "repo": "ebuild", "icon": "gear", "edition": "Definitive Guide"},
    {"name": "eIPC", "full": "eIPC", "sub": "Inter-Process Communication\nFramework",
     "tagline": "gRPC \u00b7 Protocol Buffers \u00b7 Pub/Sub \u00b7 HMAC",
     "c1": (0.475,0.753,1.0), "c2": (0.165,0.376,0.565), "c3": (0.03,0.12,0.25),
     "repo": "eIPC", "icon": "network", "edition": "Definitive Guide"},
    {"name": "eAI", "full": "eAI", "sub": "Embedded Artificial Intelligence\n& TinyML Platform",
     "tagline": "TFLite \u00b7 LoRA \u00b7 Federated Learning \u00b7 Edge AI",
     "c1": (0.737,0.549,1.0), "c2": (0.431,0.251,0.667), "c3": (0.12,0.05,0.25),
     "repo": "eAI", "icon": "brain", "edition": "Definitive Guide"},
    {"name": "eNI", "full": "eNI", "sub": "Neural Interface Platform\nfor Brain-Computer Interaction",
     "tagline": "BCI \u00b7 EEG \u00b7 Neural Decoding \u00b7 Signal Processing",
     "c1": (0.969,0.471,0.729), "c2": (0.627,0.188,0.439), "c3": (0.20,0.04,0.12),
     "repo": "eNI", "icon": "waves", "edition": "Definitive Guide"},
    {"name": "EoSim", "full": "EoSim", "sub": "Multi-Architecture\nHardware Simulation Engine",
     "tagline": "QEMU \u00b7 Renode \u00b7 SystemC \u00b7 Digital Twins",
     "c1": (0.973,0.318,0.286), "c2": (0.627,0.125,0.125), "c3": (0.22,0.03,0.03),
     "repo": "EoSim", "icon": "monitor", "edition": "Definitive Guide"},
    {"name": "EoStudio", "full": "EoStudio", "sub": "Integrated Development\nEnvironment & Design Suite",
     "tagline": "IDE \u00b7 PCB Design \u00b7 Code Generation \u00b7 Debugging",
     "c1": (0.737,0.549,1.0), "c2": (0.431,0.251,0.667), "c3": (0.10,0.04,0.22),
     "repo": "EoStudio", "icon": "palette", "edition": "Definitive Guide"},
    {"name": "eApps", "full": "eApps", "sub": "Unified Application Framework\n& Marketplace",
     "tagline": "LVGL \u00b7 Touch UI \u00b7 Widget Toolkit \u00b7 App Store",
     "c1": (0.890,0.702,0.255), "c2": (0.541,0.416,0.063), "c3": (0.18,0.12,0.02),
     "repo": "eApps", "icon": "grid", "edition": "Definitive Guide"},
    {"name": "eDB", "full": "eDB", "sub": "Embedded Multi-Model\nDatabase Engine",
     "tagline": "SQL \u00b7 Document \u00b7 Graph \u00b7 Full-Text Search",
     "c1": (0.247,0.725,0.314), "c2": (0.102,0.420,0.165), "c3": (0.02,0.14,0.05),
     "repo": "eDB", "icon": "database", "edition": "Definitive Guide"},
    {"name": "eBrowser", "full": "eBrowser", "sub": "Lightweight Embedded\nWeb Browser Engine",
     "tagline": "HTML5 \u00b7 CSS3 \u00b7 JavaScript \u00b7 HTTP/2 \u00b7 TLS 1.3",
     "c1": (0.475,0.753,1.0), "c2": (0.165,0.376,0.565), "c3": (0.02,0.08,0.22),
     "repo": "eBrowser", "icon": "globe", "edition": "Definitive Guide"},
    {"name": "eOffice", "full": "eOffice", "sub": "AI-Powered Office\nProductivity Suite",
     "tagline": "Documents \u00b7 Spreadsheets \u00b7 CRDT Collaboration",
     "c1": (0.941,0.533,0.243), "c2": (0.627,0.314,0.125), "c3": (0.18,0.07,0.02),
     "repo": "eOffice", "icon": "document", "edition": "Definitive Guide"},
    {"name": "eVera", "full": "eVera", "sub": "AI Virtual Assistant\n& 3D Avatar Platform",
     "tagline": "ReAct Agents \u00b7 RAG \u00b7 Tool Use \u00b7 Three.js",
     "c1": (0.969,0.471,0.729), "c2": (0.627,0.188,0.439), "c3": (0.18,0.03,0.10),
     "repo": "eVera", "icon": "avatar", "edition": "Definitive Guide"},
    {"name": "eStocks", "full": "eStocks Trading", "sub": "Algorithmic Trading\n& Quantitative Finance",
     "tagline": "Backtesting \u00b7 Risk Management \u00b7 ML Signals",
     "c1": (0.345,0.651,1.0), "c2": (0.431,0.463,0.506), "c3": (0.05,0.08,0.15),
     "repo": "eStocks_Trading_Scripts", "icon": "chart", "edition": "Definitive Guide"},
    {"name": "eHardware", "full": "eHardware Designs", "sub": "Hardware Design\n& Product Engineering",
     "tagline": "PCB \u00b7 Radar \u00b7 Health Sensors \u00b7 KiCad",
     "c1": (0.247,0.725,0.314), "c2": (0.102,0.420,0.165), "c3": (0.02,0.12,0.04),
     "repo": "eHardware-Designs-Products", "icon": "pcb", "edition": "Definitive Guide"},
    {"name": "EmbeddedOS", "full": "Complete Ecosystem", "sub": "15 Products \u00b7 One Platform\nFrom Bootloader to Browser",
     "tagline": "The Definitive Reference for the Full EoS Platform",
     "c1": (0.737,0.549,1.0), "c2": (0.345,0.651,1.0), "c3": (0.05,0.03,0.18),
     "repo": "embeddedos-org.github.io", "icon": "ecosystem", "edition": "Complete Platform Guide"},
]


def f2i(r, g, b, a=1.0):
    """Float color to int RGBA tuple."""
    return (int(r*255), int(g*255), int(b*255), int(a*255))


def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x+w-r, y+r, r, -math.pi/2, 0)
    ctx.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+h-r, r, math.pi/2, math.pi)
    ctx.arc(x+r, y+r, r, math.pi, 3*math.pi/2)
    ctx.close_path()


# ─── Artwork drawing (Cairo context) ────────────────────────────────────────

def draw_artwork(ctx, icon, c1, c2, cx, cy):
    random.seed(hash(icon) + 42)

    if icon == "chip":
        s = 200
        # Pins
        for i in range(-4, 5):
            for side in range(4):
                ctx.save(); ctx.translate(cx, cy); ctx.rotate(side * math.pi/2)
                ctx.set_source_rgba(*c1, 0.6)
                ctx.set_line_width(3)
                ctx.move_to(i*28, -s); ctx.line_to(i*28, -s-45); ctx.stroke()
                ctx.rectangle(i*28-7, -s-52, 14, 10); ctx.fill()
                ctx.restore()
        # Package
        ctx.set_source_rgba(*c2, 0.25)
        rounded_rect(ctx, cx-s, cy-s, s*2, s*2, 18); ctx.fill()
        ctx.set_source_rgba(*c1, 0.65); ctx.set_line_width(2.5)
        rounded_rect(ctx, cx-s, cy-s, s*2, s*2, 18); ctx.stroke()
        # Die
        ctx.set_source_rgba(*c1, 0.12)
        rounded_rect(ctx, cx-s+35, cy-s+35, (s-35)*2, (s-35)*2, 8); ctx.fill()
        ctx.set_source_rgba(*c1, 0.45); ctx.set_line_width(1.5)
        rounded_rect(ctx, cx-s+35, cy-s+35, (s-35)*2, (s-35)*2, 8); ctx.stroke()
        # Internal traces
        for _ in range(15):
            x1 = cx + random.randint(-s+50, s-50)
            y1 = cy + random.randint(-s+50, s-50)
            ctx.set_source_rgba(*c1, 0.22); ctx.set_line_width(1.5)
            ctx.move_to(x1, y1)
            ctx.line_to(x1 + random.randint(-70, 70), y1)
            ctx.line_to(x1 + random.randint(-70, 70), y1 + random.randint(-70, 70))
            ctx.stroke()
            ctx.arc(x1, y1, 3.5, 0, 2*math.pi); ctx.fill()
        ctx.set_source_rgba(*c1, 0.4)
        ctx.arc(cx-s+25, cy-s+25, 10, 0, 2*math.pi); ctx.stroke()

    elif icon == "lightning":
        bolts = [(cx, cy-50, 1.0), (cx-110, cy+40, 0.55), (cx+95, cy-10, 0.45)]
        for bx, by, sc in bolts:
            pts = [(bx-20*sc,by-190*sc),(bx+55*sc,by-190*sc),(bx+10*sc,by-35*sc),
                   (bx+75*sc,by-45*sc),(bx-25*sc,by+190*sc),(bx+18*sc,by+10*sc),(bx-45*sc,by+18*sc)]
            ctx.set_source_rgba(*c1, 0.65*sc)
            ctx.move_to(*pts[0])
            for p in pts[1:]: ctx.line_to(*p)
            ctx.close_path(); ctx.fill()
        pat = cairo.RadialGradient(cx, cy, 10, cx, cy, 280)
        pat.add_color_stop_rgba(0, *c1, 0.12); pat.add_color_stop_rgba(1, *c1, 0)
        ctx.set_source(pat); ctx.rectangle(cx-280, cy-280, 560, 560); ctx.fill()

    elif icon == "gear":
        def gear(x, y, r, teeth, rot=0):
            ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
            th = r*0.2; tw = math.pi/teeth*0.6
            ctx.new_path()
            for i in range(teeth):
                a = 2*math.pi*i/teeth
                ctx.arc(0, 0, r+th, a-tw, a+tw)
                a3 = a+math.pi/teeth-tw*0.5; a4 = a+math.pi/teeth+tw*0.5
                ctx.arc_negative(0, 0, r, a4, a3)
            ctx.close_path()
            ctx.set_source_rgba(*c2, 0.3); ctx.fill_preserve()
            ctx.set_source_rgba(*c1, 0.65); ctx.set_line_width(2.5); ctx.stroke()
            ctx.arc(0, 0, r*0.32, 0, 2*math.pi); ctx.set_line_width(3); ctx.stroke()
            for i in range(6):
                a = 2*math.pi*i/6
                ctx.move_to(r*0.12*math.cos(a), r*0.12*math.sin(a))
                ctx.line_to(r*0.30*math.cos(a), r*0.30*math.sin(a))
            ctx.set_source_rgba(*c1, 0.35); ctx.set_line_width(4); ctx.stroke()
            ctx.restore()
        gear(cx-35, cy-15, 150, 16, 0)
        gear(cx+160, cy+120, 85, 10, math.pi/10)

    elif icon == "network":
        nodes = [(cx+int(random.uniform(40,240)*math.cos(random.uniform(0,6.28))),
                  cy+int(random.uniform(40,240)*math.sin(random.uniform(0,6.28))),
                  random.uniform(7,16)) for _ in range(16)]
        for i,(x1,y1,_) in enumerate(nodes):
            for x2,y2,_ in nodes[i+1:]:
                d = math.sqrt((x1-x2)**2+(y1-y2)**2)
                if d < 240:
                    ctx.set_source_rgba(*c1, max(0.04, 0.35-d/600)); ctx.set_line_width(1.5)
                    ctx.move_to(x1,y1); ctx.line_to(x2,y2); ctx.stroke()
        for nx,ny,sz in nodes:
            pat = cairo.RadialGradient(nx,ny,0,nx,ny,sz*2)
            pat.add_color_stop_rgba(0,*c1,0.75); pat.add_color_stop_rgba(1,*c1,0)
            ctx.set_source(pat); ctx.arc(nx,ny,sz*2,0,2*math.pi); ctx.fill()
            ctx.set_source_rgba(*c1,0.85); ctx.arc(nx,ny,sz,0,2*math.pi); ctx.fill()

    elif icon == "brain":
        layers = [4, 7, 9, 7, 4, 2]
        lpos = []
        tw = 460
        for li, cnt in enumerate(layers):
            lx = cx - tw//2 + int(li*tw/(len(layers)-1))
            ps = [(lx, cy+int((ni-(cnt-1)/2)*48)) for ni in range(cnt)]
            lpos.append(ps)
        for li in range(len(lpos)-1):
            for x1,y1 in lpos[li]:
                for x2,y2 in lpos[li+1]:
                    ctx.set_source_rgba(*c1, 0.06); ctx.set_line_width(1)
                    ctx.move_to(x1,y1); ctx.line_to(x2,y2); ctx.stroke()
        for layer in lpos:
            for nx,ny in layer:
                pat = cairo.RadialGradient(nx,ny,0,nx,ny,12)
                pat.add_color_stop_rgba(0,*c1,0.75); pat.add_color_stop_rgba(1,*c1,0.08)
                ctx.set_source(pat); ctx.arc(nx,ny,12,0,2*math.pi); ctx.fill()
                ctx.set_source_rgba(*c1,0.55); ctx.set_line_width(2)
                ctx.arc(nx,ny,9,0,2*math.pi); ctx.stroke()

    elif icon == "waves":
        for wi in range(5):
            wy = cy - 180 + wi * 90
            freq = [0.5,1.5,3.0,0.2,0.8][wi]
            amp = [28,18,10,45,32][wi]
            ctx.set_source_rgba(*c1, 0.55); ctx.set_line_width(2.5)
            ctx.move_to(cx-260, wy)
            for x in range(520):
                ctx.line_to(cx-260+x, wy + amp*math.sin(x*freq*0.02+wi))
            ctx.stroke()
        ctx.set_source_rgba(*c1, 0.25); ctx.set_line_width(2)
        rounded_rect(ctx, cx-280, cy-220, 580, 480, 10); ctx.stroke()

    elif icon == "monitor":
        mw, mh = 380, 250
        ctx.set_source_rgba(*c2, 0.28)
        rounded_rect(ctx, cx-mw//2, cy-mh//2-25, mw, mh, 14); ctx.fill()
        ctx.set_source_rgba(*c1, 0.65); ctx.set_line_width(3)
        rounded_rect(ctx, cx-mw//2, cy-mh//2-25, mw, mh, 14); ctx.stroke()
        ctx.set_source_rgba(*c1, 0.08)
        rounded_rect(ctx, cx-mw//2+14, cy-mh//2-10, mw-28, mh-28, 5); ctx.fill()
        ctx.set_source_rgba(*c1, 0.75); ctx.set_line_width(2)
        ctx.move_to(cx-mw//2+24, cy-25)
        for x in range(mw-48):
            px = cx-mw//2+24+x
            ctx.line_to(px, cy-25+45*math.sin(x*0.04)*math.exp(-abs(x-(mw-48)/2)*0.005))
        ctx.stroke()
        ctx.set_source_rgba(*c1, 0.45); ctx.set_line_width(4)
        ctx.move_to(cx-35, cy+mh//2-25); ctx.line_to(cx-55, cy+mh//2+45)
        ctx.move_to(cx+35, cy+mh//2-25); ctx.line_to(cx+55, cy+mh//2+45)
        ctx.move_to(cx-75, cy+mh//2+45); ctx.line_to(cx+75, cy+mh//2+45)
        ctx.stroke()

    elif icon == "palette":
        ew, eh = 400, 280
        ctx.set_source_rgba(0.06, 0.06, 0.10, 0.85)
        rounded_rect(ctx, cx-ew//2, cy-eh//2, ew, eh, 12); ctx.fill()
        ctx.set_source_rgba(0.12, 0.12, 0.18, 0.9)
        rounded_rect(ctx, cx-ew//2, cy-eh//2, ew, 32, 12); ctx.fill()
        for i, col in enumerate([(0.9,0.3,0.3),(0.9,0.8,0.2),(0.3,0.8,0.3)]):
            ctx.set_source_rgba(*col, 0.8)
            ctx.arc(cx-ew//2+22+i*20, cy-eh//2+16, 5.5, 0, 2*math.pi); ctx.fill()
        colors = [c1, (0.3,0.8,0.5), (0.9,0.7,0.3), c1, (0.8,0.4,0.4), (0.3,0.8,0.5), c1, (0.7,0.7,0.8)]
        for i, col in enumerate(colors):
            ly = cy-eh//2+46+i*26
            indent = random.choice([0,18,36,18])
            w = random.randint(75, 280)
            ctx.set_source_rgba(*col, 0.55)
            rounded_rect(ctx, cx-ew//2+18+indent, ly, min(w, ew-46-indent), 13, 3); ctx.fill()

    elif icon == "grid":
        gc = [c1, (0.3,0.8,0.5), (0.9,0.5,0.2), (0.8,0.4,0.7),
              (0.4,0.7,0.9), (0.9,0.8,0.3), c2, (0.5,0.8,0.4), (0.9,0.4,0.4)]
        tile, gap = 95, 14
        for r in range(3):
            for c_idx in range(3):
                idx = r*3+c_idx
                tx = cx-(tile*3+gap*2)//2+c_idx*(tile+gap)
                ty = cy-(tile*3+gap*2)//2+r*(tile+gap)
                ctx.set_source_rgba(*gc[idx], 0.22)
                rounded_rect(ctx, tx, ty, tile, tile, 14); ctx.fill()
                ctx.set_source_rgba(*gc[idx], 0.65); ctx.set_line_width(2)
                rounded_rect(ctx, tx, ty, tile, tile, 14); ctx.stroke()
                ctx.set_source_rgba(*gc[idx], 0.45)
                ctx.arc(tx+tile//2, ty+tile//2, 18, 0, 2*math.pi); ctx.fill()

    elif icon == "database":
        def cyl(x, y, w, h, alpha):
            ry = h*0.15
            ctx.set_source_rgba(*c2, alpha*0.35)
            ctx.move_to(x-w//2, y+ry); ctx.line_to(x-w//2, y+h-ry)
            ctx.save(); ctx.translate(x, y+h-ry); ctx.scale(w//2, ry)
            ctx.arc(0,0,1,0,math.pi); ctx.restore()
            ctx.line_to(x+w//2, y+ry); ctx.fill()
            ctx.set_source_rgba(*c1, alpha)
            ctx.save(); ctx.translate(x, y+ry); ctx.scale(w//2, ry)
            ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.fill()
            ctx.set_source_rgba(*c1, 0.65); ctx.set_line_width(2.5)
            ctx.save(); ctx.translate(x, y+ry); ctx.scale(w//2, ry)
            ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.stroke()
            ctx.move_to(x-w//2, y+ry); ctx.line_to(x-w//2, y+h-ry); ctx.stroke()
            ctx.move_to(x+w//2, y+ry); ctx.line_to(x+w//2, y+h-ry); ctx.stroke()
            ctx.save(); ctx.translate(x, y+h-ry); ctx.scale(w//2, ry)
            ctx.arc(0,0,1,0,math.pi); ctx.restore(); ctx.stroke()
        cyl(cx, cy-130, 260, 110, 0.28)
        cyl(cx, cy-25, 260, 110, 0.33)
        cyl(cx, cy+80, 260, 110, 0.38)

    elif icon == "globe":
        r = 170
        pat = cairo.RadialGradient(cx-35, cy-35, 18, cx, cy, r)
        pat.add_color_stop_rgba(0, *c1, 0.22); pat.add_color_stop_rgba(1, *c2, 0.12)
        ctx.set_source(pat); ctx.arc(cx, cy, r, 0, 2*math.pi); ctx.fill()
        ctx.set_source_rgba(*c1, 0.65); ctx.set_line_width(3)
        ctx.arc(cx, cy, r, 0, 2*math.pi); ctx.stroke()
        for i in range(-2, 3):
            ratio = i/3.0
            ctx.set_source_rgba(*c1, 0.25); ctx.set_line_width(1.5)
            ctx.save(); ctx.translate(cx, cy)
            sx = abs(ratio)*r if ratio != 0 else r*0.02
            ctx.scale(sx, r); ctx.arc(0,0,1,0,2*math.pi); ctx.restore(); ctx.stroke()
        for lat in [-60,-30,0,30,60]:
            y_off = r*math.sin(math.radians(lat))
            hw = r*math.cos(math.radians(lat))
            ctx.set_source_rgba(*c1, 0.28 if lat != 0 else 0.45); ctx.set_line_width(1.5 if lat != 0 else 2)
            ctx.move_to(cx-hw, cy-y_off); ctx.line_to(cx+hw, cy-y_off); ctx.stroke()

    elif icon == "document":
        for ox, oy in [(28,28),(14,14),(0,0)]:
            dx, dy, dw, dh = cx-125+ox, cy-170+oy, 270, 340
            ctx.set_source_rgba(0,0,0,0.08)
            rounded_rect(ctx, dx+4, dy+4, dw, dh, 8); ctx.fill()
            ctx.set_source_rgba(1,1,1,0.06)
            rounded_rect(ctx, dx, dy, dw, dh, 8); ctx.fill()
            ctx.set_source_rgba(*c1, 0.45); ctx.set_line_width(2)
            rounded_rect(ctx, dx, dy, dw, dh, 8); ctx.stroke()
        for i in range(9):
            ctx.set_source_rgba(*c1, 0.22)
            rounded_rect(ctx, cx-95, cy-140+i*28, random.randint(90,210), 9, 3); ctx.fill()

    elif icon == "avatar":
        rh = 95
        pat = cairo.RadialGradient(cx, cy-25, 18, cx, cy-8, rh)
        pat.add_color_stop_rgba(0, *c1, 0.28); pat.add_color_stop_rgba(1, *c2, 0.12)
        ctx.set_source(pat); ctx.arc(cx, cy-25, rh, 0, 2*math.pi); ctx.fill()
        ctx.set_source_rgba(*c1, 0.65); ctx.set_line_width(3)
        ctx.arc(cx, cy-25, rh, 0, 2*math.pi); ctx.stroke()
        for ex in [cx-32, cx+32]:
            ctx.set_source_rgba(*c1, 0.85); ctx.arc(ex, cy-45, 11, 0, 2*math.pi); ctx.fill()
            pat = cairo.RadialGradient(ex, cy-45, 4, ex, cy-45, 22)
            pat.add_color_stop_rgba(0, *c1, 0.35); pat.add_color_stop_rgba(1, *c1, 0)
            ctx.set_source(pat); ctx.arc(ex, cy-45, 22, 0, 2*math.pi); ctx.fill()
        ctx.set_source_rgba(*c1, 0.55); ctx.set_line_width(2.5)
        ctx.arc(cx, cy+2, 28, 0.2, math.pi-0.2); ctx.stroke()
        for i in range(12):
            a = 2*math.pi*i/12; hr = 150
            hx, hy = cx+hr*math.cos(a), cy-25+hr*math.sin(a)
            ctx.set_source_rgba(*c1, 0.25)
            ctx.arc(hx, hy, 4.5, 0, 2*math.pi); ctx.fill()
            ctx.set_line_width(1)
            ctx.move_to(cx+rh*math.cos(a), cy-25+rh*math.sin(a)); ctx.line_to(hx, hy); ctx.stroke()
        ctx.set_source_rgba(*c1, 0.35); ctx.set_line_width(3)
        ctx.move_to(cx-110, cy+110)
        ctx.curve_to(cx-75, cy+65, cx-35, cy+60, cx, cy+65)
        ctx.curve_to(cx+35, cy+60, cx+75, cy+65, cx+110, cy+110)
        ctx.stroke()

    elif icon == "chart":
        fw, fh = 480, 330; fx, fy = cx-fw//2, cy-fh//2
        ctx.set_source_rgba(*c1, 0.25); ctx.set_line_width(2)
        rounded_rect(ctx, fx, fy, fw, fh, 8); ctx.stroke()
        for i in range(1, 5):
            ctx.set_source_rgba(*c1, 0.08); ctx.set_line_width(0.5)
            ctx.move_to(fx, fy+i*fh//5); ctx.line_to(fx+fw, fy+i*fh//5); ctx.stroke()
        data = [55,-35,75,-28,85,-65,45,65,-38,55,-45,75,28,-55,65]
        cw = 22; gap = (fw-36)/len(data)
        for i, val in enumerate(data):
            x = fx+18+i*gap+gap/2; is_up = val > 0
            bh = abs(val)*2; by = cy-bh//2+random.randint(-25,25)
            ctx.set_source_rgba(*c1, 0.35); ctx.set_line_width(1.5)
            ctx.move_to(x, by-18); ctx.line_to(x, by+bh+18); ctx.stroke()
            if is_up: ctx.set_source_rgba(0.2,0.8,0.4,0.65)
            else: ctx.set_source_rgba(0.9,0.3,0.3,0.65)
            ctx.rectangle(x-cw//2, by, cw, bh); ctx.fill()

    elif icon == "pcb":
        bw, bh = 400, 300
        ctx.set_source_rgba(0.0,0.12,0.04,0.35)
        rounded_rect(ctx, cx-bw//2, cy-bh//2, bw, bh, 8); ctx.fill()
        ctx.set_source_rgba(*c1, 0.45); ctx.set_line_width(2)
        rounded_rect(ctx, cx-bw//2, cy-bh//2, bw, bh, 8); ctx.stroke()
        for _ in range(22):
            x1 = cx+random.randint(-bw//2+18, bw//2-18)
            y1 = cy+random.randint(-bh//2+18, bh//2-18)
            ctx.set_source_rgba(*c1, 0.30); ctx.set_line_width(2)
            ctx.move_to(x1, y1)
            if random.random()>0.5:
                x2 = x1+random.randint(-90,90); ctx.line_to(x2, y1)
                ctx.line_to(x2, y1+random.randint(-55,55))
            else: ctx.line_to(x1, y1+random.randint(-75,75))
            ctx.stroke()
        for _ in range(28):
            px = cx+random.randint(-bw//2+12, bw//2-12)
            py = cy+random.randint(-bh//2+12, bh//2-12)
            ctx.set_source_rgba(*c1, 0.55); ctx.arc(px, py, 4.5, 0, 2*math.pi); ctx.fill()
        for _ in range(3):
            ix = cx+random.randint(-bw//3, bw//3); iy = cy+random.randint(-bh//3, bh//3)
            iw, ih = random.randint(28,55), random.randint(18,38)
            ctx.set_source_rgba(0.08,0.08,0.12,0.55); ctx.rectangle(ix-iw//2,iy-ih//2,iw,ih); ctx.fill()
            ctx.set_source_rgba(*c1, 0.35); ctx.set_line_width(1)
            ctx.rectangle(ix-iw//2,iy-ih//2,iw,ih); ctx.stroke()

    elif icon == "ecosystem":
        hex_r, ring_r = 55, 170
        for i in range(6):
            a = 2*math.pi*i/6-math.pi/6
            hx, hy = cx+int(ring_r*math.cos(a)), cy+int(ring_r*math.sin(a))
            ctx.new_path()
            for v in range(6):
                va = 2*math.pi*v/6+math.pi/6
                vx, vy = hx+hex_r*0.78*math.cos(va), hy+hex_r*0.78*math.sin(va)
                ctx.line_to(vx, vy) if v else ctx.move_to(vx, vy)
            ctx.close_path()
            t = i/6.0
            col = (c1[0]*(1-t)+c2[0]*t, c1[1]*(1-t)+c2[1]*t, c1[2]*(1-t)+c2[2]*t)
            ctx.set_source_rgba(*col, 0.18); ctx.fill_preserve()
            ctx.set_source_rgba(*col, 0.55); ctx.set_line_width(2); ctx.stroke()
            ctx.set_source_rgba(*c1, 0.18); ctx.set_line_width(2)
            ctx.move_to(cx, cy); ctx.line_to(hx, hy); ctx.stroke()
        ctx.new_path()
        for v in range(6):
            va = 2*math.pi*v/6+math.pi/6
            vx, vy = cx+hex_r*math.cos(va), cy+hex_r*math.sin(va)
            ctx.line_to(vx, vy) if v else ctx.move_to(vx, vy)
        ctx.close_path()
        ctx.set_source_rgba(*c1, 0.25); ctx.fill_preserve()
        ctx.set_source_rgba(*c1, 0.75); ctx.set_line_width(3); ctx.stroke()


# ─── Cover generation ────────────────────────────────────────────────────────

def generate_cover(product):
    c1, c2, c3 = product["c1"], product["c2"], product["c3"]

    # ═══ Phase 1: Cairo vector graphics ═══
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surface)

    # Background gradient
    pat = cairo.LinearGradient(0, 0, 0, H)
    pat.add_color_stop_rgb(0.0, *c3)
    pat.add_color_stop_rgb(0.30, min(1,c3[0]*1.6), min(1,c3[1]*1.6), min(1,c3[2]*1.6))
    pat.add_color_stop_rgb(0.60, min(1,c3[0]*0.9), min(1,c3[1]*0.9), min(1,c3[2]*0.9))
    pat.add_color_stop_rgb(1.0, max(0,c3[0]*0.35), max(0,c3[1]*0.35), max(0,c3[2]*0.35))
    ctx.set_source(pat); ctx.rectangle(0,0,W,H); ctx.fill()

    # Subtle diagonal texture
    ctx.set_source_rgba(*c1, 0.018); ctx.set_line_width(0.5)
    for i in range(-H, W+H, 28):
        ctx.move_to(i,0); ctx.line_to(i+H,H); ctx.stroke()

    # Top publisher band
    band_h = 95
    pat = cairo.LinearGradient(0,0,W,0)
    pat.add_color_stop_rgba(0, *c1, 0.82)
    pat.add_color_stop_rgba(0.5, *c2, 0.88)
    pat.add_color_stop_rgba(1, *c1, 0.82)
    ctx.set_source(pat); ctx.rectangle(0,0,W,band_h); ctx.fill()

    # Band accent line
    ctx.set_source_rgba(*c1, 0.55); ctx.set_line_width(3)
    ctx.move_to(0, band_h); ctx.line_to(W, band_h); ctx.stroke()

    # Decorative line above artwork
    ctx.set_source_rgba(*c1, 0.35); ctx.set_line_width(2)
    ctx.move_to(180, 590); ctx.line_to(W-180, 590); ctx.stroke()

    # Central artwork
    draw_artwork(ctx, product["icon"], c1, c2, W//2, 1150)

    # Version badge outline
    badge_y = 1500
    ctx.set_source_rgba(*c1, 0.13)
    rounded_rect(ctx, W//2-90, badge_y, 180, 40, 8); ctx.fill()
    ctx.set_source_rgba(*c1, 0.55); ctx.set_line_width(1.5)
    rounded_rect(ctx, W//2-90, badge_y, 180, 40, 8); ctx.stroke()

    # Bottom darkening gradient
    pat = cairo.LinearGradient(0, H-380, 0, H)
    pat.add_color_stop_rgba(0, 0,0,0, 0)
    pat.add_color_stop_rgba(0.5, 0,0,0, 0.28)
    pat.add_color_stop_rgba(1, 0,0,0, 0.55)
    ctx.set_source(pat); ctx.rectangle(0, H-380, W, 380); ctx.fill()

    # Bottom accent line
    ctx.set_source_rgba(*c1, 0.45); ctx.set_line_width(3)
    ctx.move_to(55, H-330); ctx.line_to(W-55, H-330); ctx.stroke()

    # Bottom publisher bar
    bar_h = 85; bar_y = H-bar_h
    ctx.set_source_rgba(*c2, 0.65); ctx.rectangle(0, bar_y, W, bar_h); ctx.fill()
    ctx.set_source_rgba(*c1, 0.75); ctx.set_line_width(3)
    ctx.move_to(0, bar_y); ctx.line_to(W, bar_y); ctx.stroke()

    # ISBN barcode placeholder
    isbn_x = W-195; isbn_y = bar_y-65
    ctx.set_source_rgba(1,1,1,0.06); ctx.rectangle(isbn_x, isbn_y, 135, 50); ctx.fill()
    for i in range(24):
        bx = isbn_x+8+i*5
        bh_bar = random.randint(22,38)
        ctx.set_source_rgba(*c1, 0.18); ctx.set_line_width(2 if random.random()>0.3 else 3)
        ctx.move_to(bx, isbn_y+4); ctx.line_to(bx, isbn_y+4+bh_bar); ctx.stroke()

    # Spine stripe
    pat = cairo.LinearGradient(0,0,0,H)
    pat.add_color_stop_rgba(0, *c1, 0.78)
    pat.add_color_stop_rgba(0.5, *c2, 0.85)
    pat.add_color_stop_rgba(1, *c1, 0.78)
    ctx.set_source(pat); ctx.rectangle(0,0,11,H); ctx.fill()

    surface.flush()

    # ═══ Phase 2: PIL text rendering ═══
    # Convert Cairo surface to PIL Image
    buf = surface.get_data()
    img = Image.frombuffer("RGBA", (W, H), bytes(buf), "raw", "BGRA", 0, 1).copy()
    draw = ImageDraw.Draw(img)

    # Color helper
    ci1 = f2i(*c1)
    ci1_a = lambda a: f2i(*c1, a)

    # Publisher text in top band
    f_publisher = load_font("heavy", 32)
    f_pub_sub = load_font("regular", 16)
    f_edition = load_font("bold", 16)
    draw.text((58, 20), "EMBEDDEDOS PRESS", fill=(255,255,255,242), font=f_publisher)
    draw.text((58, 58), "Open Source Technical Publishing", fill=(255,255,255,178), font=f_pub_sub)

    # Edition badge (right side of top band)
    ew = draw.textlength(product["edition"], font=f_edition)
    draw.text((W - int(ew) - 58, 36), product["edition"], fill=(255,255,255,204), font=f_edition)

    # Product name (large)
    name = product["name"]
    name_y = 150
    if "\n" in name:
        lines = name.split("\n")
        for i, line in enumerate(lines):
            fsize = 80
            f_name = load_font("black", fsize)
            tw = draw.textlength(line, font=f_name)
            x = (W - int(tw)) // 2
            draw.text((x+4, name_y + i*105 + 4), line, fill=(0,0,0,76), font=f_name)
            draw.text((x, name_y + i*105), line, fill=(255,255,255,250), font=f_name)
    else:
        fsize = 120 if len(name) <= 5 else 110 if len(name) <= 7 else 95 if len(name) <= 9 else 80
        f_name = load_font("black", fsize)
        tw = draw.textlength(name, font=f_name)
        x = (W - int(tw)) // 2
        draw.text((x+4, name_y+5), name, fill=(0,0,0,76), font=f_name)
        draw.text((x, name_y), name, fill=(255,255,255,250), font=f_name)

    # Full name if different
    if product["full"] != name and "\n" not in product["full"]:
        f_full = load_font("semibold", 36)
        tw = draw.textlength(product["full"], font=f_full)
        x = (W - int(tw)) // 2
        fy = name_y + (110 if len(name) <= 5 else 95 if len(name) <= 7 else 80) + 20
        draw.text((x, fy), product["full"], fill=ci1_a(0.7), font=f_full)

    # Subtitle
    f_sub = load_font("regular", 30)
    sub_y = 390 if "\n" not in name else 410
    for i, line in enumerate(product["sub"].split("\n")):
        tw = draw.textlength(line, font=f_sub)
        x = (W - int(tw)) // 2
        draw.text((x, sub_y + i * 40), line, fill=ci1_a(0.82), font=f_sub)

    # Tagline
    f_tag = load_font("medium", 20)
    tag_y = sub_y + len(product["sub"].split("\n")) * 40 + 25
    tw = draw.textlength(product["tagline"], font=f_tag)
    x = (W - int(tw)) // 2
    draw.text((x, tag_y), product["tagline"], fill=(204,204,216,178), font=f_tag)

    # Version badge text
    f_ver = load_font("bold", 22)
    ver = "Version 1.0.0"
    tw = draw.textlength(ver, font=f_ver)
    draw.text(((W - int(tw)) // 2, 1507), ver, fill=(255,255,255,230), font=f_ver)

    # Author
    f_author = load_font("bold", 36)
    f_contrib = load_font("regular", 23)
    author = "Srikanth Patchava"
    tw = draw.textlength(author, font=f_author)
    draw.text(((W - int(tw)) // 2, H - 310), author, fill=(255,255,255,242), font=f_author)
    contrib = "& EmbeddedOS Contributors"
    tw = draw.textlength(contrib, font=f_contrib)
    draw.text(((W - int(tw)) // 2, H - 268), contrib, fill=(255,255,255,153), font=f_contrib)

    # Bottom bar text
    f_bar = load_font("bold", 23)
    f_bar_sub = load_font("regular", 15)
    f_bar_r = load_font("regular", 21)
    f_bar_badge = load_font("bold", 15)
    draw.text((58, bar_y+16), "EmbeddedOS Press", fill=(255,255,255,230), font=f_bar)
    draw.text((58, bar_y+46), "embeddedos-org.github.io", fill=(255,255,255,153), font=f_bar_sub)
    draw.text((W-245, bar_y+16), "April 2026", fill=(255,255,255,178), font=f_bar_r)
    draw.text((W-245, bar_y+46), "Open Source", fill=(255,255,255,127), font=f_bar_badge)

    # Convert to RGB
    final = Image.new("RGB", (W, H), (0, 0, 0))
    final.paste(img, mask=img.split()[3])
    return final


def main():
    for product in PRODUCTS:
        repo_dir = os.path.join(ORG_DIR, product["repo"])
        book_dir = os.path.join(repo_dir, "docs", "book")
        if not os.path.isdir(repo_dir):
            print(f"SKIP: {product['repo']}"); continue
        os.makedirs(book_dir, exist_ok=True)
        out = os.path.join(book_dir, "cover.png")
        print(f"Generating: {product['name']:20s} -> {out}")
        cover = generate_cover(product)
        cover.save(out, "PNG", optimize=True)
        print(f"  {os.path.getsize(out):,} bytes ({os.path.getsize(out)/1024:.0f} KB)")
    print("\nAll covers generated!")


if __name__ == "__main__":
    main()
