# -*- coding: utf-8 -*-
"""Younger southern-tour still, and a grand cue for that scene only."""
from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

GAME = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc")
SRC = Path(r"C:\Users\Wyf\.cursor\projects\c-Users-Wyf-OneDrive-Desktop-AI\assets\bg_deng_speech_younger.jpg")
BG = GAME / "game" / "images" / "bg"
IMG = GAME / "game" / "images"
AUDIO = GAME / "game" / "audio"
SR = 22050

HZ = {
    "D2": 73.42, "A2": 110.00, "D3": 146.83, "E3": 164.81, "F#3": 185.00,
    "G3": 196.00, "A3": 220.00, "B3": 246.94, "D4": 293.66, "E4": 329.63,
    "F#4": 369.99, "A4": 440.00, "B4": 493.88, "D5": 587.33, "E5": 659.25,
}


def t_of(n):
    return np.arange(n, dtype=np.float32) / SR


def write_wav(name, data, gain=0.5):
    data = np.asarray(data, dtype=np.float32)
    peak = np.max(np.abs(data)) or 1.0
    data = data / peak * gain
    f = int(SR * 1.6)
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
    vib = 1 + vibrato * np.sin(2 * math.pi * 4.6 * tt)
    z = np.zeros(n, dtype=np.float32)
    for k, a in partials:
        z += a * np.sin(2 * math.pi * freq * k * vib * tt)
    z *= env(n, attack, release)
    peak = np.max(np.abs(z)) or 1.0
    return amp * z / peak


def strings(freq, dur, amp=0.08):
    voices = []
    for detune, gain in ((1.0, 1.0), (1.003, 0.72), (0.997, 0.72), (2.0, 0.22)):
        voices.append(tone(freq * detune, dur, [(1, 1), (2, 0.28), (3, 0.08)], amp * gain, vibrato=0.004, attack=0.45, release=0.9))
    n = min(len(v) for v in voices)
    z = voices[0][:n]
    for v in voices[1:]:
        z = z + v[:n]
    return z


def brass(freq, dur, amp=0.16):
    return tone(freq, dur, [(1, 1), (2, 0.62), (3, 0.34), (4, 0.16), (5, 0.08)], amp, vibrato=0.002, attack=0.18, release=0.55)


def choir(freq, dur, amp=0.1):
    return tone(freq, dur, [(1, 1), (2, 0.22), (3, 0.1)], amp, vibrato=0.005, attack=0.9, release=1.1)


def timpani(freq, amp=0.4):
    n = int(1.1 * SR)
    tt = t_of(n)
    phase = 2 * math.pi * freq * (tt - 0.18 * tt * tt)
    body = np.sin(phase) * np.exp(-tt * 2.6)
    knock = np.random.normal(0, 1, n).astype(np.float32) * np.exp(-tt * 30)
    z = body + 0.22 * knock
    peak = np.max(np.abs(z)) or 1.0
    return amp * z / peak


def lay(buf, voice, notes, step, amp):
    pos = 0.4
    for name, beats in notes:
        dur = max(0.25, beats * step)
        if name:
            place(buf, pos, voice(HZ[name], dur + 0.35, amp))
        pos += beats * step


