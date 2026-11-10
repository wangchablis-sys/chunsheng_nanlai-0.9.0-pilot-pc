# -*- coding: utf-8 -*-
"""Trim 浮光 from 1:20, export 南方谈话, and place the real Deng photo."""
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc")
AUDIO = ROOT / "game" / "audio"
BG = ROOT / "game" / "images" / "bg"
IMG = ROOT / "game" / "images"
PHOTO = Path(
    r"C:\Users\Wyf\.cursor\projects\c-Users-Wyf-OneDrive-Desktop-AI\assets"
) / "c__Users_Wyf_AppData_Roaming_Cursor_User_workspaceStorage_aefa265346f4e6b2d146cd406c9c950d_images_image-01943df6-2d28-4ffb-b718-207bf5bb8f10.png"
FF = imageio_ffmpeg.get_ffmpeg_exe()


def run(args):
    subprocess.check_call([FF, "-y", *args])


def cover(im, w=1920, h=1080):
    im = im.convert("RGB")
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - w) // 2)
    top = max(0, (nh - h) // 2)
    return im.crop((left, top, left + w, top + h))


def fit_on_blur(src, w=1920, h=1080):
    """Keep the whole photograph visible on a 16:9 frame."""
    src = src.convert("RGB")
    bg = cover(src, w, h).filter(ImageFilter.GaussianBlur(28))
    scale = min(w / src.width, h / src.height)
    nw, nh = int(src.width * scale + 0.5), int(src.height * scale + 0.5)
    fg = src.resize((nw, nh), Image.Resampling.LANCZOS)
    bg.paste(fg, ((w - nw) // 2, (h - nh) // 2))
    return bg


def make_photo():
    src = Image.open(PHOTO)
    print("photo", src.size)
    wide = src.width / src.height > 1.4
    full = cover(src) if wide else fit_on_blur(src)
    full.save(BG / "bg_deng_speech.jpg", "JPEG", quality=92, optimize=True)
    w, h = full.size
    near = cover(full.crop((int(w * 0.18), int(h * 0.04), int(w * 0.82), int(h * 0.96))))
    near.save(BG / "bg_deng_speech_near.jpg", "JPEG", quality=92, optimize=True)
    gap = full.copy()
    gap.save(BG / "bg_deng_gap.jpg", "JPEG", quality=92, optimize=True)

    iw, ih = 460, 560
    face = src.convert("RGB")
    card_src = cover(face, iw - 28, ih - 28)
    card = Image.new("RGBA", (iw, ih), (243, 231, 211, 255))
    card.paste(card_src, (14, 14))
    d = ImageDraw.Draw(card)
    d.rectangle((6, 6, iw - 7, ih - 7), outline=(90, 48, 36, 255), width=4)
    card.save(IMG / "deng_inset.png")
    print("stills written")


def make_audio():
    run([
        "-ss", "80",
        "-i", str(ROOT / "43127475365-1-30280.mp4"),
        "-vn", "-ar", "44100", "-c:a", "libvorbis", "-q:a", "6",
        str(AUDIO / "fuguang.ogg"),
    ])
    run([
        "-i", str(ROOT / "南方谈话.mp4"),
        "-vn", "-ar", "44100", "-c:a", "libvorbis", "-q:a", "6",
        str(AUDIO / "nanfang.ogg"),
    ])
    print("audio written")


if __name__ == "__main__":
    make_audio()
    make_photo()
