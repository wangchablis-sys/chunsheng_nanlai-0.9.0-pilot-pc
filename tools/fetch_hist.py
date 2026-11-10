# -*- coding: utf-8 -*-
"""Download freely licensed period photos and crop them to 1920x1080."""
import ssl
import urllib.request
from pathlib import Path

from PIL import Image

OUT = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc\game\images\bg")
RAW = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc\tools\hist_raw")
RAW.mkdir(parents=True, exist_ok=True)

FILES = {
    "hist_garden": "https://thumb.wikimedia.org/wikipedia/commons/thumb/4/44/China-1978_Commune_Garden_Paul_Burns.jpg/1920px-China-1978_Commune_Garden_Paul_Burns.jpg",
    "hist_street": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/77/China-1978_Pedal_powered_trucks_Paul_Burns.jpg/1920px-China-1978_Pedal_powered_trucks_Paul_Burns.jpg",
    "hist_wagon": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d0/China-1978_Mule_drawn_wagon_Paul_Burns.jpg/1920px-China-1978_Mule_drawn_wagon_Paul_Burns.jpg",
    "hist_market": "https://thumb.wikimedia.org/wikipedia/commons/thumb/2/2a/China-1978_Market_Paul_Burns.jpg/1920px-China-1978_Market_Paul_Burns.jpg",
    "hist_factory": "https://thumb.wikimedia.org/wikipedia/commons/thumb/8/86/China-1978_Lacquerware_Art_Factory_Paul_Burns.jpg/1920px-China-1978_Lacquerware_Art_Factory_Paul_Burns.jpg",
    "hist_ceramics": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/08/China-1978_Ceramics_Factory_Paul_Burns.jpg/1920px-China-1978_Ceramics_Factory_Paul_Burns.jpg",
    "hist_abacus": "https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5b/China-1978_Abacus_lesson_Paul_Burns.jpg/1920px-China-1978_Abacus_lesson_Paul_Burns.jpg",
    "hist_class": "https://thumb.wikimedia.org/wikipedia/commons/thumb/7/78/China-1978_Primary_Class_Paul_Burns.jpg/1920px-China-1978_Primary_Class_Paul_Burns.jpg",
    "hist_luohu": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Luohu_1978_01.jpg",
    "hist_border": "https://upload.wikimedia.org/wikipedia/commons/9/97/Luohu_1978_02.jpg",
    "hist_coach": "https://upload.wikimedia.org/wikipedia/commons/9/94/China_Railways_22_passenger_coach_in_Chengdu_Railway_Station%2C_1999.jpg",
    "hist_carriage": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d1/Interior_of_YZ22_-_1.jpg/1920px-Interior_of_YZ22_-_1.jpg",
    "hist_guomao": "https://upload.wikimedia.org/wikipedia/commons/1/1b/GouMou_20061222_large.jpg",
}

CTX = ssl._create_unverified_context()


def cover(im, w=1920, h=1080):
    im = im.convert("RGB")
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - w) // 2)
    top = max(0, (nh - h) // 2)
    return im.crop((left, top, left + w, top + h))


def grab(name, url):
    dest = RAW / (name + ".jpg")
    req = urllib.request.Request(url, headers={"User-Agent": "hongwei-course/0.1"})
    with urllib.request.urlopen(req, context=CTX, timeout=90) as resp:
        dest.write_bytes(resp.read())
    im = cover(Image.open(dest))
    im.save(OUT / (name + ".jpg"), "JPEG", quality=86, optimize=True)
    print(name, dest.stat().st_size, im.size)


if __name__ == "__main__":
    for name, url in FILES.items():
        grab(name, url)
