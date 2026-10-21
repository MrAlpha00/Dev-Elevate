from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from pathlib import Path

def configure_styles(doc):
    s = doc.styles['Normal']
    s.font.name = 'Times New Roman'
    s.font.size = Pt(12)
    pf = s.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing = 1.5
    pf.space_after = Pt(6)
    pf.first_line_indent = Inches(0.5)
    h1 = doc.styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(12)
    h1.font.all_caps = True
    h2 = doc.styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(14)
    h2.font.bold = True
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(9)
    h3 = doc.styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(13)
    h3.font.bold = True
    h3.paragraph_format.space_before = Pt(9)
    h3.paragraph_format.space_after = Pt(6)

def main():
    doc = Document()
    configure_styles(doc)
    doc.add_heading('ABSTRACT', level=1)
    doc.add_paragraph('ElevoraAI is an AI-powered smart education and career advancement platform that integrates structured learning, AI tutoring, coding practice, real-time contests, resume and cover letter generation, ATS scanning, quizzes and skill assessments, community features, and productivity tools into a single system. This report documents the actual implementation in the repository (full-stack React + TypeScript + Vite frontend, Node.js/Express + MongoDB backend) based on code inspection and build validation. It accurately describes implemented features, external dependencies, known issues, and validation results.')
    doc.add_page_break()
    doc.add_heading('TABLE OF CONTENTS', level=1)
    t = doc.add_table(rows=1, cols=3)
    t.style = 'Light Grid Accent 1'
    t.cell(0,0).text='SL. NO'; t.cell(0,1).text='NAME'; t.cell(0,2).text='PAGE NO'
    for c in t.rows[0].cells: c.paragraphs[0].runs[0].font.bold=True
    entries = [(1,'ABSTRACT','i'),(2,'TABLE OF CONTENTS','ii'),(3,'LIST OF FIGURES','iii'),(4,'LIST OF TABLES','iv'),(5,'ABBREVIATIONS','v'),(6,'CHAPTER – 1 INTRODUCTION','1'),(7,'CHAPTER – 2 LITERATURE SURVEY','2'),(8,'CHAPTER – 3 SYSTEM SPECIFICATION','5'),(9,'CHAPTER – 4 DESIGN','8'),(10,'CHAPTER – 5 IMPLEMENTATION','11'),(11,'CHAPTER – 6 RESULT AND TESTING','24'),(12,'CONCLUSION','30'),(13,'FUTURE ENHANCEMENTS','31'),(14,'REFERENCES','32')]
    for r in entries:
        tr=t.add_row().cells
        tr[0].text=str(r[0]); tr[1].text=r[1]; tr[2].text=r[2]
    doc.add_page_break()
    doc.add_heading('LIST OF FIGURES', level=1)
    t2 = doc.add_table(rows=1, cols=3)
    t2.style='Light Grid Accent 1'
    t2.cell(0,0).text='FIG NO'; t2.cell(0,1).text='NAME'; t2.cell(0,2).text='PAGE NO'
    for c in t2.rows[0].cells: c.paragraphs[0].runs[0].font.bold=True
    for f in [('4.1','Overall System Architecture','6'),('4.2','Navigation Map','7'),('5.1','Login Flow Demo (login-flow.gif frame)','28'),('5.2','Login Form Demo','29')]:
        tr=t2.add_row().cells; tr[0].text=f[0]; tr[1].text=f[1]; tr[2].text=f[2]
    doc.add_page_break()
    doc.add_heading('LIST OF TABLES', level=1)
    t3 = doc.add_table(rows=1, cols=3)
    t3.style='Light Grid Accent 1'
    t3.cell(0,0).text='TABLE NO'; t3.cell(0,1).text='NAME'; t3.cell(0,2).text='PAGE NO'
    for c in t3.rows[0].cells: c.paragraphs[0].runs[0].font.bold=True
    for f in [('3.1','Technology Stack','5'),('3.2','External Services and Env Vars','6'),('4.1','Major Modules','8'),('6.1','Test Cases Summary','27')]:
        tr=t3.add_row().cells; tr[0].text=f[0]; tr[1].text=f[1]; tr[2].text=f[2]
    doc.add_page_break()
    doc.add_heading('ABBREVIATIONS', level=1)
    doc.add_paragraph('AI: Artificial Intelligence; API: Application Programming Interface; ATS: Applicant Tracking System; DB: Database; JWT: JSON Web Token; MERN: MongoDB Express React Node; SPA: Single Page Application; UI: User Interface; RBAC: Role-Based Access Control; ODM: Object Document Mapper; REST: Representational State Transfer.')
    doc.add_page_break()
    doc.add_heading('CHAPTER – 1', level=1)
    doc.add_heading('INTRODUCTION', level=1)
    doc.add_paragraph('ElevoraAI consolidates fragmented tools. Frontend (React+TS+Vite), Backend (Express 5 + MongoDB + Socket.IO), external AI and services. Goals: integrated learning, coding, assessments, AI, resume/cover letter, community, admin. Distinct from prior tools by unified role-based access and real-time contest features.')
    doc.add_page_break()
    doc.add_heading('CHAPTER – 2', level=1)
    doc.add_heading('LITERATURE SURVEY', level=1)
    doc.add_paragraph('E-learning, online judges (Leetcode/HackerRank patterns), AI tutoring (LLMs), ATS tools, developer communities, placement prep, gamification (leaderboards), RBAC/JWT. Gap: fragmented workflows; ElevoraAI integrates these.')
    doc.add_page_break()
    doc.add_heading('CHAPTER – 3', level=1)
    doc.add_heading('SYSTEM SPECIFICATION', level=1)
    doc.add_paragraph('Roles: user, admin. Modules: Dashboard, Learning Hub, Video, Quiz Center, Skill Assessment, Coding, Interview, Study Buddy, Tech Feed, Community, Resume Builder, Cover Letter, Placement Prep, AI Projects, AI Models, Road Map, Notes, Calendar, Contributors. Tech stack: React 18, TS, Vite, Tailwind, Redux Toolkit, react-router-dom, Framer Motion, react-markdown, Monaco, Socket.IO-client, html2pdf/jsPDF; Node/Express 5, Mongoose, Socket.IO, JWT, bcrypt, nodemailer, OpenAI SDK, sanitize-html, pdfkit, multer, zod; MongoDB. External: Gemini/OpenAI/Groq, Judge0/RapidAPI, NewsAPI, YouTube API, Stripe, Firebase. Limitations: credentials required; some UI/demo items present.')
    doc.add_page_break()
    doc.add_heading('CHAPTER – 4', level=1)
    doc.add_heading('DESIGN', level=1)
    doc.add_paragraph('3-tier architecture. Navigation map matches 19 sidebar items. Core flows documented. ER based on actual models (User, Quiz/Question/QuizAttempt, Contest/Problem/Submission/ContestSubmission, SkillAssessment, Progress, Notes/Reviews, Notification, InterviewExperience, Course/AdminCourse, VideoProgress/SavedVideo, etc.). Authentication: JWT (cookie or Authorization header), bcrypt, OTP, Google OAuth, RBAC (authenticate/authorize). AI: Gemini chat, OpenAI assessments, Groq recommendations. Coding: Judge0 submission. Contests: Socket.IO for live leaderboard, Elo calculation, cron for finalization.')
    p = doc.add_paragraph(); r=p.add_run()
    if Path('report_output/figures/fig4_1_architecture.png').exists(): r.add_picture('report_output/figures/fig4_1_architecture.png', width=Inches(6))
    doc.add_page_break()
    doc.add_heading('CHAPTER – 5', level=1)
    doc.add_heading('IMPLEMENTATION', level=1)
    doc.add_paragraph('Frontend routing with ProtectedRoute and admin guard. API uses axios with interceptors; token read from localStorage. Key issues found: localStorage key mismatch (elevoraAiAuth vs ElevoraAIAuth) affecting auth headers; hardcoded localhost:4000 compiler URL; relative /api/user/streak in DailyGoals; hardcoded newsdata.io key in NewsWidget; VITE_GROQ_API_KEY exposed client-side; duplicate /api/v1/ai mounts in index.js; inconsistent RapidAPI env names; dashboard achievements/insights partial. Build: TypeScript compiles successfully (tsc --noEmit exit 0), Vite production build succeeds (dist/index.html and assets generated).')
    doc.add_paragraph('Fig. 5.1: Login Flow Demo (frame from login-flow.gif)')
    p=doc.add_paragraph()
    if Path('report_output/figures/fig5_1_login_flow.png').exists(): p.add_run().add_picture('report_output/figures/fig5_1_login_flow.png', width=Inches(6))
    doc.add_paragraph('Fig. 5.2: Login Form Demo')
    p=doc.add_paragraph()
    if Path('report_output/figures/fig5_2_login_form.png').exists(): p.add_run().add_picture('report_output/figures/fig5_2_login_form.png', width=Inches(5.5))
    doc.add_page_break()
    doc.add_heading('CHAPTER – 6', level=1)
    doc.add_heading('RESULT AND TESTING', level=1)
    doc.add_paragraph('Validation: static syntax checks passed (node --check all JS), TypeScript type-check passed, production build successful. Functional areas verified by code inspection: auth flows, RBAC, routing, models, controllers, AI endpoints presence, Socket.IO wiring, contest/Judge0 flow structure. Unverified at runtime: external API calls requiring credentials, live dashboard rendering, payment/checkout, notifications delivery. Test case summary includes unit/static checks and documented limitations.')
    doc.add_paragraph('Test cases (representative): TC01 Auth routes present and protected middleware configured – Verified by code. TC02 JWT middleware (cookie/header, role checks) – Verified. TC03 Gemini/OpenAI/Groq endpoints present – Verified. TC04 Judge0 compiler integration structure – Verified. TC05 Socket.IO contest leaderboard/events – Verified. TC06 ATS scanner logic – Verified. TC07 ER models aligned to features – Verified. TC08 TypeScript compiles/build succeeds – Verified. TC09 Token key mismatch – Documented defect. TC10 External secrets/URLs hardcoded – Documented.')
    doc.add_page_break()
    doc.add_heading('CONCLUSION', level=1)
    doc.add_paragraph('ElevoraAI delivers a unified, role-based AI-powered learning and career platform with substantial implemented functionality. Build and syntax validation succeed. Honest disclosure of defects and stubs ensures accuracy. With remediation of documented issues, the system is well-positioned for production use.')
    doc.add_page_break()
    doc.add_heading('FUTURE ENHANCEMENTS', level=1)
    doc.add_paragraph('Fix localStorage key consistency, proxy external calls server-side, broaden rate limiting, server-side Stripe checkout, persist dashboard insights/achievements, replace static learning content with DB-driven where intended, add automated tests, implement structured logging, capture dashboard screenshots, improve accessibility and performance.')
    doc.add_page_break()
    doc.add_heading('REFERENCES', level=1)
    for r in [('1','React','https://react.dev/'),('2','Express','https://expressjs.com/'),('3','MongoDB','https://www.mongodb.com/docs/'),('4','Mongoose','https://mongoosejs.com/docs/'),('5','Socket.IO','https://socket.io/docs/'),('6','Judge0','https://judge0.com/docs/'),('7','Google Gemini','https://ai.google.dev/docs/'),('8','OpenAI','https://platform.openai.com/docs/'),('9','Groq','https://console.groq.com/docs/'),('10','Stripe','https://docs.stripe.com/'),('11','Vite','https://vitejs.dev/guide/'),('12','Tailwind CSS','https://tailwindcss.com/docs/'),('13','JWT.io','https://jwt.io/introduction/'),('14','Monaco Editor','https://microsoft.github.io/monaco-editor/'),('15','Hamari et al. (2014)','Does Gamification Work?'),('16','Sandhu et al. (1996)','RBAC Models, IEEE Computer')]:
        doc.add_paragraph('['+r[0]+'] '+r[1]+'. '+r[2]+'.')
    doc.save('report_output/ElevoraAI_Final_Report.docx')
    print('ok')

if __name__=='__main__':
    main()
