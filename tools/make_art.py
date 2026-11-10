# -*- coding: utf-8 -*-
"""Procedural concept-art generator for 春声南来.

The goal is not photorealistic illustration, but a coherent painterly
placeholder set: watercolor gouache, muted warm brown / kerosene yellow /
teal, film grain, soft edges. Every image can be replaced by a hand-painted
or AI-generated asset with the same filename.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

BASE = Path(r"D:\try_deepseek_harness\chunsheng_nanlai")
BG = BASE / "game" / "images" / "bg"
GUI = BASE / "game" / "gui"
PORTRAIT = BASE / "game" / "images" / "portraits"
for d in (BG, GUI, PORTRAIT, GUI / "button", GUI / "overlay"):
    d.mkdir(parents=True, exist_ok=True)

S = 2
W, H = 1920 * S, 1080 * S

P = {
    "paper": "#F3E7D3",
    "cream": "#E8D6BC",
    "brown": "#8B5E3C",
    "darkbrown": "#5A3A28",
    "red": "#A33327",
    "deepred": "#6E1F1A",
    "kerosene": "#D99A4E",
    "teal": "#4F6F5A",
    "darkteal": "#2F4A42",
    "night": "#1E2428",
    "grayblue": "#5C6B73",
    "sky": "#C9B18E",
    "dust": "#B99B73",
}


def rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgba(h: str, a: int = 255):
    return rgb(h) + (a,)


def gradient(top: str, bottom: str, w=W, h=H, tint: float = 0.0):
    t = np.array(rgb(top), dtype=np.float32)
    b = np.array(rgb(bottom), dtype=np.float32)
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    arr = t[None, None, :] * (1 - y[:, :, None]) + b[None, None, :] * y[:, :, None]
    arr = np.repeat(arr, w, axis=1)
    if tint:
        x = np.linspace(-1, 1, w, dtype=np.float32)[None, :, None]
        arr = arr + tint * 12 * np.sin(x * math.pi) * np.array([1.0, 0.7, 0.4])
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")


def noise_img(w=W, h=H, scale=1.0):
    arr = np.random.normal(128, 22, (h, w)).astype(np.float32)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "L")
    if scale > 1:
        img = img.resize((w // int(scale), h // int(scale)), Image.Resampling.BILINEAR)
        img = img.resize((w, h), Image.Resampling.BILINEAR)
    return img


def add_grain(img: Image.Image, amount=5.0):
    arr = np.array(img).astype(np.float32)
    g = np.random.normal(0, amount, (img.height, img.width, 1))
    arr = np.clip(arr + g, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def add_paper(img: Image.Image, alpha=18):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(350):
        x = random.randrange(img.width)
        y = random.randrange(img.height)
        ln = random.randint(20, 160)
        d.line((x, y, x + ln, y + random.randint(-3, 3)),
               fill=rgba(P["cream"], random.randint(4, alpha)), width=1)
    layer = layer.filter(ImageFilter.GaussianBlur(0.6))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def add_brush(img: Image.Image, colors=None, n=260, alpha=10):
    colors = colors or [P["cream"], P["brown"], P["teal"], P["kerosene"]]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        x = random.randrange(img.width)
        y = random.randrange(img.height)
        w = random.randint(30, 220)
        h = random.randint(2, 10)
        col = rgba(random.choice(colors), random.randint(2, alpha))
        d.ellipse((x, y, x + w, y + h), fill=col)
    layer = layer.filter(ImageFilter.GaussianBlur(2.0))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def vignette(img: Image.Image, strength=0.45):
    w, h = img.size
    x = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
    y = np.linspace(-1, 1, h, dtype=np.float32)[:, None]
    r = np.sqrt(x * x + y * y)
    mask = np.clip(1.0 - strength * np.clip((r - 0.35) / 0.8, 0, 1) ** 1.6, 0, 1)
    arr = np.array(img).astype(np.float32) * mask[:, :, None]
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")


def glow(img: Image.Image, center, radius, color, strength=1.0, blend="screen"):
    w, h = img.size
    cx, cy = center
    x = np.arange(w, dtype=np.float32)[None, :]
    y = np.arange(h, dtype=np.float32)[:, None]
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    a = np.clip(1.0 - r / radius, 0, 1) ** 2 * strength
    layer = np.zeros((h, w, 3), dtype=np.float32)
    layer[:, :] = np.array(rgb(color), dtype=np.float32)
    out = np.array(img).astype(np.float32)
    if blend == "screen":
        out = 255 - (255 - out) * (255 - layer * a[:, :, None]) / 255
    else:
        out = out * (1 - a[:, :, None]) + layer * a[:, :, None]
    return Image.fromarray(np.uint8(np.clip(out, 0, 255)), "RGB")


def soft_poly(img: Image.Image, pts, color, blur=6):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.polygon(pts, fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def soft_ellipse(img: Image.Image, box, color, blur=8):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def line(img: Image.Image, pts, color, width=3, blur=0):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line(pts, fill=color, width=width, joint="curve")
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


_TEX_CACHE = {}


def darken(h: str, f=0.72):
    r, g, b = rgb(h)
    return "#%02X%02X%02X" % (int(r * f), int(g * f), int(b * f))


def paper_tex(color: str):
    """A full-size mottled paper fill, cached by colour."""
    if color in _TEX_CACHE:
        return _TEX_CACHE[color]
    base = np.array(rgb(color), dtype=np.float32)
    # low-frequency watercolour mottling
    small = np.random.normal(0, 1, (H // 24, W // 24)).astype(np.float32)
    small = np.array(Image.fromarray(((small - small.min()) / (np.ptp(small) + 1e-6) * 255).astype(np.uint8), "L"))
    mottle = Image.fromarray(small, "L").resize((W, H), Image.Resampling.BICUBIC)
    m = (np.array(mottle).astype(np.float32) - 127) / 127
    arr = base[None, None, :] + m[:, :, None] * 9 + np.random.normal(0, 3.0, (H, W, 1))
    img = Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB").convert("RGBA")
    d = ImageDraw.Draw(img)
    # paper fibres
    for _ in range(900):
        x = random.randrange(W)
        y = random.randrange(H)
        ln = random.randint(10, 90)
        d.line((x, y, x + ln, y + random.randint(-2, 2)),
               fill=rgba(P["cream"] if rgb(color)[0] < 150 else "#FFFFFF", random.randint(3, 10)), width=1)
    # faint stains
    for _ in range(26):
        x = random.randrange(W)
        y = random.randrange(H)
        r = random.randint(60, 260)
        d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(darken(color, 0.9), random.randint(3, 9)))
    img = img.filter(ImageFilter.GaussianBlur(0.8))
    out = img.convert("RGB")
    _TEX_CACHE[color] = out
    return out


def textured_poly(img, pts, color, alpha=255, shadow=14, jitter=3, edge=True):
    pts = [(x + random.randint(-jitter, jitter), y + random.randint(-jitter, jitter)) for x, y in pts]
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon(pts, fill=alpha)
    if shadow:
        sh = mask.filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: int(v * 0.38))
        sh = ImageChops.offset(sh, 0, max(2, shadow // 3))
        img = Image.composite(Image.new("RGBA", img.size, (16, 11, 8, 255)), img.convert("RGBA"), sh).convert("RGB")
    tex = paper_tex(color)
    img.paste(tex, (0, 0), mask)
    if edge:
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).line(pts + [pts[0]], fill=rgba(darken(color, 0.62), 90), width=3, joint="curve")
        overlay = overlay.filter(ImageFilter.GaussianBlur(1.2))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img


def textured_ellipse(img, box, color, alpha=255, shadow=10, edge=True):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse(box, fill=alpha)
    if shadow:
        sh = mask.filter(ImageFilter.GaussianBlur(shadow)).point(lambda v: int(v * 0.35))
        sh = ImageChops.offset(sh, 0, max(2, shadow // 3))
        img = Image.composite(Image.new("RGBA", img.size, (16, 11, 8, 255)), img.convert("RGBA"), sh).convert("RGB")
    tex = paper_tex(color)
    img.paste(tex, (0, 0), mask)
    if edge:
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).ellipse(box, outline=rgba(darken(color, 0.62), 80), width=3)
        overlay = overlay.filter(ImageFilter.GaussianBlur(1.0))
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return img


def person(img, x, y, h, color=P["darkbrown"], alpha=230, pose="stand", blur=2,
           simple=False, bag=False, coat=False):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = rgba(color, alpha)
    # ground shadow
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((x - h * 0.20, y - h * 0.035, x + h * 0.20, y + h * 0.03),
                               fill=(12, 8, 6, 55))
    img = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(8))).convert("RGB")
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    hx, hy = x, y - h * 0.86
    rx, ry = h * 0.072, h * 0.092
    d.ellipse((hx - rx, hy - ry, hx + rx, hy + ry), fill=c)
    # neck
    d.rectangle((x - h * 0.027, y - h * 0.79, x + h * 0.027, y - h * 0.745), fill=c)
    # shoulders
    d.polygon([(x - h * 0.17, y - h * 0.73), (x - h * 0.08, y - h * 0.775),
               (x + h * 0.08, y - h * 0.775), (x + h * 0.17, y - h * 0.73)], fill=c)
    # torso, with a slight 1980s jacket flare
    flare = h * 0.035 if coat else 0
    d.polygon([(x - h * 0.155, y - h * 0.73), (x + h * 0.155, y - h * 0.73),
               (x + h * 0.13 + flare, y - h * 0.27), (x - h * 0.13 - flare, y - h * 0.27)], fill=c)

    if simple:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
        return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

    if pose == "sit":
        # upper legs forward, lower legs down
        d.polygon([(x - h * 0.13, y - h * 0.29), (x + h * 0.13, y - h * 0.29),
                   (x + h * 0.30, y - h * 0.18), (x + h * 0.22, y - h * 0.10)], fill=c)
        d.polygon([(x + h * 0.16, y - h * 0.18), (x + h * 0.30, y - h * 0.18),
                   (x + h * 0.31, y - h * 0.01), (x + h * 0.22, y - h * 0.01)], fill=c)
        # arm resting on knee
        d.line((x - h * 0.14, y - h * 0.67, x - h * 0.02, y - h * 0.39), fill=c, width=max(2, int(h * 0.045)))
    else:
        # legs with a gap
        d.polygon([(x - h * 0.115, y - h * 0.28), (x - h * 0.018, y - h * 0.28),
                   (x - h * 0.030, y - h * 0.015), (x - h * 0.105, y - h * 0.015)], fill=c)
        d.polygon([(x + h * 0.018, y - h * 0.28), (x + h * 0.115, y - h * 0.28),
                   (x + h * 0.105, y - h * 0.015), (x + h * 0.030, y - h * 0.015)], fill=c)
        # shoes
        d.ellipse((x - h * 0.125, y - h * 0.035, x - h * 0.005, y + h * 0.005), fill=c)
        d.ellipse((x + h * 0.005, y - h * 0.035, x + h * 0.125, y + h * 0.005), fill=c)
        # arms, slightly away from body
        d.line((x - h * 0.15, y - h * 0.68, x - h * 0.20, y - h * 0.40), fill=c, width=max(2, int(h * 0.042)))
        d.line((x + h * 0.15, y - h * 0.68, x + h * 0.19, y - h * 0.40), fill=c, width=max(2, int(h * 0.042)))

    if bag:
        bx, by = x + h * 0.19, y - h * 0.40
        d.rectangle((bx, by, bx + h * 0.12, by + h * 0.17), fill=rgba("#6E4A35", alpha))
        d.arc((bx, by - h * 0.08, bx + h * 0.12, by + h * 0.05), 200, 340,
              fill=rgba("#2B2420", alpha), width=max(2, int(h * 0.012)))

    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def house(img, x, y, w, h, wall=P["dust"], roof=P["darkbrown"], alpha=255):
    # wall
    img = textured_poly(img, [(x, y - h), (x + w, y - h), (x + w, y), (x, y)],
                        wall, alpha=alpha, shadow=18, jitter=2)
    # roof with overhang
    img = textured_poly(img, [(x - w * 0.10, y - h * 0.98), (x + w * 0.50, y - h - h * 0.48),
                              (x + w * 1.10, y - h * 0.98), (x + w * 0.96, y - h * 0.88),
                              (x + w * 0.50, y - h - h * 0.35), (x + w * 0.04, y - h * 0.88)],
                        roof, alpha=alpha, shadow=14, jitter=2)
    # door
    img = textured_poly(img, [(x + w * 0.42, y - h * 0.56), (x + w * 0.58, y - h * 0.56),
                              (x + w * 0.58, y), (x + w * 0.42, y)],
                        P["darkbrown"], alpha=min(alpha, 235), shadow=8, jitter=1)
    # window with warm light
    img = textured_poly(img, [(x + w * 0.13, y - h * 0.74), (x + w * 0.30, y - h * 0.74),
                              (x + w * 0.30, y - h * 0.50), (x + w * 0.13, y - h * 0.50)],
                        P["kerosene"], alpha=180, shadow=6, jitter=1)
    # eaves line
    img = line(img, [(x - w * 0.11, y - h * 0.98), (x + w * 1.11, y - h * 0.98)],
               rgba(P["deepred"], 70), width=4, blur=2)
    return img


def tree(img, x, y, h, color=P["darkteal"], alpha=220):
    # trunk
    img = textured_poly(img, [(x - h * 0.018, y), (x + h * 0.020, y),
                              (x + h * 0.010, y - h * 0.62), (x - h * 0.010, y - h * 0.62)],
                        P["darkbrown"], alpha=alpha, shadow=8, jitter=1)
    # canopy: overlapping paper blobs
    for i in range(9):
        cx = x + random.randint(-int(h * 0.26), int(h * 0.26))
        cy = y - h * (0.50 + random.random() * 0.38)
        r = h * (0.12 + random.random() * 0.10)
        img = textured_poly(img, [(cx + r * math.cos(a), cy + r * 0.8 * math.sin(a))
                                  for a in [i * math.pi / 4 for i in range(8)]],
                            color, alpha=alpha - 20, shadow=10, jitter=3, edge=False)
    return img


def field(img, horizon, near="#8B5E3C", far="#C9A86A", rows=22):
    # ground mass
    img = textured_poly(img, [(-40, horizon), (W + 40, horizon - 12), (W + 40, H + 40), (-40, H + 40)],
                        near, alpha=255, shadow=0, jitter=2, edge=False)
    # painterly bands
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(12):
        yy = horizon + (H - horizon) * (i / 12) ** 1.45
        d.rectangle((0, yy, W, yy + (H - horizon) * 0.035), fill=rgba(far, random.randint(18, 38)))
    # furrows
    vx = W * 0.5
    for i in range(rows):
        x = -W * 0.45 + i * W * 0.075
        d.line((vx + (x - vx) * 0.02, horizon + 3, x, H),
               fill=rgba(P["darkbrown"], 55), width=max(2, int(2 + i * 0.3)))
    layer = layer.filter(ImageFilter.GaussianBlur(7))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    # grass / stubble
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(1300):
        x = random.randrange(W)
        y = random.randrange(int(horizon + (H - horizon) * 0.2), H)
        ln = random.randint(4, 20)
        d.line((x, y, x + random.randint(-3, 3), y - ln),
               fill=rgba(random.choice([far, P["cream"], P["darkbrown"]]), random.randint(15, 40)), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    # distant haze
    img = glow(img, (W * 0.55, horizon - H * 0.02), W * 0.65, P["cream"], 0.18)
    return img


def city(img, horizon, color=P["grayblue"], alpha=245, density=18):
    # haze behind skyline
    img = glow(img, (W * 0.78, horizon - H * 0.12), W * 0.35, "#C9D5D8", 0.10)
    x = int(W * 0.52)
    for i in range(density):
        bw = random.randint(int(W * 0.022), int(W * 0.060))
        bh = random.randint(int(H * 0.10), int(H * 0.36))
        bx = int(x + i * W * 0.013 + random.randint(-25, 25))
        by = int(horizon - bh)
        # building body
        img = textured_poly(img, [(bx, by), (bx + bw, by), (bx + bw, horizon), (bx, horizon)],
                            color, alpha=alpha, shadow=12, jitter=2, edge=False)
        # roof lip
        img = line(img, [(bx - 4, by), (bx + bw + 4, by)], rgba(darken(color, 0.7), 160), width=4, blur=1)
        # windows
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for wy in range(by + 24, horizon - 24, 38):
            for wx in range(bx + 14, bx + bw - 14, 28):
                if random.random() < 0.32:
                    d.rectangle((wx, wy, wx + 7, wy + 11), fill=rgba(P["kerosene"], random.randint(40, 130)))
        img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(1.2))).convert("RGB")
    # cranes and scaffolding
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(5):
        cx = W * (0.56 + i * 0.09)
        cy = horizon
        d.line((cx, cy, cx, cy - H * 0.34), fill=rgba(P["darkbrown"], 170), width=5)
        d.line((cx, cy - H * 0.32, cx + W * 0.08, cy - H * 0.30),
               fill=rgba(P["darkbrown"], 170), width=4)
        d.line((cx, cy - H * 0.32, cx - W * 0.04, cy - H * 0.30),
               fill=rgba(P["darkbrown"], 170), width=3)
    img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(2))).convert("RGB")
    # atmospheric haze in front of skyline
    img = glow(img, (W * 0.80, horizon - H * 0.10), W * 0.40, "#D8D2C4", 0.15)
    return img


def rail(img, horizon):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    vx = W * 0.5
    for off in (-0.06, 0.06):
        d.polygon([(vx + W * off * 0.1, horizon), (vx + W * off * 0.1 + 6, horizon),
                   (vx + W * off * 8, H), (vx + W * off * 8 - 10, H)],
                  fill=rgba(P["darkbrown"], 220))
    for i in range(1, 18):
        t = (i / 18) ** 1.8
        y = horizon + (H - horizon) * t
        half = W * 0.01 + W * 0.22 * t
        d.line((vx - half, y, vx + half, y), fill=rgba(P["darkbrown"], 200), width=max(2, int(2 + 6 * t)))
    layer = layer.filter(ImageFilter.GaussianBlur(1.5))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def finish(img, path, grain=4.5, vig=0.38, paper=12, brush=8, quality=92):
    img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
    img = add_paper(img, paper)
    img = add_brush(img, n=220, alpha=brush)
    img = vignette(img, vig)
    img = add_grain(img, grain)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "WEBP", quality=quality, method=6)
    print("wrote", path.name, path.stat().st_size // 1024, "KB")


# ---------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------

def clouds(img, y0, y1, color=P["cream"], alpha=40, n=18):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        x = random.randrange(W)
        y = random.randint(int(y0), int(y1))
        w = random.randint(int(W * 0.08), int(W * 0.30))
        h = random.randint(int(H * 0.02), int(H * 0.08))
        d.ellipse((x, y, x + w, y + h), fill=rgba(color, random.randint(10, alpha)))
    layer = layer.filter(ImageFilter.GaussianBlur(24))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def scene_menu():
    img = gradient("#D8B98C", "#6A4532", tint=0.6)
    img = clouds(img, H * 0.06, H * 0.34, color="#F3E7D3", alpha=55)
    # distant mountains, layered
    img = textured_poly(img, [(-100, H * 0.58), (W * 0.18, H * 0.43), (W * 0.42, H * 0.57),
                              (W * 0.66, H * 0.47), (W * 1.1, H * 0.56), (W * 1.1, H), (-100, H)],
                        "#A98A67", alpha=210, shadow=0, jitter=4, edge=False)
    img = glow(img, (W * 0.3, H * 0.5), W * 0.45, "#E8D6BC", 0.16)
    img = field(img, int(H * 0.60), near="#8B5E3C", far="#D0A76A", rows=28)
    # village left, layered
    for x, y, w, h in [(0.03, 0.66, 0.095, 0.10), (0.13, 0.69, 0.075, 0.075),
                        (0.20, 0.66, 0.10, 0.10), (0.30, 0.70, 0.065, 0.065)]:
        img = house(img, W * x, H * y, W * w, H * h, wall="#B99B73", roof="#4A3226")
    img = tree(img, W * 0.28, H * 0.71, H * 0.21, color="#4F6F5A")
    img = tree(img, W * 0.01, H * 0.72, H * 0.17, color="#3F5A4A")
    # city right, low and hazy
    img = city(img, int(H * 0.62), color="#5C6B73", density=20)
    # rail
    img = rail(img, int(H * 0.64))
    # green train, side view, on the track
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tx, ty, tw, th = W * 0.38, H * 0.56, W * 0.22, H * 0.085
    d.rounded_rectangle((tx, ty, tx + tw, ty + th), radius=26, fill=rgba("#3F5A4A", 250))
    # windows
    for i in range(5):
        wx = tx + tw * (0.06 + i * 0.18)
        d.rounded_rectangle((wx, ty + th * 0.20, wx + tw * 0.13, ty + th * 0.58), radius=8,
                            fill=rgba("#D99A4E", 165))
    # front stripe
    d.rectangle((tx, ty + th * 0.68, tx + tw, ty + th * 0.82), fill=rgba("#2F4A42", 240))
    # wheels
    for wx in (tx + tw * 0.15, tx + tw * 0.72):
        d.ellipse((wx, ty + th * 0.86, wx + th * 0.30, ty + th * 1.08), fill=rgba("#1B1511", 250))
    # steam
    for i in range(5):
        d.ellipse((tx + tw * 0.06 + i * 30, ty - 30 - i * 18, tx + tw * 0.06 + 90 + i * 30, ty + 20 - i * 18),
                  fill=rgba("#F3E7D3", 22))
    img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(2))).convert("RGB")
    # young man with bag, foreground
    img = person(img, W * 0.34, H * 0.88, H * 0.26, color="#241B16", alpha=252, blur=1, bag=True, coat=True)
    # spring wind lines
    for i in range(9):
        y = H * (0.22 + i * 0.042)
        pts = [(W * 0.02, y + 10 * math.sin(i)), (W * 0.34, y - 7), (W * 0.66, y + 5), (W * 0.99, y - 9)]
        img = line(img, pts, rgba(P["cream"], 75), width=4, blur=3)
    # warm light + dust
    img = glow(img, (W * 0.66, H * 0.34), W * 0.42, P["kerosene"], 0.30)
    img = glow(img, (W * 0.34, H * 0.74), W * 0.18, "#F3E7D3", 0.20)
    finish(img, BG / "bg_menu.webp", grain=4, vig=0.42, paper=16, brush=9)


def scene_tangwu():
    img = gradient("#2A211B", "#120F0D", tint=0.2)
    # mud wall
    img = textured_poly(img, [(0, 0), (W, 0), (W, H * 0.79), (0, H * 0.81)],
                        "#6B4B34", alpha=255, shadow=0, jitter=3, edge=False)
    # wall patches and cracks
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(28):
        x = random.randrange(W)
        y = random.randrange(int(H * 0.75))
        w = random.randint(100, 280)
        h = random.randint(20, 70)
        d.ellipse((x, y, x + w, y + h), fill=rgba("#8B5E3C", random.randint(8, 22)))
    for _ in range(18):
        x = random.randrange(W)
        y = random.randrange(int(H * 0.75))
        d.line((x, y, x + random.randint(-40, 40), y + random.randint(30, 120)),
               fill=rgba("#2A1B14", random.randint(20, 50)), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(8))).convert("RGB")
    # floor
    img = textured_poly(img, [(0, H * 0.79), (W, H * 0.77), (W, H), (0, H)],
                        "#3A2A20", alpha=255, shadow=0, jitter=3, edge=False)
    # beams
    for y in (H * 0.12, H * 0.34):
        img = textured_poly(img, [(-20, y), (W + 20, y - 12), (W + 20, y + 12), (-20, y + 24)],
                            "#2A1B14", alpha=235, shadow=8, jitter=2, edge=False)
    # table
    img = textured_poly(img, [(W * 0.22, H * 0.64), (W * 0.73, H * 0.62), (W * 0.77, H * 0.74), (W * 0.18, H * 0.76)],
                        "#4A3226", alpha=255, shadow=22, jitter=3)
    img = textured_poly(img, [(W * 0.19, H * 0.74), (W * 0.77, H * 0.72), (W * 0.77, H * 0.78), (W * 0.19, H * 0.80)],
                        "#2E211A", alpha=255, shadow=12, jitter=2, edge=False)
    # paper contract
    img = textured_poly(img, [(W * 0.39, H * 0.675), (W * 0.58, H * 0.668), (W * 0.59, H * 0.712), (W * 0.38, H * 0.720)],
                        "#D8C5A4", alpha=255, shadow=6, jitter=1)
    # black ink marks on contract
    for i in range(4):
        img = line(img, [(W * 0.405, H * (0.685 + i * 0.007)), (W * 0.555, H * (0.682 + i * 0.007))],
                   rgba("#3A2A20", 100), width=2, blur=1)
    # red ink box
    img = textured_ellipse(img, (W * 0.585, H * 0.682, W * 0.628, H * 0.706), P["red"], alpha=255, shadow=5)
    img = textured_ellipse(img, (W * 0.592, H * 0.686, W * 0.620, H * 0.701), "#7E1F18", alpha=255, shadow=2)
    # lamp
    img = glow(img, (W * 0.50, H * 0.55), W * 0.38, P["kerosene"], 0.95)
    img = glow(img, (W * 0.50, H * 0.51), W * 0.13, "#FFD79A", 1.0)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line((W * 0.50, H * 0.24, W * 0.50, H * 0.51), fill=rgba("#2A1B14", 230), width=4)
    d.ellipse((W * 0.482, H * 0.49, W * 0.518, H * 0.55), fill=rgba("#E8B86B", 255))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    # villagers around table
    for x, h, c in [(0.25, 0.21, "#1B1511"), (0.33, 0.22, "#241A14"),
                    (0.59, 0.20, "#181310"), (0.68, 0.22, "#221912"), (0.77, 0.21, "#1C1511")]:
        img = person(img, W * x, H * 0.80, H * h, color=c, alpha=245, blur=2, coat=True)
    # boy at door left, small
    img = person(img, W * 0.13, H * 0.87, H * 0.24, color="#17110E", alpha=250, blur=1, coat=True)
    # door frame
    img = line(img, [(W * 0.02, H * 0.03), (W * 0.02, H * 0.96)], rgba("#1A120E", 240), width=34, blur=3)
    img = line(img, [(W * 0.02, H * 0.04), (W * 0.17, H * 0.07)], rgba("#1A120E", 240), width=26, blur=3)
    # dust motes in the lamp light
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(120):
        x = random.uniform(W * 0.30, W * 0.70)
        y = random.uniform(H * 0.30, H * 0.72)
        r = random.uniform(1, 3)
        d.ellipse((x, y, x + r, y + r), fill=rgba("#FFE0B0", random.randint(30, 100)))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    finish(img, BG / "bg_tangwu.webp", grain=6, vig=0.55, paper=12, brush=10)


def scene_train():
    img = gradient("#3A2D22", "#171310")
    # compartment wall
    img = textured_poly(img, [(0, 0), (W, 0), (W, H * 0.80), (0, H * 0.82)],
                        "#5A4432", alpha=255, shadow=0, jitter=3, edge=False)
    # upper luggage rack
    img = textured_poly(img, [(0, H * 0.075), (W, H * 0.065), (W, H * 0.095), (0, H * 0.105)],
                        "#3A241C", alpha=245, shadow=10, jitter=2, edge=False)
    for i in range(4):
        bx = W * (0.05 + i * 0.22)
        img = textured_poly(img, [(bx, H * 0.02), (bx + W * 0.09, H * 0.018),
                                  (bx + W * 0.09, H * 0.075), (bx, H * 0.078)],
                            "#6B3F2E", alpha=245, shadow=8, jitter=2)
    # window
    wx0, wy0, wx1, wy1 = W * 0.07, H * 0.13, W * 0.52, H * 0.53
    img = textured_poly(img, [(wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1)],
                        "#1B2A2A", alpha=255, shadow=0, jitter=1, edge=False)
    # landscape through window
    win = gradient("#9FB7A0", "#D9B978", w=int(wx1 - wx0), h=int(wy1 - wy0), tint=0.3)
    ww, wh = win.size
    win = soft_poly(win, [(-20, wh * 0.58), (ww * 0.2, wh * 0.42), (ww * 0.45, wh * 0.55),
                          (ww * 0.7, wh * 0.45), (ww + 20, wh * 0.56), (ww + 20, wh + 20), (-20, wh + 20)],
                    rgba("#7A8F6A", 180), 8)
    wd = ImageDraw.Draw(win)
    for i in range(7):
        yy = wh * (0.58 + i * 0.06)
        wd.line((0, yy, ww, yy - 2), fill=rgba("#D9B978", 35), width=2)
    img.paste(win, (int(wx0), int(wy0)))
    # window frame
    img = line(img, [(wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1), (wx0, wy0)],
               rgba("#2A1B14", 245), width=20, blur=2)
    img = line(img, [(W * 0.295, wy0), (W * 0.295, wy1)], rgba("#2A1B14", 245), width=12, blur=1)
    # two facing bench seats
    img = textured_poly(img, [(0, H * 0.62), (W * 0.38, H * 0.60), (W * 0.38, H * 0.70), (0, H * 0.73)],
                        "#6B3F2E", alpha=250, shadow=18, jitter=3)
    img = textured_poly(img, [(W * 0.62, H * 0.60), (W, H * 0.62), (W, H * 0.73), (W * 0.62, H * 0.70)],
                        "#6B3F2E", alpha=250, shadow=18, jitter=3)
    # seat backrests
    img = textured_poly(img, [(0, H * 0.54), (W * 0.38, H * 0.52), (W * 0.38, H * 0.62), (0, H * 0.64)],
                        "#4A2C22", alpha=245, shadow=14, jitter=2, edge=False)
    img = textured_poly(img, [(W * 0.62, H * 0.52), (W, H * 0.54), (W, H * 0.64), (W * 0.62, H * 0.62)],
                        "#4A2C22", alpha=245, shadow=14, jitter=2, edge=False)
    # floor
    img = textured_poly(img, [(0, H * 0.82), (W, H * 0.80), (W, H), (0, H)],
                        "#2A1B14", alpha=255, shadow=0, jitter=2, edge=False)
    # four seated figures
    for x, h, c in [(0.16, 0.25, "#1A1411"), (0.32, 0.24, "#201712"),
                    (0.62, 0.25, "#181310"), (0.78, 0.24, "#231A14")]:
        img = person(img, W * x, H * 0.80, H * h, color=c, alpha=248, pose="sit", blur=1, coat=True)
    # low table between seats
    img = textured_poly(img, [(W * 0.40, H * 0.70), (W * 0.60, H * 0.70), (W * 0.61, H * 0.76), (W * 0.39, H * 0.76)],
                        "#6B3F2E", alpha=250, shadow=12, jitter=2)
    # newspaper with circuit diagram
    img = textured_poly(img, [(W * 0.43, H * 0.705), (W * 0.57, H * 0.703), (W * 0.575, H * 0.745), (W * 0.425, H * 0.747)],
                        "#D8C5A4", alpha=255, shadow=5, jitter=1)
    for i in range(3):
        img = line(img, [(W * 0.445, H * (0.716 + i * 0.010)), (W * 0.555, H * (0.714 + i * 0.010))],
                   rgba("#5A3A28", 140), width=2, blur=1)
    # circuit scribble
    img = line(img, [(W * 0.46, H * 0.738), (W * 0.48, H * 0.730), (W * 0.50, H * 0.740),
                     (W * 0.52, H * 0.728), (W * 0.54, H * 0.738)],
               rgba("#A33327", 170), width=2, blur=1)
    # warm overhead lamp
    img = glow(img, (W * 0.50, H * 0.18), W * 0.34, P["kerosene"], 0.55)
    img = glow(img, (W * 0.50, H * 0.72), W * 0.20, "#FFD79A", 0.25)
    # dust / steam
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(80):
        x = random.uniform(W * 0.1, W * 0.9)
        y = random.uniform(H * 0.1, H * 0.7)
        r = random.uniform(1, 3)
        d.ellipse((x, y, x + r, y + r), fill=rgba("#FFE0B0", random.randint(20, 80)))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    finish(img, BG / "bg_train.webp", grain=5, vig=0.48, paper=12, brush=9)


def scene_guomao():
    img = gradient("#8A969B", "#3A4448", tint=0.2)
    # tall lobby wall
    img = soft_poly(img, [(0, 0), (W, 0), (W, H * 0.72), (0, H * 0.74)], rgba("#B9B4A8", 255), 0)
    # columns
    for x in (0.06, 0.24, 0.78, 0.94):
        img = soft_poly(img, [(W * x, H * 0.02), (W * (x + 0.045), H * 0.02),
                              (W * (x + 0.045), H * 0.78), (W * x, H * 0.78)],
                        rgba("#D8D0C0", 230), 2)
    # marble floor
    img = soft_poly(img, [(0, H * 0.74), (W, H * 0.72), (W, H), (0, H)], rgba("#6B6A64", 255), 0)
    for i in range(8):
        img = line(img, [(0, H * (0.76 + i * 0.03)), (W, H * (0.74 + i * 0.03))],
                   rgba("#D8D0C0", 35), width=2)
    # crowd silhouettes
    random.seed(7)
    for i in range(46):
        x = random.uniform(0.04, 0.96)
        h = random.uniform(0.16, 0.23)
        img = person(img, W * x, H * random.uniform(0.84, 0.94), H * h,
                     color=random.choice(["#1E2428", "#2A2E30", "#3A3A38"]),
                     alpha=random.randint(170, 235), blur=2)
    # sound console left
    img = soft_poly(img, [(W * 0.08, H * 0.70), (W * 0.28, H * 0.69), (W * 0.29, H * 0.78), (W * 0.07, H * 0.79)],
                    rgba("#2E2A26", 255), 2)
    # distant elder back, no face
    img = person(img, W * 0.66, H * 0.70, H * 0.15, color="#2A2622", alpha=190, blur=6)
    # warm/cool light
    img = glow(img, (W * 0.66, H * 0.35), W * 0.25, P["kerosene"], 0.3)
    img = glow(img, (W * 0.1, H * 0.2), W * 0.3, "#CFE0E6", 0.18)
    finish(img, BG / "bg_guomao.webp", grain=5, vig=0.45, paper=8, brush=7)


# ---------------------------------------------------------------------------
# Reusable stage helpers
# ---------------------------------------------------------------------------

def stage_interior(wall="#5A4432", floor="#2A1B14", horizon=0.78, beams=True):
    img = gradient("#2A211B", "#120F0D", tint=0.2)
    img = textured_poly(img, [(0, 0), (W, 0), (W, H * horizon), (0, H * (horizon + 0.02))],
                        wall, alpha=255, shadow=0, jitter=3, edge=False)
    img = textured_poly(img, [(0, H * horizon), (W, H * (horizon - 0.02)), (W, H), (0, H)],
                        floor, alpha=255, shadow=0, jitter=3, edge=False)
    if beams:
        for y in (H * 0.12, H * 0.36):
            img = textured_poly(img, [(-20, y), (W + 20, y - 12), (W + 20, y + 12), (-20, y + 24)],
                                "#2A1B14", alpha=235, shadow=8, jitter=2, edge=False)
    return img


def stage_exterior(sky_top="#D8B98C", sky_bottom="#6A4532", horizon=0.60,
                   field_near="#8B5E3C", field_far="#D0A76A", village=True, city_skyline=False):
    img = gradient(sky_top, sky_bottom, tint=0.4)
    img = clouds(img, H * 0.06, H * 0.34, color="#F3E7D3", alpha=50)
    img = textured_poly(img, [(-100, H * (horizon - 0.02)), (W * 0.2, H * (horizon - 0.16)),
                              (W * 0.45, H * (horizon - 0.03)), (W * 0.7, H * (horizon - 0.13)),
                              (W * 1.1, H * (horizon - 0.02)), (W * 1.1, H), (-100, H)],
                        "#A98A67", alpha=210, shadow=0, jitter=4, edge=False)
    img = field(img, int(H * horizon), near=field_near, far=field_far, rows=24)
    if village:
        for x, y, w, h in [(0.03, 0.66, 0.08, 0.08), (0.12, 0.69, 0.06, 0.06),
                            (0.19, 0.66, 0.09, 0.09)]:
            img = house(img, W * x, H * y, W * w, H * h, wall="#B99B73", roof="#4A3226")
        img = tree(img, W * 0.28, H * 0.70, H * 0.18, color="#4F6F5A")
    if city_skyline:
        img = city(img, int(H * (horizon + 0.02)), density=18)
    return img


def table(img, x0, y0, x1, y1, color="#4A3226"):
    img = textured_poly(img, [(x0, y0), (x1, y0 - H * 0.01), (x1 + W * 0.02, y1), (x0 - W * 0.01, y1 + H * 0.01)],
                        color, alpha=255, shadow=20, jitter=3)
    # legs
    for lx in (x0 + W * 0.03, x1 - W * 0.03):
        img = textured_poly(img, [(lx, y1), (lx + W * 0.012, y1),
                                  (lx + W * 0.010, min(H, y1 + H * 0.12)), (lx + W * 0.002, min(H, y1 + H * 0.12))],
                            "#2E211A", alpha=245, shadow=8, jitter=1, edge=False)
    return img


def window_view(img, box, landscape_top="#9FB7A0", landscape_bottom="#D9B978"):
    x0, y0, x1, y1 = box
    win = gradient(landscape_top, landscape_bottom, w=int(x1 - x0), h=int(y1 - y0), tint=0.3)
    ww, wh = win.size
    win = soft_poly(win, [(-20, wh * 0.58), (ww * 0.2, wh * 0.42), (ww * 0.45, wh * 0.55),
                          (ww * 0.7, wh * 0.45), (ww + 20, wh * 0.56), (ww + 20, wh + 20), (-20, wh + 20)],
                    rgba("#7A8F6A", 180), 8)
    img.paste(win, (int(x0), int(y0)))
    img = line(img, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
               rgba("#2A1B14", 245), width=18, blur=2)
    img = line(img, [((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], rgba("#2A1B14", 245), width=10, blur=1)
    return img


def smoke(img, center=(0.5, 0.4), color="#D8D0C0", alpha=60, n=22):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(n):
        x = W * center[0] + random.randint(-int(W * 0.25), int(W * 0.25))
        y = H * center[1] + random.randint(-int(H * 0.15), int(H * 0.15))
        r = random.randint(int(W * 0.04), int(W * 0.12))
        d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(color, random.randint(10, alpha)))
    layer = layer.filter(ImageFilter.GaussianBlur(28))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def crowd(img, n=18, y0=0.82, y1=0.92, hmin=0.16, hmax=0.23, colors=None, alpha=220):
    colors = colors or ["#1E1A16", "#2A211B", "#3A2A20"]
    for _ in range(n):
        x = random.uniform(0.04, 0.96)
        y = H * random.uniform(y0, y1)
        h = H * random.uniform(hmin, hmax)
        img = person(img, W * x, y, h, color=random.choice(colors),
                     alpha=random.randint(170, alpha), blur=2, coat=True)
    return img


# ---------------------------------------------------------------------------
# Additional scenes
# ---------------------------------------------------------------------------

def scene_autumn():
    img = stage_interior(wall="#7A563C", floor="#3A2A20", horizon=0.76)
    img = window_view(img, (W * 0.06, H * 0.15, W * 0.38, H * 0.50), "#C9A86A", "#E8D6A8")
    img = table(img, W * 0.18, H * 0.63, W * 0.78, H * 0.76, "#6B3F2E")
    # basket and bread
    img = textured_ellipse(img, (W * 0.46, H * 0.60, W * 0.62, H * 0.66), "#B99B73", alpha=255, shadow=8)
    for i in range(4):
        img = textured_ellipse(img, (W * (0.48 + i * 0.03), H * 0.585, W * (0.53 + i * 0.03), H * 0.625),
                               "#E8D6BC", alpha=255, shadow=4)
    # steam
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(6):
        d.arc((W * (0.48 + i * 0.02), H * 0.53, W * (0.54 + i * 0.02), H * 0.61), 200, 340,
              fill=rgba("#F3E7D3", 50), width=4)
    img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(4))).convert("RGB")
    # mother and children
    img = person(img, W * 0.30, H * 0.84, H * 0.26, color="#1B1511", alpha=245, coat=True)
    img = person(img, W * 0.57, H * 0.78, H * 0.15, color="#241A14", alpha=235)
    img = person(img, W * 0.64, H * 0.80, H * 0.14, color="#201712", alpha=235)
    img = person(img, W * 0.73, H * 0.82, H * 0.19, color="#17110E", alpha=240, bag=False)
    # warm lamp / hearth
    img = glow(img, (W * 0.20, H * 0.50), W * 0.30, P["kerosene"], 0.55)
    finish(img, BG / "bg_autumn.webp", grain=5, vig=0.45, paper=12, brush=9)


def scene_boy_repair():
    img = stage_exterior("#D8B98C", "#8B5E3C", horizon=0.62, village=True)
    # house doorway left
    img = textured_poly(img, [(W * 0.04, H * 0.18), (W * 0.34, H * 0.16), (W * 0.34, H * 0.72), (W * 0.04, H * 0.74)],
                        "#6B4B34", alpha=255, shadow=18, jitter=3)
    img = textured_poly(img, [(W * 0.10, H * 0.30), (W * 0.28, H * 0.29), (W * 0.28, H * 0.72), (W * 0.10, H * 0.73)],
                        "#2A1B14", alpha=250, shadow=10, jitter=2)
    # boy sitting on threshold
    img = person(img, W * 0.26, H * 0.80, H * 0.25, color="#1B1511", alpha=250, pose="sit", blur=1, coat=True)
    # stool with radio
    img = textured_poly(img, [(W * 0.36, H * 0.70), (W * 0.46, H * 0.69), (W * 0.47, H * 0.74), (W * 0.35, H * 0.75)],
                        "#6B3F2E", alpha=250, shadow=8, jitter=2)
    img = textured_poly(img, [(W * 0.38, H * 0.66), (W * 0.45, H * 0.655), (W * 0.45, H * 0.70), (W * 0.38, H * 0.705)],
                        "#3A2A20", alpha=255, shadow=6, jitter=1)
    # tools / screws
    for i in range(8):
        x, y = W * random.uniform(0.33, 0.50), H * random.uniform(0.75, 0.82)
        img = textured_ellipse(img, (x, y, x + W * 0.008, y + H * 0.006), "#8B5E3C", alpha=220, shadow=2)
    # afternoon light
    img = glow(img, (W * 0.68, H * 0.22), W * 0.36, "#FFD79A", 0.35)
    finish(img, BG / "bg_boy_repair.webp", grain=5, vig=0.42, paper=12, brush=9)


def scene_county():
    img = stage_exterior("#C9B18E", "#8B5E3C", horizon=0.58, village=False, city_skyline=False)
    # low street buildings
    for x, y, w, h, c in [(0.02, 0.62, 0.18, 0.18, "#B99B73"), (0.24, 0.64, 0.14, 0.15, "#A98A67"),
                           (0.72, 0.63, 0.20, 0.18, "#B99B73"), (0.55, 0.66, 0.12, 0.12, "#A98A67")]:
        img = house(img, W * x, H * y, W * w, H * h, wall=c, roof="#4A3226")
    # bike repair stall
    img = textured_poly(img, [(W * 0.10, H * 0.70), (W * 0.45, H * 0.68), (W * 0.46, H * 0.76), (W * 0.09, H * 0.78)],
                        "#6B3F2E", alpha=250, shadow=18, jitter=3)
    # bicycle wheels
    for cx in (0.18, 0.30):
        img = textured_ellipse(img, (W * cx, H * 0.66, W * (cx + 0.09), H * 0.78), "#2A1B14", alpha=245, shadow=8)
    # Zhang in flared trousers
    img = person(img, W * 0.62, H * 0.84, H * 0.28, color="#241B16", alpha=250, coat=True)
    # boombox / gift cards in hand
    img = textured_poly(img, [(W * 0.65, H * 0.62), (W * 0.70, H * 0.61), (W * 0.70, H * 0.66), (W * 0.65, H * 0.67)],
                        "#3A2A20", alpha=250, shadow=5, jitter=1)
    img = glow(img, (W * 0.78, H * 0.20), W * 0.28, "#FFD79A", 0.30)
    finish(img, BG / "bg_county.webp", grain=5, vig=0.40, paper=12, brush=9)


def scene_eaves():
    img = gradient("#1B2A2E", "#0E1416", tint=0.2)
    # cramped city village buildings
    for x, w, h, c in [(0.0, 0.22, 0.55, "#3A4448"), (0.20, 0.18, 0.62, "#4A5458"),
                        (0.38, 0.20, 0.50, "#2F3A3E"), (0.58, 0.22, 0.58, "#3A4448"),
                        (0.80, 0.20, 0.52, "#2F3A3E")]:
        img = textured_poly(img, [(W * x, H * (1 - h)), (W * (x + w), H * (1 - h - 0.03)),
                                  (W * (x + w), H), (W * x, H)],
                            c, alpha=250, shadow=14, jitter=3, edge=False)
        # windows
        for wy in range(int(H * (1 - h + 0.05)), int(H * 0.9), 90):
            for wx in range(int(W * (x + 0.02)), int(W * (x + w - 0.02)), 60):
                if random.random() < 0.35:
                    img = textured_poly(img, [(wx, wy), (wx + 18, wy), (wx + 18, wy + 24), (wx, wy + 24)],
                                        "#D99A4E", alpha=random.randint(40, 120), shadow=2, jitter=1, edge=False)
    # eaves / wires
    for i in range(4):
        img = line(img, [(0, H * (0.18 + i * 0.05)), (W, H * (0.15 + i * 0.05))],
                   rgba("#12181A", 220), width=5, blur=2)
    # streetlight
    img = glow(img, (W * 0.72, H * 0.34), W * 0.22, "#D99A4E", 0.55)
    img = line(img, [(W * 0.72, H * 0.30), (W * 0.72, H * 0.58)], rgba("#12181A", 230), width=6)
    # sleeping figures under eaves
    for i, x in enumerate([0.12, 0.24, 0.36]):
        img = person(img, W * x, H * 0.90, H * 0.17, color="#12181A", alpha=245, pose="sit", blur=2)
    # luggage
    for i, x in enumerate([0.48, 0.55]):
        img = textured_poly(img, [(W * x, H * 0.82), (W * (x + 0.07), H * 0.81),
                                  (W * (x + 0.07), H * 0.90), (W * x, H * 0.91)],
                            "#6B3F2E", alpha=250, shadow=8, jitter=2)
    finish(img, BG / "bg_eaves.webp", grain=6, vig=0.55, paper=8, brush=8)


def scene_site():
    img = stage_exterior("#D8C0A0", "#8B5E3C", horizon=0.55, village=False, city_skyline=False)
    # half-built buildings
    for x, y, w, h in [(0.50, 0.62, 0.18, 0.30), (0.70, 0.66, 0.16, 0.24), (0.86, 0.60, 0.14, 0.34)]:
        img = textured_poly(img, [(W * x, H * y), (W * (x + w), H * y), (W * (x + w), H * 0.80), (W * x, H * 0.80)],
                            "#8A8A80", alpha=250, shadow=16, jitter=3)
        # bare windows
        for wy in range(int(H * y + 30), int(H * 0.75), 70):
            for wx in range(int(W * x + 25), int(W * (x + w) - 25), 50):
                img = textured_poly(img, [(wx, wy), (wx + 22, wy), (wx + 22, wy + 30), (wx, wy + 30)],
                                    "#3A3A38", alpha=220, shadow=2, jitter=1, edge=False)
    # scaffolding
    for i in range(5):
        sx = W * (0.50 + i * 0.09)
        img = line(img, [(sx, H * 0.30), (sx, H * 0.82)], rgba("#5A3A28", 220), width=5)
    for y in (0.36, 0.48, 0.60, 0.72):
        img = line(img, [(W * 0.48, H * y), (W * 0.98, H * y)], rgba("#5A3A28", 200), width=4)
    # workers
    for x, h in [(0.18, 0.20), (0.28, 0.21), (0.38, 0.19), (0.60, 0.18)]:
        img = person(img, W * x, H * 0.84, H * h, color="#2A211B", alpha=245, coat=True)
    # loudspeaker on pole
    img = line(img, [(W * 0.16, H * 0.52), (W * 0.16, H * 0.78)], rgba("#2A1B14", 230), width=6)
    img = textured_poly(img, [(W * 0.14, H * 0.48), (W * 0.19, H * 0.47), (W * 0.20, H * 0.52), (W * 0.15, H * 0.53)],
                        "#3A2A20", alpha=250, shadow=4, jitter=1)
    # dust
    img = glow(img, (W * 0.5, H * 0.45), W * 0.55, "#E8D6BC", 0.35)
    img = smoke(img, (0.5, 0.55), "#E8D6BC", 40, 12)
    finish(img, BG / "bg_site.webp", grain=5, vig=0.42, paper=12, brush=9)


def scene_stall():
    img = stage_exterior("#C9B18E", "#6A4532", horizon=0.60, village=False, city_skyline=True)
    # low buildings / city village
    for x, y, w, h in [(0.02, 0.64, 0.18, 0.16), (0.22, 0.66, 0.14, 0.13), (0.78, 0.63, 0.18, 0.18)]:
        img = house(img, W * x, H * y, W * w, H * h, wall="#A98A67", roof="#3A2A20")
    # repair table
    img = table(img, W * 0.18, H * 0.68, W * 0.62, H * 0.82, "#6B3F2E")
    # old signboard, no readable text
    img = textured_poly(img, [(W * 0.10, H * 0.42), (W * 0.46, H * 0.40), (W * 0.46, H * 0.52), (W * 0.10, H * 0.54)],
                        "#8B5E3C", alpha=250, shadow=14, jitter=3)
    for i in range(5):
        img = line(img, [(W * (0.13 + i * 0.06), H * 0.46), (W * (0.13 + i * 0.06), H * 0.50)],
                   rgba("#3A2A20", 120), width=4, blur=1)
    # radios and tools
    for i, x in enumerate([0.24, 0.34, 0.46]):
        img = textured_poly(img, [(W * x, H * 0.64), (W * (x + 0.08), H * 0.635),
                                  (W * (x + 0.08), H * 0.68), (W * x, H * 0.685)],
                            "#3A2A20", alpha=255, shadow=6, jitter=1)
        img = textured_ellipse(img, (W * (x + 0.02), H * 0.655, W * (x + 0.05), H * 0.675),
                               "#8B5E3C", alpha=230, shadow=2)
    # Lin sitting at stall
    img = person(img, W * 0.28, H * 0.90, H * 0.24, color="#1B1511", alpha=250, pose="sit", blur=1, coat=True)
    # warm afternoon light
    img = glow(img, (W * 0.72, H * 0.25), W * 0.35, "#FFD79A", 0.35)
    finish(img, BG / "bg_stall.webp", grain=5, vig=0.44, paper=12, brush=9)


def scene_nightschool():
    img = stage_interior(wall="#4A3A2E", floor="#1E1712", horizon=0.76)
    # leaky wall stains
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(12):
        x = random.randrange(W)
        y = random.randrange(int(H * 0.65))
        d.line((x, y, x + random.randint(-20, 20), y + random.randint(40, 180)),
               fill=rgba("#2A3A3A", random.randint(20, 50)), width=random.randint(2, 6))
    img = Image.alpha_composite(img.convert("RGBA"), layer.filter(ImageFilter.GaussianBlur(6))).convert("RGB")
    # window with night city
    img = window_view(img, (W * 0.62, H * 0.12, W * 0.94, H * 0.42), "#2F4A42", "#1B2A2E")
    # table with circuit board
    img = table(img, W * 0.16, H * 0.64, W * 0.72, H * 0.78, "#6B3F2E")
    img = textured_poly(img, [(W * 0.40, H * 0.64), (W * 0.58, H * 0.635), (W * 0.58, H * 0.70), (W * 0.40, H * 0.705)],
                        "#2F4A42", alpha=255, shadow=6, jitter=1)
    for i in range(5):
        img = line(img, [(W * 0.42, H * (0.65 + i * 0.008)), (W * 0.56, H * (0.648 + i * 0.008))],
                   rgba("#D99A4E", 100), width=2, blur=1)
    # Su teaching, Lin taking notes
    img = person(img, W * 0.34, H * 0.86, H * 0.25, color="#1B1511", alpha=250, pose="sit", blur=1, coat=True)
    img = person(img, W * 0.62, H * 0.88, H * 0.24, color="#17110E", alpha=250, pose="sit", blur=1)
    # oil lamp
    img = glow(img, (W * 0.50, H * 0.55), W * 0.28, P["kerosene"], 0.9)
    img = textured_ellipse(img, (W * 0.485, H * 0.55, W * 0.515, H * 0.59), "#E8B86B", alpha=255, shadow=4)
    finish(img, BG / "bg_nightschool.webp", grain=6, vig=0.52, paper=10, brush=9)


def scene_oldradio():
    img = gradient("#B99B73", "#4A3226", tint=0.3)
    img = clouds(img, H * 0.05, H * 0.25, color="#F3E7D3", alpha=40)
    # alley buildings
    for x, w, h in [(0.0, 0.20, 0.55), (0.78, 0.22, 0.60)]:
        img = textured_poly(img, [(W * x, H * (1 - h)), (W * (x + w), H * (1 - h - 0.03)),
                                  (W * (x + w), H), (W * x, H)],
                            "#6B4B34", alpha=255, shadow=14, jitter=3)
    # ground
    img = textured_poly(img, [(0, H * 0.72), (W, H * 0.70), (W, H), (0, H)],
                        "#3A2A20", alpha=255, shadow=0, jitter=3, edge=False)
    # garbage pile
    for i in range(10):
        x, y = W * random.uniform(0.28, 0.70), H * random.uniform(0.70, 0.86)
        w, h = W * random.uniform(0.02, 0.08), H * random.uniform(0.01, 0.04)
        img = textured_poly(img, [(x, y), (x + w, y - h * 0.3), (x + w * 0.8, y + h), (x - w * 0.1, y + h * 0.8)],
                            random.choice(["#5A4432", "#3A2A20", "#8B5E3C"]), alpha=240, shadow=5, jitter=2)
    # old man sitting with radio
    img = person(img, W * 0.40, H * 0.88, H * 0.23, color="#1B1511", alpha=250, pose="sit", blur=1, coat=True)
    img = textured_poly(img, [(W * 0.42, H * 0.69), (W * 0.52, H * 0.685), (W * 0.52, H * 0.74), (W * 0.42, H * 0.745)],
                        "#3A2A20", alpha=255, shadow=6, jitter=1)
    img = glow(img, (W * 0.46, H * 0.70), W * 0.16, "#FFD79A", 0.5)
    # sunrise
    img = glow(img, (W * 0.78, H * 0.30), W * 0.40, "#FFD79A", 0.45)
    finish(img, BG / "bg_oldradio.webp", grain=6, vig=0.48, paper=12, brush=9)


def scene_return():
    img = stage_exterior("#D8B98C", "#8B5E3C", horizon=0.62, village=True)
    # courtyard wall / gate
    img = textured_poly(img, [(0, H * 0.42), (W * 0.30, H * 0.40), (W * 0.30, H * 0.78), (0, H * 0.80)],
                        "#8B5E3C", alpha=250, shadow=18, jitter=3)
    img = textured_poly(img, [(W * 0.08, H * 0.50), (W * 0.22, H * 0.49), (W * 0.22, H * 0.79), (W * 0.08, H * 0.80)],
                        "#2A1B14", alpha=250, shadow=10, jitter=2)
    # villagers
    img = crowd(img, n=16, y0=0.78, y1=0.90, hmin=0.16, hmax=0.22, alpha=225)
    # Lin with boombox
    img = person(img, W * 0.40, H * 0.88, H * 0.27, color="#1B1511", alpha=250, coat=True)
    img = textured_poly(img, [(W * 0.44, H * 0.63), (W * 0.54, H * 0.625), (W * 0.54, H * 0.70), (W * 0.44, H * 0.705)],
                        "#3A2A20", alpha=250, shadow=6, jitter=1)
    # father at door
    img = person(img, W * 0.18, H * 0.82, H * 0.22, color="#17110E", alpha=245, coat=True)
    # warm dust
    img = glow(img, (W * 0.62, H * 0.30), W * 0.40, "#FFD79A", 0.35)
    img = smoke(img, (0.5, 0.6), "#E8D6BC", 30, 10)
    finish(img, BG / "bg_return.webp", grain=5, vig=0.44, paper=12, brush=9)


def scene_watch():
    img = gradient("#1B1511", "#0E0B09")
    # table surface
    img = textured_poly(img, [(0, H * 0.35), (W, H * 0.32), (W, H), (0, H)],
                        "#4A3226", alpha=255, shadow=0, jitter=3, edge=False)
    # watches scattered
    for i in range(14):
        x = W * random.uniform(0.08, 0.88)
        y = H * random.uniform(0.40, 0.82)
        r = W * random.uniform(0.018, 0.030)
        img = textured_ellipse(img, (x - r, y - r, x + r, y + r), "#D8C5A4", alpha=255, shadow=6)
        img = textured_ellipse(img, (x - r * 0.72, y - r * 0.72, x + r * 0.72, y + r * 0.72),
                               "#2A1B14", alpha=255, shadow=2)
        img = line(img, [(x, y), (x + r * 0.4, y - r * 0.5)], rgba("#D8C5A4", 180), width=2)
    # multimeter
    img = textured_poly(img, [(W * 0.58, H * 0.56), (W * 0.78, H * 0.55), (W * 0.78, H * 0.72), (W * 0.58, H * 0.73)],
                        "#8B5E3C", alpha=255, shadow=12, jitter=2)
    img = textured_poly(img, [(W * 0.60, H * 0.57), (W * 0.76, H * 0.56), (W * 0.76, H * 0.64), (W * 0.60, H * 0.65)],
                        "#D8C5A4", alpha=255, shadow=4, jitter=1)
    for i in range(4):
        img = line(img, [(W * (0.61 + i * 0.03), H * 0.575), (W * (0.61 + i * 0.03), H * 0.64)],
                   rgba("#A33327", 140), width=2)
    # hands
    img = person(img, W * 0.30, H * 1.02, H * 0.40, color="#1B1511", alpha=245, blur=3, coat=True)
    img = person(img, W * 0.82, H * 1.02, H * 0.38, color="#1B1511", alpha=245, blur=3, coat=True)
    # lamp
    img = glow(img, (W * 0.50, H * 0.30), W * 0.40, P["kerosene"], 0.75)
    finish(img, BG / "bg_watch.webp", grain=5, vig=0.55, paper=8, brush=8)


def scene_workshop():
    img = stage_interior(wall="#6B4B34", floor="#2A1B14", horizon=0.74)
    # leaky roof / corrugated lines
    for i in range(8):
        img = line(img, [(0, H * (0.02 + i * 0.025)), (W, H * (0.01 + i * 0.025))],
                   rgba("#3A2A20", 120), width=4, blur=1)
    # signboard, no readable text
    img = textured_poly(img, [(W * 0.30, H * 0.10), (W * 0.70, H * 0.09), (W * 0.70, H * 0.20), (W * 0.30, H * 0.21)],
                        "#8B5E3C", alpha=250, shadow=14, jitter=3)
    # workbenches
    for x in (0.06, 0.52):
        img = table(img, W * x, H * 0.62, W * (x + 0.40), H * 0.78, "#6B3F2E")
        # radio shells
        for i in range(3):
            img = textured_poly(img, [(W * (x + 0.04 + i * 0.10), H * 0.57),
                                      (W * (x + 0.11 + i * 0.10), H * 0.565),
                                      (W * (x + 0.11 + i * 0.10), H * 0.62),
                                      (W * (x + 0.04 + i * 0.10), H * 0.625)],
                                "#3A2A20", alpha=255, shadow=5, jitter=1)
    # shelves
    img = line(img, [(W * 0.72, H * 0.28), (W * 0.98, H * 0.27)], rgba("#3A2A20", 220), width=8)
    for i in range(6):
        img = textured_poly(img, [(W * (0.74 + i * 0.04), H * 0.20), (W * (0.77 + i * 0.04), H * 0.20),
                                  (W * (0.77 + i * 0.04), H * 0.27), (W * (0.74 + i * 0.04), H * 0.27)],
                            "#4A3226", alpha=240, shadow=4, jitter=1)
    # workers
    for x, h in [(0.16, 0.22), (0.28, 0.21), (0.62, 0.22), (0.74, 0.21)]:
        img = person(img, W * x, H * 0.86, H * h, color="#1B1511", alpha=245, pose="sit", blur=1, coat=True)
    # hanging bulbs
    for x in (0.22, 0.50, 0.82):
        img = line(img, [(W * x, H * 0.06), (W * x, H * 0.28)], rgba("#2A1B14", 230), width=3)
        img = glow(img, (W * x, H * 0.30), W * 0.12, "#FFD79A", 0.55)
        img = textured_ellipse(img, (W * (x - 0.012), H * 0.28, W * (x + 0.012), H * 0.31), "#E8B86B", alpha=255, shadow=2)
    finish(img, BG / "bg_workshop.webp", grain=6, vig=0.48, paper=10, brush=9)


def scene_market():
    img = stage_exterior("#D8C0A0", "#8B5E3C", horizon=0.58, village=True)
    # market stalls
    for x, w in [(0.08, 0.22), (0.38, 0.20)]:
        img = textured_poly(img, [(W * x, H * 0.44), (W * (x + w), H * 0.43),
                                  (W * (x + w), H * 0.50), (W * x, H * 0.51)],
                            "#A33327", alpha=220, shadow=12, jitter=3)
        img = table(img, W * x, H * 0.62, W * (x + w), H * 0.74, "#6B3F2E")
        for i in range(4):
            img = textured_poly(img, [(W * (x + 0.02 + i * 0.05), H * 0.57),
                                      (W * (x + 0.07 + i * 0.05), H * 0.565),
                                      (W * (x + 0.07 + i * 0.05), H * 0.62),
                                      (W * (x + 0.02 + i * 0.05), H * 0.625)],
                                "#3A2A20", alpha=255, shadow=4, jitter=1)
    # villagers
    img = crowd(img, n=14, y0=0.76, y1=0.90, hmin=0.16, hmax=0.22, alpha=230)
    # brick house under construction
    img = textured_poly(img, [(W * 0.66, H * 0.38), (W * 0.90, H * 0.36), (W * 0.90, H * 0.70), (W * 0.66, H * 0.72)],
                        "#A98A67", alpha=250, shadow=18, jitter=3)
    for i in range(4):
        for j in range(3):
            img = textured_poly(img, [(W * (0.67 + j * 0.06), H * (0.40 + i * 0.07)),
                                      (W * (0.70 + j * 0.06), H * (0.40 + i * 0.07)),
                                      (W * (0.70 + j * 0.06), H * (0.44 + i * 0.07)),
                                      (W * (0.67 + j * 0.06), H * (0.44 + i * 0.07))],
                                "#8B5E3C", alpha=100, shadow=0, jitter=1, edge=False)
    # warm daylight
    img = glow(img, (W * 0.78, H * 0.22), W * 0.36, "#FFD79A", 0.35)
    finish(img, BG / "bg_market.webp", grain=5, vig=0.42, paper=12, brush=9)


def scene_postoffice():
    img = stage_interior(wall="#6B5B4B", floor="#2A1B14", horizon=0.72)
    # green postal counter
    img = textured_poly(img, [(0, H * 0.55), (W, H * 0.53), (W, H * 0.74), (0, H * 0.76)],
                        "#2F4A42", alpha=255, shadow=20, jitter=3)
    img = textured_poly(img, [(0, H * 0.52), (W, H * 0.50), (W, H * 0.55), (0, H * 0.57)],
                        "#4F6F5A", alpha=245, shadow=8, jitter=2, edge=False)
    # postal window / clerk
    img = textured_poly(img, [(W * 0.56, H * 0.16), (W * 0.92, H * 0.14), (W * 0.92, H * 0.42), (W * 0.56, H * 0.44)],
                        "#1B2A2E", alpha=255, shadow=14, jitter=2)
    img = person(img, W * 0.74, H * 0.60, H * 0.22, color="#1B1511", alpha=245, pose="sit", blur=2)
    # package and remittance on counter
    img = textured_poly(img, [(W * 0.18, H * 0.60), (W * 0.34, H * 0.59), (W * 0.34, H * 0.68), (W * 0.18, H * 0.69)],
                        "#8B5E3C", alpha=255, shadow=8, jitter=2)
    img = textured_poly(img, [(W * 0.20, H * 0.615), (W * 0.33, H * 0.61), (W * 0.33, H * 0.63), (W * 0.20, H * 0.635)],
                        "#D8C5A4", alpha=255, shadow=3, jitter=1)
    img = textured_poly(img, [(W * 0.38, H * 0.615), (W * 0.48, H * 0.61), (W * 0.48, H * 0.65), (W * 0.38, H * 0.655)],
                        "#E8D6BC", alpha=255, shadow=3, jitter=1)
    # warm light from above
    img = glow(img, (W * 0.45, H * 0.20), W * 0.35, "#FFD79A", 0.35)
    finish(img, BG / "bg_postoffice.webp", grain=5, vig=0.46, paper=12, brush=8)


def scene_warehouse():
    img = gradient("#1B2428", "#0E1214", tint=0.2)
    # warehouse wall / rolled door
    img = textured_poly(img, [(0, 0), (W, 0), (W, H * 0.78), (0, H * 0.80)],
                        "#3A4448", alpha=255, shadow=0, jitter=3, edge=False)
    for i in range(14):
        img = line(img, [(0, H * (0.03 + i * 0.05)), (W, H * (0.02 + i * 0.05))],
                   rgba("#1B2428", 120), width=4, blur=1)
    # open wooden crate
    img = textured_poly(img, [(W * 0.20, H * 0.58), (W * 0.55, H * 0.55), (W * 0.58, H * 0.76), (W * 0.18, H * 0.79)],
                        "#6B3F2E", alpha=255, shadow=18, jitter=3)
    # radios inside
    for i in range(5):
        img = textured_poly(img, [(W * (0.24 + i * 0.055), H * 0.61), (W * (0.29 + i * 0.055), H * 0.60),
                                  (W * (0.29 + i * 0.055), H * 0.66), (W * (0.24 + i * 0.055), H * 0.67)],
                            "#2A1B14", alpha=255, shadow=4, jitter=1)
    # man on stool with soldering iron
    img = person(img, W * 0.68, H * 0.88, H * 0.24, color="#17110E", alpha=250, pose="sit", blur=1, coat=True)
    img = line(img, [(W * 0.70, H * 0.64), (W * 0.62, H * 0.70)], rgba("#2A1B14", 240), width=5)
    img = glow(img, (W * 0.61, H * 0.70), W * 0.09, "#FF6B3A", 0.8)
    # streetlight through door
    img = glow(img, (W * 0.90, H * 0.30), W * 0.30, "#D99A4E", 0.45)
    finish(img, BG / "bg_warehouse.webp", grain=6, vig=0.58, paper=8, brush=8)


def scene_shanghai():
    img = stage_interior(wall="#6B5B4B", floor="#3A2A20", horizon=0.74)
    # gray window with lane houses
    img = window_view(img, (W * 0.08, H * 0.14, W * 0.42, H * 0.48), "#8A969B", "#B9B4A8")
    # table / sample radio
    img = table(img, W * 0.46, H * 0.62, W * 0.88, H * 0.76, "#6B3F2E")
    img = textured_poly(img, [(W * 0.58, H * 0.57), (W * 0.76, H * 0.56), (W * 0.76, H * 0.63), (W * 0.58, H * 0.64)],
                        "#3A2A20", alpha=255, shadow=8, jitter=1)
    # Su inspecting
    img = person(img, W * 0.52, H * 0.86, H * 0.24, color="#1B1511", alpha=250, pose="sit", blur=1)
    # cool daylight
    img = glow(img, (W * 0.24, H * 0.22), W * 0.30, "#D8E0E0", 0.25)
    finish(img, BG / "bg_shanghai.webp", grain=5, vig=0.45, paper=12, brush=8)


def scene_factory():
    img = stage_interior(wall="#8B5E3C", floor="#3A2A20", horizon=0.72)
    # high windows
    for x in (0.10, 0.40, 0.70):
        img = window_view(img, (W * x, H * 0.10, W * (x + 0.18), H * 0.32), "#C9B18E", "#E8D6A8")
    # rows of workbenches
    for row, y in enumerate([0.50, 0.66]):
        for x in (0.06, 0.34, 0.62):
            img = table(img, W * x, H * y, W * (x + 0.22), H * (y + 0.12), "#6B3F2E")
            for i in range(3):
                img = person(img, W * (x + 0.04 + i * 0.07), H * (y + 0.17),
                             H * 0.16, color="#1B1511", alpha=240, pose="sit", blur=2)
    # red banner, no text
    img = textured_poly(img, [(W * 0.20, H * 0.05), (W * 0.80, H * 0.04), (W * 0.80, H * 0.10), (W * 0.20, H * 0.11)],
                        "#A33327", alpha=230, shadow=12, jitter=3)
    # warm light
    img = glow(img, (W * 0.50, H * 0.22), W * 0.45, "#FFD79A", 0.40)
    finish(img, BG / "bg_factory.webp", grain=5, vig=0.42, paper=12, brush=9)


def scene_1995():
    img = stage_interior(wall="#B99B73", floor="#4A3226", horizon=0.72)
    # large windows
    for x in (0.04, 0.30, 0.56, 0.82):
        img = window_view(img, (W * x, H * 0.08, W * (x + 0.12), H * 0.30), "#C9B18E", "#E8D6A8")
    # rows of benches
    for row, y in enumerate([0.42, 0.56, 0.70]):
        for x in (0.04, 0.28, 0.52, 0.76):
            img = table(img, W * x, H * y, W * (x + 0.18), H * (y + 0.09), "#8B5E3C")
            for i in range(2):
                img = person(img, W * (x + 0.04 + i * 0.08), H * (y + 0.14),
                             H * 0.14, color="#2A211B", alpha=235, pose="sit", blur=2)
    # training corner / blackboard with circuit
    img = textured_poly(img, [(W * 0.78, H * 0.40), (W * 0.96, H * 0.39), (W * 0.96, H * 0.66), (W * 0.78, H * 0.67)],
                        "#2F4A42", alpha=250, shadow=14, jitter=2)
    for i in range(4):
        img = line(img, [(W * 0.80, H * (0.45 + i * 0.04)), (W * 0.94, H * (0.445 + i * 0.04))],
                   rgba("#D8C5A4", 120), width=3, blur=1)
    # warm, abundant light
    img = glow(img, (W * 0.50, H * 0.20), W * 0.55, "#FFD79A", 0.45)
    finish(img, BG / "bg_1995.webp", grain=5, vig=0.38, paper=12, brush=9)


def scene_threshold():
    img = stage_exterior("#C9B18E", "#6A4532", horizon=0.62, village=True)
    # old house wall / door
    img = textured_poly(img, [(0, H * 0.10), (W * 0.42, H * 0.08), (W * 0.42, H * 0.82), (0, H * 0.84)],
                        "#8B5E3C", alpha=255, shadow=18, jitter=3)
    img = textured_poly(img, [(W * 0.10, H * 0.22), (W * 0.30, H * 0.21), (W * 0.30, H * 0.82), (W * 0.10, H * 0.83)],
                        "#2A1B14", alpha=250, shadow=10, jitter=2)
    # threshold stone
    img = textured_poly(img, [(0, H * 0.80), (W * 0.44, H * 0.78), (W * 0.44, H * 0.86), (0, H * 0.88)],
                        "#6B5B4B", alpha=255, shadow=12, jitter=2)
    # father sitting
    img = person(img, W * 0.26, H * 0.84, H * 0.26, color="#1B1511", alpha=250, pose="sit", blur=1, coat=True)
    # radio on stool and ink box
    img = textured_poly(img, [(W * 0.38, H * 0.69), (W * 0.48, H * 0.685), (W * 0.48, H * 0.74), (W * 0.38, H * 0.745)],
                        "#3A2A20", alpha=255, shadow=6, jitter=1)
    img = textured_ellipse(img, (W * 0.31, H * 0.78, W * 0.35, H * 0.80), P["red"], alpha=255, shadow=3)
    # dusk light
    img = glow(img, (W * 0.74, H * 0.30), W * 0.38, "#FFD79A", 0.40)
    finish(img, BG / "bg_threshold.webp", grain=5, vig=0.46, paper=12, brush=9)


def scene_bus():
    img = stage_exterior("#C9D5C0", "#8B5E3C", horizon=0.58, village=True)
    # village road
    img = textured_poly(img, [(W * 0.30, H * 0.72), (W * 0.70, H * 0.72), (W * 0.90, H), (W * 0.10, H)],
                        "#8B5E3C", alpha=245, shadow=0, jitter=3, edge=False)
    # roadside
    img = textured_poly(img, [(W * 0.28, H * 0.70), (W * 0.88, H * 0.68), (W * 0.92, H * 0.78), (W * 0.22, H * 0.80)],
                        "#8B5E3C", alpha=245, shadow=12, jitter=3)
    # green bus
    img = textured_poly(img, [(W * 0.38, H * 0.40), (W * 0.82, H * 0.38), (W * 0.84, H * 0.66), (W * 0.36, H * 0.68)],
                        "#3F5A4A", alpha=255, shadow=22, jitter=3)
    for i in range(4):
        img = textured_poly(img, [(W * (0.42 + i * 0.09), H * 0.44), (W * (0.49 + i * 0.09), H * 0.435),
                                  (W * (0.49 + i * 0.09), H * 0.55), (W * (0.42 + i * 0.09), H * 0.555)],
                            "#D99A4E", alpha=190, shadow=3, jitter=1)
    # door
    img = textured_poly(img, [(W * 0.70, H * 0.44), (W * 0.755, H * 0.437),
                              (W * 0.755, H * 0.66), (W * 0.70, H * 0.663)],
                        "#2F4A42", alpha=245, shadow=4, jitter=1)
    # wheels
    for wx in (0.46, 0.72):
        img = textured_ellipse(img, (W * wx, H * 0.62, W * (wx + 0.075), H * 0.70),
                               "#1B1511", alpha=255, shadow=8)
        img = textured_ellipse(img, (W * (wx + 0.015), H * 0.638, W * (wx + 0.060), H * 0.688),
                               "#6B5B4B", alpha=255, shadow=2)
    # headlight
    img = textured_ellipse(img, (W * 0.79, H * 0.56, W * 0.815, H * 0.585), "#D99A4E", alpha=230, shadow=3)
    # young workers getting off
    for x, h in [(0.28, 0.22), (0.34, 0.21), (0.40, 0.23)]:
        img = person(img, W * x, H * 0.88, H * h, color="#1B1511", alpha=245, coat=True)
    # spring light
    img = glow(img, (W * 0.50, H * 0.20), W * 0.45, "#F3E7D3", 0.35)
    img = smoke(img, (0.5, 0.5), "#F3E7D3", 25, 8)
    finish(img, BG / "bg_bus.webp", grain=5, vig=0.40, paper=12, brush=9)


def scene_spring():
    img = gradient("#D8C0A0", "#6A4532", tint=0.5)
    img = clouds(img, H * 0.06, H * 0.30, color="#F3E7D3", alpha=50)
    img = textured_poly(img, [(-100, H * 0.58), (W * 0.2, H * 0.44), (W * 0.45, H * 0.56),
                              (W * 0.7, H * 0.46), (W * 1.1, H * 0.56), (W * 1.1, H), (-100, H)],
                        "#A98A67", alpha=210, shadow=0, jitter=4, edge=False)
    img = field(img, int(H * 0.60), near="#8B5E3C", far="#D0A76A", rows=28)
    img = city(img, int(H * 0.61), color="#5C6B73", density=14)
    # wind lines
    for i in range(12):
        y = H * (0.18 + i * 0.045)
        pts = [(W * 0.02, y + 10 * math.sin(i)), (W * 0.34, y - 8), (W * 0.66, y + 6), (W * 0.99, y - 10)]
        img = line(img, pts, rgba(P["cream"], 70), width=4, blur=3)
    # red handprint / solder glow
    img = glow(img, (W * 0.34, H * 0.64), W * 0.18, "#A33327", 0.35)
    img = glow(img, (W * 0.66, H * 0.64), W * 0.16, "#FF6B3A", 0.30)
    img = glow(img, (W * 0.50, H * 0.28), W * 0.35, "#FFD79A", 0.35)
    finish(img, BG / "bg_spring.webp", grain=4, vig=0.40, paper=14, brush=10)


# ---------------------------------------------------------------------------
# Variants and endings
# ---------------------------------------------------------------------------

def glow_native(img, center, radius, color, strength=0.5):
    w, h = img.size
    cx, cy = center
    x = np.arange(w, dtype=np.float32)[None, :]
    y = np.arange(h, dtype=np.float32)[:, None]
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    a = np.clip(1.0 - r / radius, 0, 1) ** 2 * strength
    layer = np.zeros((h, w, 3), dtype=np.float32)
    layer[:, :] = np.array(rgb(color), dtype=np.float32)
    out = np.array(img).astype(np.float32)
    out = 255 - (255 - out) * (255 - layer * a[:, :, None]) / 255
    return Image.fromarray(np.uint8(np.clip(out, 0, 255)), "RGB")


def seal_strips(img, n=4):
    d = ImageDraw.Draw(img)
    for i in range(n):
        x = img.width * (0.08 + i * 0.24)
        y = img.height * 0.30
        d.polygon([(x, y), (x + 54, y + 4), (x + 48, y + 230), (x - 2, y + 220)],
                  fill=rgba("#E8D6BC", 235), outline=rgba("#A33327", 220))
        d.ellipse((x + 14, y + 82, x + 38, y + 108), fill=rgba("#A33327", 220))
        d.line((x + 12, y + 140, x + 36, y + 138), fill=rgba("#8B5E3C", 180), width=3)
    return img


def make_variant(base, out, color, alpha, brightness=1.0, glows=None, seal=False, smoke_it=False):
    img = Image.open(BG / base).convert("RGB")
    overlay = Image.new("RGB", img.size, rgb(color))
    img = Image.blend(img, overlay, alpha)
    if brightness != 1.0:
        from PIL import ImageEnhance
        img = ImageEnhance.Brightness(img).enhance(brightness)
    for center, radius, gcolor, strength in (glows or []):
        img = glow_native(img, (img.width * center[0], img.height * center[1]),
                          img.width * radius, gcolor, strength)
    if smoke_it:
        # native-size soft smoke
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for _ in range(18):
            x = random.uniform(0.25, 0.75) * img.width
            y = random.uniform(0.25, 0.65) * img.height
            r = random.uniform(0.04, 0.12) * img.width
            d.ellipse((x - r, y - r, x + r, y + r), fill=rgba("#D8D0C0", random.randint(10, 60)))
        layer = layer.filter(ImageFilter.GaussianBlur(30))
        img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    if seal:
        img = seal_strips(img)
    img = vignette(img, 0.45)
    img = add_grain(img, 5)
    img.save(BG / out, "WEBP", quality=92, method=6)
    print("wrote", out, (BG / out).stat().st_size // 1024, "KB")


def make_endings():
    make_variant("bg_bus.webp", "bg_end_e1.webp", "#D99A4E", 0.10, 1.05,
                 glows=[((0.5, 0.25), 0.5, "#FFD79A", 0.35)])
    make_variant("bg_1995.webp", "bg_end_e2.webp", "#5C6B73", 0.16, 1.02,
                 glows=[((0.5, 0.25), 0.5, "#D8E0E0", 0.25)])
    make_variant("bg_1995.webp", "bg_end_e3.webp", "#D99A4E", 0.12, 1.04,
                 glows=[((0.4, 0.3), 0.45, "#FFD79A", 0.30)])
    make_variant("bg_stall.webp", "bg_end_e4.webp", "#1B2A2E", 0.45, 0.75,
                 glows=[((0.35, 0.55), 0.25, "#FFD79A", 0.55)])
    make_variant("bg_county.webp", "bg_end_e5.webp", "#1B2428", 0.30, 0.85,
                 glows=[((0.30, 0.55), 0.25, "#FFD79A", 0.30), ((0.78, 0.45), 0.25, "#8A969B", 0.20)])
    make_variant("bg_collapse.webp", "bg_end_e6.webp", "#1E2428", 0.25, 0.65)
    make_variant("bg_stall.webp", "bg_end_e7.webp", "#8B5E3C", 0.30, 0.75)
    make_variant("bg_spring.webp", "bg_end_e8.webp", "#A33327", 0.10, 1.02,
                 glows=[((0.5, 0.5), 0.45, "#D99A4E", 0.30)])
    make_variant("bg_spring.webp", "bg_end_e0.webp", "#D99A4E", 0.08, 1.0)


def make_variants():
    make_variant("bg_workshop.webp", "bg_blackout.webp", "#1B2A2E", 0.55, 0.55,
                 glows=[((0.22, 0.55), 0.18, "#FFD79A", 0.65), ((0.50, 0.55), 0.16, "#FFD79A", 0.55),
                        ((0.82, 0.55), 0.18, "#FFD79A", 0.55)])
    make_variant("bg_workshop.webp", "bg_crisis.webp", "#3A2A20", 0.28, 0.72, smoke_it=True)
    make_variant("bg_workshop.webp", "bg_collapse.webp", "#5C6B73", 0.35, 0.55, seal=True)
    make_variant("bg_workshop.webp", "bg_reopen.webp", "#D99A4E", 0.10, 1.08,
                 glows=[((0.5, 0.20), 0.45, "#FFD79A", 0.45)])
    make_variant("bg_train.webp", "bg_longbus.webp", "#8B5E3C", 0.10, 1.02,
                 glows=[((0.5, 0.30), 0.35, "#FFD79A", 0.25)])


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    scene_menu()
    scene_tangwu()
    scene_autumn()
    scene_boy_repair()
    scene_county()
    scene_train()
    scene_eaves()
    scene_site()
    scene_stall()
    scene_nightschool()
    scene_oldradio()
    scene_return()
    scene_watch()
    scene_workshop()
    scene_market()
    scene_postoffice()
    scene_guomao()
    scene_warehouse()
    scene_shanghai()
    scene_factory()
    scene_1995()
    scene_threshold()
    scene_bus()
    scene_spring()
    make_variants()
    make_endings()
