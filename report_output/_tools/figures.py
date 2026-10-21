# -*- coding: utf-8 -*-
"""Generate academic-style diagrams for the Elevora AI final report.

All diagrams are derived from the inspected repository (ElevoraAI/Client and
ElevoraAI/Server).  Output: report_output/figures/*.png at 300 dpi.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse, Polygon

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["DejaVu Serif", "Times New Roman", "Times"]
plt.rcParams["font.size"] = 8.2

INK = "#1a1a1a"
GREY = "#f2f2f2"
MID = "#e3e3e3"
ACC = "#d9d9d9"


def canvas(w=10.0, h=6.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h / w)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def box(ax, x, y, w, h, text, fill=GREY, bold=False, fs=8.2, edge=INK, lw=0.9,
        radius=0.8, align="center", style="round"):
    """Draw a rounded rectangle with wrapped text."""
    p = dict(boxstyle=f"round,pad=0.0,rounding_size={radius}", fc=fill, ec=edge, lw=lw)
    if style == "square":
        p = dict(boxstyle="square,pad=0.0", fc=fill, ec=edge, lw=lw)
    p = FancyBboxPatch((x + radius, y + radius), w - 2 * radius, h - 2 * radius,
                       boxstyle=p["boxstyle"], fc=fill, ec=edge, lw=lw, zorder=2)
    ax.add_patch(p)
    ha = {"center": "center", "left": "left"}[align]
    tx = x + w / 2 if align == "center" else x + 1.6
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=fs, color=INK,
            fontweight="bold" if bold else "normal", zorder=3,
            linespacing=1.35)
    return p


def poly(ax, x, y, w, h, text, fill=GREY, fs=8.2, bold=False, edge=INK, lw=0.9):
    ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=edge, lw=lw, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=INK, fontweight="bold" if bold else "normal", zorder=3,
            linespacing=1.35)


def diamond(ax, cx, cy, w, h, text, fill="#fafafa", fs=7.6):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=INK, lw=0.9, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=INK, zorder=3,
            linespacing=1.3)


def oval(ax, cx, cy, w, h, text, fill="#fbfbfb", fs=7.4, lw=0.9):
    ax.add_patch(Ellipse((cx, cy), w, h, fc=fill, ec=INK, lw=lw, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=INK, zorder=3,
            linespacing=1.3)


def arrow(ax, p1, p2, style="-|>", label=None, ls="-", lw=0.9, lx=0, ly=0, fs=7.0,
          rad=0.0, ha="center"):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=9, lw=lw, ls=ls,
                        color=INK, shrinkA=1.5, shrinkB=1.5, zorder=4,
                        connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    if label:
        mx, my = (p1[0] + p2[0]) / 2 + lx, (p1[1] + p2[1]) / 2 + ly
        ax.text(mx, my, label, ha=ha, va="center", fontsize=fs, color=INK, zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.8))
    return a


def dashed(ax, p1, p2, label=None, fs=7.0, lx=0, ly=0):
    arrow(ax, p1, p2, ls=(0, (4, 3)), label=label, lx=lx, ly=ly, fs=fs)


def title(ax, text, y=None):
    if y is None:
        y = ax.get_ylim()[1] - 1.5
    ax.text(50, y, text, ha="center", va="top", fontsize=9.4, fontweight="bold",
            color=INK)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------- Fig 4.1
def fig_architecture():
    fig, ax = canvas(10.0, 6.6)
    W = ax.get_ylim()[1]
    # layer bands
    bands = [(72, 92, "PRESENTATION LAYER  -  React 18 + TypeScript SPA (Vite build)"),
             (40, 66, "APPLICATION LAYER  -  Node.js / Express 5 REST API + Socket.IO"),
             (10, 34, "DATA LAYER  -  MongoDB via Mongoose ODM (Atlas or self-hosted)")]
    for y0, y1, label in bands:
        ax.add_patch(Rectangle((2, y0), 96, y1 - y0, fc="#fcfcfc", ec=INK, lw=1.0, zorder=1))
        ax.text(3.4, y1 - 2.4, label, ha="left", va="top", fontsize=7.4, fontweight="bold",
                color=INK, zorder=3)

    box(ax, 5, 74.5, 17, 14, "React SPA\n19 nav modules\nDashboard | Learning\nQuiz | Coding | Community",
        fill=GREY, fs=7.2)
    box(ax, 25, 74.5, 17, 14, "Monaco Editor\ncode workspace\n(Ctrl+Enter = Run)",
        fill=GREY, fs=7.2)
    box(ax, 45, 74.5, 17, 14, "AI Chat panel\n(Study Buddy)\n+ AI Quiz / Note",
        fill=GREY, fs=7.2)
    box(ax, 65, 74.5, 17, 14, "Admin console\n9 management tabs\n+ Analytics",
        fill=GREY, fs=7.2)
    box(ax, 85, 74.5, 12, 14, "Socket.IO\nclient\n(live contests)", fill=GREY, fs=7.2)

    box(ax, 5, 47, 21, 13, "Auth routes\nuserRoutes.js\nJWT + OTP + OAuth", fill=MID, fs=7.0)
    box(ax, 28, 47, 20, 13, "Learning & Assessment\njava/aiml/mern/dsa\nassessmentRoutes.js", fill=MID, fs=7.0)
    box(ax, 50, 47, 20, 13, "Quiz, Notes,\nCommunity, Video\nprogress, ATS scan", fill=MID, fs=7.0)
    box(ax, 72, 47, 25, 13, "Contests & Compiler\ncontestController.js (1794 LOC)\ncompilerRoutes.js (Judge0)", fill=MID, fs=7.0)

    box(ax, 8, 15, 18, 13, "User / Auth\n(OtpToken, Feedback,\nVisitingWebsite)", fill="#fafafa", fs=7.0)
    box(ax, 28, 15, 18, 13, "Learning content\nCourse, LearningModule,\nNotes, Reviews, Progress", fill="#fafafa", fs=7.0)
    box(ax, 48, 15, 18, 13, "Assessment data\nQuiz, QuizAttempt,\nSkillAssessment", fill="#fafafa", fs=7.0)
    box(ax, 68, 15, 20, 13, "Contest data\nContest, Problem,\nContestSubmission", fill="#fafafa", fs=7.0)

    # external services band
    ax.add_patch(Rectangle((2, 1.5), 96, 8.5, fc="#f7f7f7", ec=INK, lw=1.0, zorder=1))
    ax.text(3.4, 8.4, "EXTERNAL SERVICES (credential dependent)", ha="left", va="top",
            fontsize=7.4, fontweight="bold", color=INK, zorder=3)
    ext = ["Google Gemini\n(quiz + notes)", "OpenAI\n(skill assessment)",
           "Groq / LLaMA\n(project rec.)", "Judge0\n(code execution)",
           "YouTube Data v3\n(courses)", "NewsAPI\n(tech feed)",
           "Gmail SMTP\n(OTP e-mail)"]
    w = 12.6
    for i, t in enumerate(ext):
        box(ax, 3.2 + i * (w + 0.6), 2.4, w, 5.0, t, fill="white", fs=6.1, radius=0.5)

    for x in (13, 33, 53, 73, 91):
        arrow(ax, (x, 74.2), (x, 60.5))
    arrow(ax, (16, 46.5), (16, 28.5))
    arrow(ax, (38, 46.5), (37, 28.5))
    arrow(ax, (60, 46.5), (57, 28.5))
    arrow(ax, (84, 46.5), (78, 28.5))
    for i in range(7):
        x = 3.2 + i * (w + 0.6) + w / 2
        dashed(ax, (x, 2.2), (min(max(x, 14), 86), 14.5))
    ax.text(3.4, 9.8, "Arrow style: solid = internal call;  dashed = outbound API call to a third-party provider",
            fontsize=6.4, ha="left", va="bottom", color="#333333")
    save(fig, "fig4_1_architecture.png")


# ---------------------------------------------------------------- Fig 4.2
def fig_usecase():
    fig, ax = canvas(10.0, 6.6)
    ax.add_patch(Rectangle((22, 6), 58, 88, fc="#fcfcfc", ec=INK, lw=1.0, zorder=1))
    ax.text(51, 91.5, "Elevora AI", ha="center", va="top", fontsize=9.2,
            fontweight="bold", color=INK, zorder=3)

    ux = [
        (34, 82, "Register /\nLog in (OTP,\nGoogle)"),
        (34, 70, "Manage profile\n& preferences"),
        (34, 58, "Follow learning\ntracks & track\nprogress"),
        (34, 46, "Attempt quizzes\n& skill\nassessments"),
        (34, 34, "Write & share\ncode, submit\nfor judging"),
        (34, 22, "Join contests,\nview live\nleaderboard"),
        (34, 10, "Ask / answer\ncommunity\nquestions"),
    ]
    for cx, cy, t in ux:
        oval(ax, cx, cy, 22, 9.5, t, fs=6.8)
    ux2 = [
        (70, 82, "Author quizzes\nand questions"),
        (70, 70, "Manage users\nand system logs"),
        (70, 58, "Publish and\ncurate courses"),
        (70, 46, "Moderate forum\ncontent"),
        (70, 34, "View usage\nanalytics"),
        (70, 22, "Change system\nsettings"),
    ]
    for cx, cy, t in ux2:
        oval(ax, cx, cy, 22, 9.5, t, fs=6.8)
    # system boundary for admin use cases
    ax.add_patch(Rectangle((56, 14), 32, 76, fc="none", ec="#888888", lw=0.9, ls=(0, (5, 3)), zorder=1))
    ax.text(72, 12.6, "Administration module", ha="center", va="top", fontsize=7.0,
            style="italic", color="#444444", zorder=3)

    # actors
    ax.text(8, 86, "STUDENT /\nLEARNER", ha="center", va="center", fontsize=7.6,
            fontweight="bold", color=INK)
    ax.text(92, 86, "PLATFORM\nADMIN", ha="center", va="center", fontsize=7.6,
            fontweight="bold", color=INK)
    ax.text(8, 16, "EXTERNAL\nSERVICES", ha="center", va="center", fontsize=7.0,
            fontweight="bold", color=INK)
    for cx, cy in [(8, 86), (92, 86), (8, 16)]:
        ax.add_patch(Ellipse((cx, cy), 6.5, 6.5, fc="#f5f5f5", ec=INK, lw=0.9, zorder=2))
    for cy in (82, 70, 58, 46, 34, 22, 10):
        if cy > 14:
            arrow(ax, (11.3, 80), (22.5, cy), lw=0.6)
    for cy in (82, 70, 58, 46, 34, 22):
        arrow(ax, (88.7, 80), (81.5, cy), lw=0.6)
    arrow(ax, (11.3, 19), (23.5, 34), lw=0.6, ls=(0, (3, 2)))
    ax.text(16.5, 27.5, "Judge0 /\nAI providers", fontsize=6.2, ha="center", color=INK)
    save(fig, "fig4_2_usecase.png")


# ---------------------------------------------------------------- Fig 4.3
def fig_erd():
    fig, ax = canvas(10.4, 6.8)

    def ent(x, y, w, name, attrs, fs=6.3):
        h = 3.0 + 2.3 * len(attrs)
        ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.0, zorder=2))
        ax.add_patch(Rectangle((x, y + h - 3.0), w, 3.0, fc=MID, ec=INK, lw=1.0, zorder=3))
        ax.text(x + w / 2, y + h - 1.5, name, ha="center", va="center", fontsize=fs + 0.5,
                fontweight="bold", color=INK, zorder=4)
        for i, a in enumerate(attrs):
            ax.text(x + 1.2, y + h - 4.6 - i * 2.3, a, ha="left", va="center",
                    fontsize=fs, color=INK, zorder=4)
        return (x, y, w, h)

    u = ent(2, 62, 22, "User", ["_id (PK)", "name, email", "password (hash)",
                                "role: user|admin", "googleId, streak"])
    q = ent(28, 62, 21, "Quiz", ["_id (PK)", "title, topic", "questions[]",
                                  "createdBy -> User"])
    qa = ent(53, 62, 22, "QuizAttempt", ["_id (PK)", "quiz -> Quiz", "userId -> User",
                                         "answers[], score", "completedAt"])
    sk = ent(79, 62, 19, "SkillAssessment", ["_id (PK)", "track", "answers[], score",
                                             "userId -> User"])
    n = ent(2, 36, 22, "Notes", ["_id (PK)", "userId -> User", "title, content",
                                 "isAiGenerated", "files[], likes[]"])
    rv = ent(28, 36, 21, "Reviews", ["_id (PK)", "userId -> User", "topicId", "rating"])
    pr = ent(53, 36, 22, "Progress", ["_id (PK)", "userId -> User", "topicId",
                                      "completed"])
    ct = ent(79, 36, 19, "Contest", ["_id (PK)", "title, startTime", "status, problems[]"])
    cp = ent(2, 12, 22, "ContestSubmission", ["_id (PK)", "contest -> Contest",
                                              "userId -> User", "status, points", "penalty"])
    pb = ent(28, 12, 21, "Problem", ["_id (PK)", "statement", "difficulty", "testCases[]"])
    vp = ent(53, 12, 22, "VideoProgress", ["_id (PK)", "userId -> User", "videoId",
                                            "watchedSeconds"])
    nt = ent(79, 12, 19, "Notification", ["_id (PK)", "userId -> User", "message", "read"])

    def link(a, b, la, lb, label, style="1:N", lx=0, ly=0):
        ax1 = (a[0] + a[2], a[1] + a[3] / 2)
        ax2 = (b[0] + b[2] / 2, b[1] + b[3])
        arrow(ax, ax1, ax2, style="-" if style != "1:1" else "-", lw=0.8)
        ax.text((ax1[0] + ax2[0]) / 2 + lx, (ax1[1] + ax2[1]) / 2 + ly, label,
                ha="center", va="center", fontsize=6.2, color=INK, zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.6))

    link(u, q, "1:N", "1:N", "creates")
    link(u, qa, "", "", "attempts")
    link(u, sk, "", "", "attempts")
    link(u, n, "", "", "authors")
    link(u, rv, "", "", "writes")
    link(u, pr, "", "", "tracks")
    link(u, cp, "", "", "submits")
    link(u, vp, "", "", "watches")
    link(u, nt, "", "", "receives")
    link(q, qa, "", "", "answered by")
    link(ct, cp, "", "", "judged as")
    link(ct, pb, "", "", "contains")
    ax.text(50, 92.5, "Entity-relationship model derived from the 32 Mongoose schemas in "
            "ElevoraAI/Server/model", ha="center", va="top", fontsize=7.6,
            fontweight="bold", color=INK)
    ax.text(50, 89.4, "Relationships are drawn from the ObjectId reference fields actually "
            "declared in the schemas; the 11 models with no inbound reference are omitted "
            "for clarity.", ha="center", va="top", fontsize=6.5, color="#333333")
    save(fig, "fig4_3_erd.png")


# ---------------------------------------------------------------- Fig 4.4
def fig_auth():
    fig, ax = canvas(10.0, 6.4)
    W = ax.get_ylim()[1]
    ax.text(50, W - 1.5, "Authentication and role-based authorisation flow", ha="center",
            va="top", fontsize=9.2, fontweight="bold", color=INK)

    poly(ax, 4, 78, 20, 12, "Registration\nname + email + password\n(POST /auth/signup)",
         fill=GREY, fs=7.0)
    poly(ax, 4, 60, 20, 12, "E-mail OTP\nvia Nodemailer\n(Gmail SMTP)", fill=GREY, fs=7.0)
    poly(ax, 4, 42, 20, 12, "POST /auth/verify-otp\nOtpToken lookup\nexpiry check", fill=GREY, fs=7.0)
    poly(ax, 4, 24, 20, 12, "Login\nbcrypt.compare\n(POST /auth/login)", fill=GREY, fs=7.0)
    poly(ax, 4, 6, 20, 12, "Google OAuth\nPOST /auth/google\n(firebase client token)", fill=GREY, fs=7.0)

    box(ax, 30, 40, 22, 18, "JWT issued\npayload { userId, role }\nsigned with JWT_SECRET",
        fill=MID, fs=7.2)
    box(ax, 30, 20, 22, 14, "Set-Cookie: token\nhttpOnly | secure | sameSite\n3 day expiry",
        fill=MID, fs=7.2)

    box(ax, 58, 62, 20, 16, "authenticateToken\nreads cookie or\nAuthorization header\njwt.verify + User lookup",
        fill=GREY, fs=7.0)
    box(ax, 58, 42, 20, 16, "requireAdmin /\nauthorize('admin')\nchecks req.user.role", fill=GREY, fs=7.0)
    box(ax, 58, 22, 20, 16, "Route handler\n(req.user populated)\nresource returned", fill=GREY, fs=7.0)

    poly(ax, 82, 62, 14, 16, "401\ninvalid or\nexpired token", fill="#ffffff", fs=7.0)
    poly(ax, 82, 42, 14, 16, "403\nrole not\npermitted", fill="#ffffff", fs=7.0)
    poly(ax, 82, 22, 14, 16, "200 / 201\nresponse payload", fill="#ffffff", fs=7.0)

    arrow(ax, (14, 78), (14, 72.5))
    arrow(ax, (14, 60), (14, 54.5))
    arrow(ax, (24, 48), (30, 50))
    arrow(ax, (24, 30), (30, 44), rad=-0.15)
    arrow(ax, (24, 12), (30, 44), rad=-0.25, label="same token issuance")
    arrow(ax, (52, 49), (58, 70))
    arrow(ax, (52, 27), (58, 50), rad=-0.2)
    arrow(ax, (68, 78), (82, 70), label="fail")
    arrow(ax, (78, 58), (82, 50), label="fail")
    arrow(ax, (78, 50), (82, 30))
    ax.text(51, 3.0, "Both the cookie token and the Authorization bearer token are accepted; "
            "the Socket.IO handshake uses the same secret but resolves the user from decoded.id, "
            "which the login token does not contain.", ha="center", va="center",
            fontsize=6.3, color="#333333")
    save(fig, "fig4_4_auth_flow.png")


# ---------------------------------------------------------------- Fig 4.5
def fig_ai_seq():
    fig, ax = canvas(10.0, 6.4)
    W = ax.get_ylim()[1]
    lanes = [(12, "Chatbot.tsx\n(Study Buddy)"), (32, "Chatbot.tsx\n(AI Quiz Generator)"),
             (52, "aiController.js\n/ai/generate-note"), (72, "Express route\n/api/v1/ai/*"),
             (90, "Google Gemini\n2.0 Flash")]
    ax.text(50, W - 1.2, "AI request and response sequence (Study Buddy path)", ha="center",
            va="top", fontsize=9.2, fontweight="bold", color=INK)
    for x, name in lanes:
        ax.add_patch(Rectangle((x - 7, 4), 14, W - 12, fc="#fcfcfc", ec="#999999", lw=0.8,
                               zorder=1))
        ax.text(x, W - 7.5, name, ha="center", va="center", fontsize=6.6,
                fontweight="bold", color=INK, zorder=3)
    xs = [l[0] for l in lanes]
    steps = [
        (xs[0], xs[1], "user types a question\n(text + category)"),
        (xs[1], xs[3], "axios POST /api/v1/gemini\nAuthorization: Bearer <jwt>"),
        (xs[3], xs[4], "axios POST generativelanguage\n...?key=$GEMINI_API_KEY"),
        (xs[4], xs[3], "candidates[0].content.parts[].text"),
        (xs[3], xs[0], "JSON { reply } -> markdown +\nreact-syntax-highlighter"),
    ]
    y = W - 20
    for a, b, lab in steps:
        arrow(ax, (a + 7, y), (b - 7, y))
        ax.text((a + b) / 2, y + 2.2, lab, ha="center", va="bottom", fontsize=6.2,
                color=INK, zorder=5, bbox=dict(fc="white", ec="none", pad=0.6))
        y -= 11
    ax.text(50, 9, "Failure path: a missing GEMINI_API_KEY, a provider 4xx/5xx or a network "
            "error is caught in aiController and returned to the browser as a JSON error object; "
            "no retry or fallback model is configured.", ha="center", va="center",
            fontsize=6.3, color="#333333")
    save(fig, "fig4_5_ai_sequence.png")


# ---------------------------------------------------------------- Fig 4.6
def fig_code():
    fig, ax = canvas(10.0, 6.2)
    W = ax.get_ylim()[1]
    ax.text(50, W - 1.2, "Code submission and Judge0 execution flow", ha="center", va="top",
            fontsize=9.2, fontweight="bold", color=INK)
    box(ax, 3, 62, 20, 16, "Monaco editor\nProblemsPage.tsx\nsource + language_id\n(Ctrl+Enter / Ctrl+Shift+Enter)",
        fill=GREY, fs=7.0)
    box(ax, 27, 62, 20, 16, "POST /api/v1/compiler\nbody: source_code (base64)\nlanguage_id (63/71/62/54/104)",
        fill=GREY, fs=6.8)
    box(ax, 51, 62, 20, 16, "compilerRoutes.js\naxios POST\njudge0-ce.p.rapidapi.com\nx-rapidapi-key header",
        fill=GREY, fs=6.8)
    box(ax, 75, 62, 22, 16, "Judge0 CE service\ncompile + execute\n(cu 2 s, mem 128 MB)",
        fill=MID, fs=7.0)
    box(ax, 27, 38, 20, 13, "Response JSON\nstatus_id, stdout,\nstderr, time", fill=GREY, fs=7.0)
    box(ax, 51, 38, 20, 13, "TestResults.tsx\nrenders status,\nstdout / stderr", fill=GREY, fs=7.0)
    arrow(ax, (23, 70), (27, 70))
    arrow(ax, (47, 70), (51, 70))
    arrow(ax, (71, 70), (75, 70))
    arrow(ax, (86, 61), (37, 51.5), rad=0.12)
    arrow(ax, (47, 44.5), (51, 44.5))
    ax.text(88, 52, "wait=true", fontsize=6.2, ha="center", color=INK)

    box(ax, 3, 14, 20, 16, "Contest path\nPOST /api/v1/contests/:id/submit\ncontestController.js",
        fill="#fbfbfb", fs=6.8)
    box(ax, 27, 14, 20, 16, "Judge0 (self-hosted)\nPOST /submissions\nthen poll GET /submissions/:token\nup to 10 x 1 s",
        fill="#fbfbfb", fs=6.6)
    box(ax, 51, 14, 20, 16, "Scoring\nEasy 100 / Medium 200 / Hard 300\n+ 20 min penalty per failed attempt",
        fill="#fbfbfb", fs=6.6)
    box(ax, 75, 14, 22, 16, "Leaderboard + rating\nnotifyContestSubmission()\nsocket emit 'submission-update'\nElo rating (K = 32)",
        fill="#fbfbfb", fs=6.6)
    arrow(ax, (23, 22), (27, 22))
    arrow(ax, (47, 22), (51, 22))
    arrow(ax, (71, 22), (75, 22))
    arrow(ax, (64, 46), (64, 31.5), ls=(0, (3, 2)), label="shared judging layer")
    save(fig, "fig4_6_code_judge_flow.png")


# ---------------------------------------------------------------- Fig 4.7
def fig_realtime():
    fig, ax = canvas(10.0, 5.8)
    W = ax.get_ylim()[1]
    ax.text(50, W - 1.2, "Real-time contest workflow (Socket.IO)", ha="center", va="top",
            fontsize=9.2, fontweight="bold", color=INK)
    box(ax, 4, 46, 24, 20, "Contest client\nContestCard / Leaderboard\nsocket.io-client\n(VITE_SOCKET_URL)", fill=GREY, fs=7.0)
    box(ax, 38, 46, 24, 20, "socket.js initSocketIO()\nhandshake: handshake.auth.token\njwt.verify -> User.findById(decoded.id)",
        fill=GREY, fs=6.8)
    box(ax, 72, 46, 24, 20, "Contest room\n'contest-<contestId>'\njoin-contest / leave-contest\nactive-count broadcast", fill=MID, fs=6.8)
    arrow(ax, (28, 56), (38, 56))
    arrow(ax, (62, 56), (72, 56))
    box(ax, 4, 22, 24, 16, "submitSolution()\nPOST /api/v1/contests/:id/submit\nverify user, problem, window", fill=GREY, fs=6.8)
    box(ax, 38, 22, 24, 16, "Judge0 grading\nstatus -> points, penalty,\nattempts (ContestSubmission)", fill=GREY, fs=6.8)
    box(ax, 72, 22, 24, 16, "notifyContestSubmission()\nemit 'submission-update'\n{ contestId, userId, problemId, status }", fill=MID, fs=6.6)
    arrow(ax, (16, 46), (16, 38.5))
    arrow(ax, (28, 30), (38, 30))
    arrow(ax, (62, 30), (72, 30))
    arrow(ax, (84, 46), (84, 38.5), ls=(0, (3, 2)), label="live update to all clients in the room")
    box(ax, 20, 4, 60, 13, "Observed limitation: the handshake resolves the user from decoded.id, while the "
        "login and signup tokens carry only decoded.userId; the lookup therefore fails and the socket "
        "is admitted with socket.user = null (the middleware calls next() instead of rejecting).",
        fill="#ffffff", fs=6.8)
    save(fig, "fig4_7_realtime_contest.png")


# ---------------------------------------------------------------- Fig 4.8
def fig_module_map():
    fig, ax = canvas(10.2, 6.4)
    W = ax.get_ylim()[1]
    ax.text(50, W - 1.2, "Front-end module map and the corresponding backend route groups",
            ha="center", va="top", fontsize=9.2, fontweight="bold", color=INK)
    box(ax, 4, 78, 20, 12, "App shell\nLayout + Sidebar\n(19 navigation items)", fill=MID, fs=7.0)
    groups = [
        (27, 82, "LEARNING", ["Learning Hub", "Video", "Notes", "Road Map"], "/api/v1/learning/*\n/api/v1/video/*\n/api/notes"),
        (27, 62, "ASSESSMENT", ["Quiz Center", "Skill Assessment", "Coding", "Interview"], "/api/v1/user-quiz\n/api/v1/assessments\n/api/v1/contests"),
        (27, 42, "CAREER", ["Resume Builder", "Cover Letter", "Placement Prep", "AI Projects"], "/api/v1/ats/scan\n(no cover-letter API)\n/client-side only"),
        (27, 22, "COMMUNITY", ["Community", "Tech Feed", "Contributors", "Study Buddy"], "/api/v1/community\n/api/v1/techfeed/latest\n/api/v1/ai/gemini"),
        (68, 52, "PRODUCTIVITY", ["Calendar", "Search", "Calculator", "Profile & Settings"], "local state +\n/api/v1/get-profile"),
        (68, 28, "ADMIN", ["Users", "Courses", "Quizzes", "Analytics & Logs"], "/api/v1/admin/*\n/api/v1/admin/analytics"),
    ]
    for x, y, name, items, api in groups:
        h = 16
        ax.add_patch(Rectangle((x, y), 27, h, fc="#fcfcfc", ec=INK, lw=1.0, zorder=1))
        ax.add_patch(Rectangle((x, y + h - 3.2), 27, 3.2, fc=MID, ec=INK, lw=1.0, zorder=2))
        ax.text(x + 13.5, y + h - 1.6, name, ha="center", va="center", fontsize=7.2,
                fontweight="bold", color=INK, zorder=3)
        ax.text(x + 1.5, y + h - 5.6, "\n".join("• " + i for i in items), ha="left", va="top",
                fontsize=6.4, color=INK, zorder=3, linespacing=1.45)
        ax.text(x + 13.5, y + 1.2, api, ha="center", va="bottom", fontsize=6.0,
                style="italic", color="#444444", zorder=3)
    arrow(ax, (24, 84), (27, 90))
    arrow(ax, (24, 84), (27, 70))
    arrow(ax, (24, 84), (27, 50))
    arrow(ax, (24, 84), (27, 30))
    arrow(ax, (54, 90), (68, 60), rad=0.15)
    arrow(ax, (54, 30), (68, 36), rad=-0.15)
    save(fig, "fig4_8_module_map.png")


if __name__ == "__main__":
    fig_architecture()
    fig_usecase()
    fig_erd()
    fig_auth()
    fig_ai_seq()
    fig_code()
    fig_realtime()
    fig_module_map()
