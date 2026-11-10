# -*- coding: utf-8 -*-
"""Southern-tour stills, per-chapter music, and the chapter-6 hold."""
from __future__ import annotations

import math
import re
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

GAME = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc")
ASSETS = Path(r"C:\Users\Wyf\.cursor\projects\c-Users-Wyf-OneDrive-Desktop-AI\assets")
BG = GAME / "game" / "images" / "bg"
IMG = GAME / "game" / "images"
AUDIO = GAME / "game" / "audio"
SR = 22050

HZ = {
    "C3": 130.81, "D3": 146.83, "F3": 174.61, "G3": 196.00, "A3": 220.00,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F#4": 369.99, "G4": 392.00,
    "A4": 440.00, "B4": 493.88, "D5": 587.33, "E5": 659.25, "A5": 880.00,
}


def t_of(n):
    return np.arange(n, dtype=np.float32) / SR


def write_wav(name, data, gain=0.45):
    data = np.asarray(data, dtype=np.float32)
    peak = np.max(np.abs(data)) or 1.0
    data = data / peak * gain
    # seamless-ish edge
    f = int(SR * 1.2)
    if len(data) > f * 3:
        ramp = np.linspace(0, 1, f, dtype=np.float32)
        head = data[:f].copy()
        data = data[:-f]
        data[:f] = data[:f] * ramp + head * (1 - ramp)
    pcm = np.int16(np.clip(data, -1, 1) * 32767)
    path = AUDIO / name
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wav", name, path.stat().st_size // 1024, "KB")


def bed(dur):
    return np.zeros(int(SR * dur), dtype=np.float32)


def place(buf, start, snd):
    i = int(start * SR)
    if i >= len(buf) or i < 0:
        return
    n = min(len(snd), len(buf) - i)
    buf[i:i + n] += snd[:n]


