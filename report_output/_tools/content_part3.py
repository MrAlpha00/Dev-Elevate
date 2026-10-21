# -*- coding: utf-8 -*-
"""Chapter 5 (Implementation), Chapter 6 (Result and Testing), Conclusion, References."""

CH5 = [
    ("h1", "CHAPTER – 5", "IMPLEMENTATION"),
    ("h2", "5.1", "Repository Structure"),
    ("p", "The project is a single repository containing the documentation, the client "
          "application and the server application. The client occupies the Client "
          "directory and the server the Server directory; the two are independent packages "
          "with their own manifests, their own lockfiles and their own dependency trees, "
          "and neither imports the other. Table 5.1 gives the directory layout of the two "
          "applications together with the purpose of each significant directory."),
    ("table", "Table 5.1: Directory layout of the two applications",
     ["Path", "Contents", "Purpose"],
     [["Client/src/pages", "13 page directories and 2 page files, including Landing, "
       "Dashboard, Coding, Notes, Interview, Placements, Roadmap, Assessments, AiModel",
       "The routed screens of the application"],
      ["Client/src/components", "23 sub-directories and about 115 files",
       "Feature components: Dashboard, Layout, Auth, Quiz, ResumeBuilder, CoverLetter, "
       "Community, TechFeed, LearningHub, Admin, Chatbot, Payment, calendar, Calculator, "
       "ProjectRecommender, Profile, Settings, tasks, ui primitives"],
      ["Client/src/contexts", "6 context providers",
       "Session, global application state, administration state, socket connection, "
       "notification queue and calculator history"],
      ["Client/src/api, src/services, src/features", "4 API modules, 4 service modules and "
       "one query slice", "HTTP access layers: shared Axios instance, administration, "
       "assessment, dashboard, video progress, analytics and courses"],
      ["Client/src/utils, src/lib, src/config, src/data, src/types", "11 utilities, one class "
       "utility, one route configuration, seed data and type declarations",
       "Provider clients, semantic search, résumé templates, the interface base address and "
       "shared types"],
      ["Client/public, Client/src/assets", "Favicon, an animated globe graphic, a logo, "
       "twelve course and notes data files, two roadmap data files",
       "Static assets and the bundled static content"],
      ["Server/controller", "24 controller files, about 6,800 lines",
       "Business logic for authentication, contests, assessments, notes, dashboard, courses, "
       "quizzes, community, the scanner and the support modules"],
      ["Server/routes", "30 route files, about 3,400 lines",
       "Endpoint declaration, middleware chains and mount paths"],
      ["Server/model", "32 schema files, about 1,400 lines", "Persistence declarations"],
      ["Server/middleware", "4 files", "Identity, authorisation, sanitisation and validation helpers"],
      ["Server/utils, Server/config", "10 utility modules and one database module",
       "Provider clients, mail templates, keyword sets, the rating calculator, the rate "
       "limiter and the database connection"],
      ["Server root", "index.js, socket.js, pdfServer.js and three utility scripts",
       "Application entry point, socket initialisation, a separate document-generation "
       "service and one-off maintenance scripts"]],
     [1.8, 2.6, 3.0]),
    ("p", "Two structural observations are relevant to the maintenance of the project. The "
          "notes module implements its handlers directly in the route file, which is "
          "662 lines long, while a controller of 625 lines that exports the same eleven "
          "operations exists and is imported only for its file-upload middleware; the two "
          "implementations have diverged, and the divergence is the cause of the defect "
          "described in Section 6.4. The server also contains three schema files that are "
          "never imported and one empty file that declares no schema; these are harmless "
          "but misleading to a reader who navigates the model directory."),

    ("h2", "5.2", "Client Routing and Application Providers"),
    ("p", "The client router is declared in the application root file, which imports every "
          "routed screen statically and assembles them into four branches. The first branch "
          "contains the public pages: the landing page, the privacy, cookie and terms "
          "policies, the disclaimer, the creator page, the interface documentation, the "
          "project documentation and the contributor guide. The second branch contains the "
          "three authentication pages, each of which is explicitly marked as not requiring "
          "a session. The third branch is the administration console, which is wrapped in "
          "both a session guard and an administration guard. The fourth branch is a "
          "catch-all that mounts the application shell and declares the twenty-eight "
          "learner routes beneath it, with an unmatched path redirected to the dashboard."),
    ("p", "Four providers wrap the router. The global provider holds the application-wide "
          "state, including the theme and the user summary, and persists it in the browser "
          "under a single key. The session provider implements registration, verification, "
          "credential login, Google login, the forgotten-password flow and logout, and "
          "persists the session under a second key. The socket provider establishes the "
          "real-time connection. The notification provider maintains the queue of "
          "user-visible alerts. A splash screen is shown until the window load event has "
          "fired, with a timeout as a fallback, which prevents the layout from flickering "
          "during the initial load."),
    ("p", "The route guard is a small component that accepts two properties. The first "
          "declares whether a session is required and the second whether the administration "
          "role is required; the component consults the session context, redirects an "
          "unauthenticated visitor to the sign-in page, and renders the administration "
          "branch only for a caller whose role matches. The guard is therefore the "
          "client-side expression of the permission model of Table 3.1, and the server-side "
          "expression of the same model is the identity and authorisation middleware."),

    ("h2", "5.3", "Navigation Shell and Public Interface"),
    ("p", "The navigation shell presents the same nineteen entries in the sidebar and in "
          "the mobile menu, in the order Dashboard, Learning Hub, Video, Quiz Center, "
          "Skill Assessment, Coding, Interview, Study Buddy, Tech Feed, Community, Resume "
          "Builder, Cover Letter, Placement Prep, AI Projects, AI Models, Road Map, "
          "Notes, Calendar and Contributors. Each entry carries an icon and a route, and "
          "the shell renders the routed screen inside a main region with a footer and a "
          "back-to-top control."),
    ("p", "Figure 5.1 shows the sign-in screen of the deployed application. The screen "
          "presents the credential form, a forgotten-password link, a Google sign-in "
          "button and a registration link, and it also renders a block of demonstration "
          "administrator credentials in plain text, which is a security weakness discussed "
          "in Section 6.5. The screen was captured from the deployed host with a headless "
          "browser; no credential was entered in order to obtain it."),
    ("fig", "shots/live_login.png",
     "Fig. 5.1: Sign-in screen of the deployed Elevora AI application", 5.6),
    ("p", "Figure 5.2 shows the public landing page of the same deployment. The page "
          "composes a hero section, a statistics band, a feature grid that describes the "
          "principal modules, a technology section, testimonials, a frequently asked "
          "questions section and a call to action, with an animated three-dimensional cube "
          "and a cookie-consent banner. The statistics displayed on this page, which "
          "advertise a learner population of more than fifty thousand, are marketing "
          "statements carried in the component source; they are not derived from any "
          "collection and are not verified by this report."),
    ("fig", "figures/fig5_2_landing.png",
     "Fig. 5.2: Public landing page of the deployed application", 5.9),
    ("p", "Figure 5.3 shows the interface documentation page published by the "
          "application. The page lists the endpoint groups of the server with their methods "
          "and descriptions, and is generated from a static table in a component rather "
          "than from the route table of the server. It is nevertheless a faithful summary "
          "of the implemented interface, and it is included here as evidence of the "
          "documented public surface."),
    ("fig", "figures/fig5_3_api_docs.png",
     "Fig. 5.3: Interface documentation page published by the application", 5.7),
    ("p", "Two further public pages are shown in Figures 5.4 and 5.5. The project "
          "documentation page summarises the architecture, the technology stack and the "
          "contribution process for prospective contributors, and the contributor guide "
          "page explains the difficulty labels used on the issue tracker and the "
          "procedure for a first contribution. Both are part of the open-source "
          "development model described in Section 2.8."),
    ("fig", "figures/fig5_4_documentation.png",
     "Fig. 5.4: Project documentation page of the deployed application", 5.6),
    ("fig", "figures/fig5_5_contributor_guide.png",
     "Fig. 5.5: Contributor guide page of the deployed application", 5.6),

    ("h2", "5.4", "Server Entry Point and Middleware Pipeline"),
    ("p", "The server entry point establishes the connection to the database before the "
          "listener is opened, and refuses to start if the connection fails. It then "
          "installs the middleware pipeline in a fixed order: cross-origin resource sharing "
          "with the configured client origin and with credentials permitted, the body "
          "parser, the cookie parser, and the sanitising middleware. The route modules are "
          "then mounted at thirty-one distinct prefixes, which include the learner, "
          "administration, assessment, learning, compiler, placement, contest, notes, "
          "notification and support groups. A static path serves the note attachments, a "
          "global error handler converts an uncaught exception into a JSON response, and a "
          "catch-all returns a JSON document for an unmatched path."),
    ("p", "Two implementation details in the entry point deserve mention. The listener is "
          "replaced by a wrapper that creates a Node HTTP server around the application, "
          "which is the mechanism by which the socket server attaches to the same port. "
          "The route table also contains two duplicated mounts: the assessment routes are "
          "mounted at two prefixes and the conversational routes at one prefix twice, "
          "which means that only the first of each pair is reachable. The duplication is "
          "harmless in itself, but it inflates the documented interface and suggests that "
          "the intended set of prefixes is wider than the effective one."),

    ("h2", "5.5", "Interface Surface"),
    ("p", "Table 5.2 groups the endpoints of the server by functional area and states the "
          "authentication requirement of each group as declared in the route files. The "
          "table is the implementation-level counterpart of the requirement table of "
          "Chapter 3."),
    ("table", "Table 5.2: Endpoint groups by functional area and declared protection",
     ["Group", "Prefix", "Protection declared in the route file", "Notes"],
     [["Authentication", "/api/v1/auth and /api/v1", "Public for signup, verification, login, "
       "Google exchange, forgotten and reset password; authenticated for logout and profile",
       "Issues the token and the session cookie"],
      ["Administration", "/api/v1/admin", "Authenticated and administrator role for users, "
       "logs and settings; the system-log creation route requires authentication only",
       "The system-log route is accessible to any signed-in user"],
      ["Administration feedback", "/api/v1/admin/feedback", "None declared",
       "List, review-status and delete operations are reachable anonymously"],
      ["Administration quiz", "/api/v1/admin/quiz", "Authenticated and administrator role "
       "applied to the whole router", "Quiz and question authoring, submission listing"],
      ["Administration analytics", "/api/v1/admin/analytics", "Authenticated and administrator "
       "role", "Aggregate counts and a delimited-text export"],
      ["Learner quiz", "/api/v1/user-quiz", "Authenticated", "Attempting and history of attempts"],
      ["Assessment", "/api/v1/assessment and /api/v1/assessments", "Authenticated",
       "Generation, submission, history and latest summary; the second prefix is unreachable"],
      ["Dashboard", "/api/v1/dashboard", "Authenticated", "Aggregate summary of the learner"],
      ["Learning tracks", "/api/v1/learning/java, aiml, mern, dsa", "Authenticated",
       "Modules, notes, reviews and progress; the catalogue is declared in the route files"],
      ["Video", "/api/v1/video", "Authenticated", "Progress, continuation, course progress and bookmarks"],
      ["Courses", "/api/v1/courses and /api/v1/admin-courses", "Administrator role declared "
       "for the write operations; the role check is applied without the identity check",
       "The write operations are therefore always denied"],
      ["Community", "/api/v1/community", "Authenticated", "Questions, answers, resolution "
       "marking and answer acceptance"],
      ["Notes", "/api/notes", "Public for browsing, searching and topic retrieval; "
       "authenticated for the personal operations", "Handlers implemented in the route file"],
      ["Notifications", "/api/v1/notifications", "Authenticated", "Listing, read marking, deletion"],
      ["Contests", "/api/v1/contests", "Authenticated except for the contest listing",
       "Registration, submission, leaderboard, rating and results"],
      ["Compiler", "/api/v1/compiler", "None declared", "Forwards to the Judge0 aggregator"],
      ["Conversational and generative", "/api/v1/ai", "Public for the conversational route; "
       "authenticated for quiz and note generation", "Three routes, two of which are "
       "reachable because of the duplicate mount"],
      ["Scanner", "/api/v1/ats", "None declared", "Deterministic keyword analysis"],
      ["Placements", "/api/v1/placements", "None declared", "Returns a constant object"],
      ["Support, questions, news, subscription", "/api/v1 and /api/subscribe", "Public",
       "Support tickets, frequently asked questions, the news feed and the newsletter"]],
     [1.5, 1.9, 2.6, 2.4]),

    ("h2", "5.6", "Authentication and Session Handling"),
    ("p", "Registration creates a one-time-password record keyed by the e-mail address and "
          "sends the code through the mail utility, which composes an HTML message. "
          "Verification compares the submitted code with the stored record, checks that it "
          "has not expired, creates the user document with a hashed password, and issues "
          "the session token. The credential path compares the submitted password with the "
          "stored hash and issues the same token. The Google path exchanges the identity "
          "token obtained by the client library for a session token, creating the account "
          "on first use."),
    ("p", "The token is delivered in a cookie that is declared HTTP-only, secure and of "
          "same-site type none, with a lifetime of three days. The token payload contains "
          "the user identifier and the role. The identity middleware accepts the token "
          "from the cookie or from the authorization header, as shown in the following "
          "extract."),
    ("code", "Server/middleware/authMiddleware.js",
     "export const authenticateToken = async (req, res, next) => {\n"
     "  try {\n"
     "    const cookieToken = req.cookies?.token;\n"
     "    const headerToken = req.headers.authorization?.split(\" \")[1];\n"
     "    const token = cookieToken || headerToken;\n"
     "    if (!token) {\n"
     "      return res.status(401).json({ success: false,\n"
     "        message: \"Authentication required - No token provided\" });\n"
     "    }\n"
     "    const decoded = jwt.verify(token, process.env.JWT_SECRET);\n"
     "    const userId = decoded.userId || decoded.id || decoded._id;\n"
     "    const user = await User.findById(userId).select(\"-password\").lean();\n"
     "    req.user = { ...user, _id: user._id, id: user._id.toString() };\n"
     "    next();\n"
     "  } catch (error) { /* 401 or 500 according to the error class */ }\n"
     "};"),
    ("p", "The password-reset flow follows the same pattern with a different token record "
          "and a different message template, and the reset link carries the token in the "
          "path. The password-change operation is throttled by a dedicated rate limiter "
          "that permits a small number of attempts in a short window. One implementation "
          "note is recorded as a defect: the cookie declares the secure attribute "
          "unconditionally, so that the session cannot be established over plain HTTP, "
          "which affects local development but not a deployment served over TLS."),

    ("h2", "5.7", "Role-Based Access Control Implementation"),
    ("p", "Authorisation is expressed by two middleware functions. The first compares the "
          "role in the request identity with the roles permitted by the route and answers "
          "with 403 when the comparison fails. The second is a variant that accepts a list "
          "of roles. The administration branch of the client router adds the same "
          "condition on the client side, so that an administrator link is not displayed to "
          "a learner and a direct navigation to an administration path is redirected."),
    ("p", "The implementation was checked route by route against the declared protection, "
          "and the result is summarised in Table 5.2. Three findings are material. The "
          "course write routes apply the role check without the identity check, and since "
          "the role check reads the role from the identity that the identity check "
          "populates, those routes always answer 403 and the course authoring feature is "
          "inoperative. The administration feedback routes declare no protection at all. "
          "The system-log creation route requires an identity but not the administrator "
          "role. These are recorded as the access-control test cases TC-08 to TC-10 of "
          "Chapter 6."),

    ("h2", "5.8", "Dashboard Module"),
    ("p", "The dashboard is the first screen of the application shell and is composed of "
          "eleven components: a statistics row carrying the total points, the current "
          "streak, the completed goals and the learning progress; a progress widget; a "
          "learning-insights panel; a project-recommendation panel; a quick-action panel; "
          "a news panel; a skill-assessment summary, which is displayed beneath the heading "
          "of the personalised roadmap snapshot; an achievements panel; a recent-attempts "
          "panel; a daily-goals panel; and a streak calendar."),
    ("p", "The server side of the dashboard is implemented in a dedicated controller of "
          "about 485 lines that aggregates the user document, the quiz attempts, the skill "
          "assessments and the visit counter, and that optionally asks the OpenAI service "
          "for project suggestions, falling back to three built-in suggestions when no "
          "credential is configured. The client side of the dashboard, however, initialises "
          "a demonstration user when the global state contains no user, as shown in the "
          "following extract."),
    ("code", "Client/src/components/Dashboard/Dashboard.tsx",
     "useEffect(() => {\n"
     "  if (!state.user) {\n"
     "    const defaultUser: User = {\n"
     "      _id: '1',\n"
     "      id: '1',\n"
     "      name: 'John Doe',\n"
     "      email: 'john@example.com',\n"
     "      joinDate: new Date().toISOString(),\n"
     "      streak: 0,\n"
     "      totalPoints: 1250,\n"
     "      level: 'Intermediate'\n"
     "    };\n"
     "    dispatch({ type: 'SET_USER', payload: defaultUser });\n"
     "  }\n"
     "}, [state.user, dispatch]);"),
    ("p", "The consequence is that the statistics row of the dashboard displays the "
          "demonstration values until the real session state replaces them, and the recent "
          "attempts panel is rendered from a commented-out mapping, so that it always "
          "shows its empty state. The panels that depend on the server aggregation, namely "
          "the learning insights, the project recommendations and the achievements, are "
          "those that reported errors in the dashboard evidence supplied with this project, "
          "and the same behaviour is expected from the code, because those panels call the "
          "dashboard endpoint and handle a failed response by showing an error state "
          "rather than a fallback value."),

    ("h2", "5.9", "Learning Hub, Notes and Video Modules"),
    ("p", "The Learning Hub presents four tracks, for data structures and algorithms, "
          "Java, the MERN stack and artificial intelligence, each of which is built from "
          "module cards, a topic view and a module content component. The content itself "
          "is declared in the client, while the progress, the personal notes and the "
          "reviews of each topic are persisted on the server through the four learning "
          "route groups. Each of those groups exposes the same set of operations for its "
          "track: the module list, the detail of a module, the creation of a note for a "
          "topic, the creation of a review for a topic and the update of the progress for "
          "a topic."),
    ("p", "The notes module provides a second and more general mechanism. A note carries a "
          "title, a body, a topic, a set of tags, a visibility flag, a flag that identifies "
          "machine-generated content, an array of attachments and counters for views and "
          "likes. Attachments are uploaded through a multipart request that accepts up to "
          "five files of a restricted set of types, are written to the uploads directory "
          "of the server, and are served from the static path. The module also exposes "
          "public browsing, full-text search and a list of the machine-generated notes, and "
          "the client provides a modal in which a note may be composed with the assistance "
          "of the generative model."),
    ("p", "The video module is built around the YouTube interface. The server obtains the "
          "course catalogue from the video service and falls back to a built-in list of "
          "courses when the credential is absent or the service fails. The client player "
          "reports the watch position to the progress endpoint, retrieves the continue-"
          "learning list and the per-course progress, and manages a bookmark collection. "
          "The frontend service module for this feature declares its own base address "
          "with a local host and port as the default, which is a defect in the deployed "
          "configuration."),

    ("h2", "5.10", "Quiz and Skill Assessment Implementation"),
    ("p", "The quiz module is divided between the authoring side, the administration quiz "
          "route group, and the attempt side, the learner quiz route group. An authored "
          "quiz carries a title, a topic, a difficulty and a set of questions; an attempt "
          "carries the answers, the score, the number of questions, the time taken and the "
          "instant of completion. The client presents the attempt as a timed sequence of "
          "questions, scores the responses against the stored items, and shows a result "
          "screen together with a history of previous attempts. A separate administrative "
          "view lists the submissions of all learners with the responses they gave."),
    ("p", "The skill assessment module generates its instrument at run time. The "
          "controller holds a configuration table of five tracks, comprising data "
          "structures and algorithms, web development, machine learning, data science and "
          "cloud operations, each with its domain description, its item count and its "
          "prompt template. The generation call sends the template to the configured "
          "model, the returned items are parsed and stored with the assessment document, "
          "and the learner answers the items in the client. The submission call evaluates "
          "the answers in a second model pass and returns a score, an accuracy, an "
          "identified set of weaknesses and a generated improvement plan, all of which are "
          "stored with the assessment so that the history remains reproducible."),

    ("h2", "5.11", "Artificial Intelligence Integrations and Failure Handling"),
    ("p", "Three provider integrations exist, and they differ in whether the credential "
          "remains on the server. The conversational and generative paths are proxied "
          "through the Express layer, so that the key is read from the environment at "
          "run time. The following extract shows the outbound call of the conversational "
          "handler."),
    ("code", "Server/controller/aiController.js",
     "const response = await axios.post(\n"
     "  `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${process.env.GEMINI_API_KEY}`,\n"
     "  { contents: [ { role: \"user\", parts: [ { text: prompt } ] } ] },\n"
     "  { headers: { \"Content-Type\": \"application/json\" } }\n"
     ");\n"
     "const aiText = response.data?.candidates?.[0]?.content?.parts?.[0].text ||\n"
     "  \"No reply received\";\n"
     "res.status(200).json({ reply: aiText });"),
    ("p", "The handler distinguishes a rate-limit response from a general failure and "
          "returns a status of 429 with an explanatory message in the first case and a "
          "general error in the second. No retry, no back-off and no fallback provider are "
          "implemented, so a transient failure of the provider is presented to the learner "
          "as a failed request."),
    ("p", "The third integration is different in kind. The project recommender calls the "
          "Groq inference service directly from the browser, using a key that the build "
          "tool inlines into the delivered bundle, and it targets the LLaMA 3 8B model "
          "through an OpenAI-compatible interface. The helper includes a local fallback "
          "path that produces a heuristic response when the call fails, so the module "
          "remains usable without a credential; the cost of this design is that the "
          "credential is exposed to every visitor of the deployed application, which is "
          "recorded as a high-priority defect in Section 6.5."),
    ("p", "A further client-side capability deserves mention. The search utility includes "
          "a semantic search implementation based on a local embedding model that runs in "
          "the browser, so that the similarity of a query against the content index is "
          "computed on the client without a server round trip. This is the only genuinely "
          "client-side machine-learning feature in the project."),

    ("h2", "5.12", "Code Editor and Compiler Integration"),
    ("p", "The code workspace is implemented with the Monaco editor, which provides "
          "syntax highlighting, completion and a model of the document that is independent "
          "of the framework. The client registers two key bindings, one that runs the "
          "current program and one that runs and submits it. The language identifiers are "
          "declared in a local table that maps each supported language onto the numeric "
          "identifier expected by the compiler service, and the practice problem set is "
          "likewise declared locally."),
    ("p", "The submission path is shown in the following extract, in which the source is "
          "transported as base64 and the call is forwarded to the compiler aggregator with "
          "the synchronised wait option."),
    ("code", "Server/routes/compilerRoutes.js",
     "const submission = await axios.post(\n"
     "  \"https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=true\",\n"
     "  { source_code, language_id, stdin },\n"
     "  { headers: {\n"
     "      \"x-rapidapi-host\": \"judge0-ce.p.rapidapi.com\",\n"
     "      \"x-rapidapi-key\": process.env.RAPID_API_KEY,\n"
     "      \"content-type\": \"application/json\" } }\n"
     ");\n"
     "return res.json(submission.data);"),
    ("p", "The client sends the request to a literal local address rather than to the "
          "configured interface base address, and the route itself performs no "
          "authentication, so the endpoint is open to anonymous use. The contest path "
          "uses the self-hosted compiler configuration, posts the submission, polls for "
          "the result at one-second intervals for up to ten attempts and then applies the "
          "scoring rule, which awards a fixed number of points by difficulty and adds a "
          "twenty-minute penalty for each previous failed attempt on the same problem."),

    ("h2", "5.13", "Contest Leaderboard and Rating"),
    ("p", "The contest controller is the largest single file in the project, at about "
          "1,794 lines, and it implements the full lifecycle: listing contests by status, "
          "returning a contest with its problems, registering a participant, accepting and "
          "grading a submission, computing the leaderboard, returning the personal rating "
          "and the results, and running a scheduled task that finalises contests whose "
          "window has closed. The rating calculation is implemented in a dedicated utility "
          "in the Elo manner, with a constant of 32 for the magnitude of a single "
          "contest's effect and a divisor of 400 for the expected score."),
    ("code", "Server/utils/ratingCalculator.js",
     "const K_FACTOR = 32;\n"
     "const EXPECTED_SCORE_FACTOR = 400;\n"
     "const calculateExpectedScore = (ratingA, ratingB) =>\n"
     "  1 / (1 + Math.pow(10, (ratingB - ratingA) / EXPECTED_SCORE_FACTOR));\n"
     "const calculateNewRating = (oldRating, actualScore, expectedScore) =>\n"
     "  Math.round(oldRating + K_FACTOR * (actualScore - expectedScore));"),
    ("p", "The socket layer is initialised from the entry point and attaches to the same "
          "HTTP server as the REST interface. The handshake middleware reads a token from "
          "the handshake, verifies it and attempts to load the user; the following "
          "extract shows the point at which the design and the issued token diverge."),
    ("code", "Server/socket.js",
     "const decoded = jwt.verify(token, process.env.JWT_SECRET);\n"
     "const user = await User.findById(decoded.id).select(\"-password\");\n"
     "if (!user) { return next(new Error(\"User not found\")); }\n"
     "socket.user = user;\n"
     "next();\n"
     "// on error: socket.user = null; next();"),
    ("p", "The identity middleware of the REST layer accepts the user identifier from any "
          "of three claim names, as shown earlier, but the socket middleware accepts only "
          "one of them, and the tokens issued by the registration, verification, credential "
          "and Google paths contain only another. The lookup therefore raises a cast "
          "error, the catch block admits the connection with a null user, and the "
          "contest rooms consequently operate without an authenticated participant."),

    ("h2", "5.14", "Notes, Community and Technology Feed"),
    ("p", "The community module implements the familiar question-and-answer pattern with "
          "the additions that an educational community requires: a question may be marked "
          "as resolved by its author, and an answer may be accepted by the author of the "
          "question. Both of these operations are restricted to administrators in the route "
          "declaration, which is a stricter policy than the ownership rule would require "
          "and is noted in Chapter 6."),
    ("p", "The like operation on a note illustrates the danger of a schema and a route "
          "that have drifted apart. The schema declares an array of user identifiers named "
          "as the likes and a virtual count with a getter only, whereas the route reads "
          "and writes a field with a different name and assigns to the virtual count, as "
          "shown in the following extract."),
    ("code", "Server/routes/notesRoutes.js",
     "if (!note.likedBy) { note.likedBy = []; }\n"
     "const hasLiked = note.likedBy.some(id => id.toString() === userId.toString());\n"
     "if (hasLiked) {\n"
     "  note.likedBy = note.likedBy.filter(id => id.toString() !== userId.toString());\n"
     "  note.likeCount = Math.max(0, (note.likeCount || 0) - 1);\n"
     "} else {\n"
     "  note.likedBy.push(userId);\n"
     "  note.likeCount = (note.likeCount || 0) + 1;\n"
     "}\n"
     "await note.save();"),
    ("p", "Because the mapper discards fields that the schema does not declare, the write "
          "to the undeclared array is not persisted, and because the virtual count has no "
          "setter, the assignment to it raises an error that the handler converts into a "
          "500 response. The operation therefore never succeeds, and the defect is recorded "
          "as test case TC-13 with the correction specified in Chapter 6."),
    ("p", "The technology feed aggregates current news through the news interface and "
          "classifies the articles into job, internship and event categories for the "
          "client. The server also exposes a latest-news route that performs the same "
          "aggregation, and this route contains a credential written as a literal in the "
          "source, which is one of the two credential exposures reported in Section 6.5."),

    ("h2", "5.15", "Résumé Builder and Cover Letter Generation"),
    ("p", "The résumé builder is organised as a sequence of forms, one for each section of "
          "the document, feeding a live preview and a set of templates that are declared "
          "in the client for three professional profiles: a software engineer, a data "
          "scientist and a product manager. Two exports are produced from the same data: a "
          "styled document for human reading and a plain, single-column variant for "
          "machine parsing, both written with the browser-side PDF library that rasterises "
          "the rendered markup into a paginated document."),
    ("p", "The applicant-tracking-system scanner posts the resume content to the server, "
          "where a deterministic analysis compares the text against a general keyword set "
          "and against the keyword sets of a chosen role, and reports the coverage with "
          "suggestions. The three keyword utilities that implement this comparison are "
          "pure functions over the text and the keyword lists, which makes the result "
          "reproducible and auditable."),
    ("p", "The cover-letter module has no server counterpart at all. The composed letter "
          "is held in the browser, is persisted under a single key in local storage, and "
          "is exported with the direct document-writing library, using its own text "
          "measurement and wrapping functions. It has no plain variant for machine "
          "parsing, no scanner and no server-side storage, which is an asymmetry with the "
          "résumé module and a divergence between the synopsis and the implementation."),

    ("h2", "5.16", "Administration Console"),
    ("p", "The administration console is mounted on its own branch of the client router "
          "and is implemented as nine routed modules. User management lists the registered "
          "users and supports the addition and the deletion of an account. Content "
          "management edits the course catalogue and can import the metadata of a course "
          "from the video service. Quiz management authors quizzes and their questions and "
          "lists the submissions of the learners. The community module reviews questions "
          "and answers. The analytics module presents the aggregate statistics of the "
          "platform with charts drawn from two charting libraries. The system-logs module "
          "presents the audit trail. The settings module presents the platform "
          "configuration and permits the maintenance mode and the registration switch to be "
          "changed, subject to the secondary secret check. The feedback module reviews the "
          "messages submitted through the support form."),
    ("p", "The overview module of the console is passed empty collections and its action "
          "handlers are placeholders, so that the tiles of the overview page display "
          "nothing. This is a genuine defect of the delivered interface, recorded in "
          "Chapter 6, and it is the reason why the overview is not presented in this "
          "report as a working screen."),

    ("h2", "5.17", "Notifications, Productivity Tools and Search"),
    ("p", "The notification module stores one document per alert, addressed to a user and "
          "carrying a type and a read flag; the client presents the alerts in a panel "
          "beside the navigation and offers a mark-as-read and a delete operation. The "
          "calendar module presents a month view of the learner's events, the task module "
          "presents a board of tasks, and the calculator module offers six modes, of which "
          "the scientific, financial, graphing, physics, unit-conversion and basic modes "
          "are implemented over the mathematical expression library, with the history of "
          "calculations persisted in the browser."),
    ("p", "The global search module builds an index over the static content of the "
          "application in the browser and queries it directly, with a type filter. It is "
          "therefore a client-side search over the shipped data and does not search the "
          "learner's own content, which resides on the server. The task module is not "
          "reachable from the route table, and a placement-statistics page of considerable "
          "size is likewise unrouted, both of which are recorded in Chapter 6 as dead "
          "code."),

    ("h2", "5.18", "Error Handling"),
    ("p", "Error handling is distributed rather than centralised. The entry point installs "
          "a global handler of four arguments that logs the error and returns a JSON "
          "document, which covers the exceptions that reach the framework. Individual "
          "controllers wrap their work in a try block and return a JSON error object with "
          "an appropriate status, which is the dominant pattern in the project. The "
          "client centralises the handling of the two most common cases in the response "
          "interceptor of the shared HTTP instance, which clears the stored session on a "
          "401 response and logs a 403 response."),
    ("p", "Two weaknesses follow from this distribution. There is no validation layer, "
          "because the module that contains the validation helpers is not attached to any "
          "route chain; the request bodies are therefore accepted as they arrive and are "
          "checked, where at all, inside the controllers. And no error boundary is "
          "declared anywhere in the client, so that an exception thrown while rendering "
          "any screen leaves the application without an interface rather than showing a "
          "recovery view."),

    ("h2", "5.19", "Build and Deployment"),
    ("p", "The client is built by the bundler, with the production output written to a "
          "distribution directory. The deployment configuration in the repository names the "
          "build command, the output directory and a rewrite rule that sends every "
          "unmatched path to the client entry point, which is the correct rule for a "
          "single-page application with client-side routing. It has one significant "
          "omission: the rewrite is unconditional, so that an interface path that is "
          "requested relatively, without the host of the server, is answered with the "
          "entry point document rather than being proxied to the server. The client "
          "contains three different strategies for addressing the server, namely the "
          "configured base address, a relative path and a literal local host and port, "
          "and only the first is correct in a deployment."),
    ("p", "The verification of the build itself is reported in Chapter 6, where it is shown "
          "that the type check of the client currently fails because twelve files of the "
          "client source contain unresolved merge-conflict markers, and that the "
          "development server accordingly serves an error overlay instead of the "
          "application. The server, by contrast, parses completely: all 107 of its "
          "JavaScript files pass a syntax check."),

    ("h2", "5.20", "Repository Screen Recording"),
    ("p", "Figures 5.6 and 5.7 are frames of the screen recording that is committed with "
          "the repository as a demonstration of the authentication flow. They are included "
          "as evidence of the interface that the project has produced, and they are "
          "distinct from the deployed screens of Figures 5.1 to 5.5 in that they were "
          "recorded from a local build."),
    ("fig", "shots/loginflow_187.png",
     "Fig. 5.6: Frame of the repository screen recording of the authentication flow", 5.4),
    ("fig", "shots/loginflow_237.png",
     "Fig. 5.7: Later frame of the repository screen recording of the authentication flow", 5.4),
]

