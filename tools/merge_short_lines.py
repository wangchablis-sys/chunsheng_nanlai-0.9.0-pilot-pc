# -*- coding: utf-8 -*-
"""Join short consecutive lines, then mark in-chapter beats."""
from __future__ import annotations

import re
from pathlib import Path

PATH = Path(r"C:\Users\Wyf\OneDrive\Desktop\本科课程\课程安排\大二上\毛概\chunsheng_nanlai-0.9.0-pilot-pc\game\script.rpy")
SAY = re.compile(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*) "(.*)"\s*$')
MAX_LEN = 68
MAX_PARTS = 3

# substring -> beat id. Menu captions mark the menu above them.
BEATS = [
    ("十二岁的孙红卫缩在堂屋门后", "seal", "line"),
    ("第二年秋收", "harvest", "line"),
    ("回去，叫一声爹", "father", "menu"),
    ("1984年，十八岁的孙红卫", "train", "line"),
    ("苏文静笑了", "circuit", "line"),
    ("label wu_menu:", "wu", "after"),
    ("张长喜留的地址", "eaves", "line"),
    ("接过工具。", "tools", "menu"),
    ("继续修，修到响为止", "radio", "menu"),
    ("陈海生嗅出了商机", "gold", "line"),
    ("追进去，解释清楚", "invoice", "menu"),
    ("label watch_menu:", "watch", "after"),
    ("倒卖的利润越来越薄", "workshop", "line"),
    ("偷偷接电", "power", "menu"),
    ("执行编号质检", "qc", "menu"),
    ("订单越接越多", "orders", "line"),
    ("先抽检，再装机", "caps", "menu"),
    ("隐瞒出货", "accident", "menu"),
    ("回凤阳，先给父亲治腿", "leg", "menu"),
    ("红卫靠着维修摊慢慢还债", "stall", "line"),
    ("推掉债主会面", "tour", "menu"),
    ("# speech-hold-begin", "speech", "after"),
    ("南巡的讲话，没有立刻送来订单", "restart", "line"),
    ("先做十台", "ten", "menu"),
    ("全部接受苏文静的三个条件", "su", "menu"),
    ("如实还款", "debt", "menu"),
    ("回凤阳，把根扎回乡土", "home", "menu"),
]


def is_glue(line: str) -> bool:
    return line.strip().endswith("# auto-bg")


def is_quote(text: str) -> bool:
    return text.startswith("“") or "改革开放" in text or "大胆地闯" in text or "硬道理" in text


def sentences(text: str) -> int:
    return sum(text.count(ch) for ch in "。！？")


def merge_run(items: list[tuple]) -> list[str]:
    """items: ('say', indent, who, text) or ('keep', line)."""
    out: list[str] = []
    buf: list[tuple[str, str, str]] = []
    glue_before: list[str] = []

    def flush():
        nonlocal buf
        if not buf:
            return
        indent, who, text = buf[0]
        parts = 1
        acc = text
        for ind, w, t in buf[1:]:
            if w == who and not is_quote(acc) and not is_quote(t) and parts < MAX_PARTS and len(acc) + len(t) <= MAX_LEN and (len(acc) <= 26 or len(t) <= 18):
                acc += t
                parts += 1
            else:
                out.append(f'{indent}{who} "{acc}"')
                indent, who, acc = ind, w, t
                parts = 1
        out.append(f'{indent}{who} "{acc}"')
        buf = []

    for kind, *rest in items:
        if kind == "keep":
            flush()
            out.append(rest[0])
        else:
            buf.append(tuple(rest))
    flush()
    return out


