# -*- coding: utf-8 -*-
"""UI, portrait medallions and icon assets for 春声南来."""
from __future__ import annotations

import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = Path(r"D:\try_deepseek_harness\chunsheng_nanlai")
GUI = BASE / "game" / "gui"
BG = BASE / "game" / "images" / "bg"
PORTRAIT = BASE / "game" / "images" / "portraits"
FONT = BASE / "game" / "fonts" / "SourceHanSansLite.ttf"
for d in (GUI, GUI / "button", GUI / "overlay", PORTRAIT):
    d.mkdir(parents=True, exist_ok=True)

P = {
    "paper": "#F3E7D3",
    "cream": "#E8D6BC",
    "brown": "#8B5E3C",
    "darkbrown": "#4A3226",
    "red": "#A33327",
    "deepred": "#6E1F1A",
    "kerosene": "#D99A4E",
    "teal": "#4F6F5A",
    "night": "#1E2428",
}


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgba(h, a=255):
    return rgb(h) + (a,)


def paper_panel(w, h, color=P["cream"], border=P["brown"], alpha=245, seed=1):
    random.seed(seed)
    np.random.seed(seed)
    base = np.array(rgb(color), dtype=np.float32)
    arr = base[None, None, :] + np.random.normal(0, 4, (h, w, 1))
    img = Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB").convert("RGBA")
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # fibres
    for _ in range(max(80, w * h // 5000)):
        x = random.randrange(w)
        y = random.randrange(h)
        ln = random.randint(8, 70)
        d.line((x, y, x + ln, y + random.randint(-2, 2)),
               fill=rgba("#FFFFFF", random.randint(3, 10)), width=1)
    # soft stains
    for _ in range(8):
        x = random.randrange(w)
        y = random.randrange(h)
        r = random.randint(20, 100)
        d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(P["brown"], random.randint(2, 6)))
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    # border
    d.rectangle((0, 0, w - 1, h - 1), outline=rgba(border, 120), width=2)
    # torn top edge
    pts = [(0, 6)]
    for x in range(0, w, 24):
        pts.append((x, 4 + random.randint(-3, 3)))
    pts.append((w, 6))
    d.line(pts, fill=rgba(border, 110), width=2)
    return img


def save(img, path):
    img.save(path, "PNG")
    print("wrote", path.name, path.stat().st_size // 1024, "KB")


def make_textbox():
    w, h = 1920, 300
    img = paper_panel(w, h, P["paper"], P["brown"], 238, seed=2)
    d = ImageDraw.Draw(img)
    # translucent dark wash at bottom for contrast
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(h):
        a = int(80 * (y / h) ** 2)
        od.line((0, y, w, y), fill=(20, 14, 10, a))
    img = Image.alpha_composite(img, overlay)
    # red rule
    d = ImageDraw.Draw(img)
    d.line((60, 34, w - 60, 30), fill=rgba(P["red"], 160), width=3)
    d.line((60, 278, w - 60, 274), fill=rgba(P["brown"], 90), width=2)
    # corner seal
    d.rectangle((w - 96, 22, w - 26, 92), fill=rgba(P["red"], 210))
    d.text((w - 80, 34), "春", font=ImageFont.truetype(str(FONT), 42), fill=rgba(P["paper"], 245))
    save(img, GUI / "textbox.png")


def make_namebox():
    w, h = 520, 96
    img = paper_panel(w, h, "#7A2E2E", "#4A1814", 245, seed=3)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 10, h), fill=rgba(P["kerosene"], 220))
    d.text((28, 18), "名", font=ImageFont.truetype(str(FONT), 36), fill=rgba(P["paper"], 30))
    save(img, GUI / "namebox.png")


def make_choice_buttons():
    for name, color, border in [
        ("choice_idle_background.png", "#EFE1C9", "#8B5E3C"),
        ("choice_hover_background.png", "#F7E9D2", "#A33327"),
    ]:
        w, h = 1400, 104
        img = paper_panel(w, h, color, border, 242, seed=4 if "idle" in name else 5)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 14, h), fill=rgba(P["red"], 230))
        d.line((36, 16, w - 36, 14), fill=rgba(border, 90), width=2)
        d.line((36, h - 18, w - 36, h - 20), fill=rgba(border, 60), width=2)
        save(img, GUI / "button" / name)


