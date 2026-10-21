# -*- coding: utf-8 -*-
"""Prepare the genuine screenshot assets used in the report.

Sources
  1. The deployed application (https://elevoraai.vercel.app) rendered with
     headless Chrome -> PDF -> PNG (public routes only, no credentials).
  2. The repository screen-recording ElevoraAI/login-flow.gif -> PNG frames.
Every frame is checked for actual content (pixel statistics) before use.
"""
import io
import json
import os
import sys
import subprocess
import pymupdf
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHOTS = os.path.join(ROOT, "report_output", "shots")
FIGS = os.path.join(ROOT, "report_output", "figures")
os.makedirs(SHOTS, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "https://elevoraai.vercel.app"

PUBLIC = [
    ("landing", "/"),
    ("apidocs", "/api-docs"),
    ("documentation", "/documentation"),
    ("creator", "/about-creator"),
    ("contributors", "/contributor-guide"),
]


def pdf(url, out):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    "--user-data-dir=%s\\cp_pdf" % os.environ.get("TEMP", "."),
                    "--virtual-time-budget=22000", "--print-to-pdf=%s" % out, url],
                   capture_output=True, timeout=180)
    return os.path.exists(out)


def pdf_to_png(pdf_path, png_path, page=0, dpi=150):
    d = pymupdf.open(pdf_path)
    pix = d[page].get_pixmap(dpi=dpi)
    pix.save(png_path)
    txt = d[page].get_text()
    d.close()
    return txt


def gif_frames():
    gif = os.path.join(ROOT, "ElevoraAI", "login-flow.gif")
    im = Image.open(gif)
    n = getattr(im, "n_frames", 1)
    picks = [int(n * f) for f in (0.15, 0.45, 0.75, 0.95)]
    picked = []
    for i in picks:
        im.seek(i)
        fr = im.convert("RGB")
        stat = frame_stats(fr)
        if stat["std"] < 18 or stat["colors"] < 60:
            continue
        out = os.path.join(SHOTS, "loginflow_%03d.png" % i)
        fr.save(out)
        picked.append({"index": i, "path": out, **stat})
    return picked


def frame_stats(fr):
    small = fr.resize((160, 100))
    px = list(small.getdata())
    lum = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in px]
    mean = sum(lum) / len(lum)
    var = sum((l - mean) ** 2 for l in lum) / len(lum)
    colors = len(set(px))
    return {"mean": round(mean, 1), "std": round(var ** 0.5, 1), "colors": colors}


def main():
    report = {}
    for name, path in PUBLIC:
        pdf_path = os.path.join(SHOTS, "pub_%s.pdf" % name)
        if pdf(BASE + path, pdf_path):
            txt = pdf_to_png(pdf_path, os.path.join(SHOTS, "pub_%s.png" % name), 0, 150)
            report[name] = {"pdf": pdf_path, "chars": len(txt), "head": txt[:300]}
            print("captured", name, len(txt), "chars of text")
    picks = gif_frames()
    print("gif frames kept:", json.dumps(picks, indent=1))
    with open(os.path.join(SHOTS, "asset_report.json"), "w", encoding="utf-8") as fh:
        json.dump({"public": report, "gif": picks}, fh, indent=1)


if __name__ == "__main__":
    main()