def cover(im, w=1920, h=1080):
    im = im.convert("RGB")
    scale = max(w / im.width, h / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - w) // 2)
    top = max(0, (nh - h) // 2)
    return im.crop((left, top, left + w, top + h))


def make_stills():
    full = cover(Image.open(SRC))
    full.save(BG / "bg_deng_speech.jpg", "JPEG", quality=90, optimize=True)
    w, h = full.size
    near = cover(full.crop((int(w * 0.08), int(h * 0.02), int(w * 0.62), int(h * 0.92))))
    near.save(BG / "bg_deng_speech_near.jpg", "JPEG", quality=90, optimize=True)

    gap = full.convert("RGBA")
    shade = Image.new("RGBA", gap.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    d.polygon([(0, int(h * 0.42)), (0, h), (int(w * 0.28), h), (int(w * 0.14), int(h * 0.55))], fill=(12, 10, 9, 230))
    d.ellipse((int(w * 0.0), int(h * 0.22), int(w * 0.18), int(h * 0.62)), fill=(16, 13, 12, 235))
    d.polygon([(w, int(h * 0.36)), (w, h), (int(w * 0.70), h), (int(w * 0.84), int(h * 0.50))], fill=(12, 10, 9, 230))
    d.ellipse((int(w * 0.80), int(h * 0.18), int(w * 0.99), int(h * 0.58)), fill=(16, 13, 12, 235))
    shade = shade.filter(ImageFilter.GaussianBlur(10))
    gap = Image.alpha_composite(gap, shade).convert("RGB")
    gap.save(BG / "bg_deng_gap.jpg", "JPEG", quality=90, optimize=True)

    iw, ih = 460, 560
    card_src = full.crop((int(w * 0.10), int(h * 0.04), int(w * 0.58), int(h * 0.96)))
    card_src = card_src.resize((iw - 28, ih - 28), Image.Resampling.LANCZOS)
    card = Image.new("RGBA", (iw, ih), (243, 231, 211, 255))
    card.paste(card_src, (14, 14))
    d = ImageDraw.Draw(card)
    d.rectangle((6, 6, iw - 7, ih - 7), outline=(90, 48, 36, 255), width=4)
    card.save(IMG / "deng_inset.png")
    print("stills", full.size)


def chord_bed(buf, chords, brass_amp, choir_amp):
    for start, length, names in chords:
        for name in names:
            place(buf, start, brass(HZ[name], length + 0.4, brass_amp))
            place(buf, start, choir(HZ[name] * 2, length + 0.6, choir_amp))


CHORDS = [
    (0.0, 8.0, ("D3", "F#3", "A3")),
    (8.0, 8.0, ("A2", "E3", "A3")),
    (16.0, 8.0, ("G3", "B3", "D4")),
    (24.0, 8.0, ("D3", "F#3", "A3")),
    (32.0, 8.0, ("D3", "A3", "D4")),
]

MELODY = [
    ("D4", 2), ("F#4", 2), ("A4", 2), ("B4", 1), ("A4", 1),
    ("F#4", 2), ("E4", 2), ("D4", 4),
    ("A4", 2), ("B4", 2), ("D5", 3), ("A4", 1),
    ("F#4", 2), ("E4", 2), ("D4", 4),
    ("D5", 2), ("B4", 2), ("A4", 2), ("F#4", 2), ("D4", 4),
]


def foundation(dur):
    z = bed(dur)
    z += strings(HZ["D2"], dur, 0.18)
    z += strings(HZ["A2"], dur, 0.12)
    z += strings(HZ["D3"], dur, 0.08)
    return z


def make_music():
    np.random.seed(19)
    dur = 42
    speech = foundation(dur)
    chord_bed(speech, CHORDS, 0.13, 0.06)
    pos = 0.2
    while pos < dur - 1.2:
        place(speech, pos, timpani(HZ["D2"], 0.34))
        pos += 2.0
    lay(speech, strings, MELODY, 0.82, 0.16)
    lay(speech, brass, [("D4", 4), ("A4", 4), ("D5", 4), ("A4", 4), ("D4", 6)], 1.6, 0.07)
    write_wav("mus_c6_speech.wav", speech, 0.52)

    hold = foundation(32)
    chord_bed(hold, [
        (0.0, 8.0, ("D3", "F#3", "A3")),
        (8.0, 8.0, ("A2", "E3", "A3")),
        (16.0, 8.0, ("G3", "B3", "D4")),
        (24.0, 8.0, ("D3", "A3", "D4")),
    ], 0.11, 0.055)
    pos = 0.2
    while pos < 30:
        place(hold, pos, timpani(HZ["D2"], 0.22))
        pos += 4.0
    lay(hold, strings, [("D5", 4), (None, 2), ("A4", 4), (None, 2), ("F#4", 4), ("D5", 6), ("A4", 4)], 1.05, 0.12)
    write_wav("mus_c6_hold.wav", hold, 0.48)

    after = foundation(36)
    chord_bed(after, [
        (0.0, 12.0, ("D3", "F#3", "A3")),
        (12.0, 12.0, ("G3", "B3", "D4")),
        (24.0, 12.0, ("D3", "A3", "D4")),
    ], 0.08, 0.04)
    lay(after, strings, [("A4", 3), ("F#4", 2), ("E4", 2), ("D4", 6), ("F#4", 2), ("A4", 3), ("D5", 4), ("D4", 6)], 1.15, 0.12)
    write_wav("mus_c6_grand.wav", after, 0.46)


if __name__ == "__main__":
    make_stills()
    make_music()
