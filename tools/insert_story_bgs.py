# -*- coding: utf-8 -*-
"""Copy story stills, make extra framings, and change the picture every 2–3 lines."""
from __future__ import annotations

import re
from collections import deque
from pathlib import Path

from PIL import Image

GAME = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc")
ASSETS = Path(r"C:\Users\Wyf\.cursor\projects\c-Users-Wyf-OneDrive-Desktop-AI\assets")
BG = GAME / "game" / "images" / "bg"

DIALOGUE = re.compile(r"^(\s*)(?:n|l|f|u|m|s|c|w|liang|z|j|old|zhang|nv) \"")
SCENE = re.compile(r"^\s*scene\s+(\S+)")
LABEL = re.compile(r"^label\s+([A-Za-z0-9_]+)\b")

LABEL_CHAPTER = {
    "prologue": "pro",
    "chapter1": "c1",
    "chapter2": "c2",
    "chapter3": "c3",
    "chapter4": "c4",
    "chapter5": "c5",
    "downfall_route": "down",
    "chapter6": "c6",
    "chapter7": "c7",
    "apply_fixed_bonuses": "end",
    "ending_hidden": "end",
    "ending_home": "end",
    "ending_quality": "end",
    "ending_skills": "end",
    "ending_divided": "end",
    "ending_stable": "end",
    "ending_fail": "end",
    "ending_stuck": "end",
    "ending_common": "end",
}

# Ending labels stay inside one set of pictures.
LABEL_FAMILY = {
    "ending_hidden": "hidden",
    "ending_home": "home_end",
    "ending_quality": "quality_end",
    "ending_skills": "skills_end",
    "ending_divided": "divided_end",
    "ending_stable": "stable_end",
    "ending_fail": "fail_end",
    "ending_stuck": "stuck_end",
    "ending_common": "common_end",
    "apply_fixed_bonuses": "common_end",
}


def shots(name):
    """Base still plus a closer framing and a side framing."""
    return [name, name + "_c", name + "_z"]