def transform(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    i = 0
    merged = 0
    n = len(lines)
    while i < n:
        if SAY.match(lines[i]):
            block = []
            say_count = 0
            while i < n:
                m = SAY.match(lines[i])
                if m:
                    block.append(("say", m.group(1), m.group(2), m.group(3)))
                    say_count += 1
                    i += 1
                    continue
                if not lines[i].strip() or is_glue(lines[i]):
                    # peek: more says ahead before a hard line?
                    j = i
                    while j < n and (not lines[j].strip() or is_glue(lines[j])):
                        j += 1
                    if j < n and SAY.match(lines[j]):
                        while i < j:
                            if is_glue(lines[i]):
                                block.append(("keep", lines[i]))
                            i += 1
                        continue
                break
            before = say_count
            piece = merge_run(block)
            after = sum(1 for line in piece if SAY.match(line))
            merged += before - after
            # Drop auto-bg glue that sat between lines we joined:
            # merge_run kept glue as 'keep' only if we stored it. We stored glue as keep,
            # so joins still have scenes between them. Remove glue sandwiched by two says
            # of the same speaker that are both short enough that they SHOULD have joined
            # — actually merge_run doesn't join across keep. Fix: don't put glue in the
            # block at all when the surrounding says can merge.
            out.extend(piece)
            continue
        out.append(lines[i])
        i += 1
    return out, merged


def transform2(lines: list[str]) -> tuple[list[str], int]:
    """Merge says separated only by blank lines and auto-bg glue."""
    out: list[str] = []
    i = 0
    n = len(lines)
    merged = 0
    while i < n:
        if not SAY.match(lines[i]):
            out.append(lines[i])
            i += 1
            continue
        group: list[tuple[str, str, str]] = []
        glue_slots: list[list[str]] = [[]]
        while i < n:
            m = SAY.match(lines[i])
            if m:
                group.append((m.group(1), m.group(2), m.group(3)))
                glue_slots.append([])
                i += 1
                continue
            j = i
            gap: list[str] = []
            while j < n and (not lines[j].strip() or is_glue(lines[j])):
                if lines[j].strip():
                    gap.append(lines[j])
                j += 1
            if j < n and SAY.match(lines[j]) and gap and all(is_glue(g) for g in gap):
                glue_slots[-1] = gap
                i = j
                continue
            break
        # fold
        folded: list[tuple[str, str, str, list[str]]] = []
        for idx, (indent, who, text) in enumerate(group):
            gap = glue_slots[idx]
            if folded:
                pind, pwho, ptext, pgap = folded[-1]
                if (
                    who == pwho
                    and not is_quote(ptext)
                    and not is_quote(text)
                    and sentences(ptext) < MAX_PARTS
                    and len(ptext) + len(text) <= MAX_LEN
                    and (len(ptext) <= 26 or len(text) <= 18)
                ):
                    folded[-1] = (pind, pwho, ptext + text, pgap)
                    merged += 1
                    continue
            folded.append((indent, who, text, gap))
        for indent, who, text, gap in folded:
            out.extend(gap)
            out.append(f'{indent}{who} "{text}"')
        # trailing gap after last say stays unconsumed (i points at hard line)
    return out, merged


def insert_beats(lines: list[str]) -> int:
    used = set()
    added = 0
    for needle, bid, kind in BEATS:
        idx = next((i for i, line in enumerate(lines) if needle in line), None)
        if idx is None:
            print("missing anchor", bid, needle)
            continue
        if kind == "after":
            idx += 1
        elif kind == "menu":
            indent = len(lines[idx]) - len(lines[idx].lstrip(" "))
            j = idx
            while j > 0:
                j -= 1
                raw = lines[j]
                if not raw.strip():
                    continue
                ind = len(raw) - len(raw.lstrip(" "))
                if raw.strip().startswith("menu:") and ind < indent:
                    idx = j
                    break
        if any(f'mark_beat("{bid}")' in lines[k] for k in range(max(0, idx - 2), idx + 1)):
            continue
        pad = lines[idx][: len(lines[idx]) - len(lines[idx].lstrip(" "))]
        lines.insert(idx, f'{pad}$ mark_beat("{bid}")')
        used.add(bid)
        added += 1
    return added


def main():
    text = PATH.read_text(encoding="utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines()
    lines, merged = transform2(lines)
    added = insert_beats(lines)
    PATH.write_text(nl.join(lines) + nl, encoding="utf-8", newline="")
    print("merged", merged, "beats", added, "lines", len(lines))


if __name__ == "__main__":
    main()