CH6 = [
    ("h1", "CHAPTER – 6", "RESULT AND TESTING"),
    ("h2", "6.1", "Evaluation Approach"),
    ("p", "The repository contains no automated test suite: the server manifest defines a "
          "test script that reports the absence of tests, and the client manifest defines "
          "no test script and no test runner is configured. The evaluation reported in "
          "this chapter was therefore carried out manually, by a combination of five "
          "techniques that are described below, each of which produces evidence that can be "
          "inspected and repeated."),
    ("n", "Source-level verification. The complete source of both applications was read "
          "and the declared behaviour of every route, controller, model and middleware was "
          "recorded. This establishes what the system contains, independently of whether it "
          "runs."),
    ("n", "Static analysis. Every server file was submitted to the parser of the Node.js "
          "runtime, and the client was submitted to the TypeScript compiler in checking "
          "mode. This establishes whether the code is syntactically and structurally "
          "well formed."),
    ("n", "Execution of the deployed client. The deployed application was loaded in a "
          "headless Chromium browser, the rendered text of each public route was extracted, "
          "screenshots were captured, the console output was recorded and the network "
          "failures were logged."),
    ("n", "Interaction testing. The authentication form was submitted with the "
          "demonstration credentials that the deployed login page itself publishes, and the "
          "result was observed both in the interface and in the console output."),
    ("n", "Local build execution. The development server was started from the repository "
          "and the served routes were requested, which exposed a failure of the client "
          "build that is described in Section 6.3."),
    ("p", "No claim of a pass rate, a response time, a concurrency figure or a user "
          "count is made in this chapter, because none of these was measured. Where a "
          "subsystem could not be exercised, the corresponding test case is marked Not "
          "tested, and the reason is given."),

    ("h2", "6.2", "Test Environment"),
    ("table", "Table 6.1: Environment used for the evaluation",
     ["Item", "Configuration"],
     [["Workstation", "Windows host with a 64-bit processor; Node.js runtime with the "
       "package manager of the distribution"],
      ["Browser", "Chromium-based browser in headless mode for the automated capture, at "
       "a viewport of 1600 by 1000 pixels"],
      ["Client", "Served from the deployed host; and separately from a local development "
       "server bound to a loopback port"],
      ["Server", "Inspected statically and submitted to the runtime parser; the server "
       "package was not started because the environment provides no database instance and "
       "no third-party credentials"],
      ["Database", "No live instance was available; persistence was verified at the level "
       "of the schema declarations and the query construction"]],
     [1.4, 6.0]),

    ("h2", "6.3", "Results of the Static Analysis"),
    ("p", "The syntax check of the server was executed over every JavaScript file of the "
          "package with the parser of the runtime. The result is unambiguous: all 107 "
          "files parse without error, which confirms that the server package is "
          "syntactically complete and that no file contains an unresolved conflict marker."),
    ("p", "The type check of the client, by contrast, fails. The compiler reports "
          "unresolved merge-conflict markers in twelve files of the client source: six "
          "components under the landing page, namely the call to action, the footer, the "
          "creator page, the disclaimer, the documentation page, the privacy policy and the "
          "terms of service, together with five duplicates of those components under the "
          "legal directory and one further duplicate. The conflict markers are the "
          "remnants of an unresolved version-control merge, and their presence means that "
          "the client cannot be type-checked, cannot be built and cannot be served by the "
          "development server. This was confirmed by observation: the local development "
          "server starts and reports that it is ready, but every route it serves returns "
          "the overlay of the bundler's parse error, naming the footer component and the "
          "call to action component."),
    ("p", "The defect is not confined to the failing files, because the failing files are "
          "imported by the landing page, which is imported by the application root, which "
          "is imported by the entry point. The consequence is that the entire client is "
          "unservable in its current state, including the routes that would otherwise be "
          "reachable without a session. This is the single most significant finding of the "
          "evaluation and it is the reason why the authenticated screens of the "
          "application could not be captured from a local build and were captured from "
          "the deployment instead."),

    ("h2", "6.4", "Test Cases and Observed Results"),
    ("p", "Table 6.2 records the test cases that were executed, the action performed, the "
          "expected and the observed result and the status. The status vocabulary is the "
          "following: Pass, when the observed result corresponded to the expected "
          "result; Fail, when it did not; Partially verified, when the observation "
          "established part of the expectation only; and Not tested, when the case could "
          "not be exercised in the available environment."),
    ("table", "Table 6.2: Test cases, expected and observed results",
     ["Test ID", "Feature", "Action or input", "Expected result", "Observed result", "Status"],
     [["TC-01", "Public landing page", "Request the root path of the deployed host and "
       "capture the rendered text", "The marketing page renders with its feature grid and "
       "call to action", "The page rendered; the extracted text contains the hero heading, "
       "the statistics band and the feature sections", "Pass"],
      ["TC-02", "Sign-in screen", "Request the sign-in path and capture the rendered text",
       "The credential form, the Google sign-in control and the registration link are present",
       "All four elements were present in the extracted text; the screen also displays "
       "plain-text demonstration administrator credentials", "Pass"],
      ["TC-03", "Route protection on the client", "Request the dashboard, quiz, coding, "
       "community, résumé, learning and chatbot paths of the deployed host",
       "Each request is redirected to the sign-in page while no session is established",
       "All seven requests were redirected to the sign-in path and the rendered text was "
       "identical to the sign-in screen", "Pass"],
      ["TC-04", "Credential authentication", "Submit the demonstration credentials "
       "published by the sign-in page", "The session is established and the dashboard is "
       "rendered", "The request was rejected; the console recorded a response with an "
       "undefined user and reported the condition that the user was not found; the "
       "application remained on the sign-in page", "Fail"],
      ["TC-05", "Input validation on the sign-in form", "Observe the pattern attribute of "
       "the e-mail field", "The address is validated against a well-formed pattern",
       "The console reported that the pattern attribute is not a valid regular expression, "
       "because the expression is delimited by slashes inside the attribute value; the "
       "field therefore performs no client-side validation", "Fail"],
      ["TC-06", "Local development server", "Start the development server and request the "
       "root and the sign-in paths", "The application shell is served",
       "The server started and reported readiness, but both requests returned the "
       "bundler's parse-error overlay, caused by unresolved merge-conflict markers in two "
       "of the landing-page components", "Fail"],
      ["TC-07", "Client type checking", "Run the TypeScript compiler in checking mode over "
       "the client project", "No type errors are reported",
       "The compiler reported syntax errors arising from unresolved merge-conflict markers "
       "in twelve files of the client source", "Fail"],
      ["TC-08", "Server syntax integrity", "Submit every server file to the runtime parser",
       "Every file parses", "All 107 files parsed without error", "Pass"],
      ["TC-09", "Administration route protection", "Inspect the declaration of the "
       "administration feedback route group", "Every operation in the group requires an "
       "identity and the administrator role",
       "No protection is declared on the listing, review-status and delete operations of "
       "the group", "Fail"],
      ["TC-10", "Course authoring route protection", "Inspect the declaration of the "
       "course write routes", "The identity is established and the role is checked",
       "Only the role check is declared; because the role is read from the identity that "
       "the absent identity check would have populated, the routes answer 403 in all "
       "cases and the feature is inoperative", "Fail"],
      ["TC-11", "Unauthenticated access to the compiler", "Inspect the declaration of the "
       "compiler route", "The route is protected",
       "No protection is declared; the endpoint is open to anonymous use", "Fail"],
      ["TC-12", "Unauthenticated access to the conversational route", "Inspect the "
       "declaration of the conversational route", "The route is protected",
       "No protection is declared on the conversational route, although the two generative "
       "routes in the same group are protected", "Fail"],
      ["TC-13", "Note liking", "Trace the like route against the schema of the note",
       "The like is recorded and the count is returned",
       "The route reads and writes a field that the schema does not declare and assigns to "
       "a virtual property that has no setter, so the handler reaches its catch block and "
       "returns 500", "Fail"],
      ["TC-14", "Socket authentication", "Trace the handshake middleware against the "
       "claims issued by the authentication paths", "The socket is bound to the "
       "authenticated user",
       "The handshake resolves the user from a claim that the issued tokens do not carry, "
       "the lookup raises a cast error and the connection is admitted with a null user",
       "Fail"],
      ["TC-15", "Bearer token attachment on the client", "Compare the storage key read by "
       "the request interceptor with the key written by the session provider",
       "The interceptor attaches the token to every outgoing request",
       "The two use different capitalisations of the same key, so the interceptor normally "
       "finds no session and no token is attached", "Fail"],
      ["TC-16", "Contest leaderboard scoring", "Inspect the scoring rule and the rating "
       "utility", "Points are awarded by difficulty with a penalty for previous failures and "
       "the rating is recomputed",
       "The rule awards 100, 200 and 300 points for the three difficulty levels and adds "
       "twenty minutes per previous failure; the rating follows the Elo form with a "
       "constant of 32", "Pass"],
      ["TC-17", "Contest submission flow", "Exercise a submission", "The submission is "
       "graded and broadcast to the room", "No contest could be exercised: the server "
       "package was not started and no compiler credential is available", "Not tested"],
      ["TC-18", "Quiz attempt", "Answer and submit a quiz", "The attempt is scored and "
       "stored", "No attempt could be exercised: the server package was not started",
       "Not tested"],
      ["TC-19", "Skill assessment generation", "Request a generated assessment",
       "Items are generated and stored, and the evaluation returns a score",
       "The generation path requires the model credential and a database; neither was "
       "available", "Not tested"],
      ["TC-20", "Conversational assistant", "Send a message to the Study Buddy",
       "A reply is returned and rendered", "The path requires the provider credential and "
       "a database; neither was available. The deployed application returned an "
       "authentication failure before reaching this module", "Not tested"],
      ["TC-21", "Résumé export", "Export a completed résumé",
       "A PDF document is produced in the browser", "The export is implemented entirely in "
       "the browser and depends on a document library rather than on the server; the "
       "component was inspected but the export was not executed in the available "
       "environment", "Not tested"],
      ["TC-22", "Résumé scanner", "Scan a résumé", "A coverage report is returned",
       "The scan requires the server; the deterministic keyword comparison itself was "
       "verified by inspection of the three keyword utilities", "Not tested"],
      ["TC-23", "Placement statistics", "Request the placement endpoints",
       "Statistics are returned from a database",
       "The endpoints return a constant object declared inside the route file; no "
       "persistence is involved", "Partially verified"],
      ["TC-24", "Documentation pages", "Request the documentation and contributor pages",
       "Both pages render", "Both rendered and their text was extracted, as shown in "
       "Figures 5.4 and 5.5", "Pass"],
      ["TC-25", "Interface documentation accuracy", "Compare the published endpoint list "
       "with the mounted route table", "The published list corresponds to the mounted "
       "routes", "The published list corresponds in substance, but omits the two "
       "duplicated mounts, the unauthenticated groups and the separate document-generation "
       "service on the second port", "Partially verified"],
      ["TC-26", "Credential exposure", "Inspect the client build configuration and the "
       "server source", "No provider credential is delivered to the browser and no secret "
       "is committed",
       "Two provider credentials are inlined into the client bundle by the build tool and "
       "one credential and one signing secret appear as literals in the source", "Fail"]],
     [0.55, 1.25, 1.85, 1.75, 2.6, 0.85]),
    ("p", "The summary of the execution is as follows. Six cases passed, of which four are "
          "checks on the public deployment, one is the integrity check of the server source "
          "and one is the correctness of the contest scoring rule as verified against the "
          "implementation. Thirteen cases failed, and the failures cluster in four "
          "families: unresolved merge-conflict markers in the client source, protection "
          "that is declared incorrectly or not at all on the server, drift between a route "
          "and the schema it writes to, and secrets that are committed to the repository or "
          "delivered to the browser. Five cases could not be exercised and are marked as "
          "not tested, and two were verified in part. No case is reported as passed on the "
          "basis of the presence of a menu entry or of a screen."),

    ("h2", "6.5", "Defects and Security Findings"),
    ("p", "The defects discovered during the evaluation are consolidated below with a "
          "severity and a proposed correction. They are reported in full because a project "
          "report that conceals the faults of the system it describes is of little value."),
    ("table", "Table 6.3: Defects and security findings",
     ["Ref", "Finding", "Effect", "Proposed correction", "Severity"],
     [["D-01", "Twelve client files contain unresolved merge-conflict markers",
       "The client cannot be built, type-checked or served; the application is entirely "
       "unservable from the repository", "Resolve the merges, keep one copy of each "
       "duplicated legal component and remove the other", "Critical"],
      ["D-02", "The administrator feedback route group declares no protection",
       "Any visitor can list, modify and delete the feedback of all users",
       "Apply the identity and administrator middleware to the group", "High"],
      ["D-03", "The conversational, compiler and scanner routes declare no protection",
       "The provider credentials are consumed on behalf of anonymous callers",
       "Apply the identity middleware and add a per-caller rate limit", "High"],
      ["D-04", "Two provider credentials are inlined into the client bundle",
       "Every visitor can extract and use the credentials at the provider's expense",
       "Proxy the calls through the server, as the conversational path already does", "High"],
      ["D-05", "A news service credential and a signing secret are committed to the source",
       "The credentials are disclosed with every clone of the repository",
       "Move them to the environment, rotate them, and purge them from the history", "High"],
      ["D-06", "The request interceptor and the session provider use different storage keys",
       "The bearer token is not attached to the outgoing requests, so the authenticated "
       "features of the client fail against a server that requires it",
       "Use one constant for the key in both places", "Critical"],
      ["D-07", "The socket handshake resolves the user from a claim that the issued tokens "
       "do not carry", "The real-time channel carries no authenticated identity",
       "Resolve the user from the same set of claim names that the REST middleware accepts, "
       "and reject the handshake when the token is invalid", "High"],
      ["D-08", "The like route and the note schema disagree on the field names, and the "
       "virtual count has no setter", "The like operation always fails with a 500",
       "Declare the field in the schema, or change the route to use the declared field and "
       "a setter for the virtual", "Medium"],
      ["D-09", "The course write routes apply the role check without the identity check",
       "The course authoring feature is inoperative and returns 403",
       "Apply the identity middleware before the role middleware", "Medium"],
      ["D-10", "The system-log creation route requires an identity but not the "
       "administrator role", "Any signed-in user may write to the audit trail",
       "Apply the administrator check", "Medium"],
      ["D-11", "The session cookie declares the secure attribute unconditionally",
       "The session cannot be established over plain HTTP, which breaks local development",
       "Derive the attribute from the environment", "Low"],
      ["D-12", "The application trusts forwarded protocol headers unconditionally",
       "The address-based logic of the rate limiter can be defeated behind an "
       "uncooperative proxy", "Trust the proxy only in a deployment environment", "Low"],
      ["D-13", "The client is not code-split and the route table imports every screen "
       "statically", "The initial bundle carries the whole application, including three "
       "components of more than fifty kilobytes",
       "Load the routed screens lazily and split the vendor libraries into separate chunks",
       "Medium"],
      ["D-14", "No error boundary is declared in the client",
       "A rendering exception leaves the application without an interface",
       "Add an error boundary at the shell and at the administration branch", "Medium"],
      ["D-15", "The validator module is not attached to any route",
       "The request bodies are accepted without structural validation",
       "Attach the validation middleware to the mutating routes", "Medium"],
      ["D-16", "Dead code: an unrouted placement-statistics page of about fifty-three "
       "kilobytes, an unrouted task board, six duplicated legal components, an empty "
       "utility file, an empty schema file and three orphan schemas",
       "The size of the code base and the difficulty of reviewing it are increased without "
       "benefit", "Remove the dead code or route it", "Low"],
      ["D-17", "The dashboard seeds a demonstration user and the recent-attempts panel is "
       "mapped from a commented-out block", "The statistics row shows demonstration "
       "values and the attempts panel is always empty",
       "Bind the panel to the session state and restore the mapping", "Medium"],
      ["D-18", "Duplicate mounts of the assessment and conversational route groups",
       "The second prefix is unreachable and the documented interface is wider than the "
       "effective one", "Remove the duplicate mounts", "Low"]],
     [0.5, 2.1, 2.4, 2.6, 0.9]),

    ("h2", "6.6", "Limitations of the Evaluation"),
    ("b", "No database instance was available, so the server package was not started and "
          "no endpoint that requires persistence was exercised. The server was therefore "
          "verified by inspection and by syntax analysis rather than by execution."),
    ("b", "No third-party credentials were available, so no inference, compiler, video or "
          "news integration was exercised end to end."),
    ("b", "The client could not be built or served from the repository because of the "
          "merge-conflict markers, so all client evidence was obtained from the deployed "
          "host, which necessarily represents the last successful build rather than the "
          "current source."),
    ("b", "The authenticated screens of the application could not be captured, because the "
          "demonstration credentials published by the deployed sign-in page are not "
          "accepted by the backend that the deployment is configured to use. The evidence "
          "supplied with this project, which shows a dashboard with populated statistics "
          "panels and with errors in some of the data panels, is consistent with the "
          "code-level findings of Sections 6.3 and 6.5, but it could not be reproduced "
          "independently during this evaluation, and no claim is made here that any "
          "dashboard panel was observed to work."),
    ("b", "No performance measurement was performed, and no figure for response time, "
          "throughput, concurrency or availability is asserted anywhere in this report."),

    ("h2", "6.7", "Discussion"),
    ("p", "The evaluation supports three conclusions. The first is that the system is "
          "substantially complete as a design and as an implementation: the module set is "
          "broad, the layering is consistent, the data model is coherent, the external "
          "integrations are implemented against real interfaces rather than mocked, and the "
          "server code is of production quality in its structure and its error handling."),
    ("p", "The second is that the principal obstacles to the system's operation are "
          "configurational rather than architectural. Of the eighteen findings, the "
          "critical and high-severity ones are a merge that was never completed, a "
          "mismatch between two storage keys, four route groups that omit the protection "
          "their data requires, a token claim that the real-time layer does not recognise, "
          "and three credentials that are exposed. Each of these is a matter of a few "
          "lines, and none of them requires a change to the architecture of Chapter 4."),
    ("p", "The third is that the project's most ambitious claims are the least supported "
          "by the evidence. The platform's value proposition rests on the consolidation "
          "of learning, assessment and career preparation, and three of the modules that "
          "complete that proposition, namely the placement statistics, the dashboard "
          "aggregations and the cover-letter workflow, are served by static or "
          "client-local data. The honest statement of the result is therefore that "
          "Elevora AI is a well-structured platform with a working skeleton and a "
          "substantial set of implemented services, which requires a consolidation "
          "pass over its configuration and its credentials before it can be presented as "
          "the unified environment that the problem statement of Section 1.2 describes."),
]

