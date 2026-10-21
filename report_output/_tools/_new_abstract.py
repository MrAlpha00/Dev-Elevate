# -*- coding: utf-8 -*-
"""Replace the abstract with a tighter version that fits on one page."""
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
P = "report_output/_tools/content_part1.py"
s = open(P, encoding="utf-8").read()
i = s.find("FRONT = [")
j = s.find("CH1 = [")
assert i > 0 and j > i

new = '''FRONT = [
    ("h1", "ABSTRACT", None),
    ("p", "The proliferation of specialised learning platforms has left the technology student "
          "with a fragmented preparation workflow: course material is consumed on one portal, "
          "problem solving is practised on a second, résumés are assembled on a third and "
          "interview preparation on a fourth, and no single service holds the record of what "
          "the learner has actually covered. Elevora AI (Dev-Elevate) is a full-stack web "
          "application that consolidates learning, assessment, coding practice, documentation "
          "and placement preparation behind one authenticated, role-based interface."),
    ("p", "It is implemented as a React 18 single-page application in TypeScript, bundled with "
          "Vite 7, styled with Tailwind CSS 3 and shadcn/Radix primitives, and served by an "
          "Express 5 application on Node.js. Persistence is provided by MongoDB through "
          "Mongoose 8, whose thirty-two schemas cover users, learning tracks, notes, quizzes, "
          "attempts, skill assessments, contests, submissions, video progress and "
          "notifications. Authentication is stateless: JSON Web Tokens are issued after e-mail "
          "one-time-password verification or Google OAuth, delivered in an HTTP-only cookie "
          "and verified by dedicated server middleware. Artificial intelligence is supplied by "
          "three providers, namely Google Gemini 2.0 Flash for the Study Buddy, quiz and note "
          "generation, the OpenAI interface for skill-assessment generation and evaluation, "
          "and a Groq-hosted LLaMA 3 8B model for project recommendation. Code execution is "
          "delegated to Judge0, through the RapidAPI endpoint for the practice playground and "
          "a self-hosted instance for contests, where Socket.IO broadcasts live submission "
          "updates and Elo ratings are recalculated."),
    ("p", "The report documents the problem definition, the review of comparable systems, the "
          "specification derived from the source code, the architectural and data design, the "
          "implementation of each module and the verification evidence. Verification combined "
          "static review of the source tree, execution of the deployed client in a headless "
          "browser and manual exercise of the authentication path, and it distinguishes "
          "functionality observed to work from functionality that depends on third-party "
          "credentials, is presented by the interface but served by static data, or is "
          "specified but absent from the repository. Among the discrepancies reported are the "
          "absence of a server-side cover-letter module, hard-coded placement statistics and a "
          "mismatch between the token claims and the Socket.IO handshake that prevents socket "
          "authentication. The outcome is a working, if partially integrated, platform that "
          "consolidates twenty-three user-facing modules and forty-two API endpoint groups "
          "within a single repository that can be built and deployed with three commands."),
]

'''

s = s[:i] + new + s[j:]
open(P, "w", encoding="utf-8").write(s)
print("abstract replaced")