def make_small_buttons():
    for name, color in [("idle_background.png", "#E8D6BC"), ("hover_background.png", "#F3E7D3")]:
        w, h = 320, 64
        img = paper_panel(w, h, color, P["brown"], 235, seed=6)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 6, h), fill=rgba(P["red"], 200))
        save(img, GUI / "button" / name)
    for name, color in [("quick_idle_background.png", "#1E2428"), ("quick_hover_background.png", "#3A2A20")]:
        w, h = 150, 40
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, w - 1, h - 1), radius=6, fill=rgba(color, 120))
        save(img, GUI / "button" / name)


def make_slots():
    for name, color in [("slot_idle_background.png", "#E8D6BC"), ("slot_hover_background.png", "#F3E7D3")]:
        w, h = 380, 170
        img = paper_panel(w, h, color, P["brown"], 238, seed=7)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, 8, h), fill=rgba(P["red"], 200))
        save(img, GUI / "button" / name)


def make_frame_notify():
    img = paper_panel(900, 600, P["cream"], P["brown"], 245, seed=8)
    save(img, GUI / "frame.png")
    img = paper_panel(760, 82, P["paper"], P["red"], 242, seed=9)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 10, 82), fill=rgba(P["red"], 220))
    save(img, GUI / "notify.png")


def make_overlays():
    w, h = 1920, 1080
    # main menu left gradient
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for x in range(w):
        a = int(180 * max(0, 1 - x / (w * 0.62)) ** 1.5)
        d.line((x, 0, x, h), fill=(18, 12, 9, a))
    img.save(GUI / "overlay" / "main_menu.png")
    # game menu dark wash
    img = Image.new("RGBA", (w, h), (18, 12, 9, 190))
    img.save(GUI / "overlay" / "game_menu.png")
    # confirm wash
    img = Image.new("RGBA", (w, h), (10, 8, 6, 210))
    img.save(GUI / "overlay" / "confirm.png")
    # vignette
    x = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
    y = np.linspace(-1, 1, h, dtype=np.float32)[:, None]
    r = np.sqrt(x * x + y * y)
    a = np.clip((r - 0.55) / 0.7, 0, 1) ** 1.5 * 150
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[:, :, 0:3] = 12
    arr[:, :, 3] = a.astype(np.uint8)
    Image.fromarray(arr, "RGBA").save(GUI / "overlay" / "vignette.png")
    print("wrote overlays")


def make_backgrounds():
    menu = Image.open(BG / "bg_menu.webp").convert("RGB")
    menu.save(GUI / "main_menu.png")
    spring = Image.open(BG / "bg_spring.webp").convert("RGB").filter(ImageFilter.GaussianBlur(6))
    # darken
    arr = np.array(spring).astype(np.float32) * 0.55
    spring = Image.fromarray(np.uint8(np.clip(arr, 0, 255)), "RGB")
    spring.save(GUI / "game_menu.png")
    print("wrote menu backgrounds")


def seal_icon(size=256):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # irregular seal square
    pad = size * 0.08
    pts = []
    for a in range(0, 360, 30):
        r = size * 0.45 + random.randint(-3, 3)
        pts.append((size / 2 + r * math.cos(math.radians(a)), size / 2 + r * math.sin(math.radians(a))))
    d.polygon(pts, fill=rgba(P["red"], 235))
    d.rectangle((pad * 2, pad * 2, size - pad * 2, size - pad * 2), outline=rgba("#F3E7D3", 160), width=max(2, int(size * 0.02)))
    f = ImageFont.truetype(str(FONT), int(size * 0.52))
    bbox = d.textbbox((0, 0), "春", font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1] - size * 0.02), "春", font=f, fill=rgba("#F3E7D3", 245))
    return img


def make_icons():
    icon = seal_icon(256)
    icon.save(GUI / "window_icon.png")
    icon.save(GUI / "seal.png")
    # logo with text
    w, h = 900, 360
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(FONT), 132)
    text = "春声南来"
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    d.text(((w - tw) / 2, 70), text, font=f, fill=rgba("#F3E7D3", 245),
           stroke_width=4, stroke_fill=rgba("#5A1E18", 180))
    d.line((140, 250, w - 140, 250), fill=rgba(P["kerosene"], 180), width=3)
    f2 = ImageFont.truetype(str(FONT), 34)
    sub = "一个凤阳青年的十七年"
    bb2 = d.textbbox((0, 0), sub, font=f2)
    d.text(((w - (bb2[2] - bb2[0])) / 2, 270), sub, font=f2, fill=rgba("#D9C9B8", 220))
    img.save(GUI / "logo.png")
    print("wrote icons")