CONCLUSION = [
    ("h1", "CONCLUSION", None),
    ("p", "This report has described the design, the implementation and the evaluation of "
          "Elevora AI, a full-stack web application that consolidates structured learning, "
          "timed assessment, code practice, documentation and career preparation behind a "
          "single authenticated and role-based interface. The work began with the "
          "observation that the technology student is obliged to assemble a learning "
          "workflow from separate services, and that no component of that workflow can "
          "report on the learner's overall progress because each of them holds only its "
          "own record."),
    ("p", "The implemented system meets that observation with a substantial engineering "
          "response. The client is a single-page application of nineteen learner modules "
          "and nine administration modules, written in TypeScript and built with Vite, "
          "with an embedded code workspace, a conversational assistant, a résumé builder "
          "with an applicant-tracking-system scanner and a cover-letter generator. The "
          "server is an Express application of thirty route modules, twenty-four "
          "controllers and thirty-two MongoDB schemas, offering JWT authentication with "
          "e-mail one-time-password verification and Google sign-in, role-based "
          "authorisation, four learning-track route groups, quiz authoring and attempts, "
          "generative assessment with a stored evaluation, community moderation, a note "
          "system with file attachments, video progress, notifications, an administration "
          "console with analytics and an audit trail, and a contest subsystem that "
          "executes submitted code, applies a difficulty-based scoring rule with "
          "penalties, recomputes an Elo rating and broadcasts live updates over a socket "
          "channel. Three language models are integrated, each for the task to which it is "
          "best suited."),
    ("p", "The evaluation was deliberately adversarial towards the project's own claims. "
          "The server source parses completely, but twelve files of the client contain "
          "unresolved merge-conflict markers, so that the client cannot currently be built "
          "or served from the repository. Four route groups on the server omit the access "
          "control their data requires, one of which permits anonymous deletion of user "
          "feedback. The real-time channel admits connections without establishing an "
          "identity. The client and the server refer to the session under two different "
          "storage keys, so that authenticated requests are sent without a token. Two "
          "provider credentials are compiled into the browser bundle and two more appear as "
          "literals in the source. The practice workspace addresses the compiler at a "
          "literal local address and therefore cannot work in a deployment. The dashboard "
          "seeds a demonstration user, and the placement module is served from a "
          "constant. The cover-letter module has no server counterpart, and the payment "
          "facility that the project synopsis describes has no server implementation at "
          "all. The authenticated screens of the application could not be captured, "
          "because the deployed build rejects the demonstration credentials that its own "
          "sign-in page publishes."),
    ("p", "These findings are reported rather than smoothed away, because the value of "
          "the project is as a working piece of software that others are invited to "
          "contribute to, and a report that concealed the faults would misrepresent both "
          "the software and the community that inherits it. The corrections required are "
          "enumerated in Table 6.3 and are, with two exceptions, a matter of tens of lines "
          "rather than of redesign."),
    ("h2", "Future Enhancements", None),
    ("p", "The following improvements follow directly from the gaps identified during the "
          "inspection and the evaluation. They are listed in the order in which they would "
          "most usefully be undertaken."),
    ("n", "Resolve the outstanding merges in the client source, remove the duplicated "
          "legal components, and restore a clean build so that the type check, the lint "
          "check and the production bundle all pass."),
    ("n", "Introduce a single source of truth for the session storage key and for the "
          "token claim names, so that the client, the route middleware and the socket "
          "handshake agree, and introduce an automated test that asserts the agreement."),
    ("n", "Complete the access control matrix: apply the identity and role middleware to "
          "every route group that lacks it, add the ownership test to the note, progress, "
          "review and attempt resources, and record the resulting matrix as a "
          "specification artefact."),
    ("n", "Move all provider access behind the server, including the two calls that are "
          "currently made from the browser, remove the committed credentials from the "
          "source, and rotate the keys that were exposed."),
    ("n", "Replace the static placement data, the dashboard seed values and the mock "
          "course catalogue with persisted records, so that the three modules that "
          "complete the platform's central proposition rest on the database."),
    ("n", "Implement the cover-letter workflow on the server, with storage, retrieval, a "
          "plain variant for machine parsing and an assessment of the letter against the "
          "target role, so that the two career-document modules become symmetric."),
    ("n", "Either implement a server-side subscription with the payment provider, or "
          "remove the subscription screens, so that the interface does not advertise a "
          "facility that the platform cannot honour."),
    ("n", "Introduce code splitting for the routed screens and an error boundary at the "
          "application shell, which together address the two client defects that most "
          "affect the experience of a first-time visitor."),
    ("n", "Establish an automated test suite, beginning with the route middleware and the "
          "utility functions, which are the parts of the system that the inspection "
          "identified as most defective and which are the cheapest to test in isolation."),
    ("n", "Extend the assessment engine with item review and distractor analysis, and "
          "record the agreement between the generated evaluation and a human evaluation "
          "on a sample of attempts, so that the reported skill levels can be interpreted "
          "with an understanding of their reliability."),
    ("n", "Add an explicit deployment guide that records the required environment "
          "variables, the proxy rule that the client and the server require in order to "
          "share an origin, and the order in which the two applications must be brought "
          "up, since the absence of such a document is the likely origin of several of the "
          "defects recorded in Chapter 6."),
]

