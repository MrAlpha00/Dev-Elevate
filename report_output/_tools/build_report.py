# -*- coding: utf-8 -*-
"""Build the Elevora AI final report as an editable .docx.

Typography follows the reference report (finalreport.pdf):
  A4 portrait, 1 inch margins, Times New Roman 12 pt justified body,
  1.5 line spacing, 0.5 inch first-line indent, centred bold 18 pt chapter
  titles, 14 pt section headings, bordered tables and centred figure captions.
"""
import io
import os
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_part1 as c1
import content_part2 as c2
import content_part3 as c3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(ROOT, "report_output")
DOCX = os.path.join(REPORT_DIR, "ElevoraAI_Final_Report.docx")

SERIF = "Times New Roman"
MONO = "Consolas"

# ----------------------------------------------------------------- helpers
TOC_ENTRIES = []   # (kind, key, label)
FIG_ENTRIES = []   # (number, caption)
TBL_ENTRIES = []   # (number, caption)


def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def set_table_borders(table, sz=6):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tblPr.append(borders)


def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trPr.append(el)


def cell_margins(table, top=60, bottom=60, left=90, right=90):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for name, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement("w:%s" % name)
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def add_field(paragraph, instr, size=11, bold=False):
    run = paragraph.add_run()
    run.font.name = SERIF
    run.font.size = Pt(size)
    run.bold = bold
    fld = OxmlElement("w:fldChar")
    fld.set(qn("w:fldCharType"), "begin")
    run._r.append(fld)
    run2 = paragraph.add_run()
    run2.font.name = SERIF
    run2.font.size = Pt(size)
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    run2._r.append(it)
    run3 = paragraph.add_run()
    run3.font.name = SERIF
    run3.font.size = Pt(size)
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run3._r.append(fld2)


def add_border(paragraph, edge="bottom", sz=12, space=4):
    pPr = paragraph._p.get_or_add_pPr()
    bdr = pPr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        pPr.append(bdr)
    el = OxmlElement("w:%s" % edge)
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), "000000")
    bdr.append(el)


def set_pgnum(section, fmt, start=None):
    sectPr = section._sectPr
    for old in sectPr.findall(qn("w:pgNumType")):
        sectPr.remove(old)
    el = OxmlElement("w:pgNumType")
    el.set(qn("w:fmt"), fmt)
    if start is not None:
        el.set(qn("w:start"), str(start))
    sectPr.append(el)


def style_run(run, size=12, bold=False, italic=False, font=SERIF, caps=False):
    run.font.name = font
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)
    rPr = run._r.get_or_add_rPr()
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rPr.append(rf)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(attr), font)
    if caps:
        c = OxmlElement("w:caps")
        c.set(qn("w:val"), "1")
        rPr.append(c)
    return run


