# -*- coding: utf-8 -*-
"""Push the painted scenes and interface a step more saturated."""
from pathlib import Path

from PIL import Image, ImageEnhance

GAME = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc\game")


def boost(path: Path, color: float, contrast: float = 1.06, bright: float = 1.02):
    im = Image.open(path)
    im = ImageEnhance.Color(im).enhance(color)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Brightness(im).enhance(bright)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        im = im.convert("RGB")
        im.save(path, "JPEG", quality=90, optimize=True)
    else:
        im.save(path)
    print(path.name)


def main():
    for path in (GAME / "images" / "bg").glob("*.webp"):
        boost(path, 1.42)


if __name__ == "__main__":
    main()