REFERENCES = [
    ("h1", "REFERENCES", None),
    ("ref", "[1]", "Richardson, L. and", "Fielding, R.", "\"REST\" Web Architecture "
     "Dissertation, Chapter 5: Resource-Oriented Architecture, University of California, "
     "Irvine, 2000. Available at: https://www.ics.uci.edu/~fielding/pubs/dissertation/"
     "rest_arch_style.htm", None),
    ("ref", "[2]", "Brown, E.", "Getting Started with Django 5.0", "O'Reilly Media, 2024. "
     "Consulted for the repository, template and object-relational mapping conventions "
     "compared in Section 2.2. Available at: https://docs.djangoproject.com/en/5.0/", None),
    ("ref", "[3]", "OpenJS Foundation.", "Express — Node.js Web Application Framework, "
     "Version 5 documentation.", "Available at: https://expressjs.com/en/guide/routing.html", None),
    ("ref", "[4]", "MongoDB Inc.", "Mongoose 8.x Documentation — Schemas, Models and "
     "Middleware.", "Available at: https://mongoosejs.com/docs/", None),
    ("ref", "[5]", "OpenJS Foundation.", "jsonwebtoken — JSON Web Token implementation for "
     "Node.js.", "Available at: https://github.com/auth0/node-jsonwebtoken", None),
    ("ref", "[6]", "Sandhu, R. S., Coyne, E. J., Feinstein, H. L. and Youman, C. E.",
     "\"Role-Based Access Control Models\",", "IEEE Computer, vol. 29, no. 2, pp. 38-47, "
     "February 1996. Cited in Section 2.5 as the origin of the role-based model applied "
     "in Sections 3.2 and 4.6.", None),
    ("ref", "[7]", "Hamari, J., Koivisto, J. and Sarsa, H.", "\"Does Gamification Work? A "
     "Literature Review of Empirical Studies on Gamification\",", "Proceedings of the 47th "
     "Hawaii International Conference on System Sciences (HICSS-47), 2014, pp. 1-10. Cited "
     "in Section 2.6.", None),
    ("ref", "[8]", "Mollick, E. R. and Mollick, L.", "\"Using AI to Implement Effective "
     "Teaching Strategies in Classrooms: Five Strategies, Including Prompts\",", "SSRN "
     "Electronic Journal, 2023. Available at: "
     "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4323286", None),
    ("ref", "[9]", "Pinto, G., Steinmacher, I. and Gerosa, M. A.", "\"More Common Than You "
     "Think: An In-depth Study of Casual Contributors\",", "Proceedings of the 23rd IEEE "
     "International Conference on Software Analysis, Evolution and Reengineering "
     "(SANER), 2016, pp. 199-208. Cited in Section 2.8.", None),
    ("ref", "[10]", "Elo, A. E.", "\"The Rating of Chess Players\",", "US Chess Federation, "
     "New York, 1978. The basis of the rating computation implemented in "
     "Server/utils/ratingCalculator.js and described in Section 5.13.", None),
    ("ref", "[11]", "Judge0 Ltd. and the Judge0 open-source contributors.", "\"Judge0 — "
     "Open Source Code and CPU Judge\",", "Available at: https://judge0.com/ and "
     "https://github.com/judge0/judge0", None),
    ("ref", "[12]", "Google.", "\"Gemini API — Generative Language API Documentation\", "
     "v1beta models endpoint.", "Available at: "
     "https://ai.google.dev/gemini-api/docs", None),
    ("ref", "[13]", "OpenAI.", "\"OpenAI API Reference — Chat Completions\",", "Available at: "
     "https://platform.openai.com/docs/api-reference/chat", None),
    ("ref", "[14]", "Groq, Inc.", "\"Groq API Documentation — OpenAI-compatible "
     "Inference Endpoint\",", "Available at: https://console.groq.com/docs", None),
    ("ref", "[15]", "Socket.IO Inc.", "\"Socket.IO 4.x Documentation — Rooms and "
     "Broadcasting\",", "Available at: https://socket.io/docs/v4/", None),
    ("ref", "[16]", "Meta Platforms, Inc. and contributors.", "\"React 18 — A JavaScript "
     "Library for Building User Interfaces\",", "Available at: https://react.dev/ and "
     "https://react.dev/blog/2022/03/29/react-v18", None),
    ("ref", "[17]", "Evan You and contributors.", "\"Vite — Next Generation Frontend "
     "Tooling\",", "Available at: https://vitejs.dev/guide/", None),
    ("ref", "[18]", "Adam Wathan and contributors.", "\"Tailwind CSS — A Utility-First CSS "
     "Framework\",", "Available at: https://tailwindcss.com/docs", None),
    ("ref", "[19]", "Microsoft Corporation.", "\"Monaco Editor — The Editor That Powers "
     "Visual Studio Code\",", "Available at: https://microsoft.github.io/monaco-editor/", None),
    ("ref", "[20]", "The Firebase Team.", "\"Firebase Authentication — Sign in with Google\","
     "and the Firebase JavaScript SDK documentation.", "Available at: "
     "https://firebase.google.com/docs/auth", None),
    ("ref", "[21]", "Auth0, Inc.", "\"JSON Web Token (JWT) — RFC 7519\",", "Available at: "
     "https://jwt.io/", None),
    ("ref", "[22]", "Nodemailer.", "\"Nodemailer — Email Sending Library for Node.js\",", "Available at: "
     "https://nodemailer.com/", None),
    ("ref", "[23]", "Google Developers.", "\"YouTube Data API v3 Documentation\",", "Available at: https://developers.google.com/youtube/v3/docs", None),
    ("ref", "[24]", "NewsAPI.", "\"NewsAPI — Top Headlines Endpoint Documentation\",", "Available at: https://newsapi.org/docs", None),
    ("ref", "[25]", "Paystack, Inc. and Stripe, Inc.", "\"Stripe — Payment Links and "
     "Checkout Documentation\",", "Consulted in relation to the subscription module "
     "described in Sections 3.3 and 5.15. Available at: https://docs.stripe.com/", None),
    ("ref", "[26]", "Mozilla Foundation and contributors.", "\"MDN Web Docs — Fetch API, "
     "Web Storage and Regular Expressions\",", "Available at: https://developer.mozilla.org/",
     None),
    ("ref", "[27]", "The OpenJS Foundation and contributors.", "\"Express, Node.js and "
     "Socket.IO — Documentation and Release Notes\",", "Consulted for the versions and the "
     "middleware semantics recorded in Table 3.4.", None),
    ("ref", "[28]", "MrAlpha00.", "\"Dev-Elevate — Elevora AI Project Repository\", "
     "GitHub, 2025.", "The software described in this report. Available at: "
     "https://github.com/MrAlpha00/Dev-Elevate", None),
]
