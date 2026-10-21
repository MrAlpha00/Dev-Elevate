# -*- coding: utf-8 -*-
"""Render selected PDF pages to PNG and print their text head for inspection."""
import io
import os
import sys

import pymupdf

REPORT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(REPORT_DIR, "ElevoraAI_Final_Report.pdf")
OUT = os.path.join(REPORT_DIR, "_ref", "out")
os.makedirs(OUT, exist_ok=True)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

pages = [int(a) for a in sys.argv[1:]] or [1]
doc = pymupdf.open(PDF)
print("pages:", len(doc))
for pno in pages:
    p = doc[pno - 1]
    pix = p.get_pixmap(dpi=100)
    path = os.path.join(OUT, "page_%03d.png" % pno)
    pix.save(path)
    txt = p.get_text("text").strip().split("\n")
    print("\n=== page %d -> %s (%d lines)" % (pno, path, len(txt)))
    for line in txt[:14]:
        print("   ", line)
