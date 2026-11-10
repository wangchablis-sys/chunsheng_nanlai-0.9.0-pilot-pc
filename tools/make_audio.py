# -*- coding: utf-8 -*-
"""Small procedural ambience set for the Ren'Py pilot."""
from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np

BASE = Path(r"D:\try_deepseek_harness\chunsheng_nanlai")
AUDIO = BASE / "game" / "audio"
AUDIO.mkdir(parents=True, exist_ok=True)

SR = 22050


def write(name, data, gain=0.7):
    data = np.asarray(data, dtype=np.float32)
    peak = np.max(np.abs(data)) or 1.0
    data = data / peak * gain
    pcm = np.int16(np.clip(data, -1, 1) * 32767)
    path = AUDIO / name
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("wrote", name, path.stat().st_size // 1024, "KB")


def t(dur):
    return np.arange(int(SR * dur), dtype=np.float32) / SR


def env_ad(n, a=0.02, d=0.3):
    a = max(1, int(SR * a))
    d = max(1, int(SR * d))
    e = np.ones(n, dtype=np.float32)
    a = min(a, n)
    d = min(d, n)
    e[:a] = np.linspace(0, 1, a)
    e[-d:] *= np.linspace(1, 0, d)
    return e


def sine(freq, dur, amp=0.3, detune=0.0):
    x = t(dur)
    return amp * np.sin(2 * math.pi * (freq + detune) * x)


def triangle(freq, dur, amp=0.2):
    x = t(dur)
    return amp * (2 / math.pi) * np.arcsin(np.sin(2 * math.pi * freq * x))


def smooth_noise(dur, cutoff=0.02):
    n = int(SR * dur)
    x = np.random.normal(0, 1, n).astype(np.float32)
    # simple one-pole low-pass
    y = np.empty_like(x)
    acc = 0.0
    for i in range(n):
        acc += cutoff * (x[i] - acc)
        y[i] = acc
    return y / (np.max(np.abs(y)) or 1.0)


def crossfade_loop(x, fade=1.0):
    n = len(x)
    f = int(SR * fade)
    if f * 2 >= n:
        return x
    head = x[:f].copy()
    tail = x[-f:].copy()
    x = x[:-f].copy()
    x[:f] = tail * np.linspace(0, 1, f) + head * np.linspace(1, 0, f)
    return x


def make_wind():
    dur = 24
    x = smooth_noise(dur, 0.008)
    y = smooth_noise(dur, 0.03)
    z = 0.65 * x + 0.35 * y
    z *= (0.55 + 0.45 * np.sin(2 * math.pi * 0.06 * t(dur)) ** 2)
    z = crossfade_loop(z, 2.0)
    write("wind_loop.wav", z, 0.35)


def make_room():
    dur = 24
    x = t(dur)
    hum = 0.10 * np.sin(2 * math.pi * 50 * x) + 0.05 * np.sin(2 * math.pi * 100 * x)
    air = 0.18 * smooth_noise(dur, 0.01)
    creak = np.zeros_like(x)
    for pos in [3.2, 9.8, 16.4]:
        i = int(pos * SR)
        n = int(0.6 * SR)
        if i + n < len(creak):
            tt = np.arange(n) / SR
            creak[i:i + n] += 0.12 * np.sin(2 * math.pi * (180 + 40 * tt) * tt) * np.exp(-tt * 4)
    z = hum + air + creak
    z = crossfade_loop(z, 2.0)
    write("room_loop.wav", z, 0.35)


def make_train():
    dur = 18
    x = t(dur)
    z = 0.10 * np.sin(2 * math.pi * 42 * x) + 0.06 * smooth_noise(dur, 0.02)
    # wheel clatter
    for pos in np.arange(0.0, dur, 0.72):
        i = int(pos * SR)
        n = int(0.12 * SR)
        if i + n < len(z):
            tt = np.arange(n) / SR
            z[i:i + n] += 0.22 * np.sin(2 * math.pi * 95 * tt) * np.exp(-tt * 40)
            z[i:i + n] += 0.10 * smooth_noise(0.12, 0.05)[:n] * np.exp(-tt * 30)
    z = crossfade_loop(z, 1.2)
    write("train_loop.wav", z, 0.4)


def make_city():
    dur = 24
    x = t(dur)
    z = 0.07 * np.sin(2 * math.pi * 55 * x) + 0.05 * np.sin(2 * math.pi * 110 * x)
    z += 0.18 * smooth_noise(dur, 0.004)
    z *= 0.8 + 0.2 * np.sin(2 * math.pi * 0.09 * x)
    z = crossfade_loop(z, 2.0)
    write("city_loop.wav", z, 0.35)


def make_workshop():
    dur = 24
    x = t(dur)
    z = 0.08 * np.sin(2 * math.pi * 60 * x) + 0.04 * np.sin(2 * math.pi * 120 * x)
    z += 0.16 * smooth_noise(dur, 0.012)
    for pos in [2.5, 7.8, 13.9, 19.2]:
        i = int(pos * SR)
        n = int(0.18 * SR)
        if i + n < len(z):
            tt = np.arange(n) / SR
            z[i:i + n] += 0.12 * np.sin(2 * math.pi * 900 * tt) * np.exp(-tt * 50)
    z = crossfade_loop(z, 2.0)
    write("workshop_loop.wav", z, 0.35)


def make_static():
    dur = 2.8
    z = smooth_noise(dur, 0.25) * 0.7 + 0.15 * smooth_noise(dur, 0.05)
    z *= np.linspace(0, 1, len(z)) ** 2
    write("radio_static.wav", z, 0.45)


def make_click():
    dur = 0.12
    x = t(dur)
    z = np.sin(2 * math.pi * 1400 * x) * np.exp(-x * 70) * 0.4
    z += np.sin(2 * math.pi * 700 * x) * np.exp(-x * 50) * 0.2
    write("click.wav", z, 0.4)


def make_chime():
    dur = 3.0
    x = t(dur)
    z = np.zeros_like(x)
    for f, a in [(523.25, 0.25), (659.25, 0.18), (783.99, 0.12)]:
        z += a * np.sin(2 * math.pi * f * x) * np.exp(-x * 1.6)
    write("chapter.wav", z, 0.45)


def make_theme():
    dur = 32
    x = t(dur)
    z = 0.06 * np.sin(2 * math.pi * 73.42 * x)  # D2 drone
    notes = [146.83, 174.61, 196.00, 220.00, 261.63, 220.00, 196.00, 174.61]
    for i, f in enumerate(notes):
        start = i * 4.0
        n = int(4.0 * SR)
        i0 = int(start * SR)
        if i0 + n > len(z):
            n = len(z) - i0
        tt = np.arange(n) / SR
        e = np.minimum(1, tt / 0.6) * np.exp(-tt * 0.7)
        z[i0:i0 + n] += 0.14 * (np.sin(2 * math.pi * f * tt) + 0.3 * np.sin(2 * math.pi * f * 2 * tt)) * e
    # slow swell
    z *= 0.75 + 0.25 * np.sin(2 * math.pi * 0.03 * x)
    z *= env_ad(len(z), 2.0, 4.0)
    write("theme.wav", z, 0.45)


if __name__ == "__main__":
    np.random.seed(5)
    make_wind()
    make_room()
    make_train()
    make_city()
    make_workshop()
    make_static()
    make_click()
    make_chime()
    make_theme()
