# -*- coding: utf-8 -*-
"""Iterate build -> PDF -> page-resolution until the contents page numbers
reach a fixed point (the printed numbers no longer move pagination)."""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.dirname(TOOLS)
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
PAGEMAP = os.path.join(TOOLS, "pagemap.json")
DOCX = os.path.join(REPORT, "ElevoraAI_Final_Report.docx")
PDF = os.path.join(REPORT, "ElevoraAI_Final_Report.pdf")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        raise SystemExit("command failed: %s" % (args,))
    return r.stdout


def digest():
    if not os.path.exists(PAGEMAP):
        return None
    with open(PAGEMAP, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def convert():
    run([SOFFICE, "--headless", "--norestore", "--convert-to", "pdf",
         "--outdir", REPORT, DOCX])


prev = None
for i in range(1, 5):
    run([sys.executable, os.path.join(TOOLS, "build_report.py")])
    convert()
    out = run([sys.executable, os.path.join(TOOLS, "resolve_pages.py")])
    for line in out.splitlines():
        if line.startswith(("pdf pages", "body starts", "resolved", "  MISSING")):
            print("  ", line)
    cur = digest()
    print("iteration %d pagemap %s" % (i, (cur or "")[:12]))
    if cur == prev:
        print("stable after %d iterations" % i)
        break
    prev = cur
else:
    print("WARNING: page map did not stabilise")
