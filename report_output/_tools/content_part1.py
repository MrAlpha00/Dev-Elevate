# -*- coding: utf-8 -*-
"""Front matter, Chapter 1 and Chapter 2 of the Elevora AI final report.

Every technical statement is derived from the inspected repository
(ElevoraAI/Client, ElevoraAI/Server) or from the deployed application.
"""

FRONT = [
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

CH1 = [
    ("h1", "CHAPTER – 1", "INTRODUCTION"),
    ("h2", "1.1", "Background and Context"),
    ("p", "Software education in the past decade has been shaped by a simple observation: no "
          "single tool can be good at everything, so users stopped expecting one tool to be "
          "good at everything. A student who wants to master data structures enrols on a "
          "video-course platform, migrates to a competitive programming portal to solve "
          "problems, opens a résumé template editor to produce an application document, and "
          "finally visits an internship board to look for an opening. Each of these services "
          "is individually competent and each of them is individually successful, yet the "
          "student experiences them as separate products with separate accounts, separate "
          "credentials and separate notions of progress. The consequence is that the learner's "
          "record of achievement is scattered across data silos that cannot be queried "
          "together."),
    ("p", "This fragmentation is usually discussed in terms of convenience, but its more "
          "serious consequence is analytical. Because a course platform knows which videos "
          "were watched and a coding platform knows which problems were solved, while a "
          "résumé builder knows nothing about either, no component of the workflow can answer "
          "the questions a learner actually cares about: how much have I improved this month, "
          "which of my weaknesses is closing, and am I ready for the interview I have been "
          "invited to? A personalised recommendation is impossible without a unified view, and "
          "a personalised recommendation is precisely the capability that recent large "
          "language models have made inexpensive enough to offer at scale."),
    ("p", "At the same time, the administrative layer of educational platforms has remained "
          "thin. A college that deploys a learning platform, a coding platform and a career "
          "portal as three separate products inherits three separate reporting pipelines, "
          "three sets of credentials to administer and three opportunities for student data "
          "to be exposed. The administrator in such an institution has no consolidated view "
          "of platform usage and no single place to moderate the community, author "
          "assessments or publish content."),
    ("p", "Elevora AI was conceived against this background. The intent was not to build "
          "another course catalogue or another judge, but to build the shell that a student "
          "and an administrator can both live in: a single authenticated application whose "
          "modules share one identity, one progress model, one notification channel and one "
          "administrative control surface."),

    ("h2", "1.2", "Problem Statement"),
    ("p", "The problem addressed by this project may be stated precisely as follows: to "
          "design and implement an AI-assisted learning and career-advancement platform that "
          "consolidates structured learning, timed assessment, code practice, documentation "
          "and placement preparation into a single role-based web application, in which the "
          "learner's progress is recorded once and reused by every module, and in which the "
          "administrator has a consolidated view of users, content and usage."),
    ("p", "The problem decomposes into the following sub-problems, each of which is addressed "
          "by a specific part of the system described in this report."),
    ("n", "Identity fragmentation. A learner who uses five platforms must maintain five "
          "accounts. Elevora AI addresses this with a single registration and login surface "
          "offering e-mail OTP verification and Google OAuth, backed by one JWT session "
          "model."),
    ("n", "Progress fragmentation. Completion in one activity is invisible to the others. "
          "Elevora AI addresses this with a common user record carrying points, streaks, "
          "goals and completion counters, and with a dashboard aggregation endpoint that "
          "assembles these values from the quiz, assessment and learning collections."),
    ("n", "Absence of AI assistance in the learning loop. Elevora AI addresses this with "
          "three separate model integrations chosen for distinct purposes: Gemini for "
          "conversational help and content generation, OpenAI for item generation and "
          "assessment evaluation, and Groq for lightweight recommendation."),
    ("n", "Isolation of practice from learning. Elevora AI addresses this by embedding a "
          "Monaco-based code workspace and a contest leaderboard inside the same "
          "authenticated shell as the learning tracks."),
    ("n", "Lack of administrative consolidation. Elevora AI addresses this with a dedicated "
          "administration console exposing user management, course authoring, quiz authoring, "
          "community moderation, analytics, system logs and configuration."),
    ("h2", "1.3", "Objectives"),
    ("p", "The objectives of the project are stated below. Each objective is later mapped to "
          "the requirement identifiers of Chapter 3 and to the implementation evidence of "
          "Chapter 5, so that the extent to which it has been met can be assessed rather than "
          "asserted."),
    ("n", "O1. To consolidate the major functions of a learning and career platform into one "
          "authenticated, role-based web application with a single navigation shell."),
    ("n", "O2. To provide structured learning tracks with module and topic level progress "
          "tracking that is persisted on the server."),
    ("n", "O3. To provide an AI assistance surface for doubt resolution and for the "
          "generation of quizzes and notes."),
    ("n", "O4. To provide a working code workspace with multi-language execution and a "
          "competitive contest mode with a live leaderboard and rating."),
    ("n", "O5. To provide automated skill assessment with scored feedback and a generated "
          "improvement plan."),
    ("n", "O6. To provide career-document tooling in the form of a résumé builder with "
          "applicant-tracking-system scoring and a cover-letter generator, both exporting to "
          "PDF."),
    ("n", "O7. To provide a peer community with administrative moderation."),
    ("n", "O8. To provide an administration console with user, content, assessment, "
          "analytics, log and configuration management."),
    ("n", "O9. To secure the system with token-based authentication, role checks, input "
          "sanitisation and rate limiting on sensitive operations."),
    ("n", "O10. To document the system to academic reporting standard, including design "
          "diagrams derived from the implemented code rather than from an abstract ideal."),

    ("h2", "1.4", "Scope of the System"),
    ("p", "The scope covers the complete repository hosted at the MrAlpha00/Dev-Elevate "
          "address, comprising a client application of approximately three hundred and "
          "seventeen source files under the Client directory and a server application of one "
          "hundred and seven hand-written JavaScript files under the Server directory. The "
          "functional scope comprises twenty-three user-facing modules grouped as learning, "
          "assessment, career, community and productivity, together with nine administration "
          "modules."),
    ("p", "The following boundaries are declared explicitly so that the claims of this report "
          "may be read against them."),
    ("b", "The system is a web application. No native mobile client exists in the repository, "
          "and no offline synchronisation mechanism is implemented."),
    ("b", "Payment processing is out of scope as implemented. The client contains a plan "
          "comparison screen and links to externally hosted checkout pages; the server "
          "contains no payment provider integration, no payment route and no payment model."),
    ("b", "Video content is not hosted by the platform. The video module integrates with "
          "the YouTube Data interface and stores only progress and bookmark state."),
    ("b", "The cover-letter module is a client-side document generator. No server-side "
          "storage, retrieval or validation of cover letters exists in the inspected "
          "repository."),
    ("b", "Placement statistics are demonstration data held in a server-side constant rather "
          "than in a database collection."),
    ("b", "No automated unit or integration test suite is present in either package; the "
          "verification described in Chapter 6 is therefore manual and code-level."),

    ("h2", "1.5", "Intended Users"),
    ("p", "The primary user of the system is a student in the final two years of an "
          "undergraduate engineering or computer science programme who is preparing for a "
          "campus placement drive. This user needs a single view of the syllabus covered, a "
          "measurable record of practice, and application documents that can be produced in "
          "minutes rather than hours. A second category is the self-taught learner or career "
          "switcher who has no institutional curriculum and therefore requires an explicit "
          "roadmap. A third is the competitive programmer who needs an execution environment "
          "and a ranked contest. A fourth is the institutional administrator, typically a "
          "course coordinator, who requires visibility of activity and the ability to "
          "moderate content."),
    ("p", "The interface reflects these four profiles. The learner receives a dashboard "
          "centred on points, streaks, goals and progress; the administrator receives a "
          "separate console reached through a distinct route branch and guarded by a role "
          "check; the contestant is offered a dedicated workspace; and the self-learner is "
          "offered the roadmap and placement modules."),

    ("h2", "1.6", "Development Approach"),
    ("p", "The project was developed as two independently deployable applications. The "
          "client is a single-page application in which routing, state and data access are "
          "handled by React Router, four React contexts and a small number of service "
          "modules that wrap the Axios HTTP client. The server is a stateless REST "
          "application in which each functional area is represented by a route file that "
          "declares its endpoints, a controller file that holds the business logic, and one "
          "or more Mongoose schema files that declare the persisted shape of the data. This "
          "separation is visible in the repository as a consistent convention across all "
          "thirty route modules, twenty-four controllers and thirty-two models, and it "
          "allows a reviewer to trace any endpoint from its HTTP path to the collection it "
          "writes to."),
    ("p", "Authentication was designed as a stateless bearer-token scheme rather than as a "
          "server-side session store, which keeps the API horizontally scalable and allows "
          "the same identity to be presented to the REST layer, the file-upload layer and "
          "the WebSocket layer. Authorisation is expressed as two middleware functions: one "
          "that establishes the identity of the caller and one that compares the role stored "
          "in the database record against the role required by the route."),
    ("p", "The development of the artificial-intelligence features followed a different "
          "pattern. Rather than implementing a single provider abstraction, each model was "
          "introduced where its characteristics were most useful: Gemini for conversational "
          "response generation, the OpenAI interface for structured item generation and "
          "evaluation of skill assessments, and Groq for short recommendation prompts that "
          "must return quickly in the browser. This decision has the advantage of matching "
          "each provider's cost and latency profile to the interaction, and the disadvantage "
          "of distributing the failure modes across three separate credential sets, which is "
          "discussed in Chapter 6."),

    ("h2", "1.7", "Organization of the Report"),
    ("p", "The remainder of the report is organised in the conventional order of a software "
          "engineering project report. Chapter 2 reviews the classes of existing system that "
          "the project draws upon and compares their characteristics with those of Elevora "
          "AI. Chapter 3 states the system specification, including the functional and "
          "non-functional requirements, the technology stack, the external dependencies and "
          "the assumptions on which the design rests, together with a requirement "
          "traceability table that records the observed status of each requirement. Chapter 4 "
          "describes the design, presenting the architecture, the role model, the data "
          "model, the principal workflows and eight diagrams derived from the implemented "
          "code. Chapter 5 describes the implementation module by module, with the directory "
          "layout, the routing table, the endpoint groups, the data models, the client-side "
          "modules and the build and deployment procedure, supported by genuine screenshots "
          "of the running application. Chapter 6 reports the verification work, the test "
          "plan, the test cases with their observed results, and the limitations that were "
          "discovered during evaluation. The conclusion summarises the contribution of the "
          "project and separates what was achieved from what remains to be done."),
]

CH2 = [
    ("h1", "CHAPTER – 2", "LITERATURE SURVEY"),
    ("h2", "2.1", "Scope of the Survey"),
    ("p", "The literature relevant to this project spans several distinct literatures. The "
          "first is the literature on electronic learning platforms and on the integration "
          "of artificial intelligence with instruction. The second is the literature on "
          "programmatic problem solving and online judging, which supplies the execution "
          "model behind the code workspace. The third is the literature on role-based access "
          "control, which supplies the authorisation model. The fourth is the literature on "
          "gamification and real-time collaboration, which supplies the motivational and "
          "communication models used by the contest and progress features. The fifth is the "
          "practical literature on applicant tracking systems, which supplies the evaluation "
          "criteria of the résumé scanner. Finally, the open source contribution literature "
          "provides the context in which the project is developed and licensed."),
    ("p", "Because the project is an implemented system rather than an experimental study, the "
          "sources used in this survey are of two kinds: peer-reviewed and pre-print "
          "publications for the conceptual claims, and the official technical documentation "
          "of each framework and external service for the implementation claims. Where a "
          "publication could not be verified from an accessible record, it is identified as "
          "such in the reference list rather than being presented as established."),

    ("h2", "2.2", "E-Learning Platforms"),
    ("p", "Massive open online course providers such as Coursera, edX and Udemy, and "
          "open-course consortia such as the OpenCourseWare movement, have established the "
          "modern expectations of an electronic learning system: a browsable catalogue, "
          "self-paced video or reading material, an assessment instrument, and a record of "
          "completion. Their strength is breadth and the quality control that a large "
          "instructional team can apply. Their limitation, for the purpose of this project, "
          "is that the catalogue is a closed body of content. The learner cannot ask why a "
          "given construct works, cannot generate a practice instrument on an adjacent "
          "topic, and cannot transfer the record of what was studied into an employment "
          "document. The distinction that matters for Elevora AI is not quality but "
          "generativity: the learning content of a platform is authored once, whereas the "
          "content of an assisted platform can be produced on demand."),
    ("p", "A second class of learning platform is the interactive curriculum platform, of "
          "which Codecademy and Exercism are representative, in which the learner writes "
          "code inside the page that teaches it. These systems close the gap between "
          "instruction and practice that the course platform leaves open, and they are the "
          "direct precedent for the code workspace of Chapter 5. Their remaining limitation "
          "is that the exercise set is fixed and, in the case of most such systems, is "
          "confined to a single language."),

    ("h2", "2.3", "Online Judges and Competitive Programming"),
    ("p", "Online judging systems provide the execution substrate for programming "
          "education. Judge0, the service used by this project, was conceived as an "
          "infrastructure layer rather than a user interface: it exposes a submission "
          "interface, an execution sandbox with configurable limits on CPU time and memory, "
          "and a polling interface that returns the compilation status, standard output, "
          "standard error and resource consumption of a completed run. This separation "
          "between judging infrastructure and pedagogy is important, because it allows the "
          "educational value to be added independently of the sandbox."),
    ("p", "Contest platforms such as Codeforces, LeetCode and HackerRank add to this "
          "substrate the elements of competition: a fixed time window, a scoring rule that "
          "combines solved problems with penalties for failed attempts, and a rating system "
          "that orders participants across contests. The rating mechanism used by Elevora AI "
          "is the Elo system, developed for competitive chess and subsequently applied to "
          "rating systems in many domains, in which each participant's rating changes by a "
          "quantity proportional to the expected score against the actual score. The "
          "parameter used in the implementation is 32, the value that Elo himself used in "
          "the original chess tables for periods of a month or more."),

    ("h2", "2.4", "Artificial Intelligence in Education"),
    ("p", "The most significant development in the literature relevant to this project is "
          "the shift from rule-based intelligent tutoring systems to systems built on large "
          "language models. Mollick and Mollick have summarised the practical prompt "
          "patterns that make a general purpose model behave as a tutor, and their central "
          "observation is relevant to the design of this project: a model used as a tutor "
          "must be prompted into a constrained pedagogical role rather than permitted to "
          "answer freely. The Elevora AI chatbot satisfies this partially by requiring the "
          "user to select a query category, which constrains the system prompt, and by "
          "rendering the reply through a Markdown renderer with syntax highlighting so that "
          "code remains legible in a learning context."),
    ("p", "A second strand of the literature concerns automated assessment. Item "
          "generation with a language model, followed by a second model pass that evaluates "
          "the learner's answers, is a known design pattern for formative assessment at "
          "scale, and it is the pattern used by the skill-assessment module, in which "
          "OpenAI generates a domain-specific question set, stores it with the learner's "
          "responses, and returns a score together with a generated improvement plan. The "
          "literature also raises the well-known reliability concern that a generative "
          "model may produce items that are ambiguous, that are answerable by inference "
          "rather than by knowledge, or that are duplicated across candidates. The "
          "implementation in this project mitigates only the last of these, by storing the "
          "generated items in the database with the attempt, so that the instrument actually "
          "administered is reproducible; it does not implement item review, distractor "
          "analysis or inter-rater agreement, and this is recorded as a limitation in "
          "Chapter 6."),
    ("p", "The third strand concerns the placement of a model inside an application. The "
          "architecture used in this project routes conversational generation through the "
          "server, so that the provider credential remains on the server, but routes the "
          "project recommender directly from the browser to the Groq service, so that the "
          "credential is embedded in the delivered bundle. This asymmetry is a deliberate "
          "engineering trade-off in terms of latency, and it is a security weakness in terms "
          "of credential custody, as discussed in Sections 3.8 and 6.5."),

    ("h2", "2.5", "Role-Based Access Control"),
    ("p", "The access control model of the system follows the role-based access control "
          "formalisation of Sandhu, Coyne, Feinstein and Youman, in which permissions are "
          "attached to roles, users are assigned roles, and a session is evaluated against "
          "the permissions of the roles it activates. The formalism separates the concepts "
          "of user, role, session and permission, which allows an access control "
          "requirement to be stated in terms of the roles that may activate it. In the "
          "implementation the two roles are user and administrator, the session is the JSON "
          "Web Token issued at authentication, and the permission check is performed by two "
          "middleware functions, one that establishes identity and one that compares the "
          "role."),
    ("p", "The literature on web security is relevant to the observation that identity "
          "establishment and authorisation are distinct obligations and that the second is "
          "meaningless without the first. In the inspected server, several route groups "
          "apply only the authorisation check without first establishing identity; because "
          "the authorisation check reads the role from the identity object that the first "
          "check populates, such routes are permanently denied rather than insecurely "
          "open. The reverse error also occurs, in which a route group omits both checks. "
          "These observations are the subject of the security analysis of Section 3.9 and "
          "the test cases of Chapter 6."),

    ("h2", "2.6", "Gamification and Real-Time Collaboration"),
    ("p", "Gamification is the application of game design elements in a non-game context. "
          "Hamari, Koivisto and Sarsa reviewed a substantial body of empirical work on the "
          "subject and concluded that the effects of gamification are mixed and strongly "
          "dependent on the context in which the elements are applied; that is, gamification "
          "is not inherently effective, but is effective where the element is congruent with "
          "the activity it decorates. The features of Elevora AI that employ such elements "
          "are the daily streak counter, the points total, the achievement badges, the "
          "contribution leaderboard and the competitive contest. The congruence argument "
          "applies most strongly to the contest, which is competitive in its own right, and "
          "weakly to the points total, which is a measure of activity rather than of "
          "learning."),
    ("p", "Real-time collaboration in educational systems is usually implemented with the "
          "WebSocket protocol or with a library built upon it. Socket.IO, the library used "
          "here, adds a transport upgrade mechanism, automatic reconnection and a room "
          "abstraction that maps a logical group of clients onto a shared broadcast channel. "
          "The contest module of this project uses exactly that abstraction: each contest "
          "occupies a room named from the contest identifier, clients join and leave that "
          "room, and the server broadcasts the current participant count and the status of "
          "each judged submission to the members of the room."),

    ("h2", "2.7", "Applicant Tracking Systems and Résumé Optimisation"),
    ("p", "The applicant tracking system occupies a decisive position in modern recruitment "
          "practice. A résumé that is rejected by an automated screen is never read by a "
          "recruiter, and the screens in question are parsers that extract structured fields "
          "from a document and compare them against the requisition and the keyword set of "
          "the advertisement. The engineering implication for a résumé builder is that the "
          "document must be both attractive to a human reader and legible to a parser, "
          "which is a genuine tension, since the human reader is best served by a two-column "
          "layout with visual hierarchy while the parser is best served by a single-column "
          "document with conventional headings."),
    ("p", "The Elevora AI résumé builder resolves this tension by generating two documents "
          "from a single data model: a styled preview intended for human reading and a "
          "plain, single-column variant intended for machine parsing, together with a "
          "scanner that reports keyword coverage against a general keyword set and "
          "role-specific keyword sets. The scanner is a deterministic keyword analysis, not "
          "a machine-learning classifier, and its output should be read as coverage "
          "guidance rather than as a prediction of screening outcome."),

    ("h2", "2.8", "Open Source Development as a Learning Model"),
    ("p", "The project is developed and published as an open source repository with a "
          "contributor guide, a code of conduct and a security policy. Pinto, Steinmacher "
          "and Gerosa studied the population of casual contributors to open source projects "
          "and found it to be considerably larger and more diverse than is commonly "
          "assumed, and that the principal barriers to contribution are motivational and "
          "procedural rather than technical. The contributor guide published by the "
          "application addresses exactly those barriers: it defines the meaning of the "
          "various difficulty labels attached to issues, distinguishes the repository from "
          "an unrelated project of similar name, and lists the classes of issue suitable "
          "for a first contribution. The relevance of this literature to the project is "
          "direct, because the platform exists partly to attract such contributions and "
          "the contributor-facing screens are part of the delivered interface."),

    ("h2", "2.9", "Comparative Summary"),
    ("p", "Table 2.1 summarises the classes of system reviewed above and compares their "
          "characteristics with those of Elevora AI. The comparison is deliberately made "
          "at the level of capability rather than of branding, and the right-hand column "
          "reflects the state of the implementation as established by the inspection "
          "reported in Chapters 4 to 6 rather than the ambition stated in the project "
          "synopsis."),
    ("table", "Table 2.1: Comparison of related system classes with Elevora AI",
     ["System class", "Principal strength", "Principal limitation",
      "Elevora AI as implemented"],
     [["Video course platforms (Coursera, edX, Udemy)",
       "Broad authored catalogue, asynchronous delivery",
       "No embedded code execution, no AI tutoring, no career documents",
       "Learning Hub and Video modules give module progress, but the catalogue is smaller and the AI assistance is limited to the Study Buddy"],
      ["Interactive curriculum platforms (Codecademy, Exercism)",
       "Instruction and practice in one surface",
       "Single language focus, fixed exercise set, no assessment or placement tooling",
       "Monaco workspace with multi-language Judge0 execution, but the practice problem set is local static data"],
      ["Online judges and contest platforms (Codeforces, LeetCode, HackerRank)",
       "Reliable sandboxed execution, ranking, established community",
       "No structured curriculum, no résumé or interview preparation",
       "Contest module reproduces execution, scoring and Elo rating, but problems are declared in the model rather than harvested from a database"],
      ["AI tutoring systems and assistants",
       "On-demand explanation, generated practice material",
       "Typically unintegrated with progress records; credential custody is often weak",
       "Gemini for the Study Buddy and for quiz and note generation, OpenAI for assessment; the Groq key is exposed in the client bundle"],
      ["Résumé and cover-letter builders (Zety, Novoresume, Canva)",
       "Document design, templates, immediate export",
       "No skill tracking, no ATS analysis, no connection to preparation activity",
       "Résumé builder with ATS scan and dual export; the cover letter has export but no ATS variant and no server persistence"],
      ["Applicant tracking systems and job boards (LinkedIn, Naukri)",
       "Employer connectivity, workflow integration",
       "Do not teach; do not measure preparation",
       "Placement module and ATS scanner provide preparation, not employer connectivity"],
      ["Developer communities (Stack Overflow, Discord)",
       "Peer knowledge exchange at scale",
       "Weak coupling to formal curricula and to progress tracking",
       "Community forum with answers, resolution marking and administrative moderation"]],
     [1.5, 1.4, 1.6, 2.5]),
    ("h2", "2.10", "Conclusion of the Survey"),
    ("p", "The survey shows that each capability required by this project is available "
          "separately and well implemented in the state of the art, and that the value of "
          "the consolidation is not in any single capability but in the shared context "
          "between them. It also shows that consolidation is not free: the literature on "
          "gamification cautions that merged features dilute their effect, the literature on "
          "role-based control cautions that merged privilege sets widen the consequence of "
          "a single authorisation mistake, and the security literature makes the obvious "
          "point that a larger attack surface produces more places in which a credential "
          "may be exposed. Elevora AI consequently treats consolidation as an engineering "
          "problem to be managed rather than an accumulation to be displayed, and the "
          "remainder of this report documents how that management was performed."),
]
