# -*- coding: utf-8 -*-
import re
from pathlib import Path

GAME = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc\game")
PAT = re.compile(r'play music "audio/(?!fuguang\.ogg|mus_c1_a\.wav)[^"]+"')

for name in ("script.rpy", "endings.rpy"):
    path = GAME / name
    text = path.read_text(encoding="utf-8")
    new, n = PAT.subn('play music "audio/mus_c1_a.wav"', text)
    path.write_text(new, encoding="utf-8", newline="")
    print(name, n)
