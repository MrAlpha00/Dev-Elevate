# -*- coding: utf-8 -*-
"""Chapter 3 (System Specification) and Chapter 4 (Design)."""

CH3 = [
    ("h1", "CHAPTER – 3", "SYSTEM SPECIFICATION"),
    ("h2", "3.1", "System Overview"),
    ("p", "Elevora AI is specified as a three-tier, service-oriented web application with a "
          "browser-resident presentation tier, an application tier that exposes a stateless "
          "REST interface together with a WebSocket channel, and a document data tier. The "
          "presentation tier is a single-page application in which every functional module "
          "is mounted inside one application shell, so that the authenticated session, the "
          "notification channel, the theme state and the navigation are shared by every "
          "module without duplication."),
    ("p", "The application tier is organised around the resource that each route group "
          "manages. Each functional area of the specification has a corresponding route "
          "module that declares its endpoints and its middleware requirements, a "
          "corresponding controller that holds the business logic, and a set of Mongoose "
          "schemas that declare the persisted form of the data. The data tier is MongoDB, "
          "reached through the Mongoose object document mapper, which permits the schema "
          "of a collection to evolve without a migration, an advantage for the "
          "document-shaped artefacts of this system such as quiz items, contest problems "
          "and learning notes."),
    ("p", "Four classes of external service are integrated. Three are inference services, "
          "used respectively for conversation, assessment and recommendation. One is a "
          "compiler service, used to execute submitted source code. Two are content "
          "services, used to supply course metadata and current news. One is a messaging "
          "service, used to deliver verification and password-reset mail. Each integration "
          "is optional at run time: the system starts, serves its static and unauthenticated "
          "resources, and degrades the corresponding module when the credential for a "
          "provider is absent."),

    ("h2", "3.2", "User Roles and Permissions"),
    ("p", "Two roles are defined. A registered learner holds the role user and may exercise "
          "every module of the application shell. An administrator holds the role admin and "
          "may additionally exercise the administration console, the authoring endpoints "
          "and the moderation endpoints. The role is stored on the user document, is copied "
          "into the issued token, and is re-read from the database on every authenticated "
          "request, so that a change of role takes effect without requiring the user to "
          "re-authenticate."),
    ("table", "Table 3.1: Roles and the permissions attached to them",
     ["Capability", "Anonymous", "User (learner)", "Admin"],
     [["View public landing, legal and documentation pages", "Permitted", "Permitted", "Permitted"],
      ["Register, verify by OTP, log in, log in with Google", "Permitted", "Permitted", "Permitted"],
      ["Access the application shell and all learner modules", "Denied", "Permitted", "Permitted"],
      ["Submit and attempt quizzes and skill assessments", "Denied", "Permitted", "Permitted"],
      ["Write, publish and share notes and community content", "Denied", "Permitted", "Permitted"],
      ["Manage learners, courses, quizzes and community content", "Denied", "Denied", "Permitted"],
      ["Read analytics, system logs and system settings", "Denied", "Denied", "Permitted"],
      ["Change system settings", "Denied", "Denied", "Permitted, with a secondary secret-key check"]],
     [3.0, 1.3, 1.4, 1.8]),
    ("p", "The permission model is enforced in three places. The presentation tier routes "
          "the administration branch through a guard component that checks the role held in "
          "the client-side session and redirects an unauthorised caller. The application "
          "tier applies an identity middleware and, where required, an authorisation "
          "middleware to the individual endpoints. The data tier is not separately "
          "protected, because no user-facing query accepts an identifier belonging to "
          "another user without an ownership test in the controller; the ownership test is "
          "present for the notes, progress, review, assessment and attempt resources and "
          "is absent for some of the administrator resources, where it is unnecessary."),

    ("h2", "3.3", "Functional Requirements"),
    ("p", "The functional requirements are derived from the route table of the server and "
          "the route table of the client, and are therefore traceable to an implementation. "
          "The status column records the state observed during the inspection described in "
          "Chapters 4 to 6. Four values are used: Implemented, where the behaviour exists "
          "in the source and was observed to work; Implemented, credential dependent, where "
          "the behaviour exists but requires a third-party credential or a running "
          "database; Partially implemented, where the endpoint group exists but some part of "
          "the behaviour is static, hard-coded or defective; and Not implemented, where the "
          "capability described in the project synopsis has no server-side counterpart."),
    ("table", "Table 3.2: Functional requirements, evidence and observed status",
     ["ID", "Requirement", "Primary evidence", "Status"],
     [["FR-01", "Register with e-mail address, name and password; verify the account by a "
                "one-time password sent over SMTP", "userRoutes.js; userController.registerUser, "
                "verifySignupOtp; utils/mailer.js; OtpToken model", "Implemented, credential dependent"],
      ["FR-02", "Authenticate with e-mail and password, or with a Google identity token",
       "AuthContext.tsx; userController.loginUser, googleUser; firebase.ts", "Implemented"],
      ["FR-03", "Issue a signed token at authentication and present it on subsequent requests",
       "authMiddleware.authenticateToken; axiosinstance.ts request interceptor", "Implemented (see NFR-09)"],
      ["FR-04", "Restrict administration functionality by role", "ProtectedRoute component; "
       "requireAdmin and authorize middleware", "Implemented, with exceptions (see Section 6.4)"],
      ["FR-05", "Display a dashboard summarising points, streak, goals, progress, recent "
                "attempts and achievements", "dashboardRoutes.js; dashboardController.js; "
                "Dashboard component group", "Partially implemented (static seed values on the client)"],
      ["FR-06", "Follow structured learning tracks for DSA, Java, MERN and AI/ML with "
                "module progress, notes and reviews", "javaRoutes, aimlRoutes, mernRoutes, "
                "dsaRoutes; Notes, Reviews and Progress models", "Implemented"],
      ["FR-07", "Attempt author-written quizzes with timing, scoring and a history of attempts",
       "quizRoutes.js; userQuizRoutes.js; Quiz and QuizAttempt models", "Implemented"],
      ["FR-08", "Generate a quiz on a chosen topic and difficulty", "aiController.generateAIQuiz; "
       "AIQuizGenerator component", "Implemented, credential dependent"],
      ["FR-09", "Generate a skill assessment across five domains, submit answers and receive a "
                "scored evaluation with an improvement plan", "assessmentController.js "
       "(TRACK_CONFIG); assessmentRoutes.js; SkillAssessment model", "Implemented, credential dependent"],
      ["FR-10", "Write source code in an embedded editor, run it and read compiler output",
       "CodeEditor.tsx; ProblemsPage.tsx; compilerRoutes.js", "Implemented, credential dependent"],
      ["FR-11", "Participate in a timed contest with a live leaderboard and a rating",
       "contestController.js; socket.js; Contest, Problem and ContestSubmission models",
       "Implemented, credential dependent (see Section 4.8)"],
      ["FR-12", "Ask the AI Study Buddy for help on learning, career or general questions",
       "Chatbot.tsx; aiRoutes.js; aiController.getAIReply", "Implemented, credential dependent"],
      ["FR-13", "Create, edit, publish, search, like and attach files to notes",
       "notesRoutes.js; notesController.js; Notes model", "Partially implemented (the like "
       "operation fails on a schema mismatch)"],
      ["FR-14", "Ask and answer questions in a community forum with resolution marking and "
                "acceptance of an answer", "communityRoutes.js; Question and Answer models",
       "Implemented"],
      ["FR-15", "Build a résumé from structured forms, scan it for applicant-tracking-system "
                "compatibility and export it", "ResumeBuilder components; atsRoutes.js; "
                "atsController.js; utils/keywordExtractor.js", "Implemented, credential dependent (scan)"],
      ["FR-16", "Compose and export a cover letter", "CoverLetter.tsx (jsPDF export)", "Implemented on the client only; "
                "no server-side module exists"],
      ["FR-17", "Follow a career roadmap by role or by skill", "Roadmap.jsx; "
                "assets/json/rolebasedRoadmaps.json and skillbasedRoadmaps.json", "Implemented (static data)"],
      ["FR-18", "Read current technology news and career updates", "newsRoutes.js; "
                "newsAggregator.js (NewsAPI); TechFeed component", "Implemented, credential dependent"],
      ["FR-19", "Track video progress, bookmark videos and resume a course",
       "videoProgressRoutes.js; VideoProgress and SavedVideo models", "Implemented"],
      ["FR-20", "Search across the platform", "utils/search.ts; utils/semanticSearch.js",
       "Implemented on the client only"],
      ["FR-21", "Receive in-application notifications and read or delete them",
       "notificationRoutes.js; Notification model; NotificationContext", "Implemented"],
      ["FR-22", "Administer users, courses, quizzes, community content, feedback, analytics, "
                "logs and settings", "adminRoutes.js; adminCourseRoutes.js; adminFeedbackRoutes.js; "
                "analytics.js; SystemSettingRoute.js", "Partially implemented (see Section 6.4)"],
      ["FR-23", "Take a paid subscription for premium features", "PremiumPage.tsx; PaymentPage.tsx",
       "Not implemented as a server-side capability; the client links to externally hosted "
       "checkout pages and the server contains no payment route or model"]],
     [0.6, 2.5, 2.6, 1.7]),

    ("h2", "3.4", "Non-Functional Requirements"),
    ("p", "The non-functional requirements are stated as design obligations, and the "
          "measured position is reported only where a measurement was actually taken. No "
          "response-time target, throughput figure or availability guarantee is asserted, "
          "because the repository contains no load-test evidence, and the deployed "
          "application could not be exercised with a measurable concurrent workload during "
          "this evaluation."),
    ("table", "Table 3.3: Non-functional requirements and the position observed",
     ["ID", "Requirement", "Design obligation", "Position observed"],
     [["NFR-01", "Usability", "A single navigation shell of nineteen modules shall be reachable "
                "from every authenticated page", "Met: the sidebar and navbar expose the same "
                "nineteen entries and the catch-all route resolves unknown paths to the dashboard"],
      ["NFR-02", "Maintainability", "The server shall separate route declaration, business logic "
                "and persistence", "Met by convention across thirty route modules, twenty-four "
                "controllers and thirty-two models"],
      ["NFR-03", "Portability", "The client shall build and run without platform-specific code",
       "Met: the build completed and the client was served from a static host in the "
       "evaluation environment"],
      ["NFR-04", "Accessibility", "Interactive controls shall carry labels and be keyboard reachable",
       "Partially met: the editor registers keyboard shortcuts, but no formal accessibility "
       "audit was performed"],
      ["NFR-05", "Availability of optional integrations", "Absence of a third-party credential "
                "shall not prevent the application from starting", "Met: the client and the server "
                "start without any provider credential; the affected module reports an error"],
      ["NFR-06", "Data model flexibility", "New fields shall be persistable without a schema "
                "migration", "Met by the use of the document data model, at the cost of the "
                "schema discipline discussed in Section 3.8"],
      ["NFR-07", "Real-time responsiveness", "Contest submission state shall be broadcast to the "
                "participants of a contest", "Implemented in code; not observed in operation because "
                "the socket handshake does not resolve the user (Section 4.8)"],
      ["NFR-08", "Input hygiene", "Text submitted by users shall be sanitised before it is stored "
                "or rendered", "Partially met: a sanitising middleware is applied globally, but "
                "the validator module is not attached to any route"],
      ["NFR-09", "Session integrity", "Every authenticated request shall carry an identity that "
                "the server can verify", "Defective: the client interceptor and the session "
                "context use two different storage keys, so the bearer token is not attached "
                "(Section 6.3)"],
      ["NFR-10", "Credential custody", "No provider credential shall be delivered to the browser",
       "Not met: the Groq and Gemini keys are inlined into the client bundle by the build tool "
       "(Section 3.9)"]],
     [0.6, 1.3, 2.4, 3.1]),

    ("h2", "3.5", "Hardware, Software and Development Requirements"),
    ("p", "The development of the project requires a workstation capable of running the "
          "client build, a Node.js runtime, a MongoDB instance and an editor with support "
          "for the two languages used. The following requirements are stated for the "
          "development environment; the runtime requirements of the deployed system are "
          "substantially smaller."),
    ("b", "A 64-bit workstation with at least 8 GB of memory and 10 GB of free disk space; "
          "the client dependency tree occupies approximately 400 MB and the server "
          "approximately 100 MB."),
    ("b", "Node.js version 20.19 or later, which is the version required by the Vite 7 "
          "bundler used by the client. The client manifest declares a lower bound, which is "
          "insufficient for the bundled toolchain."),
    ("b", "A MongoDB instance, either local or hosted, reachable through a connection string "
          "supplied in the environment. The server terminates the process if the connection "
          "fails."),
    ("b", "A Chromium-based browser for the client and an SMTP account for the verification "
          "and password-reset messages."),
    ("b", "Third-party credentials for the inference services, the compiler service, the "
          "YouTube interface and the news interface, each of which may be absent for local "
          "development at the cost of the corresponding module."),
    ("p", "The deployment requirements are a static host for the client and a Node.js host "
          "for the server. The client deployment configuration observed in the repository "
          "specifies a build command, an output directory and a rewrite rule that sends "
          "every unmatched path to the single-page entry point."),

    ("h2", "3.6", "Technology Stack"),
    ("p", "Table 3.4 records the technology stack with the version declared in the "
          "lockfile and the purpose that each component actually serves in this "
          "repository. Where the project synopsis names a technology that the inspected code "
          "does not use, the discrepancy is recorded in the final column."),
    ("table", "Table 3.4: Technology stack, declared version and actual use",
     ["Layer", "Component", "Version", "Purpose in this system"],
     [["Client", "React / React DOM", "18.3.1", "Component model for nineteen modules and the "
       "administration console"],
      ["Client", "TypeScript", "5.5.3", "Type discipline across 181 TSX and 36 TS source files"],
      ["Client", "Vite", "7.1.12", "Development server, hot replacement and production bundling"],
      ["Client", "React Router DOM", "7.12.0", "Client-side routing and route guarding"],
      ["Client", "Tailwind CSS", "3.4.1", "Utility styling and the design token set "
       "(electric, neon, cyber palettes)"],
      ["Client", "Radix UI and shadcn primitives", "1.1 – 2.2", "Accessible dialog, tab, select, "
       "dropdown and toast primitives"],
      ["Client", "Monaco Editor", "0.53.0", "In-browser code editing with language services"],
      ["Client", "Axios", "1.11.0", "HTTP access to the application tier, with an interceptor "
       "that attaches the bearer token"],
      ["Client", "Socket.IO client", "4.8.1", "Contest room membership and live updates"],
      ["Client", "jsPDF and html2pdf.js", "4.0.0 / 0.14.0", "Résumé and cover-letter PDF export"],
      ["Client", "Firebase SDK", "12.4.0", "Google identity token acquisition on the client"],
      ["Client", "Stripe libraries", "18.3.0 / 7.6.1", "Declared but not used to create a "
       "payment session; the client links to externally hosted payment pages"],
      ["Server", "Node.js with Express", "5.2.1", "REST interface, middleware pipeline, static "
       "file serving"],
      ["Server", "Mongoose and the MongoDB driver", "8.16.4 / 6.20.0", "Persistence of "
       "thirty-two collections"],
      ["Server", "jsonwebtoken", "9.0.2", "Token signing and verification"],
      ["Server", "bcrypt and bcryptjs", "6.0.0 / 3.0.2", "Password hashing and comparison"],
      ["Server", "Socket.IO", "4.8.1", "Contest rooms, participant counts, submission updates"],
      ["Server", "OpenAI SDK", "4.104.0", "Skill-assessment item generation and evaluation"],
      ["Server", "Nodemailer", "7.0.11", "One-time-password and password-reset mail over SMTP"],
      ["Server", "PDFKit", "0.17.1", "Generation of interview, system-design and cheatsheet "
       "guides in a separate service on port 3001"],
      ["Server", "sanitize-html", "2.17.0", "Global input sanitisation middleware"],
      ["Server", "express-rate-limit", "8.1.0", "Throttling of the password-change endpoint"],
      ["External", "Google Gemini 2.0 Flash", "API", "Study Buddy replies, quiz generation, note "
       "generation (invoked from the server and, in one path, from the client)"],
      ["External", "OpenAI model (configurable)", "API", "Skill-assessment questions and scoring"],
      ["External", "Groq, LLaMA 3 8B", "API", "Project recommendations, called directly from the browser"],
      ["External", "Judge0", "API", "Compilation and execution of submitted source code"],
      ["External", "YouTube Data API v3", "API", "Course metadata and video catalogue"],
      ["External", "NewsAPI", "API", "Technology news aggregation"]],
     [0.8, 1.7, 1.0, 3.2]),
    ("p", "Two discrepancies between the project synopsis and the inspected code deserve "
          "statement. The synopsis attributes the conversational assistant to Gemini and "
          "the assessment engine to the OpenAI interface with GPT-4; in the code the "
          "assessment model is named by an environment variable and the conversational "
          "assistant is served through a backend route that proxies to Gemini 2.0 Flash, so "
          "the functional allocation in the synopsis is broadly correct. The synopsis, "
          "however, lists the cover letter and the payments integration as features of the "
          "platform. The cover letter exists only as a client component with a browser-side "
          "export, and no payment integration exists on the server at all; the server's "
          "subscription module is a newsletter sign-up that stores an e-mail address."),

    ("h2", "3.7", "External Services and Dependencies"),
    ("p", "The dependencies of the system on external services are summarised in Table 3.5 "
          "together with the behaviour observed when the corresponding credential is "
          "absent. This table is central to the verification chapters, because it explains "
          "why several modules could not be exercised end to end in the evaluation "
          "environment."),
    ("table", "Table 3.5: External services, credentials and degradation behaviour",
     ["Service", "Used by", "Credential", "Behaviour when absent or unreachable"],
     [["Gemini inference", "aiController.js for the Study Buddy, quiz and note generation",
       "GEMINI_API_KEY", "The request fails and the error object is returned to the client; "
       "no alternative provider is attempted"],
      ["OpenAI inference", "assessmentController.js and dashboardController.js",
       "OPENAI_API_KEY and the model name", "Assessment generation fails; the dashboard falls "
       "back to three hard-coded project suggestions"],
      ["Groq inference", "utils/groqAPI.ts, called from the browser", "VITE_GROQ_API_KEY",
       "The client helper falls back to a locally generated response"],
      ["Judge0 through RapidAPI", "compilerRoutes.js for the practice workspace",
       "RAPID_API_KEY", "Compilation does not occur and no result is returned"],
      ["Judge0, self-hosted", "contestController.js for contest submissions",
       "JUDGE0_API_URL, JUDGE0_API_KEY and JUDGE0_HOST", "Submissions cannot be graded and "
       "the leaderboard does not advance"],
      ["YouTube Data v3", "utils/youtubeService.js and adminCourseController.js",
       "YOUTUBE_API_KEY", "The service returns a built-in mock catalogue of courses"],
      ["NewsAPI", "newsAggregator.js and the latest-news handler in userController.js",
       "NEWS_API_KEY", "The feed endpoint returns an error status"],
      ["SMTP over Gmail", "utils/mailer.js for verification and reset messages",
       "MAIL_USER and MAIL_PASS", "Registration cannot be completed and the password-reset "
       "link cannot be delivered"],
      ["MongoDB", "config/db.js", "MONGO_URI", "The server logs the failure and terminates"],
      ["Firebase client", "utils/firebase.ts for the Google identity flow",
       "VITE_FIREBASE_* variables", "The Google sign-in button cannot complete the exchange"]],
     [1.4, 2.3, 1.6, 2.4]),

    ("h2", "3.8", "Database and Storage Approach"),
    ("p", "The data tier is a document database accessed through the object document mapper. "
          "Thirty-two schemas are defined, of which twenty-nine are reachable from a route "
          "or a controller; three are declared and never imported, and one is an empty file "
          "that defines no schema at all. The principal collections and their relationships "
          "are summarised in Table 3.6 and are drawn in the entity-relationship diagram of "
          "Figure 4.4."),
    ("table", "Table 3.6: Principal collections, purpose and notable fields",
     ["Collection", "Purpose", "Principal fields"],
     [["User", "Account, credential and gamification state",
       "name, email, password hash, role, googleId, streak, points and goal counters"],
      ["OtpToken", "One-time passwords for registration and password reset",
       "email, otp, purpose, expiry, verification flag"],
      ["Notes", "User notes, shared notes and generated notes",
       "userId, title, content, topicId, topicName, isAiGenerated, tags, isPublic, files, likes, views"],
      ["Reviews, Progress", "Per-topic ratings and completion state in the learning tracks",
       "userId, topicId, rating, comment, completed, timestamps"],
      ["Course, LearningModule, AdminCourse", "Course catalogue, module structure and "
       "administrator-authored course records", "courseId, title, description, modules, "
       "youtube metadata, module order"],
      ["Quiz, QuizAttempt", "Authored instruments and the learner's responses",
       "title, topic, difficulty, questions, answers, score, totalQuestions, timeTaken, completedAt"],
      ["SkillAssessment", "Generated assessments and evaluations",
       "track, questions, answers, score, accuracy, skillLevel, improvements, roadmap"],
      ["Contest, Problem, ContestSubmission", "Contest definition, problem statements and judged "
       "submissions", "title, startTime, status, problems, statement, testCases, difficulty, "
       "status, points, penalty, attempts"],
      ["VideoProgress, SavedVideo", "Watch position and bookmarks",
       "userId, videoId, courseId, watchedSeconds, completed"],
      ["Question, Answer", "Community discussions", "question, answers, accepted answer, resolved flag"],
      ["Notification", "In-application alerts", "userId, message, type, read"],
      ["AdminLog, SystemSettings, Feedback, Faq, ContactSupport, Subscriber, VisitingWebsite",
       "Administration, configuration and ancillary records",
       "action, adminId, settings key and value, content, email, count"]],
     [1.6, 2.3, 3.4]),
    ("p", "Three properties of the storage approach are worth recording. First, the schema "
          "of a collection is declared in code and enforced by the mapper at run time, with "
          "unknown fields discarded by default; this strictness is the direct cause of the "
          "defect in the note-liking operation reported in Section 6.4, in which the route "
          "writes a field that the schema does not declare. Second, several collections carry "
          "compound indexes on the user identifier and the topic identifier, and on the "
          "visibility and topic pair, which are the access patterns of the notes listing. "
          "Third, file attachments are stored on the file system of the server and are "
          "served as static content from a dedicated path, with the metadata held in the "
          "notes collection; this choice avoids placing binary data in the document store but "
          "requires that the server file system be writable and that it be shared if the "
          "server is replicated."),

    ("h2", "3.9", "Security and Privacy Considerations"),
    ("p", "The system stores personal data of three kinds: credentials and identity data, "
          "learning and assessment activity, and free-text content created by users. The "
          "following controls are present in the code."),
    ("b", "Passwords are hashed with a memory-hard key derivation function before storage "
          "and compared in constant time by the library."),
    ("b", "Tokens are signed with a secret held in the environment and are delivered in a "
          "cookie declared HTTP-only and secure, with a same-site policy and a three-day "
          "expiry."),
    ("b", "Every mutating and reading route that exposes personal data requires an "
          "authenticated identity, and the routes that expose administrative resources "
          "additionally require the administrative role."),
    ("b", "All request bodies, query strings and route parameters pass through a "
          "sanitising middleware that removes unsafe markup before the value reaches a "
          "controller."),
    ("b", "The password-change endpoint is throttled by a dedicated rate limiter."),
    ("b", "Updates to the system configuration additionally require a secondary secret "
          "supplied in a header, which separates the configuration operation from ordinary "
          "administrator activity."),
    ("p", "The following weaknesses were identified and are reported honestly rather than "
          "omitted."),
    ("b", "Two provider credentials are compiled into the browser bundle, because the build "
          "tool inlines every variable prefixed for client exposure. Any visitor can extract "
          "them and use them at will. The correct remedy is to proxy these calls through "
          "the server, as the conversational path already does."),
    ("b", "A signing secret is committed in a utility script at the root of the client "
          "directory, and a news service credential appears as a literal in the server "
          "source. Neither value is reproduced in this report, and both should be rotated "
          "and removed from the repository."),
    ("b", "The administration feedback group and the compiler, the conversational and the "
          "résumé-scanning endpoints are reachable without authentication, which exposes "
          "them to anonymous use."),
    ("b", "The socket handshake resolves the user from a claim that the login token does "
          "not contain, and admits the connection when resolution fails, so that the "
          "real-time channel carries no authenticated identity."),
    ("b", "The cookie is declared secure unconditionally, which prevents the session from "
          "being established over plain HTTP in a local development environment."),
    ("b", "The application trusts forwarded protocol headers unconditionally, which "
          "weakens the address-based logic of the rate limiter when the service is deployed "
          "behind a proxy that does not overwrite the header."),

    ("h2", "3.10", "Assumptions and Constraints"),
    ("b", "A MongoDB instance is available and reachable; the design does not provide for a "
          "relational alternative."),
    ("b", "The inference services continue to expose the interfaces used by the code, namely "
          "a content generation endpoint for Gemini and a chat completion endpoint for the "
          "OpenAI and Groq compatible interfaces."),
    ("b", "A Judge0-compatible service is available with the language identifiers assumed "
          "by the code, in particular the identifiers for C, C++, Java, Python and JavaScript."),
    ("b", "The browser environment supports the modern JavaScript and CSS features used by "
          "the client and the editor."),
    ("b", "For the deployment to function as a whole, the client and the server must be "
          "reachable under a single origin, or a proxy rule must be configured; the "
          "deployment configuration observed in the repository rewrites every unmatched "
          "path to the client entry point and therefore does not, by itself, proxy the "
          "interface paths to the server."),

    ("h2", "3.11", "Feasibility Analysis"),
    ("p", "The project is technically feasible within the stated constraints. Every "
          "component it depends upon is either a freely available library or a documented "
          "commercial interface, and the architecture requires no capability that is not "
          "present in the inspected runtime. The volume of code, approximately forty-two "
          "hundred files in total, is at the upper end of what a small team can maintain but "
          "is consistent with the open source contribution model that the project adopts."),
    ("p", "The project is economically feasible in the sense that its running cost is "
          "dominated by the free tiers of the third-party services and by a static host and "
          "a small application host for the server. The principal cost exposure is the "
          "inference services, which are metered per token or per request."),
    ("p", "The project is operationally feasible for its intended scale. The observed "
          "operational weaknesses are concentrated in configuration rather than in design, "
          "and the majority of them are corrected by a small number of changes: aligning the "
          "client storage keys, adding the identity middleware to the three unprotected "
          "route groups, reconciling the token claims with the socket handshake, and moving "
          "the two browser-exposed provider credentials behind the server."),
]