# Each place has several pictures. Keywords move the story to that place.
FAMILIES = {
    "hall": {
        "images": ["bg_tangwu", *shots("bg_g01_hall"), *shots("bg_g02_thumb")],
        "keys": ["堂屋", "契约", "印泥", "拇指", "红印", "手印", "包产", "煤油", "成分"],
        "chapters": {"pro"},
    },
    "harvest": {
        "images": ["bg_autumn", *shots("bg_g03_harvest")],
        "keys": ["秋收", "馒头", "丰收", "掰成", "弟弟"],
        "chapters": {"pro"},
    },
    "boy": {
        "images": ["bg_boy_repair", *shots("bg_g04_repair")],
        "keys": ["手电筒", "拆拆装装", "门槛上", "琢磨", "不响了"],
        "chapters": {"pro"},
    },
    "county": {
        "images": ["bg_county", *shots("bg_g05_county")],
        "keys": ["县城", "自行车", "喇叭裤", "贺卡", "张长喜"],
        "chapters": {"c1"},
    },
    "farewell": {
        "images": [*shots("bg_g06_farewell"), "bg_tangwu"],
        "keys": ["棉袄", "二十元", "针脚", "村口", "院门", "半大的猪", "巴掌"],
        "chapters": {"c1"},
    },
    "train": {
        "images": ["bg_train", *shots("bg_g07_train"), *shots("bg_g08_circuit"), *shots("bg_g38_hills")],
        "keys": ["火车", "车厢", "绿皮", "吴国强", "电路图", "平原", "丘陵", "五元", "介绍费"],
        "chapters": {"c1"},
    },
    "eaves": {
        "images": ["bg_eaves", *shots("bg_g09_eaves")],
        "keys": ["屋檐", "粤语", "介绍信", "货运站", "遍地黄金", "行李险些"],
        "chapters": {"c2"},
    },
    "site": {
        "images": ["bg_site", *shots("bg_g10_site"), *shots("bg_g37_tools")],
        "keys": ["工地", "水泥", "搬砖", "扩音器", "包工头", "砌砖", "螺丝刀", "电工"],
        "chapters": {"c2"},
    },
    "stall": {
        "images": ["bg_stall", *shots("bg_g11_stall"), *shots("bg_g27_stall2")],
        "keys": ["维修摊", "彪子", "招牌", "街口", "孙老板"],
        "chapters": {"c2", "c5", "c6"},
    },
    "night": {
        "images": ["bg_nightschool", *shots("bg_g12_night")],
        "keys": ["夜校", "周三", "周六", "电路板", "万用表", "超外差", "水泡", "二极管", "老化"],
        "chapters": {"c2"},
    },
    "dawn": {
        "images": ["bg_oldradio", *shots("bg_g13_dawn")],
        "keys": ["老工人", "垃圾堆", "线圈", "儿子留下", "广播声"],
        "chapters": {"c2"},
    },
    "bus": {
        "images": ["bg_longbus", *shots("bg_g14_bus")],
        "keys": ["长途", "货源", "跑遍", "合伙", "录音机的需求"],
        "chapters": {"c3"},
    },
    "return": {
        "images": ["bg_return", *shots("bg_g15_return")],
        "keys": ["新夹克", "双卡", "三百元", "有发票", "一院子"],
        "chapters": {"c3"},
    },
    "watches": {
        "images": ["bg_watch", *shots("bg_g16_watches")],
        "keys": ["晶振", "走时", "残次", "降价", "校准", "三分之一"],
        "chapters": {"c3"},
    },
    "workshop": {
        "images": ["bg_workshop", *shots("bg_g17_workshop"), *shots("bg_g19_qc")],
        "keys": ["作坊", "平房", "组装", "外壳", "天线", "编号", "质检", "梁师傅"],
        "chapters": {"c3", "c4", "c5"},
    },
    "blackout": {
        "images": ["bg_blackout", *shots("bg_g18_blackout")],
        "keys": ["停电", "偷电", "私接", "煤油灯"],
        "chapters": {"c4"},
    },
    "market": {
        "images": ["bg_market", *shots("bg_g20_market")],
        "keys": ["农村市场", "声音大", "价格低", "坏了好修"],
        "chapters": {"c4"},
    },
    "house": {
        "images": [*shots("bg_g21_house")],
        "keys": ["砖房", "堂屋正中", "盖起了"],
        "chapters": {"c4"},
    },
    "caps": {
        "images": [*shots("bg_g22_caps"), "bg_workshop"],
        "keys": ["赵万金", "电容", "抽检", "极低"],
        "chapters": {"c5"},
    },
    "smoke": {
        "images": ["bg_crisis", *shots("bg_g23_smoke")],
        "keys": ["冒烟", "过热", "供销社", "退回", "假货", "赔偿", "召回"],
        "chapters": {"c5", "down"},
    },
    "sealed": {
        "images": ["bg_collapse", *shots("bg_g24_sealed")],
        "keys": ["封条", "查封", "树倒", "另起炉灶", "设计图纸"],
        "chapters": {"c5", "down", "end"},
    },
    "kang": {
        "images": [*shots("bg_g25_kang")],
        "keys": ["摔断", "医药", "电报", "炕上", "治腿", "药费"],
        "chapters": {"c5", "down"},
    },
    "post": {
        "images": ["bg_postoffice", *shots("bg_g26_post")],
        "keys": ["邮局", "汇款", "挂面", "布鞋", "布包裹"],
        "chapters": {"c5"},
    },
    "winter": {
        "images": [*shots("bg_g40_winter"), "bg_stall"],
        "keys": ["一九九二年", "冷清", "修收音机的人"],
        "chapters": {"c6"},
    },
    "lobby": {
        "images": ["bg_guomao", *shots("bg_g28_lobby")],
        "keys": ["国贸", "音控", "大厅", "南巡", "接头"],
        "chapters": {"c6"},
    },
    "solder": {
        "images": ["bg_warehouse", *shots("bg_g29_solder")],
        "keys": ["旧仓库", "烙铁", "木箱", "退回来", "第一台"],
        "chapters": {"c6", "c7"},
    },
    "shanghai": {
        "images": ["bg_shanghai", *shots("bg_g30_shanghai")],
        "keys": ["弄堂", "保护电路", "样机", "请她"],
        "chapters": {"c7", "end"},
    },
    "reopen": {
        "images": ["bg_reopen", *shots("bg_g31_reopen")],
        "keys": ["重新开门", "作坊门", "再干"],
        "chapters": {"c7"},
    },
    "factory": {
        "images": ["bg_factory", *shots("bg_g32_factory")],
        "keys": ["建厂", "板车", "组装车间", "招工"],
        "chapters": {"c7", "end"},
    },
    "line": {
        "images": ["bg_1995", *shots("bg_g33_line"), *shots("bg_g39_class")],
        "keys": ["流水", "培训", "工资", "女工", "黑板", "学员"],
        "chapters": {"c7", "end"},
    },
    "threshold": {
        "images": ["bg_threshold", *shots("bg_g34_threshold")],
        "keys": ["门槛", "干裂", "换班"],
        "chapters": {"c7", "end"},
    },
    "busstop": {
        "images": ["bg_bus", *shots("bg_g35_busstop")],
        "keys": ["班车", "下车", "返青"],
        "chapters": {"c7", "end"},
    },
    "spring": {
        "images": ["bg_spring", *shots("bg_g36_spring")],
        "keys": ["春风", "春天每年", "掠过"],
        "chapters": {"c7", "end"},
    },
    "hidden": {
        "images": ["bg_end_e8", *shots("bg_g36_spring"), *shots("bg_g02_thumb"), *shots("bg_g29_solder")],
        "keys": ["潮头", "回声"],
        "chapters": {"end"},
    },
    "home_end": {
        "images": ["bg_end_e1", *shots("bg_g32_factory"), *shots("bg_g35_busstop"), *shots("bg_g34_threshold")],
        "keys": ["归乡", "共同富裕"],
        "chapters": {"end"},
    },
    "quality_end": {
        "images": ["bg_end_e2", *shots("bg_g33_line"), *shots("bg_g30_shanghai")],
        "keys": ["质造", "品牌"],
        "chapters": {"end"},
    },
    "skills_end": {
        "images": ["bg_end_e3", *shots("bg_g39_class"), *shots("bg_g11_stall")],
        "keys": ["培训班", "薪火"],
        "chapters": {"end"},
    },
    "divided_end": {
        "images": ["bg_end_e5", *shots("bg_g14_bus"), *shots("bg_g28_lobby")],
        "keys": ["两路", "分叉"],
        "chapters": {"end"},
    },
    "stable_end": {
        "images": ["bg_end_e4", *shots("bg_g27_stall2"), *shots("bg_g04_repair")],
        "keys": ["安稳", "小店"],
        "chapters": {"end"},
    },
    "fail_end": {
        "images": ["bg_end_e6", *shots("bg_g24_sealed"), *shots("bg_g23_smoke")],
        "keys": ["失信", "查封"],
        "chapters": {"end"},
    },
    "stuck_end": {
        "images": ["bg_end_e7", *shots("bg_g27_stall2"), *shots("bg_g16_watches")],
        "keys": ["故步", "积灰"],
        "chapters": {"end"},
    },
    "common_end": {
        "images": ["bg_end_e0", *shots("bg_g36_spring"), *shots("bg_g03_harvest")],
        "keys": ["日子还在", "每年都会"],
        "chapters": {"end"},
    },
}