# ----------------------------------------------------------------- document
def build():
    doc = Document()

    # base style
    normal = doc.styles["Normal"]
    normal.font.name = SERIF
    normal.font.size = Pt(12)
    rpr = normal.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(attr), SERIF)
    pf = normal.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing = 1.5
    pf.space_after = Pt(0)
    pf.first_line_indent = Inches(0.5)

    sec = doc.sections[0]
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(0.9)
    sec.header_distance = Inches(0.45)
    sec.footer_distance = Inches(0.45)

    # ---------------- front matter footer (roman numerals, centred)
    footer = sec.footer
    fp = footer.paragraphs[0]
    fp.text = ""
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.paragraph_format.first_line_indent = Inches(0)
    fp.paragraph_format.space_before = Pt(0)
    add_field(fp, " PAGE ", size=10)
    set_pgnum(sec, "lowerRoman", 1)

    # ---------------- styles used by headings
    styles = doc.styles
    ch_style = styles.add_style("ChapterTitle", 1)   # 1 = paragraph style
    ch_style.base_style = styles["Normal"]
    ch_style.font.name = SERIF
    ch_style.font.size = Pt(18)
    ch_style.font.bold = True
    ch_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ch_style.paragraph_format.space_before = Pt(6)
    ch_style.paragraph_format.space_after = Pt(18)
    ch_style.paragraph_format.first_line_indent = Inches(0)
    ch_style.paragraph_format.keep_with_next = True

    sec_style = styles.add_style("SectionHeading", 1)
    sec_style.base_style = styles["Normal"]
    sec_style.font.name = SERIF
    sec_style.font.size = Pt(14)
    sec_style.font.bold = True
    sec_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sec_style.paragraph_format.space_before = Pt(14)
    sec_style.paragraph_format.space_after = Pt(6)
    sec_style.paragraph_format.first_line_indent = Inches(0)
    sec_style.paragraph_format.keep_with_next = True

    cap_style = styles.add_style("FigureCaption", 1)
    cap_style.base_style = styles["Normal"]
    cap_style.font.name = SERIF
    cap_style.font.size = Pt(12)
    cap_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_style.paragraph_format.first_line_indent = Inches(0)
    cap_style.paragraph_format.space_before = Pt(4)
    cap_style.paragraph_format.space_after = Pt(14)
    cap_style.paragraph_format.keep_with_next = False

    def para(text, size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
             first_indent=0.5, space_before=0, space_after=0, line=1.5, font=SERIF,
             keep_with_next=False):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = align
        pf.first_line_indent = Inches(first_indent)
        pf.space_before = Pt(space_before)
        pf.space_after = Pt(space_after)
        pf.line_spacing = line
        pf.keep_with_next = keep_with_next
        if text:
            style_run(p.add_run(text), size=size, bold=bold, italic=italic, font=font)
        return p

    def bullet(text, numbered=False, number=None):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.left_indent = Inches(0.5)
        pf.first_line_indent = Inches(-0.25)
        pf.space_after = Pt(4)
        pf.line_spacing = 1.4
        marker = ("%s. " % number) if numbered else ("•  ")
        style_run(p.add_run(marker), size=12)
        style_run(p.add_run(text), size=12)
        return p

    def chapter(number_text, title_text, key):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        style_run(p.add_run(number_text), size=18, bold=True)
        tp = doc.add_paragraph(style="ChapterTitle")
        style_run(tp.add_run(title_text), size=18, bold=True)
        TOC_ENTRIES.append(("chapter", key, title_text))

    def section(number_text, title_text):
        p = doc.add_paragraph(style="SectionHeading")
        style_run(p.add_run("%s  %s" % (number_text, title_text)), size=14, bold=True)
        TOC_ENTRIES.append(("section", number_text, title_text))
        return p

    def table_block(caption, headers, rows, widths, number):
        cp = doc.add_paragraph()
        cp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.first_line_indent = Inches(0)
        cp.paragraph_format.space_before = Pt(10)
        cp.paragraph_format.space_after = Pt(4)
        cp.paragraph_format.keep_with_next = True
        cp.paragraph_format.line_spacing = 1.0
        style_run(cp.add_run(caption), size=11, bold=True)
        TBL_ENTRIES.append((number, caption))

        t = doc.add_table(rows=1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        set_table_borders(t)
        cell_margins(t)
        hdr = t.rows[0]
        set_repeat_header(hdr)
        for i, h in enumerate(headers):
            c = hdr.cells[i]
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            style_run(p.add_run(h), size=10.5, bold=True)
            set_cell_bg(c, "E8E8E8")
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                c = cells[i]
                c.text = ""
                p = c.paragraphs[0]
                p.paragraph_format.first_line_indent = Inches(0)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.line_spacing = 1.05
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if i else WD_ALIGN_PARAGRAPH.CENTER
                style_run(p.add_run(str(val)), size=10)
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return t

    def figure_block(rel_path, caption, width, number):
        path = os.path.join(REPORT_DIR, rel_path)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(path, width=Inches(width))
        cp = doc.add_paragraph(style="FigureCaption")
        style_run(cp.add_run(caption), size=12)
        FIG_ENTRIES.append((number, caption))

    def code_block(source, text):
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(t, sz=4)
        cell_margins(t, top=80, bottom=80, left=120, right=120)
        c = t.rows[0].cells[0]
        c.text = ""
        set_cell_bg(c, "F4F4F4")
        first = True
        for line in text.split("\n"):
            p = c.paragraphs[0] if first else c.add_paragraph()
            first = False
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            style_run(p.add_run(line), size=9, font=MONO)
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.first_line_indent = Inches(0)
        cap.paragraph_format.space_before = Pt(3)
        cap.paragraph_format.space_after = Pt(12)
        cap.paragraph_format.line_spacing = 1.0
        style_run(cap.add_run("Extract: %s" % source), size=10, italic=True)

    # --------------------------------------------------------- render blocks
    def render(blocks):
        for blk in blocks:
            kind = blk[0]
            if kind == "h1":
                if blk[1] == "ABSTRACT":
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.first_line_indent = Inches(0)
                    p.paragraph_format.space_after = Pt(16)
                    p.paragraph_format.line_spacing = 1.15
                    style_run(p.add_run("ABSTRACT"), size=18, bold=True)
                elif blk[1] == "CONCLUSION":
                    doc.add_page_break()
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.first_line_indent = Inches(0)
                    p.paragraph_format.space_after = Pt(16)
                    p.paragraph_format.line_spacing = 1.15
                    style_run(p.add_run("CONCLUSION"), size=18, bold=True)
                    TOC_ENTRIES.append(("chapter", "CONCLUSION", "CONCLUSION"))
                elif blk[1] == "REFERENCES":
                    doc.add_page_break()
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.first_line_indent = Inches(0)
                    p.paragraph_format.space_after = Pt(16)
                    p.paragraph_format.line_spacing = 1.15
                    style_run(p.add_run("REFERENCES"), size=18, bold=True)
                    TOC_ENTRIES.append(("chapter", "REFERENCES", "REFERENCES"))
                else:
                    doc.add_page_break()
                    chapter(blk[1], blk[2], blk[1])
            elif kind == "h2":
                section(blk[1], blk[2])
            elif kind == "p":
                para(blk[1])
            elif kind == "b":
                bullet(blk[1])
            elif kind == "n":
                bullet(blk[1], numbered=True, number=blk[2] if len(blk) > 2 else "")
            elif kind == "table":
                number = "T%d.%d" % (chapter_no[0], table_no[0])
                table_no[0] += 1
                table_block(blk[1], blk[2], blk[3], blk[4], number)
            elif kind == "fig":
                number = "%s.%d" % (chapter_no[0], fig_no[0])
                fig_no[0] += 1
                figure_block(blk[1], blk[2], blk[3], number)
            elif kind == "code":
                code_block(blk[1], blk[2])
            elif kind == "ref":
                p = doc.add_paragraph()
                pf = p.paragraph_format
                pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                pf.left_indent = Inches(0.4)
                pf.first_line_indent = Inches(-0.4)
                pf.space_after = Pt(6)
                pf.line_spacing = 1.25
                style_run(p.add_run(blk[1] + " "), size=11, bold=True)
                style_run(p.add_run(blk[2] + " "), size=11, italic=True)
                style_run(p.add_run("\"" + blk[3] + "\", "), size=11)
                style_run(p.add_run(blk[4]), size=11)

    # ----------------------------------------------------------- front matter
    chapter_no = [0]
    table_no = [0]
    fig_no = [0]

    render(c1.FRONT)

    # ---- TABLE OF CONTENTS placeholder table
    doc.add_page_break()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.space_after = Pt(14)
    style_run(p.add_run("TABLE OF CONTENTS"), size=18, bold=True)

    # ---------------- end of front matter: insert section break for body
    body_sec = doc.add_section(WD_SECTION.NEW_PAGE)
    body_sec.page_width = Inches(8.27)
    body_sec.page_height = Inches(11.69)
    body_sec.left_margin = Inches(1.0)
    body_sec.right_margin = Inches(1.0)
    body_sec.top_margin = Inches(1.0)
    body_sec.bottom_margin = Inches(0.9)
    body_sec.header_distance = Inches(0.45)
    body_sec.footer_distance = Inches(0.45)
    set_pgnum(body_sec, "decimal", 1)

    body_sec.header.is_linked_to_previous = False
    body_sec.footer.is_linked_to_previous = False

    hp = body_sec.header.paragraphs[0]
    hp.text = ""
    hp.paragraph_format.first_line_indent = Inches(0)
    hp.paragraph_format.space_after = Pt(2)
    hp.paragraph_format.line_spacing = 1.0
    tabs = hp.paragraph_format.tab_stops
    tabs.add_tab_stop(Inches(6.27), WD_TAB_ALIGNMENT.RIGHT)
    style_run(hp.add_run("Elevora AI  -  Dev-Elevate"), size=11)
    style_run(hp.add_run("\t"), size=11)
    add_field(hp, ' STYLEREF "ChapterTitle" \\* MERGEFORMAT ', size=11)
    add_border(hp, "bottom", sz=18, space=3)

    ftr = body_sec.footer.paragraphs[0]
    ftr.text = ""
    ftr.paragraph_format.first_line_indent = Inches(0)
    ftr.paragraph_format.space_before = Pt(2)
    ftr.paragraph_format.line_spacing = 1.0
    tabs = ftr.paragraph_format.tab_stops
    tabs.add_tab_stop(Inches(3.13), WD_TAB_ALIGNMENT.CENTER)
    tabs.add_tab_stop(Inches(6.27), WD_TAB_ALIGNMENT.RIGHT)
    style_run(ftr.add_run("Elevora AI"), size=11)
    style_run(ftr.add_run("\t"), size=11)
    style_run(ftr.add_run("Dev-Elevate"), size=11)
    style_run(ftr.add_run("\t"), size=11)
    add_field(ftr, " PAGE ", size=11)
    add_border(ftr, "top", sz=6, space=3)

    # ----------------------------------------------------------- body
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

    # ------------------------------------------- build contents/figure tables
    build_front_matter_tables(doc)

    doc.save(DOCX)
    print("saved", DOCX)
    print("toc entries", len(TOC_ENTRIES), "figures", len(FIG_ENTRIES),
          "tables", len(TBL_ENTRIES))


# ------------------------------------------------------------------ front matter tables
def build_front_matter_tables(doc):
    """Insert the TOC, list of figures and list of tables in the front matter."""
    body = doc.element.body
    # locate the paragraph that holds the "TABLE OF CONTENTS" heading
    toc_p = None
    for p in doc.paragraphs:
        if p.text.strip() == "TABLE OF CONTENTS":
            toc_p = p
            break
    assert toc_p is not None

    def new_table_after(anchor_el, headers, widths, rows):
        t = doc.add_table(rows=1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        set_table_borders(t)
        cell_margins(t, top=50, bottom=50, left=90, right=90)
        hdr = t.rows[0]
        set_repeat_header(hdr)
        for i, h in enumerate(headers):
            c = hdr.cells[i]
            c.text = ""
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            style_run(p.add_run(h), size=12, bold=True)
            set_cell_bg(c, "E8E8E8")
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                c = cells[i]
                c.text = ""
                p = c.paragraphs[0]
                p.paragraph_format.first_line_indent = Inches(0)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.05
                if i == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    style_run(p.add_run(str(val)), size=11, bold=True)
                elif i == len(headers) - 1:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    style_run(p.add_run(str(val)), size=11)
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    style_run(p.add_run(str(val)), size=11)
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Inches(w)
        anchor_el.addnext(t._tbl)
        return t

    # ---- contents rows
    rows = []
    sl = 0
    for kind, key, label in TOC_ENTRIES:
        if kind == "chapter":
            sl += 1
            rows.append((sl, label, "00"))
        else:
            rows.append(("", label, "00"))
    toc_tbl = new_table_after(toc_p._p, ["SL. NO", "NAME", "PAGE NO"], [0.9, 4.1, 1.27], rows)

    # ---- list of figures
    fig_p = doc.add_paragraph()
    fig_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fig_p.paragraph_format.first_line_indent = Inches(0)
    fig_p.paragraph_format.space_after = Pt(14)
    style_run(fig_p.add_run("FIGURE OF CONTENT"), size=18, bold=True)
    toc_p._p.addnext(fig_p._p)
    # order: contents table, then figure heading, then figure table
    fig_rows = [(num, cap.replace("Fig. ", ""), "00") for num, cap in FIG_ENTRIES]
    fig_tbl = new_table_after(fig_p._p, ["FIG NO", "NAME", "PAGE NO"], [0.9, 4.1, 1.27], fig_rows)

    # ---- list of tables
    tbl_p = doc.add_paragraph()
    tbl_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tbl_p.paragraph_format.first_line_indent = Inches(0)
    tbl_p.paragraph_format.space_after = Pt(14)
    style_run(tbl_p.add_run("LIST OF TABLES"), size=18, bold=True)
    fig_p._p.addnext(tbl_p._p)
    tbl_rows = [(num, cap, "00") for num, cap in TBL_ENTRIES]
    tbl_tbl = new_table_after(tbl_p._p, ["TABLE NO", "NAME", "PAGE NO"], [0.9, 4.1, 1.27], tbl_rows)

    # page breaks: figure heading starts a new page, table heading starts a new page
    for p in (fig_p, tbl_p):
        pb = OxmlElement("w:pageBreakBefore")
        p._p.get_or_add_pPr().append(pb)

    # the body section break must stay after these tables: ensure ordering
    # (contents -> figures -> tables -> body section) by moving the sectPr marker
    return toc_tbl, fig_tbl, tbl_tbl


if __name__ == "__main__":
    build()
