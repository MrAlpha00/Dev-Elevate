# -*- coding: utf-8 -*-
"""Render the same structured content as ElevoraAI_Final_Report.md.

The Markdown file mirrors the DOCX one-to-one and links the figures and
screenshots that live in report_output/figures and report_output/shots.
A two-pass render is used so that the table of contents, the figure list and
the table list can be emitted before the body while still carrying the real
page numbers resolved from the PDF.
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_part1 as c1
import content_part2 as c2
import content_part3 as c3

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.dirname(TOOLS_DIR)
MD = os.path.join(REPORT_DIR, "ElevoraAI_Final_Report.md")


def clean_caption(cap):
    s = re.sub(r"^\s*(Fig\.|Figure|Table)\s*[\d.]+\s*[:.\-]?\s*", "", cap)
    return s.strip().rstrip(".")


def esc(text):
    return str(text).replace("|", "\\|")


def main():
    with open(os.path.join(TOOLS_DIR, "pagemap.json"), encoding="utf-8") as fh:
        pagemap = json.load(fh)

    body = []
    front = []
    toc = []
    figs = []
    tbls = []
    chapter_no = [0]
    table_no = [0]
    fig_no = [0]

    def plain(text):
        body.append(text)
        body.append("")

    def h1(num, title):
        if num == "ABSTRACT":
            body.append("# ABSTRACT")
            body.append("")
            return
        if num in ("CONCLUSION", "REFERENCES"):
            body.append("# %s" % num)
            body.append("")
            toc.append(("chapter", num, num))
            return
        chapter_no[0] = int(re.search(r"(\d+)", num).group(1))
        table_no[0] = 0
        fig_no[0] = 0
        body.append("# %s" % num.replace("\u2014", "\u2013"))
        body.append("")
        if title:
            body.append("## %s" % title)
            body.append("")
        toc.append(("chapter", num, title or num))

    def h2(num, title):
        body.append("### %s   %s" % (num, title))
        body.append("")
        toc.append(("section", num, title))

    def table(caption, headers, rows):
        table_no[0] += 1
        number = "%d.%d" % (chapter_no[0], table_no[0])
        body.append("**Table %s: %s**" % (number, caption.split(":", 1)[-1].strip()))
        body.append("")
        body.append("| " + " | ".join(esc(h) for h in headers) + " |")
        body.append("|" + "|".join([" --- "] * len(headers)) + "|")
        for r in rows:
            body.append("| " + " | ".join(esc(c) for c in r) + " |")
        body.append("")
        tbls.append((number, caption))

    def figure(rel_path, caption, width):
        fig_no[0] += 1
        number = "%d.%d" % (chapter_no[0], fig_no[0])
        body.append("![%s](%s)" % (clean_caption(caption), rel_path.replace("\\", "/")))
        body.append("")
        body.append("*Fig. %s: %s*" % (number, caption.split(":", 1)[-1].strip()))
        body.append("")
        figs.append((number, caption))

    def code(source, text):
        body.append("```")
        body.append(text)
        body.append("```")
        body.append("")
        body.append("*Extract: %s*" % source)
        body.append("")

    def ref(num, author, title, extra):
        author = author.strip()
        if not author.endswith("."):
            author += "."
        line = '**%s** *%s* "%s"' % (num, author, title.strip())
        if extra:
            line += ", " + extra.strip()
        body.append(line)
        body.append("")

    def render(blocks, target):
        nonlocal body
        saved = body
        body = target
        for blk in blocks:
            kind = blk[0]
            if kind == "h1":
                h1(blk[1], blk[2] if len(blk) > 2 else blk[1])
            elif kind == "h2":
                h2(blk[1], blk[2])
            elif kind == "p":
                plain(blk[1])
            elif kind == "b":
                body.append("- %s" % blk[1])
                body.append("")
            elif kind == "n":
                body.append("%s. %s" % (blk[2] if len(blk) > 2 else "", blk[1]))
                body.append("")
            elif kind == "table":
                table(blk[1], blk[2], blk[3])
            elif kind == "fig":
                figure(blk[1], blk[2], blk[3])
            elif kind == "code":
                code(blk[1], blk[2])
            elif kind == "ref":
                ref(blk[1], blk[2], blk[3], blk[4] if len(blk) > 4 else "")
        body = saved

    # pass 1: front matter and body, collecting the three indexes
    render(c1.FRONT, front)
    for module, chapter in ((c1.CH1, 1), (c1.CH2, 2), (c2.CH3, 3), (c2.CH4, 4),
                            (c3.CH5, 5), (c3.CH6, 6)):
        chapter_no[0] = chapter
        render(module, body)
    render(c3.CONCLUSION, body)
    render(c3.REFERENCES, body)

    out = list(front)

    out.append("# TABLE OF CONTENTS")
    out.append("")
    out.append("| SL. NO | NAME | PAGE NO |")
    out.append("|---|---|---|")
    sl = 0
    for kind, key, label in toc:
        if kind == "chapter":
            sl += 1
            out.append("| %d | %s | %s |" % (sl, label, pagemap.get(key, "")))
        else:
            out.append("| | %s   %s | %s |" % (key, label, pagemap.get(key, "")))
    out.append("")

    out.append("# FIGURE OF CONTENT")
    out.append("")
    out.append("| FIG NO | NAME | PAGE NO |")
    out.append("|---|---|---|")
    for num, cap in figs:
        out.append("| %s | %s | %s |" % (num, clean_caption(cap), pagemap.get("FIG:" + num, "")))
    out.append("")

    out.append("# LIST OF TABLES")
    out.append("")
    out.append("| TABLE NO | NAME | PAGE NO |")
    out.append("|---|---|---|")
    for num, cap in tbls:
        out.append("| %s | %s | %s |" % (num, clean_caption(cap), pagemap.get("TBL:" + num, "")))
    out.append("")

    out.append("---")
    out.append("")
    out.extend(body)

    with io.open(MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out).rstrip() + "\n")
    print("saved", MD)
    print("toc", len(toc), "figures", len(figs), "tables", len(tbls))


if __name__ == "__main__":
    main()