def portrait(kind, ring, accent):
    size = 320
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # paper disc
    d.ellipse((8, 8, size - 8, size - 8), fill=rgba(P["cream"], 245), outline=rgba(ring, 230), width=8)
    d.ellipse((22, 22, size - 22, size - 22), outline=rgba(P["brown"], 80), width=2)
    # silhouette
    cx, cy = size / 2, size * 0.58
    head_r = size * 0.15
    d.ellipse((cx - head_r, cy - size * 0.30, cx + head_r, cy - size * 0.30 + head_r * 2.1),
              fill=rgba(P["darkbrown"], 245))
    # shoulders
    d.polygon([(cx - size * 0.30, size * 0.92), (cx - size * 0.24, size * 0.66),
               (cx + size * 0.24, size * 0.66), (cx + size * 0.30, size * 0.92)],
              fill=rgba(P["darkbrown"], 245))
    # hair / cap / bun variations
    if kind in ("father", "uncle", "liang", "wu"):
        # worker cap
        d.pieslice((cx - size * 0.18, cy - size * 0.38, cx + size * 0.18, cy - size * 0.12),
                   180, 360, fill=rgba(accent, 245))
        d.rectangle((cx - size * 0.19, cy - size * 0.25, cx + size * 0.19, cy - size * 0.21),
                    fill=rgba(accent, 245))
    elif kind == "mother":
        d.ellipse((cx - size * 0.22, cy - size * 0.42, cx + size * 0.22, cy - size * 0.18),
                  fill=rgba(accent, 220))
    elif kind == "su":
        d.ellipse((cx - size * 0.21, cy - size * 0.40, cx + size * 0.21, cy - size * 0.14),
                  fill=rgba(accent, 230))
        # glasses
        d.rectangle((cx - size * 0.12, cy - size * 0.30, cx - size * 0.02, cy - size * 0.24),
                    outline=rgba(P["paper"], 220), width=3)
        d.rectangle((cx + size * 0.02, cy - size * 0.30, cx + size * 0.12, cy - size * 0.24),
                    outline=rgba(P["paper"], 220), width=3)
    elif kind == "chen":
        # flared collar
        d.polygon([(cx - size * 0.24, size * 0.72), (cx - size * 0.12, size * 0.92),
                   (cx, size * 0.78), (cx + size * 0.12, size * 0.92),
                   (cx + size * 0.24, size * 0.72)], fill=rgba(accent, 230))
    elif kind == "zhao":
        # slick hair
        d.ellipse((cx - size * 0.18, cy - size * 0.40, cx + size * 0.18, cy - size * 0.18),
                  fill=rgba(accent, 230))
    # small seal mark
    d.rectangle((size - 78, size - 64, size - 34, size - 20), fill=rgba(P["red"], 210))
    d.text((size - 70, size - 60), "春", font=ImageFont.truetype(str(FONT), 28), fill=rgba(P["paper"], 240))
    return img


def make_portraits():
    specs = {
        "lin": ("#A33327", "#4A1814"),
        "father": ("#6B5B4B", "#3A2A20"),
        "uncle": ("#8B5E3C", "#4A3226"),
        "mother": ("#8A6A4A", "#5A3A28"),
        "su": ("#4F6F5A", "#2F4A42"),
        "chen": ("#8A6D3B", "#5A3A20"),
        "wu": ("#5C6B73", "#3A4448"),
        "liang": ("#6B5B4B", "#3A2A20"),
        "zhao": ("#7A2E2E", "#4A1814"),
        "dealer": ("#6B5B4B", "#3A2A20"),
    }
    for kind, (ring, accent) in specs.items():
        img = portrait(kind, ring, accent)
        img.save(PORTRAIT / f"portrait_{kind}.png")
        print("wrote portrait", kind)


if __name__ == "__main__":
    random.seed(21)
    np.random.seed(21)
    make_textbox()
    make_namebox()
    make_choice_buttons()
    make_small_buttons()
    make_slots()
    make_frame_notify()
    make_overlays()
    make_backgrounds()
    make_icons()
    make_portraits()
