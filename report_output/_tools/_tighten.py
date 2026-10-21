# -*- coding: utf-8 -*-
"""Tighten the typography of the front-matter tables."""
p = "report_output/_tools/build_report.py"
s = open(p, encoding="utf-8").read()

pairs = [
    ("cell_margins(t, top=25, bottom=25, left=90, right=90)",
     "cell_margins(t, top=12, bottom=12, left=90, right=90)"),
    ("            p.paragraph_format.space_before = Pt(1)\n"
     "            p.paragraph_format.space_after = Pt(1)",
     "            p.paragraph_format.space_before = Pt(0.5)\n"
     "            p.paragraph_format.space_after = Pt(0.5)"),
    ("style_run(p.add_run(h), size=11, bold=True)", "style_run(p.add_run(h), size=10, bold=True)"),
    ("style_run(p.add_run(str(val)), size=10.5, bold=True)",
     "style_run(p.add_run(str(val)), size=10, bold=True)"),
    ("style_run(p.add_run(str(val)), size=10.5)", "style_run(p.add_run(str(val)), size=10)"),
]
for old, new in pairs:
    if old in s:
        s = s.replace(old, new)
    else:
        print("NOT FOUND:", old[:60])
open(p, "w", encoding="utf-8").write(s)
print("done")