CH4 = [
    ("h1", "CHAPTER – 4", "DESIGN"),
    ("h2", "4.1", "Design Principles"),
    ("p", "The design of Elevora AI follows five principles that were applied consistently "
          "in the source and that are visible in the structure of the repository."),
    ("n", "One shell, many modules. The application shell owns the session, the navigation, "
          "the notification channel and the theme. A module is added by registering a route "
          "and, where required, a navigation entry; it does not introduce a second shell."),
    ("n", "Identity once, applied everywhere. A single token, issued once, is understood by "
          "the route guard on the client, by the identity middleware on the server, by the "
          "file-upload path and by the socket handshake. This is the principle that the "
          "defect discussed in Section 4.8 violates."),
    ("n", "The server decides. Every mutation is performed by the server, which owns the "
          "authorisation check, the ownership test and the persistence. The client owns "
          "presentation and, in the documented exceptions of the résumé and cover-letter "
          "modules, the local document state."),
    ("n", "Graceful degradation at the boundary. A module whose external service is "
          "unavailable reports an error rather than preventing the application from "
          "loading; the exception is the practice workspace, whose compiler endpoint has no "
          "fallback."),
    ("n", "No code without a route. Every persistent entity in the data model is reachable "
          "from an endpoint, except for the three orphaned schemas, which are recorded as "
          "such in Table 3.6."),

    ("h2", "4.2", "Overall System Architecture"),
    ("p", "Figure 4.1 presents the overall architecture of the system as three horizontal "
          "bands. The upper band is the presentation tier: the single-page application with "
          "its nineteen learner modules, the embedded code workspace, the conversational "
          "panel, the administration console and the socket client. The middle band is the "
          "application tier, in which the route groups are shown in the grouping actually "
          "used by the server. The lower band is the data tier, in which the principal "
          "collections are grouped by the functional area that owns them. Beneath these, a "
          "fourth band represents the external services with which the application tier and, "
          "in two documented cases, the presentation tier communicate directly."),
    ("fig", "figures/fig4_1_architecture.png",
     "Fig. 4.1: Overall system architecture of Elevora AI", 6.1),
    ("p", "Three characteristics of the architecture deserve comment. The application tier "
          "is stateless with respect to the client, which permits any number of instances "
          "behind a load balancer; the only server-side session state is the file system "
          "that holds note attachments. The presentation tier communicates with the "
          "application tier through three channels: the HTTP interface for request and "
          "response, the WebSocket channel for contest events, and the static path for note "
          "attachments. The third characteristic is that the diagram does not show the "
          "single-page rewrite in the deployment configuration, which sends unmatched paths "
          "to the client entry point; the consequence of that configuration for the "
          "interface paths is discussed in Section 6.3."),

    ("h2", "4.3", "Module Organisation and Component Boundaries"),
    ("p", "The client is organised by feature rather than by layer. The pages directory "
          "holds the routed screens, the components directory holds the shared and "
          "feature-specific components, the contexts directory holds the four providers that "
          "carry cross-module state, the services directory holds the modules that wrap the "
          "HTTP client, and the api directory holds the thin endpoint wrappers used by the "
          "administration and assessment screens. Figure 4.2 maps the nineteen navigation "
          "entries to their functional groups and to the server route group that serves "
          "each one, and it marks the two groups for which the server provides no support."),
    ("fig", "figures/fig4_8_module_map.png",
     "Fig. 4.2: Front-end module map and the corresponding server route groups", 6.1),
    ("p", "The server follows a matching convention. A functional area has one route file, "
          "one or more controller files and one or more model files. The route file "
          "declares the mount path relative to the application root, the HTTP method, the "
          "middleware chain and the handler. The controller holds the logic and owns the "
          "interactions with the models and with the external services. The model declares "
          "the schema, the indexes and, where the schema benefits from it, the virtual "
          "properties. This convention is followed consistently by the thirty route modules, "
          "which is why a reader can move from the API documentation published by the "
          "application to the implementing file in a single step."),

    ("h2", "4.4", "Use-Case Model"),
    ("p", "Figure 4.5 states the use-case model of the system. The learner actor performs "
          "sixteen use cases, grouped in the figure into registration and profile "
          "management, learning, assessment, code practice, contest participation and "
          "community participation. The administrator actor performs six use cases, all of "
          "which are drawn inside the administration boundary. The external services actor "
          "is connected to the code practice use case, because the execution of a submitted "
          "program is delegated to the compiler service rather than performed by the "
          "platform."),
    ("fig", "figures/fig4_2_usecase.png",
     "Fig. 4.3: Use-case diagram for the learner, the administrator and the external services", 6.1),
    ("p", "The use-case model clarifies an important boundary of the system. The platform "
          "does not itself place the learner in employment: the placement module supplies "
          "prepared material and links, and the résumé and cover-letter modules produce "
          "documents, but no recruitment workflow is implemented. Similarly, the community "
          "module implements question and answer exchange with resolution marking and "
          "acceptance, but no messaging or notification between members beyond the general "
          "notification channel is provided."),

    ("h2", "4.5", "Data Model and Entity Relationships"),
    ("p", "The entity-relationship diagram of Figure 4.4 is derived directly from the "
          "Mongoose schemas. The diagram shows the eleven entities that are the subject of "
          "reference relationships and omits the remaining collections, which are "
          "independent of the others."),
    ("fig", "figures/fig4_3_erd.png",
     "Fig. 4.4: Entity-relationship model derived from the Mongoose schemas", 6.2),
    ("p", "The central entity is the user, to which the notes, the reviews, the progress "
          "records, the quiz attempts, the skill assessments, the contest submissions, the "
          "video progress records and the notifications are all attached. The quiz and the "
          "contest form two further aggregate roots, each with a child collection that "
          "records a completed activity: an attempt for a quiz and a submission for a "
          "contest. The remaining entities are weak in the sense that they have no "
          "independent lifecycle."),
    ("p", "Two modelling decisions are worth recording. The note entity carries an array of "
          "user identifiers for the likes and a virtual property that exposes the count of "
          "those identifiers; the property is declared as a getter only, with no setter, "
          "which is correct for a derived value but means that the route that attempts to "
          "assign to it fails at run time. The contest submission entity carries both the "
          "number of attempts and the accumulated penalty, which are computed by the "
          "controller at judging time and stored, so that the leaderboard can be computed "
          "without recomputing the scoring rule."),

    ("h2", "4.6", "Authentication and Authorisation Flow"),
    ("p", "Figure 4.5 shows the flow of the authentication and authorisation processes. Two "
          "paths reach a token: the registration path, in which a one-time password is "
          "mailed to the applicant and verified against the stored token record, and the "
          "credential path, in which the password is compared with the stored hash. A third "
          "path, the Google path, exchanges an identity token obtained by the client "
          "library for a session token. All three issue a token whose payload contains the "
          "user identifier and the role."),
    ("fig", "figures/fig4_4_auth_flow.png",
     "Fig. 4.5: Authentication, token issuance and role-based authorisation flow", 6.1),
    ("p", "On each subsequent request the identity middleware reads the token from the "
          "cookie or from the authorization header, verifies the signature, loads the user "
          "record with the password excluded, and attaches the record to the request. The "
          "authorisation middleware then compares the role in that record with the role the "
          "route requires, and rejects the request with a status of 401 when the identity "
          "is absent or invalid and 403 when the role is insufficient. The design intent is "
          "that identity is always established before authorisation is evaluated; the "
          "inspection identified route groups that invert this order, and the consequence "
          "is recorded in Section 6.4."),

    ("h2", "4.7", "Artificial Intelligence Request and Response Flow"),
    ("p", "The artificial-intelligence features of the system are reached in three ways. "
          "Figure 4.6 traces the conversational path, in which the learner types a question "
          "in the Study Buddy panel, the client posts it to the server route, the controller "
          "forwards it to the Gemini content generation interface with the provider key "
          "taken from the environment, and the reply is returned to the browser and rendered "
          "as Markdown with syntax highlighting."),
    ("fig", "figures/fig4_5_ai_sequence.png",
     "Fig. 4.6: Request and response sequence for the AI Study Buddy", 6.1),
    ("p", "The generative path differs in that the output is stored rather than displayed. "
          "When the learner requests a generated quiz, the controller builds a prompt from "
          "the requested topic, difficulty and question count, sends it to the provider, "
          "parses the returned items, assembles a quiz document with its questions and "
          "returns it, after which the learner may attempt it through the ordinary quiz "
          "interface and the resulting attempt is scored against the stored items. The "
          "note-generation path is analogous: the generated text is stored as a note with "
          "the flag that identifies it as machine-generated, so that it can be listed "
          "separately from the learner's own material."),
    ("p", "The assessment path is the most structured of the three. The controller holds a "
          "configuration table of five tracks, each of which specifies the domain, the "
          "number of items and the prompt template, and it uses the OpenAI interface to "
          "generate the items and, in a second pass, to evaluate the learner's answers and "
          "produce a score, an accuracy, an identified set of weaknesses and a generated "
          "improvement plan. The generated instrument and the responses are both persisted "
          "with the attempt, which makes the evaluation reproducible."),

    ("h2", "4.8", "Code Submission and Execution Flow"),
    ("p", "Figure 4.7 describes the two execution paths of the system. The practice path "
          "begins in the embedded editor, where the learner writes source code in one of "
          "the supported languages and triggers the run or submit action with the keyboard "
          "or with the toolbar. The client base64-encodes the source, selects the numeric "
          "language identifier from a local table, and posts the pair to the compiler route "
          "of the server. The route forwards the request to the Judge0 instance exposed "
          "through a public application programming interface aggregator, with the "
          "synchronised wait option so that the response carries the result of the run."),
    ("fig", "figures/fig4_6_code_judge_flow.png",
     "Fig. 4.7: Code submission and Judge0 execution flow for practice and for contests", 6.1),
    ("p", "The contest path is more elaborate. The submission is accepted only when the "
          "contest is open and the participant is registered, the source is posted to the "
          "configured Judge0 instance, and the server polls for the result at intervals of "
          "one second for up to ten attempts. The grading rule awards a fixed number of "
          "points according to the difficulty of the problem and adds a penalty of twenty "
          "minutes for each previous failed attempt on the same problem. The outcome is "
          "stored as a submission document and is broadcast to the contestants of the "
          "room."),
    ("p", "The design contains one inconsistency that the evaluation confirmed: the "
          "practice path and the contest path use different Judge0 endpoints, different "
          "authentication mechanisms and different waiting strategies, and the practice "
          "path additionally hard-codes the host and port of the server rather than "
          "deriving it from the configured interface base address. Consequently the run "
          "button of the practice workspace cannot succeed in a deployed environment in its "
          "present form, as recorded in Chapter 6."),

    ("h2", "4.9", "Real-Time Contest Workflow"),
    ("p", "The contest module is the only part of the system that uses the WebSocket "
          "channel. Figure 4.8 shows the workflow. The client establishes a socket "
          "connection, presenting a token in the handshake, and then emits an event that "
          "causes it to join the room named for the contest. The server maintains the "
          "participant count for the room and broadcasts it. When a submission is judged, "
          "the controller notifies the socket layer, which emits an event carrying the "
          "contest identifier, the participant, the problem and the status to every member "
          "of the room."),
    ("fig", "figures/fig4_7_realtime_contest.png",
     "Fig. 4.8: Real-time contest workflow over the Socket.IO channel", 6.0),
    ("p", "The handshake middleware in the server is intended to bind the socket to an "
          "authenticated user by verifying the token presented in the handshake and loading "
          "the corresponding user record. The implementation resolves the user from a "
          "claim named as the identifier, whereas the tokens issued by the registration, "
          "verification, credential and Google paths carry only a claim named as the user "
          "identifier. The lookup therefore fails, the middleware catches the failure and "
          "admits the connection with a null user rather than rejecting it. The practical "
          "consequence is that the room membership and the broadcast mechanism operate "
          "correctly, while the identity of the socket is not established; this is "
          "reported in Chapter 6 as a defect with a specified correction."),

    ("h2", "4.10", "Administration Workflows"),
    ("p", "The administration console is mounted on a distinct branch of the client route "
          "table and renders nine modules: an overview, user management, content "
          "management, community moderation, news updates, quiz management, analytics, "
          "system logs and system settings, together with a feedback module. The server "
          "supports these with four route groups: the administration group for users and "
          "system logs, the administration course group for authored course records and "
          "the import of course metadata from the video service, the administration quiz "
          "group for the authoring of quizzes and questions and the retrieval of "
          "submissions, and the analytics group for the aggregate statistics and their "
          "export as a delimited text file."),
    ("p", "The settings module is the most sensitive of the nine, because it controls "
          "whether the platform accepts new registrations and whether it is placed in "
          "maintenance mode. Its update operation requires the administrator role and, in "
          "addition, a secondary secret supplied in a header, which is a form of two-factor "
          "authorisation that depends on a shared secret rather than on a second "
          "credential. The audit trail is provided by the system log collection, which "
          "records the administrator, the action and the timestamp of each recorded "
          "operation."),

    ("h2", "4.11", "User Interface Design"),
    ("p", "The interface follows the design system described by the client configuration. "
          "A utility-first stylesheet with four extended colour scales supplies the visual "
          "language; a component library of headless primitives supplies accessible "
          "dialog, tab, select, dropdown, label and alert behaviour; and a small utility "
          "module merges conditional class names. The application supports a dark theme "
          "whose state is held in a global context and persisted in the browser."),
    ("p", "Three interface decisions are worth recording because they affect the "
          "responsiveness of the design. The navigation appears twice, once as a persistent "
          "sidebar on wide screens and once as a collapsible menu in the top bar on narrow "
          "screens, and the two menus are constructed from the same list of entries, so that "
          "a new module appears in both. The code workspace uses a split layout in which "
          "the editor, the problem description and the result panel are independently "
          "scrollable, which is appropriate for the fixed viewport of a coding contest but "
          "is cramped on a small screen. Finally, the client is not code-split: every "
          "routed screen is imported statically by the route table, including three "
          "components of more than fifty kilobytes each, so that the initial bundle "
          "carries the whole application. This is a performance defect, recorded in "
          "Chapter 6."),
]
