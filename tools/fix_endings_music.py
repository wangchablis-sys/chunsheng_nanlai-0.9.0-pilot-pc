# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc\game\endings.rpy")
text = p.read_text(encoding="utf-8")
cues = {
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
label = None
out = []
for line in text.splitlines(keepends=True):
    m = re.match(r"^label\s+(\w+)", line)
    if m and m.group(1) in cues:
        label = m.group(1)
    if 'play music "audio/m"' in line and label:
        vol = " volume 0.55" if label == "ending_common" else ""
        line = f'    play music "audio/{cues[label]}" fadein 2.0 loop{vol}\n'
        print(label, cues[label])
    out.append(line)
p.write_text("".join(out), encoding="utf-8", newline="")
