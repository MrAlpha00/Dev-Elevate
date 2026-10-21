# -*- coding: utf-8 -*-
"""Automated layout QA over the produced PDF."""
import io
import os
import re
import sys

import pymupdf

REPORT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(REPORT, "ElevoraAI_Final_Report.pdf")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

doc = pymupdf.open(PDF)
PW, PH = doc[0].rect.width, doc[0].rect.height
LEFT, RIGHT = 72.0, PW - 72.0
TOP, BOTTOM = 72.0, PH - 64.8

print("page size: %.1f x %.1f pt" % (PW, PH))
print("text box: %.1f..%.1f  %.1f..%.1f" % (LEFT, RIGHT, TOP, BOTTOM))

problems = []
blank = []
no_number = []
overflow = []
stranded = []
images_out = []
caption_split = []

heading_rx = re.compile(r"^(\d+\.\d+\s|CHAPTER\s*[–-]\s*\d|ABSTRACT$|CONCLUSION$|REFERENCES$|TABLE OF CONTENTS$|FIGURE OF CONTENT$|LIST OF TABLES$)")

for i, page in enumerate(doc):
    pno = i + 1
    text = page.get_text("text")
    lines = [l for l in text.split("\n") if l.strip()]
    if len(lines) <= 2:
        blank.append(pno)

    # footer page number
    words = page.get_text("words")
    footer = [w for w in words if w[3] > PH - 60]
    if not any(re.fullmatch(r"[ivxlcdm]+|\d+", w[4].strip(), re.I) for w in footer):
        no_number.append(pno)

    # horizontal overflow of text
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b["lines"]:
            x0, y0, x1, y1 = l["bbox"]
            if x1 > RIGHT + 2.5 or x0 < LEFT - 2.5:
                overflow.append((pno, round(x0, 1), round(x1, 1),
                                 "".join(s["text"] for s in l["spans"])[:60]))

    # images outside the text box
    for img in page.get_images(full=True):
        for r in page.get_image_rects(img[0]):
            if r.x0 < LEFT - 3 or r.x1 > RIGHT + 3:
                images_out.append((pno, round(r.x0, 1), round(r.x1, 1)))

    # stranded heading: last body line looks like a heading
    body_lines = [l for l in lines if not re.fullmatch(r"[ivxlcdm]+|\d+", l.strip(), re.I)]
    # drop header/footer lines
    body_lines = [l for l in body_lines if l.strip() not in
                  ("Elevora AI  -  Dev-Elevate", "Elevora AI", "Dev-Elevate")]
    if body_lines and heading_rx.match(body_lines[-1].strip()) and pno < len(doc):
        stranded.append((pno, body_lines[-1][:60]))

# figure caption / image co-location
cap_pages = {}
for i, page in enumerate(doc):
    for m in re.finditer(r"Fig\.\s*(\d+\.\d+):", page.get_text("text")):
        cap_pages.setdefault(m.group(1), []).append(i + 1)
for num, pages in sorted(cap_pages.items()):
    if len(pages) > 1:
        print("caption %s appears on pages %s" % (num, pages))

print("\nblank / near-empty pages:", blank)
print("pages without a page number:", no_number)
print("lines outside the text box:", len(overflow))
for o in overflow[:12]:
    print("   p%-3d x0=%-6s x1=%-6s %r" % o)
print("images outside the text box:", len(images_out), images_out[:6])
print("possible stranded headings:", stranded)

print("\ncaption pages:")
for num, pages in sorted(cap_pages.items(), key=lambda kv: [int(x) for x in kv[0].split(".")]):
    print("   Fig %-4s page %s" % (num, pages))
