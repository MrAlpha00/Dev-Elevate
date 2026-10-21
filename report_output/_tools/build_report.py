from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from pathlib import Path
import os, sys

FIG_DIR = Path('report_output/figures')
ASSET_DIR = Path('report_output/assets')
ASSET_DIR.mkdir(parents=True, exist_ok=True)

def set_document_props(doc):
    doc.core_properties.title = 'ElevoraAI - Final Project Report'
    doc.core_properties.author = 'ElevoraAI Project'
    doc.core_properties.subject = 'Full-Stack AI-Powered Learning Platform'

def configure_styles(doc):
    # Set default
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    para = style.paragraph_format
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.line_spacing = 1.5
    para.space_after = Pt(6)
    para.first_line_indent = Inches(0.5)

    # Title style
    if 'Title' not in [s.name for s in doc.styles]:
        title_style = doc.styles.add_style('ReportTitle', WD_STYLE_TYPE.PARAGRAPH)
    else:
        title_style = doc.styles['ReportTitle']
    title_style.font.name = 'Times New Roman'
    title_style.font.size = Pt(20)
    title_style.font.bold = True
    title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_style.paragraph_format.space_before = Pt(24)
    title_style.paragraph_format.space_after = Pt(24)

    # Heading 1
    h1 = doc.styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0,0,0)
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(12)
    h1.font.all_caps = True

    # Heading 2
    h2 = doc.styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(14)
    h2.font.bold = True
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(9)

    # Heading 3
    h3 = doc.styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(13)
    h3.font.bold = True
    h3.paragraph_format.space_before = Pt(9)
    h3.paragraph_format.space_after = Pt(6)

def main():
    doc = Document()
    set_document_props(doc)
    configure_styles(doc)
    # Front matter
    doc.add_paragraph('ABSTRACT', style='Heading 1')
    doc.add_paragraph('ElevoraAI is an AI-powered smart education and career advancement platform that integrates structured learning, AI tutoring, coding practice, real-time contests, resume and cover letter generation, ATS scanning, quizzes and skill assessments, community interaction, and productivity tools in a single system. Built on a modern MERN/React+TypeScript stack with JWT-based role access, multiple AI providers (Google Gemini, OpenAI), and code execution via Judge0, ElevoraAI addresses fragmentation across disparate learning tools. This report documents the actual repository implementation: modules, data models, authentication and authorization, AI integrations, contest and compiler flows, admin capabilities, frontend UX, and deployment configuration. It distinguishes implemented, configured-but-external-dependent, partial, and UI-only components, reports known issues (including token storage key inconsistencies and hardcoded endpoints/keys noted in the codebase), and presents testing and validation results.')
    doc.add_page_break()
    doc.add_paragraph('TABLE OF CONTENTS', style='Heading 1')
    doc.add_table(rows=1, cols=3)
    table = doc.tables[-1]
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.cell(0,0).text = 'SL. NO'
    table.cell(0,1).text = 'NAME'
    table.cell(0,2).text = 'PAGE NO'
    for i in range(3): table.rows[0].cells[i].paragraphs[0].runs[0].font.bold = True
    # minimal TOC entries (will be correct with field updates; for now placeholders - we'll add more later)
    rows = [(1,'ABSTRACT','i'),(2,'TABLE OF CONTENTS','ii'),(3,'LIST OF FIGURES','iii'),(4,'LIST OF TABLES','iv'),(5,'ABBREVIATIONS','v'),(6,'CHAPTER – 1 INTRODUCTION','1')]
    for r in rows:
        tr = table.add_row().cells
        tr[0].text = str(r[0]); tr[1].text = str(r[1]); tr[2].text = str(r[2])
    doc.add_page_break()
    doc.add_paragraph('LIST OF FIGURES', style='Heading 1')
    t2 = doc.add_table(rows=1, cols=3)
    t2.style = 'Light Grid Accent 1'
    t2.cell(0,0).text='FIG NO'; t2.cell(0,1).text='NAME'; t2.cell(0,2).text='PAGE NO'
    for i in range(3): t2.rows[0].cells[i].paragraphs[0].runs[0].font.bold=True
    figs = [('4.1','Overall System Architecture','5'),('4.2','Navigation Map','6'),('5.1','Login/Sign-up Flow Demo','27'),('5.2','Login Form Demo','28')]
    for i,f in enumerate(figs, start=1):
        c = t2.add_row().cells; c[0].text=str(f[0]); c[1].text=f[1]; c[2].text=f[2]
    doc.add_page_break()
    # Chapter 1
    doc.add_heading('CHAPTER – 1', 1)
    doc.add_heading('INTRODUCTION', 1)
    doc.add_paragraph('1.1 Background and Context')
    doc.add_paragraph('ElevoraAI is a comprehensive, AI-powered smart education and career advancement platform that consolidates structured learning, coding practice, assessments, AI assistance, resume building, and placement preparation into a single unified system. The repository at C:\\Users\\user\\Downloads\\Dev-Elevate-main\\Dev-Elevate-main\\ElevoraAI is the source of truth for implementation, built as a full-stack web application with separate Client (React + TypeScript + Vite) and Server (Node.js + Express) components.')
    doc.add_paragraph('1.2 Problem Statement')
    doc.add_paragraph('Learners must navigate fragmented tools (courses, coding judges, resume tools, job platforms, communities), leading to disjointed progress tracking, lack of AI-powered guidance, and limited real-time collaboration. ElevoraAI aims to eliminate this fragmentation through role-based access, unified dashboards, and AI-assisted workflows.')
    doc.add_paragraph('1.3 Objectives')
    doc.add_paragraph('The primary objectives include providing structured learning tracks (DSA, Java, MERN, AI/ML), AI Study Buddy, coding platform with Judge0 integration, real-time contests with leaderboards and Elo ratings, ATS-optimized resume builder and cover letter generator, AI-generated quizzes/assessments, community forum, video course management, placement resources, and comprehensive admin controls.')
    doc.add_paragraph('1.4 Scope and Limitations')
    doc.add_paragraph('Scope includes the features implemented in the codebase. Limitations include dependencies on external services (OpenAI, Gemini, Groq, NewsAPI, YouTube, Judge0, Firebase, Stripe) and credential requirements for those features; some modules are UI-only or hardcoded in the current implementation as documented.')
    doc.add_paragraph('1.5 Organization of the Report')
    doc.add_paragraph('This report follows the sample structure: Introduction (Ch.1), Literature Survey (Ch.2), System Specification (Ch.3), Design (Ch.4), Implementation (Ch.5), Result and Testing (Ch.6), Conclusion, Future Enhancements, and References.')
    doc.save('report_output/ElevoraAI_Final_Report.docx')
    print('written')

if __name__ == '__main__':
    main()