def env(n, attack, release):
    e = np.ones(n, dtype=np.float32)
    a = min(n // 3, max(1, int(SR * attack)))
    r = min(n // 2, max(1, int(SR * release)))
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.linspace(1, 0, r)
    return e


def tone(freq, dur, partials, amp=0.2, vibrato=0.0, attack=0.08, release=0.5):
    n = max(8, int(SR * dur))
    tt = t_of(n)
    vib = 1 + vibrato * np.sin(2 * math.pi * 5.2 * tt)
    z = np.zeros(n, dtype=np.float32)
    for k, a in partials:
        z += a * np.sin(2 * math.pi * freq * k * vib * tt)
    z *= env(n, attack, release)
    peak = np.max(np.abs(z)) or 1.0
    return amp * z / peak


def erhu(freq, dur, amp=0.16):
    return tone(freq, dur, [(1, 1), (2, 0.45), (3, 0.22), (4, 0.08)], amp, vibrato=0.012, attack=0.18, release=0.7)


def dizi(freq, dur, amp=0.1):
    n = max(8, int(SR * dur))
    tt = t_of(n)
    breath = 0.04 * np.random.normal(0, 1, n).astype(np.float32)
    z = np.sin(2 * math.pi * freq * tt) + 0.15 * np.sin(2 * math.pi * freq * 2 * tt)
    z = z * env(n, 0.06, 0.45) + breath * env(n, 0.02, 0.3)
    peak = np.max(np.abs(z)) or 1.0
    return amp * z / peak


def guitar(freq, dur, amp=0.12):
    return tone(freq, dur, [(1, 1), (2, 0.35), (3, 0.18)], amp, attack=0.005, release=min(1.4, dur * 0.8))


def piano(freq, dur, amp=0.14):
    return tone(freq, dur, [(1, 1), (2, 0.42), (3, 0.18), (4, 0.08)], amp, attack=0.012, release=min(2.2, dur * 0.85))


def clarinet(freq, dur, amp=0.13):
    return tone(freq, dur, [(1, 1), (3, 0.45), (5, 0.18), (7, 0.08)], amp, vibrato=0.004, attack=0.09, release=0.45)


def strings(freq, dur, amp=0.08):
    a = tone(freq, dur, [(1, 1), (2, 0.3)], amp, vibrato=0.003, attack=0.6, release=0.8)
    b = tone(freq * 1.004, dur, [(1, 1)], amp * 0.7, vibrato=0.003, attack=0.7, release=0.8)
    n = min(len(a), len(b))
    return a[:n] + b[:n]


def noise_bed(dur, cutoff=0.01, amp=0.08):
    n = int(SR * dur)
    x = np.random.normal(0, 1, n).astype(np.float32)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(n):
        acc += cutoff * (x[i] - acc)
        y[i] = acc
    peak = np.max(np.abs(y)) or 1.0
    return amp * y / peak


def ticks(buf, every, freq=180, amp=0.05):
    dur = len(buf) / SR
    pos = 0.4
    while pos < dur - 0.2:
        tt = t_of(int(0.06 * SR))
        snd = amp * np.sin(2 * math.pi * freq * tt) * np.exp(-tt * 40)
        place(buf, pos, snd)
        pos += every


def lay(buf, voice, notes, step, amp, gap=0.0):
    pos = 0.6
    for name, beats in notes:
        dur = max(0.2, beats * step - gap)
        if name:
            place(buf, pos, voice(HZ[name], dur + 0.3, amp))
        pos += beats * step


def make_music():
    np.random.seed(7)
    # Prologue: slow erhu, then erhu plus dizi.
    dur = 32
    pro = bed(dur)
    pro += noise_bed(dur, 0.006, 0.04)
    pro += 0.05 * np.sin(2 * math.pi * 73.4 * t_of(len(pro)))
    phrase = [("D4", 2), ("E4", 2), ("A4", 3), ("F#4", 2), ("D4", 2), ("B4", 1), ("A4", 2), ("D4", 4)]
    lay(pro, erhu, phrase + [("E4", 2), ("D4", 4), (None, 2)], 1.15, 0.16)
    write_wav("mus_pro_a.wav", pro, 0.42)
    pro_b = pro.copy()
    lay(pro_b, dizi, [("A5", 2), (None, 2), ("E5", 2), ("D5", 3), ("A5", 2), (None, 3)], 1.3, 0.07)
    write_wav("mus_pro_b.wav", pro_b, 0.4)

    # Chapter 1
    c1 = noise_bed(28, 0.012, 0.12)
    c1 *= 0.65 + 0.35 * np.sin(2 * math.pi * 0.05 * t_of(len(c1)))
    lay(c1, guitar, [("D4", 4), (None, 4), ("A3", 4), (None, 6)], 1.0, 0.05)
    write_wav("mus_c1_a.wav", c1, 0.36)
    c1b = noise_bed(24, 0.02, 0.05)
    c1b += 0.06 * np.sin(2 * math.pi * 42 * t_of(len(c1b)))
    ticks(c1b, 0.72, 95, 0.08)
    lay(c1b, guitar, [("D4", 1), ("E4", 1), ("A4", 2), ("D4", 2)], 0.9, 0.06)
    write_wav("mus_c1_b.wav", c1b, 0.4)

    # Chapter 2
    c2 = noise_bed(30, 0.004, 0.16)
    c2 += 0.07 * np.sin(2 * math.pi * 55 * t_of(len(c2)))
    write_wav("mus_c2_a.wav", c2, 0.34)
    c2b = noise_bed(30, 0.008, 0.035)
    lay(c2b, guitar, [("E4", 1), (None, 3), ("D4", 1), (None, 4), ("A4", 1), (None, 3), ("B4", 1), (None, 5), ("D4", 2)], 1.0, 0.1)
    write_wav("mus_c2_b.wav", c2b, 0.38)

    # Chapter 3
    c3 = noise_bed(26, 0.018, 0.07)
    c3 += 0.05 * np.sin(2 * math.pi * 48 * t_of(len(c3)))
    ticks(c3, 0.55, 140, 0.04)
    lay(c3, guitar, [("G3", 1), ("D4", 1), ("E4", 1), ("G4", 2), ("E4", 1), ("D4", 2)], 0.55, 0.09)
    write_wav("mus_c3_a.wav", c3, 0.4)
    c3b = noise_bed(28, 0.008, 0.04)
    c3b += 0.04 * np.sin(2 * math.pi * 50 * t_of(len(c3b)))
    # radio hiss bursts
    for pos in (4.0, 14.0, 22.0):
        burst = noise_bed(0.7, 0.2, 0.12) * np.linspace(1, 0, int(0.7 * SR))
        place(c3b, pos, burst)
    lay(c3b, erhu, [("D4", 3), ("E4", 2), ("D4", 4)], 1.2, 0.08)
    write_wav("mus_c3_b.wav", c3b, 0.36)

    # Chapter 4
    c4 = noise_bed(28, 0.01, 0.03)
    ticks(c4, 0.48, 720, 0.035)
    lay(c4, clarinet, [("D4", 1), ("E4", 1), ("F#4", 1), ("A4", 2), ("B4", 1), ("A4", 2), ("F#4", 1), ("D4", 2)], 0.62, 0.12)
    write_wav("mus_c4_a.wav", c4, 0.4)
    c4b = noise_bed(28, 0.007, 0.05)
    c4b += 0.06 * np.sin(2 * math.pi * 62 * t_of(len(c4b)))
    lay(c4b, clarinet, [("A4", 1), (None, 2), ("F#4", 0.5), (None, 3), ("D4", 2)], 1.1, 0.07)
    write_wav("mus_c4_b.wav", c4b, 0.34)

    # Chapter 5: same shape as chapter 4, one note sour, then almost empty.
    c5 = noise_bed(28, 0.01, 0.03)
    ticks(c5, 0.48, 640, 0.03)
    lay(c5, clarinet, [("D4", 1), ("E4", 1), ("F3", 1), ("A4", 2), ("G3", 1), ("A4", 2), ("F#4", 1), ("D4", 2)], 0.62, 0.11)
    write_wav("mus_c5_a.wav", c5, 0.38)
    c5b = noise_bed(32, 0.005, 0.025)
    lay(c5b, piano, [("D3", 1), (None, 7), ("A3", 1), (None, 8)], 1.0, 0.06)
    write_wav("mus_c5_b.wav", c5b, 0.32)

    # Chapter 6
    c6 = noise_bed(30, 0.006, 0.05)
    c6 += 0.03 * np.sin(2 * math.pi * 58 * t_of(len(c6)))
    lay(c6, piano, [("A4", 1), (None, 3), ("E4", 1), (None, 4), ("D4", 2)], 1.0, 0.05)
    write_wav("mus_c6_a.wav", c6, 0.32)
    speech = bed(36)
    tt = t_of(len(speech))
    speech += strings(146.83, 36, 0.12)
    speech += strings(220.00, 36, 0.06)
    lay(speech, piano, [("D3", 2), ("F3", 2), ("A3", 2), ("C4", 2), ("A3", 2), ("F3", 2), ("D3", 4)], 1.35, 0.1)
    write_wav("mus_c6_speech.wav", speech, 0.4)
    hold = bed(28)
    hold += strings(220.00, 28, 0.05)
    lay(hold, piano, [("A3", 3), (None, 5), ("A3", 3), (None, 6)], 1.0, 0.09)
    write_wav("mus_c6_hold.wav", hold, 0.3)
    after = noise_bed(30, 0.005, 0.035)
    lay(after, piano, [("D4", 2), (None, 2), ("A3", 2), (None, 3)], 1.1, 0.06)
    write_wav("mus_c6_after.wav", after, 0.3)

    # Chapter 7
    c7 = noise_bed(32, 0.006, 0.02)
    lay(c7, clarinet, [("D4", 1), ("E4", 1), ("A4", 2), (None, 1), ("F#4", 1), ("D4", 2), (None, 2),
                       ("E4", 1), ("F#4", 1), ("A4", 2), ("B4", 1), ("A4", 3)], 0.85, 0.13)
    write_wav("mus_c7_a.wav", c7, 0.4)
    c7b = c7 * 0.85
    c7b += noise_bed(32, 0.01, 0.02)[:len(c7b)]
    lay(c7b, dizi, [("D5", 1), ("E5", 1), ("A5", 2), (None, 1), ("E5", 1), ("D5", 2)], 0.85, 0.08)
    lay(c7b, strings, [("D3", 8), ("A3", 8)], 1.0, 0.06)
    write_wav("mus_c7_b.wav", c7b, 0.42)


def cover(im, w=1920, h=1080):
    im = im.convert("RGB")
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - w) // 2)
    top = max(0, (nh - h) // 2)
    return im.crop((left, top, left + w, top + h))


def make_stills():
    src = Image.open(ASSETS / "bg_deng_speech.jpg")
    full = cover(src)
    full.save(BG / "bg_deng_speech.jpg", "JPEG", quality=90, optimize=True)
    w, h = full.size
    cw, ch = int(w * 0.62), int(h * 0.62)
    left = int(w * 0.22)
    top = int(h * 0.12)
    near = cover(full.crop((left, top, left + cw, top + ch)))
    near.save(BG / "bg_deng_speech_near.jpg", "JPEG", quality=90, optimize=True)

    gap = full.convert("RGBA")
    shade = Image.new("RGBA", gap.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    d.polygon([(0, int(h * 0.42)), (0, h), (int(w * 0.30), h), (int(w * 0.16), int(h * 0.58))], fill=(12, 10, 9, 230))
    d.ellipse((int(w * 0.02), int(h * 0.30), int(w * 0.20), int(h * 0.62)), fill=(16, 13, 12, 235))
    d.polygon([(w, int(h * 0.40)), (w, h), (int(w * 0.68), h), (int(w * 0.82), int(h * 0.55))], fill=(12, 10, 9, 230))
    d.ellipse((int(w * 0.78), int(h * 0.26), int(w * 0.98), int(h * 0.60)), fill=(16, 13, 12, 235))
    shade = shade.filter(ImageFilter.GaussianBlur(8))
    gap = Image.alpha_composite(gap, shade).convert("RGB")
    gap.save(BG / "bg_deng_gap.jpg", "JPEG", quality=90, optimize=True)

    # Small card of the elder, for the newspaper branch.
    iw, ih = 460, 560
    card_src = full.crop((int(w * 0.30), int(h * 0.08), int(w * 0.68), int(h * 0.78)))
    card_src = card_src.resize((iw - 28, ih - 28), Image.Resampling.LANCZOS)
    card = Image.new("RGBA", (iw, ih), (243, 231, 211, 255))
    card.paste(card_src, (14, 14))
    d = ImageDraw.Draw(card)
    d.rectangle((6, 6, iw - 7, ih - 7), outline=(90, 48, 36, 255), width=4)
    card.save(IMG / "deng_inset.png")
    print("stills", "bg_deng_speech", "near", "gap", "inset")


SPEECH = r'''    # speech-hold-begin
    scene bg_g28_lobby at slow_push
    with fade
    play music "audio/mus_c6_speech.wav" fadein 2.5 loop

    if flag_tour > 0:
        n "国贸大厦的大厅里，已经站满了人。"
        n "红卫钻在音控台后面，拧着接头。"

        scene bg_g28_lobby_z at slow_push
        with dissolve
        n "外面忽然传来一阵脚步声。"
        n "工作人员示意所有人停下手里的活。"
        n "有人低声说：“小平同志来了。”"

        scene bg_deng_speech at slow_push
        with dissolve
        n "人群往两边让开。"
        n "一位老人站在大厅中间，深色大衣，头发花白。"
        n "旁边有人拿着本子，一笔一笔地记。"

        scene bg_deng_gap at slow_push
        with dissolve
        n "人群挡住了视线。"
        n "红卫站在最后排，手上还沾着线路上的黑油。"
        n "他只能从肩膀的缝隙里，看见那位老人。"

        scene bg_deng_speech_near at slow_push
        with dissolve
        n "谈话不是慷慨激昂的演讲。"
        n "更像和身边人的闲聊。"
        n "他离得远，听不全，只断断续续接住几句。"

        play music "audio/mus_c6_hold.wav" fadein 1.4 loop
        scene bg_deng_speech at slow_push
        with dissolve
        n "“改革开放胆子要大一些，敢于试验。”"

        scene bg_deng_speech_near at slow_push
        with dissolve
        n "“看准了的，就大胆地试，大胆地闯。”"

        scene bg_deng_speech at slow_push
        with dissolve
        n "“发展才是硬道理。”"

        play music "audio/mus_c6_speech.wav" fadein 1.6 loop
        scene bg_deng_speech_near at slow_push
        with dissolve
        n "周围的人往前挤、鼓掌。"
        n "他却站着没动。"
        n "三个声音，在他脑子里来回响。"

        u "总得有人先走一步。"
        s "错了敢认，也得有本事改。"
        f "坏了的东西，你也卖吗？"

        play music "audio/mus_c6_after.wav" fadein 2.0 loop
        scene bg_stall at slow_push
        with dissolve
        n "后来他才知道，那天老人还说了很多。"
        n "他把报纸上的话剪下来，贴在维修摊的挡板上。"

        n "他忽然懂了。"
        n "自己以前只想着“敢闯”，却没看清该往哪儿闯。"
        n "只想着快点赚钱，却忘了当初靠什么站住的脚。"

        n "人群散去后，梁师傅催他收工具。"
        n "却看见他盯着修好的扩音器发呆。"
        liang "想什么呢？"
        l "我以前只顾着闯，没看清往哪儿闯。"
        liang "那就重新看。"
        n "梁师傅把螺丝刀递回他手里。"
    else:
        scene bg_stall at slow_push
        with fade
        show deng_inset at inset_card
        n "几天后，红卫在维修摊前，一字一句读完了那篇谈话。"
        n "报纸上的话印得清清楚楚，他却读得很慢。"
        n "像在跟每一个字较劲。"

        play music "audio/mus_c6_hold.wav" fadein 1.4 loop
        n "“改革开放胆子要大一些，敢于试验。”"
        n "“看准了的，就大胆地试，大胆地闯。”"
        n "“发展才是硬道理。”"

        play music "audio/mus_c6_after.wav" fadein 2.0 loop
        n "三个声音，在他脑子里来回响。"
        u "总得有人先走一步。"
        s "错了敢认，也得有本事改。"
        f "坏了的东西，你也卖吗？"

        hide deng_inset
        n "他忽然懂了。"
        n "自己以前只想着“敢闯”，却没看清该往哪儿闯。"
        n "只想着快点赚钱，却忘了当初靠什么站住的脚。"

        n "收工后，梁师傅打来电话，说国贸的活干完了，工钱一分不少。"
        n "红卫道了谢，挂了电话，在摊前坐了很久。"
    # speech-hold-end
'''

OLD_MUSIC = ("room_loop.wav", "wind_loop.wav", "train_loop.wav", "city_loop.wav", "workshop_loop.wav", "theme.wav")
PLAY = re.compile(r'play music "audio/([^"]+)" fadein ([0-9.]+)( loop)?')
LABEL = re.compile(r"^label\s+([A-Za-z0-9_]+)\b")

CHAPTER_CUES = {
    "prologue": ["mus_pro_a.wav", "mus_pro_b.wav", "mus_pro_b.wav"],
    "chapter1": ["mus_c1_a.wav", "mus_c1_b.wav"],
    "chapter2": ["mus_c2_a.wav", "mus_c2_a.wav", "mus_c2_b.wav", "mus_c2_b.wav"],
    "chapter3": ["mus_c3_a.wav", "mus_c3_b.wav", "mus_c3_a.wav", "mus_c4_a.wav"],
    "chapter4": ["mus_c4_a.wav", "mus_c4_b.wav", "mus_c4_a.wav"],
    "chapter5": ["mus_c5_b.wav"] * 6,
    "downfall_route": ["mus_c5_b.wav"],
    "chapter6": ["mus_c6_a.wav", "mus_c7_a.wav"],
    "chapter7": ["mus_c7_a.wav"] * 4 + ["mus_c7_b.wav"] * 6,
}
# chapter 5 opens on the sour workshop motif, then drops into the empty room.
CHAPTER_CUES["chapter5"][0] = "mus_c5_a.wav"

ENDING_CUES = {
    "ending_hidden": "mus_c7_b.wav",
    "ending_home": "mus_c7_b.wav",
    "ending_quality": "mus_c7_b.wav",
    "ending_skills": "mus_c7_b.wav",
    "ending_divided": "mus_c6_after.wav",
    "ending_stable": "mus_c6_after.wav",
    "ending_fail": "mus_c5_b.wav",
    "ending_stuck": "mus_c5_b.wav",
    "ending_common": "mus_pro_a.wav",
}


def swap(line, filename, volume=None):
    vol = f" volume {volume}" if volume else ""

    def repl(m):
        return f'play music "audio/{filename}" fadein {m.group(2)} loop{vol}'

    new, n = PLAY.subn(repl, line, count=1)
    return new, n


def retune(text, cues_by_label, default_label):
    label = default_label
    index = 0
    out = []
    for line in text.splitlines(keepends=True):
        m = LABEL.match(line)
        if m and m.group(1) in cues_by_label:
            label = m.group(1)
            index = 0
        found = PLAY.search(line)
        if found and found.group(1) in OLD_MUSIC and label in cues_by_label:
            cues = cues_by_label[label]
            filename = cues[min(index, len(cues) - 1)]
            volume = 0.55 if filename == "mus_pro_a.wav" and label == "ending_common" else None
            line, n = swap(line, filename, volume)
            if n:
                index += 1
                print("music", label, index, filename.strip())
        out.append(line)
    return "".join(out)


def patch_script():
    path = GAME / "game" / "script.rpy"
    text = path.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    start = text.find("    scene bg_guomao at slow_push")
    # the guomao scene that begins the speech, not an earlier auto one
    start = text.find('    scene bg_guomao at slow_push\n    with fade\n    play music "audio/city_loop.wav"')
    end = text.find("    scene bg_warehouse at slow_push\n    with fade\n    play music", start if start != -1 else 0)
    if start < 0 or end < 0:
        raise SystemExit(f"speech block not found {start} {end}")
    speech = SPEECH.replace("\n", nl)
    if not speech.endswith(nl):
        speech += nl
    text = text[:start] + speech + text[end:]
    text = retune(text, CHAPTER_CUES, "prologue")
    path.write_text(text, encoding="utf-8", newline="")
    print("script patched")


def patch_endings():
    path = GAME / "game" / "endings.rpy"
    text = retune(path.read_text(encoding="utf-8"), ENDING_CUES, "ending_hidden")
    path.write_text(text, encoding="utf-8", newline="")
    print("endings patched")


if __name__ == "__main__":
    make_stills()
    make_music()
    patch_script()
    patch_endings()
