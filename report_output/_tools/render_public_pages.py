# -*- coding: utf-8 -*-
"""Render the captured public pages (PDF) into PNG figures and record their text."""
import io
import json
import os
import sys
import pymupdf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHOTS = os.path.join(ROOT, "report_output", "shots")
FIGS = os.path.join(ROOT, "report_output", "figures")

JOBS = [
    ("live_landing.pdf", "fig5_2_landing.png", 0),
    ("live_apidocs.pdf", "fig5_3_api_docs.png", 0),
    ("pub_1.pdf", "fig5_4_documentation.png", 0),
    ("pub_3.pdf", "fig5_5_contributor_guide.png", 0),
]

info = {}
for src, dst, page in JOBS:
    p = os.path.join(SHOTS, src)
    if not os.path.exists(p):
        print("missing", src)
        continue
    d = pymupdf.open(p)
    pix = d[page].get_pixmap(dpi=140)
    out = os.path.join(FIGS, dst)
    pix.save(out)
    txt = d[page].get_text()
    info[dst] = {"source": src, "pages": d.page_count, "chars": len(txt),
                 "text": txt[:1200]}
    print(dst, "<-", src, "pages", d.page_count, "chars", len(txt))
    d.close()

with open(os.path.join(SHOTS, "figure_text.json"), "w", encoding="utf-8") as fh:
    json.dump(info, fh, indent=1, ensure_ascii=False)
