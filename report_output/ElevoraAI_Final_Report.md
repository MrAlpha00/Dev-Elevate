# ElevoraAI - Final Project Report

**Project Title:** ElevoraAI - An AI-Powered Smart Education and Career Advancement Platform

## Abstract

ElevoraAI is an AI-powered smart education and career advancement platform integrating structured learning, AI tutoring, coding practice, real-time contests, resume and cover letter generation, ATS scanning, quizzes and skill assessments, community features, and productivity tools in a single system. This report documents the actual repository implementation (full-stack React + TypeScript + Vite frontend, Node.js/Express 5 + MongoDB backend) based on code inspection and build validation. It accurately describes implemented features, external dependencies, known issues, and validation results.

## Table of Contents

1. [Abstract](#abstract)
2. [Introduction](#1-introduction)
3. [Literature Survey](#2-literature-survey)
4. [System Specification](#3-system-specification)
5. [Design](#4-design)
6. [Implementation](#5-implementation)
7. [Result and Testing](#6-result-and-testing)
8. [Conclusion](#conclusion)
9. [Future Enhancements](#future-enhancements)
10. [References](#references)

## 1. Introduction

ElevoraAI consolidates fragmented tools. Frontend: React 18 + TypeScript + Vite + TailwindCSS; Backend: Node.js/Express 5 + MongoDB/Mongoose + Socket.IO. Integrations: Google Gemini, OpenAI, Groq, Judge0, Stripe, Firebase OAuth, NewsAPI, YouTube API. Goals include integrated learning, coding, assessments, AI, resume/cover letter, community, and admin capabilities.

## 2. Literature Survey

Existing e-learning, online judges, AI tutoring, ATS tools, and placement prep platforms solve parts but remain fragmented. ElevoraAI addresses the integration gap with role-based access and real-time contest features.

## 3. System Specification

Roles: User and Admin. Modules: Dashboard, Learning Hub, Video, Quiz Center, Skill Assessment, Coding, Interview, Study Buddy, Tech Feed, Community, Resume Builder, Cover Letter, Placement Prep, AI Projects, AI Models, Road Map, Notes, Calendar, Contributors (19 navigation items).

**Key Findings:**
- Real API-backed areas: Auth/Profile/Settings, Video/Course, Quiz, Skill Assessment, Interview, Chatbot, Admin (users/courses/analytics/logs/feedback), dashboard streak, analytics.
- Partial/hardcoded: Coding (hardcoded localhost:4000 compiler, static problems), Tech Feed fallback, NewsWidget (hardcoded API key), AI Projects fallback, dashboard achievements/insights partial.
- UI-local: Calendar/Tasks, Cover Letter, Calculator, Search (client-side), Road Map, AI Models (static).

## 4. Design

Three-tier architecture: React SPA, Express REST API + Socket.IO, MongoDB. ER based on models (User, Quiz/Question/QuizAttempt, Contest/Problem/Submission/ContestSubmission, SkillAssessment, Progress, Notes/Reviews, Notification, InterviewExperience, Course/AdminCourse, VideoProgress/SavedVideo, VisitingWebsite, etc.). Auth: JWT (cookie/header), bcrypt, OTP, Google OAuth, RBAC. AI: Gemini, OpenAI, Groq. Coding/Contests: Judge0, Socket.IO, Elo, cron finalization.

## 5. Implementation

- Frontend: react-router v7, Context API + Redux, Framer Motion, react-markdown, Monaco Editor, html2pdf/jsPDF, socket.io-client.
- Backend: Express 5, middleware (auth/authorize/sanitize), Mongoose, controllers/routes, Socket.IO.
- Build: TypeScript compiles (tsc --noEmit exit 0), Vite production build succeeds (dist/index.html + assets generated; main JS ~6.5MB).
- Known issues: localStorage token key mismatch (elevoraAiAuth vs ElevoraAIAuth), hardcoded localhost:4000 compiler URL, relative /api/user/streak in DailyGoals.tsx, hardcoded newsdata.io key in NewsWidget.tsx, VITE_GROQ_API_KEY exposed to client bundle, duplicate /api/v1/ai mounts in index.js, inconsistent RapidAPI env naming, dashboard achievements/insights stub, missing service modules noted in audit docs.

**Figures:** ![Architecture](figures/fig4_1_architecture.png) Fig 4.1 Architecture; ![Login Flow](figures/fig5_1_login_flow.png) Fig 5.1 Login Flow Demo; ![Login Form](figures/fig5_2_login_form.png) Fig 5.2 Login Form Demo

## 6. Result and Testing

Static validation: all server JS syntax checks pass; TypeScript compiles; Vite production build succeeds. Code inspection confirms core flows and model/route/controller structure. Runtime external APIs and live UI testing limited by credentials/services. Representative test cases documented (auth/RBAC, AI endpoints, Judge0/socket flows, ATS, build validation) with untested items marked as Not tested.

## Conclusion

ElevoraAI delivers a unified, role-based AI-powered learning and career platform with substantial implemented functionality and successful build validation. Honest disclosure of defects/stubs ensures accuracy; with remediation, the system is production-ready.

## Future Enhancements

Fix token-key consistency; proxy external calls server-side; broaden rate limiting; server-side Stripe checkout; persist dashboard insights/achievements; replace static learning content with DB-driven where intended; add automated tests; structured logging; capture dashboard screenshots; improve accessibility/performance.

## References

[1] React docs (react.dev). [2] Express (expressjs.com). [3] MongoDB (mongodb.com/docs). [4] Mongoose (mongoosejs.com/docs). [5] Socket.IO (socket.io/docs). [6] Judge0 (judge0.com/docs). [7] Google Gemini (ai.google.dev/docs). [8] OpenAI (platform.openai.com/docs). [9] Groq (console.groq.com/docs). [10] Stripe (docs.stripe.com). [11] Vite (vitejs.dev/guide). [12] Tailwind CSS (tailwindcss.com/docs). [13] JWT.io. [14] Monaco Editor (microsoft.github.io/monaco-editor). [15] Hamari et al., Does Gamification Work? (2014). [16] Sandhu et al., RBAC Models, IEEE Computer (1996).
