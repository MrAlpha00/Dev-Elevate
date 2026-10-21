from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT

def configure_styles(doc):
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    para = style.paragraph_format
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    para.line_spacing = 1.5
    para.space_after = Pt(6)
    para.first_line_indent = Inches(0.5)

    # Heading 1
    h1 = doc.styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(16)
    h1.font.bold = True
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
    configure_styles(doc)
    # add front matter
    doc.add_heading('ABSTRACT', level=1)
    doc.add_paragraph('ElevoraAI is an AI-powered smart education and career advancement platform integrating structured learning, AI tutoring, coding practice, real-time contests, resume and cover letter generation, ATS scanning, quizzes and skill assessments, community features, and productivity tools. This report documents the actual repository implementation.')
    doc.add_page_break()
    doc.add_heading('TABLE OF CONTENTS', level=1)
    t = doc.add_table(rows=1, cols=3)
    t.style = 'Light Grid Accent 1'
    t.cell(0,0).text='SL. NO'; t.cell(0,1).text='NAME'; t.cell(0,2).text='PAGE NO'
    for c in t.rows[0].cells: c.paragraphs[0].runs[0].font.bold=True
    for r in [(1,'ABSTRACT','i'),(2,'TABLE OF CONTENTS','ii'),(3,'LIST OF FIGURES','iii'),(4,'LIST OF TABLES','iv'),(5,'ABBREVIATIONS','v'),(6,'CHAPTER – 1 INTRODUCTION','1'),(7,'CHAPTER – 2 LITERATURE SURVEY','2'),(8,'CHAPTER – 3 SYSTEM SPECIFICATION','5'),(9,'CHAPTER – 4 DESIGN','8'),(10,'CHAPTER – 5 IMPLEMENTATION','11'),(11,'CHAPTER – 6 RESULT AND TESTING','24'),(12,'CONCLUSION','30'),(13,'FUTURE ENHANCEMENTS','31'),(14,'REFERENCES','32')]:
        tr=t.add_row().cells
        tr[0].text=str(r[0]); tr[1].text=r[1]; tr[2].text=r[2]
    doc.add_page_break()
    doc.add_heading('LIST OF FIGURES', level=1)
    t2 = doc.add_table(rows=1, cols=3)
    t2.style='Light Grid Accent 1'
    t2.cell(0,0).text='FIG NO'; t2.cell(0,1).text='NAME'; t2.cell(0,2).text='PAGE NO'
    for c in t2.rows[0].cells: c.paragraphs[0].runs[0].font.bold=True
    for f in [('4.1','Overall System Architecture','6'),('4.2','Navigation Map','7'),('5.1','Login Flow Demo','28'),('5.2','Login Form Demo','29')]:
        tr=t2.add_row().cells
        tr[0].text=f[0]; tr[1].text=f[1]; tr[2].text=f[2]
    doc.add_page_break()
    # chapter 1
    doc.add_heading('CHAPTER – 1', level=1)
    doc.add_heading('INTRODUCTION', level=1)
    doc.add_paragraph('ElevoraAI is a full-stack AI-powered platform developed to unify structured learning, coding practice, AI assistance, career tools, and community interaction. The repository (Dev-Elevate) is the implementation source. Frontend: React 18 + TypeScript + Vite + TailwindCSS; Backend: Node.js/Express 5 + MongoDB/Mongoose + Socket.IO. External integrations: Google Gemini, OpenAI, Groq, Judge0, Stripe, Firebase OAuth, NewsAPI, YouTube.')
    doc.add_page_break()
    # remaining chapters briefly for structure
    doc.add_heading('CHAPTER – 2', level=1)
    doc.add_heading('LITERATURE SURVEY', level=1)
    doc.add_paragraph('A survey of existing e-learning, online judges, AI tutoring, ATS tools, and community platforms reveals gaps in integration. ElevoraAI consolidates multiple capabilities into one role-based ecosystem with real-time contests and AI assistance.')
    doc.add_page_break()
    doc.add_heading('CHAPTER – 3', level=1)
    doc.add_heading('SYSTEM SPECIFICATION', level=1)
    doc.add_paragraph('System roles: User and Admin. Major modules include Dashboard, Learning Hub, Video, Quiz Center, Skill Assessment, Coding, Interview, Study Buddy (chatbot), Tech Feed, Community, Resume Builder, Cover Letter, Placement Prep, AI Projects (Groq recommendations), AI Models, Road Map, Notes, Calendar, Contributors. Non-functional: responsive, role-based access, security (JWT/httpOnly where applicable), maintainability.')
    doc.add_page_break()
    doc.add_heading('CHAPTER – 4', level=1)
    doc.add_heading('DESIGN', level=1)
    doc.add_paragraph('The system follows a 3-tier architecture (React SPA client, Express REST API with Socket.IO, MongoDB). Navigation spans 19 routes as implemented in Sidebar. Core flows: JWT authentication, Gemini/OpenAI calls, Judge0 code submission with contest flow and Elo rating updates.')
    doc.add_paragraph('Fig. 4.1: Overall System Architecture').add_run().add_break()
    p = doc.add_paragraph()
    r = p.add_run()
    if (Path('report_output/figures/fig4_1_architecture.png').exists()):
        r.add_picture('report_output/figures/fig4_1_architecture.png', width=Inches(6))
    doc.add_page_break()
    doc.add_heading('CHAPTER – 5', level=1)
    doc.add_heading('IMPLEMENTATION', level=1)
    doc.add_paragraph('Frontend uses React Router v7 with protected/admin routes, Context API and Redux, Framer Motion, React-Markdown, Monaco Editor, html2pdf.js/jsPDF, Socket.IO client. Backend uses Express 5 with middleware for auth/authorization/sanitization, Mongoose models (User, Quiz, Contest/Problem/Submission/ContestSubmission, SkillAssessment, Progress, Notes, Notification, InterviewExperience, etc.), controllers, routes, and Socket.IO for real-time events. AI integrations: Gemini chat; OpenAI for skill assessments; Groq for project recommendations. ATS scanner performs keyword extraction. Code execution uses Judge0 RapidAPI.')
    doc.add_paragraph('Fig. 5.1: Login Flow Demo')
    p = doc.add_paragraph()
    if (Path('report_output/figures/fig5_1_login_flow.png').exists()):
        p.add_run().add_picture('report_output/figures/fig5_1_login_flow.png', width=Inches(6))
    doc.add_paragraph('Fig. 5.2: Login Form Demo')
    p = doc.add_paragraph()
    if (Path('report_output/figures/fig5_2_login_form.png').exists()):
        p.add_run().add_picture('report_output/figures/fig5_2_login_form.png', width=Inches(5.5))
    doc.add_paragraph('Known implementation issues (evidence-based): localStorage token key mismatch (AuthContext uses elevoraAiAuth; axios interceptor reads ElevoraAIAuth), hardcoded localhost:4000 compiler endpoint in ProblemsPage.tsx, relative /api/user/streak URL in DailyGoals.tsx, hardcoded newsdata.io API key in NewsWidget.tsx, Groq API key exposed to client bundle (VITE_GROQ_API_KEY), duplicate /api/v1/ai mount in index.js, inconsistent RapidAPI env naming, hardcoded achievements/insights stub in dashboard, and missing service modules noted in audit docs. TypeScript build: tsc --noEmit passes; production Vite build succeeds.')
    doc.add_page_break()
    doc.add_heading('CHAPTER – 6', level=1)
    doc.add_heading('RESULT AND TESTING', level=1)
    doc.add_paragraph('Validation was performed by static code inspection (server Node.js syntax checked, TypeScript compilation passed, Vite production build succeeded), review of routes/models/controllers/contexts, and documentation/audit review. Test coverage below is based on code evidence and build validation; items marked Not tested reflect inability to run full runtime tests without live services/credentials.')
    doc.add_page_break()
    doc.add_heading('CONCLUSION', level=1)
    doc.add_paragraph('ElevoraAI implements a unified, role-based platform with AI, coding, contests, assessments, career tools, and admin features. While core functionality is implemented server-side and frontend builds successfully, there are documented issues (configuration/key mismatches, hardcoded endpoints, and several UI/demo/stub areas) that should be addressed. Overall, the repository represents a substantial, working foundation meeting the project’s integration objectives.')
    doc.add_page_break()
    doc.add_heading('FUTURE ENHANCEMENTS', level=1)
    doc.add_paragraph('Future work: fix token-key consistency, move external API calls to server proxy, enforce rate limiting broadly, implement real payment/checkout server-side, replace hardcoded data with DB-driven content where intended, add comprehensive automated tests, implement proper logging, add dashboard screenshot/capture pipeline, and expand real-time features.')
    doc.add_page_break()
    doc.add_heading('REFERENCES', level=1)
    doc.add_paragraph('[1] React Documentation. https://react.dev/ (2026).')
    doc.add_paragraph('[2] Express.js Documentation. https://expressjs.com/.')
    doc.add_paragraph('[3] MongoDB Documentation. https://www.mongodb.com/docs/.')
    doc.add_paragraph('[4] Mongoose Documentation. https://mongoosejs.com/docs/.')
    doc.add_paragraph('[5] Socket.IO Documentation. https://socket.io/docs/.')
    doc.add_paragraph('[6] Judge0 Documentation. https://judge0.com/docs/.')
    doc.add_paragraph('[7] Google Gemini API. https://ai.google.dev/docs/.')
    doc.add_paragraph('[8] OpenAI API Reference. https://platform.openai.com/docs/.')
    doc.add_paragraph('[9] Groq Documentation. https://console.groq.com/docs/.')
    doc.add_paragraph('[10] Stripe Documentation. https://docs.stripe.com/.')
    doc.add_paragraph('[11] Vite Documentation. https://vitejs.dev/guide/.')
    doc.add_paragraph('[12] Tailwind CSS Documentation. https://tailwindcss.com/docs/.')
    doc.add_paragraph('[13] JWT.io. https://jwt.io/introduction/.')
    doc.add_paragraph('[14] Monaco Editor. https://microsoft.github.io/monaco-editor/.')
    doc.add_paragraph('[15] Hamari et al., Does Gamification Work?, 2014.')
    doc.add_paragraph('[16] Sandhu et al., RBAC Models, IEEE Computer, 1996.')
    doc.save('report_output/ElevoraAI_Final_Report.docx')
    print('ok')

if __name__=='__main__':
    main()