IMAGE_FAMILY = {}
for fid, fam in FAMILIES.items():
    for image in fam["images"]:
        IMAGE_FAMILY.setdefault(image, fid)


def cover_resize(im):
    w, h = 1920, 1080
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - w) // 2)
    top = max(0, (nh - h) // 2)
    return im.crop((left, top, left + w, top + h))


def save_jpeg(im, dest: Path):
    im.convert("RGB").save(dest, "JPEG", quality=88, optimize=True)


def copy_stills():
    n = 0
    for src in sorted(ASSETS.glob("bg_g*.jpg")):
        base = cover_resize(Image.open(src))
        dest = BG / f"{src.stem}.jpg"
        save_jpeg(base, dest)
        w, h = base.size
        # Closer framing.
        cw, ch = int(w * 0.74), int(h * 0.74)
        close = base.crop(((w - cw) // 2, int(h * 0.08), (w - cw) // 2 + cw, int(h * 0.08) + ch))
        save_jpeg(cover_resize(close), BG / f"{src.stem}_c.jpg")
        # Left-weighted framing.
        lw, lh = int(w * 0.8), int(h * 0.8)
        left = base.crop((int(w * 0.02), int(h * 0.1), int(w * 0.02) + lw, int(h * 0.1) + lh))
        save_jpeg(cover_resize(left), BG / f"{src.stem}_z.jpg")
        n += 1
    print("base stills", n)


def available_names():
    return {p.stem for p in BG.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}}


def next_chunk(lines, start, count):
    parts = []
    for line in lines[start:]:
        if DIALOGUE.match(line):
            parts.append(line)
            if len(parts) >= count:
                break
        elif parts and (line.strip().startswith("label ") or (line.strip().startswith("scene ") and "# auto-bg" not in line)):
            break
    return "".join(parts)


def family_hits(fid, text):
    return sum(1 for key in FAMILIES[fid]["keys"] if key in text)


def choose_family(text, chapter, current, locked):
    if locked or current is None:
        return current
    best = current
    best_hits = family_hits(current, text)
    for fid, fam in FAMILIES.items():
        if fid == current:
            continue
        hits = family_hits(fid, text)
        if hits <= 0:
            continue
        same = chapter in fam["chapters"]
        if not same and hits < 2:
            continue
        if hits > best_hits or (hits == best_hits and hits > 0 and same and chapter not in FAMILIES[current]["chapters"]):
            best = fid
            best_hits = hits
    return best


def choose_image(fid, current, used, recent, names):
    images = [name for name in FAMILIES[fid]["images"] if name in names and name != current]
    if not images:
        return None
    fresh = [name for name in images if name not in recent]
    pool = fresh or images
    pool.sort(key=lambda name: (used.get(name, 0), name))
    return pool[0]


def transform(text, default_chapter):
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = [ln + nl for ln in text.splitlines()]
    lines = [ln for ln in lines if "# auto-bg" not in ln]
    names = available_names()
    used = {}
    recent = deque(maxlen=4)
    chapter = default_chapter
    family = "hall" if default_chapter == "pro" else "common_end"
    locked = default_chapter == "end"
    current = None
    since = 0
    quota = 2
    inserted = 0
    hold = False
    out = []
    for i, line in enumerate(lines):
        if "speech-hold-begin" in line:
            hold = True
        if "speech-hold-end" in line:
            hold = False
            since = 0
        label = LABEL.match(line)
        if label:
            name = label.group(1)
            if name in LABEL_CHAPTER:
                chapter = LABEL_CHAPTER[name]
            if name in LABEL_FAMILY:
                family = LABEL_FAMILY[name]
                locked = True
            elif name in LABEL_CHAPTER and chapter != "end":
                locked = False
        scene = SCENE.match(line)
        if scene and "# auto-bg" not in line:
            current = scene.group(1)
            if not locked and current in IMAGE_FAMILY:
                family = IMAGE_FAMILY[current]
            since = 0
            out.append(line)
            continue
        if DIALOGUE.match(line) and not hold:
            if since >= quota:
                indent = DIALOGUE.match(line).group(1)
                chunk = next_chunk(lines, i, quota)
                family = choose_family(chunk, chapter, family, locked)
                bg = choose_image(family, current, used, recent, names)
                if bg:
                    out.append(f"{indent}scene {bg} at slow_push  # auto-bg{nl}")
                    out.append(f"{indent}with dissolve  # auto-bg{nl}")
                    current = bg
                    used[bg] = used.get(bg, 0) + 1
                    recent.append(bg)
                    inserted += 1
                    since = 0
                    quota = 2 if quota == 3 else 3
            out.append(line)
            since += 1
            continue
        out.append(line)
    return "".join(out), inserted, used


def longest_dialogue_run(text):
    longest = run = 0
    for line in text.splitlines():
        if line.strip().startswith("scene "):
            longest = max(longest, run)
            run = 0
        elif DIALOGUE.match(line):
            run += 1
    return max(longest, run)


def main():
    if not (BG / "bg_g01_hall_c.jpg").exists():
        copy_stills()
    else:
        print("stills already copied")
    names = available_names()
    missing = sorted({img for fam in FAMILIES.values() for img in fam["images"] if img not in names})
    print("missing", missing)
    for name, default in (("script.rpy", "pro"), ("endings.rpy", "end")):
        path = GAME / "game" / name
        updated, inserted, used = transform(path.read_text(encoding="utf-8"), default)
        path.write_text(updated, encoding="utf-8", newline="")
        print(name, "insertions", inserted, "longest", longest_dialogue_run(updated), "unique", len(used))


if __name__ == "__main__":
    main()
