# -*- coding: utf-8 -*-
"""Resolve the real page number of every contents / figure / table entry.

Reads the PDF that Word produced, finds the page on which each heading,
figure caption and table caption appears, and writes pagemap.json so the
next DOCX build can print the true page numbers.
"""
import io
import json
import os
import re
import sys

import fitz  # PyMuPDF

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.dirname(TOOLS_DIR)
PDF = os.path.join(REPORT_DIR, "ElevoraAI_Final_Report.pdf")
PAGEMAP = os.path.join(TOOLS_DIR, "pagemap.json")
ENTRIES = os.path.join(TOOLS_DIR, "toc_entries.json")


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def footer_number(page):
    """The printed page number lives in the footer band, right aligned."""
    h = page.rect.height
    best = None
    for w in page.get_text("words"):
        x0, y0, x1, y1, word = w[0], w[1], w[2], w[3], w[4]
        if y1 < h - 55:
            continue
        if not re.fullmatch(r"[ivxlcdm]+|\d+", word.strip(), re.I):
            continue
        if best is None or x0 > best[0]:
            best = (x0, word.strip())
    return best[1] if best else None


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    doc = fitz.open(PDF)
    pages = []
    for i, page in enumerate(doc):
        txt = page.get_text("text")
        pages.append({
            "index": i,
            "text": txt,
            "norm": norm(txt),
            "label": footer_number(page),
        })
    total = len(pages)
    print("pdf pages:", total)

    # ---- locate the first body page (Arabic numbering starts there) -----
    body_start = None
    for p in pages:
        if re.search(r"CHAPTER\s*[–\-—]\s*1\b", p["text"]):
            body_start = p["index"]
            break
    if body_start is None:
        print("ERROR: could not find the start of Chapter 1")
        return 1
    print("body starts at physical page", body_start + 1)
    body = pages[body_start:]

    def label_of(p):
        if p["label"]:
            return p["label"]
        return str(p["index"] - body_start + 1)

    pagemap = {}

    def find_first(needle, restrict=None):
        n = norm(needle)
        for p in body:
            if restrict and not restrict(p):
                continue
            if n and n in p["norm"]:
                return p
        return None

    # ---- chapters -------------------------------------------------------
    with open(ENTRIES, encoding="utf-8") as fh:
        entries = json.load(fh)

    for e in entries["toc"]:
        key, kind, label = e["key"], e["kind"], e["label"]
        if kind == "chapter":
            if key.startswith("CHAPTER"):
                pat = re.compile(r"CHAPTER\s*[–\-—]\s*\d+")
                hit = None
                for p in body:
                    if pat.search(p["text"]):
                        hit = p
                        break
                if hit:
                    pagemap[key] = label_of(hit)
            else:
                rx = re.compile(r"^\s*%s\s*$" % re.escape(key), re.M)
                hit = None
                for p in body:
                    if rx.search(p["text"]):
                        hit = p
                        break
                if hit:
                    pagemap[key] = label_of(hit)
        else:
            # section heading: "<number>  <title>"
            hit = find_first("%s %s" % (key, label))
            if hit is None:
                hit = find_first("%s %s" % (key, label.replace("’", "'")))
            if hit:
                pagemap[key] = label_of(hit)

    # ---- figures --------------------------------------------------------
    for f in entries["figures"]:
        num = f["number"]
        cap = f["caption"]
        hit = find_first(cap)
        if hit is None:
            hit = find_first(cap.split(":")[0] + ":")
        if hit:
            pagemap["FIG:" + num] = label_of(hit)

    # ---- tables ---------------------------------------------------------
    for t in entries["tables"]:
        num = t["number"]
        cap = t["caption"]
        hit = find_first(cap)
        if hit is None:
            hit = find_first(cap.split(":")[0] + ":")
        if hit:
            pagemap["TBL:" + num] = label_of(hit)

    with open(PAGEMAP, "w", encoding="utf-8") as fh:
        json.dump(pagemap, fh, indent=1, ensure_ascii=False)

    missing = []
    for e in entries["toc"]:
        if e["key"] not in pagemap:
            missing.append(("toc", e["key"], e["label"]))
    for f in entries["figures"]:
        if "FIG:" + f["number"] not in pagemap:
            missing.append(("fig", f["number"], f["caption"]))
    for t in entries["tables"]:
        if "TBL:" + t["number"] not in pagemap:
            missing.append(("tbl", t["number"], t["caption"]))

    print("resolved", len(pagemap), "entries; missing", len(missing))
    for m in missing:
        print("  MISSING", m[0], m[1], m[2][:70])
    return 0


if __name__ == "__main__":
    sys.exit(main())
