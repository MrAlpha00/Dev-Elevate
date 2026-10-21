# -*- coding: utf-8 -*-
"""Dump the built DOCX as plain text for proofreading."""
import io
import os
import sys

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

REPORT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(REPORT_DIR, "ElevoraAI_Final_Report.docx")
OUT = os.path.join(REPORT_DIR, "_tools", "docx_text.txt")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

doc = Document(DOCX)
lines = []
for child in doc.element.body:
    tag = child.tag.split("}")[-1]
    if tag == "p":
        p = Paragraph(child, doc)
        lines.append(p.text)
    elif tag == "tbl":
        t = Table(child, doc)
        lines.append("[TABLE %dx%d]" % (len(t.rows), len(t.columns)))
        for r in t.rows:
            lines.append("   | " + " | ".join(c.text.replace("\n", " ") for c in r.cells))

with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines))
print("wrote", OUT, len(lines), "blocks")
