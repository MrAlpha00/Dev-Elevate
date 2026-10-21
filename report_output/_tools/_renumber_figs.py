# -*- coding: utf-8 -*-
"""Renumber the Chapter 4 figures so that they ascend in document order.

In the source the module map was numbered 4.8 but placed directly after
Fig. 4.1.  The numbers, the captions and every in-text cross reference are
remapped together so that the text and the figure list stay consistent.
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

FILES = ["content_part1.py", "content_part2.py", "content_part3.py"]
BASE = os.path.dirname(os.path.abspath(__file__))

# old figure number -> new figure number (document order in chapter 4)
REMAP = {
    "4.1": "4.1",
    "4.8": "4.2",
    "4.2": "4.3",
    "4.3": "4.4",
    "4.4": "4.5",
    "4.5": "4.6",
    "4.6": "4.7",
    "4.7": "4.8",
}

TOKEN = "@@F%s@@"

changed = 0
for name in FILES:
    path = os.path.join(BASE, name)
    src = open(path, encoding="utf-8").read()
    orig = src
    # phase 1 - protect the old numbers with unique tokens
    for old in REMAP:
        for prefix in ("Figure ", "Fig. "):
            src = src.replace(prefix + old, prefix + TOKEN % old.replace(".", "_"))
    # phase 2 - restore them with the new numbers
    for old, new in REMAP.items():
        src = src.replace(TOKEN % old.replace(".", "_"), new)
    if src != orig:
        open(path, "w", encoding="utf-8").write(src)
        changed += 1
        print("patched", name)
print("files changed:", changed)
