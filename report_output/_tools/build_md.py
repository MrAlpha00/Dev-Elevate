# -*- coding: utf-8 -*-
"""Render the same structured content as ElevoraAI_Final_Report.md.

The Markdown file mirrors the DOCX one-to-one and links the figures and
screenshots that live in report_output/figures and report_output/shots.
"""
import io
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
    out = []
    chapter_no = [0]
    table_no = [0]
    fig_no = [0]
    toc = []
    figs = []
    tbls = []

    def para(text):
        out.append(text)
        out.append("")

    def h1(num, title):
        if num == "ABSTRACT":
            out.append("# ABSTRACT")
            out.append("")
            toc.append(("chapter", "ABSTRACT", "ABSTRACT"))
            return
        if num in ("CONCLUSION", "REFERENCES"):
            out.append("# %s" % num)
            out.append("")
            toc.append(("chapter", num, num))
            return
        chapter_no[0] = int(re.search(r"(\d+)", num).group(1))
        table_no[0] = 0
        fig_no[0] = 0
        out.append("# CHAPTER %s" % re.sub(r"\s*[–\-]\s*", " - ", num))
        out.append("")
        out.append("## %s" % title)
        out.append("")
        toc.append(("chapter", num, title))

    def h2(num, title):
        out.append("### %s  %s" % (num, title))
        out.append("")
        toc.append(("section", num, title))

    def table(caption, headers, rows):
        number = "%d.%d" % (chapter_no[0], table_no[0])
        table_no[0] += 1
        out.append("**Table %s: %s**" % (number, caption.split(":", 1)[-1].strip()))
        out.append("")
        out.append("| " + " | ".join(esc(h) for h in headers) + " |")
        out.append("|" + "|".join([" --- "] * len(headers)) + "|")
        for r in rows:
            out.append("| " + " | ".join(esc(c) for c in r) + " |")
        out.append("")
        tbls.append((number, caption))

    def figure(rel_path, caption, width):
        number = "%d.%d" % (chapter_no[0], fig_no[0])
        fig_no[0] += 1
        out.append("![%s](%s)" % (clean_caption(caption), rel_path.replace("\\", "/")))
        out.append("")
        out.append("*Fig. %s: %s*" % (number, caption.split(":", 1)[-1].strip()))
        out.append("")
        figs.append((number, caption))

    def code(source, text):
        out.append("```")
        out.append(text)
        out.append("```")
        out.append("")
        out.append("*Extract: %s*" % source)
        out.append("")

    def ref(num, author, title, extra):
        line = "**%s** %s %s" % (num, author, title)
        if extra:
            line += " " + extra
        out.append(line)
        out.append("")

    def render(blocks):
        for blk in blocks:
            kind = blk[0]
            if kind == "h1":
                h1(blk[1], blk[2] if len(blk) > 2 else blk[1])
            elif kind == "h2":
                h2(blk[1], blk[2])
            elif kind == "p":
                para(blk[1])
            elif kind == "b":
                out.append("- %s" % blk[1])
                out.append("")
            elif kind == "n":
                out.append("%s. %s" % (blk[2] if len(blk) > 2 else "", blk[1]))
                out.append("")
            elif kind == "table":
                table(blk[1], blk[2], blk[3])
            elif kind == "fig":
                figure(blk[1], blk[2], blk[3])
            elif kind == "code":
                code(blk[1], blk[2])
            elif kind == "ref":
                ref(blk[1], blk[2], blk[3], blk[4] if len(blk) > 4 else "")

    render(c1.FRONT)

    # ---------------- table of contents (generated, with real page numbers)
    import json
    try:
        with open(os.path.join(TOOLS_DIR, "pagemap.json"), encoding="utf-8") as fh:
            pagemap = json.load(fh)
    except Exception:
        pagemap = {}

    out.append("# TABLE OF CONTENTS")
    out.append("")
    out.append("| SL. NO | NAME | PAGE NO |")
    out.append("|---|---|---|")
    sl = 0
    for kind, key, label in toc:
        page = pagemap.get(key, "")
        if kind == "chapter":
            sl += 1
            out.append("| %d | %s | %s |" % (sl, label, page))
        else:
            out.append("| | %s   %s | %s |" % (key, label, page))
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

    chapter_no[0] = 1
    render(c1.CH1)
    chapter_no[0] = 2
    render(c1.CH2)
    chapter_no[0] = 3
    render(c2.CH3)
    chapter_no[0] = 4
    render(c2.CH4)
    chapter_no[0] = 5
    render(c3.CH5)
    chapter_no[0] = 6
    render(c3.CH6)
    render(c3.CONCLUSION)
    render(c3.REFERENCES)

    with io.open(MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out).rstrip() + "\n")
    print("saved", MD)
    print("toc", len(toc), "figures", len(figs), "tables", len(tbls))


if __name__ == "__main__":
    main()
