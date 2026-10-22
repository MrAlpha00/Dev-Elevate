import React, { useState, useMemo } from "react";
import { motion } from "framer-motion";
import {
  Play,
  RotateCcw,
  Terminal,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  CheckCircle2,
  Code2,
  Eye,
  Loader2,
} from "lucide-react";
import axiosInstance from "../../../api/axiosinstance";
import { useGlobalState } from "../../../contexts/GlobalContext";

export interface LanguageConfig {
  name: string;
  id: number | "web";
  extension: string;
  filename: string;
  starterCode: string;
}

export const LANGUAGES: LanguageConfig[] = [
  {
    name: "Python",
    id: 71,
    extension: "py",
    filename: "main.py",
    starterCode: `# Python (3.8.1)\ndef greet(name: str) -> str:\n    return f"Hello, {name}!"\n\nif __name__ == "__main__":\n    print(greet("World"))\n`,
  },
  {
    name: "C",
    id: 50,
    extension: "c",
    filename: "main.c",
    starterCode: `// C (GCC 9.2.0)\n#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}\n`,
  },
  {
    name: "C++",
    id: 54,
    extension: "cpp",
    filename: "main.cpp",
    starterCode: `// C++ (GCC 9.2.0)\n#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}\n`,
  },
  {
    name: "Java",
    id: 62,
    extension: "java",
    filename: "Main.java",
    starterCode: `// Java (OpenJDK 13.0.1)\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}\n`,
  },
  {
    name: "JavaScript (Node.js)",
    id: 63,
    extension: "js",
    filename: "index.js",
    starterCode: `// JavaScript (Node.js 12.14.0)\nfunction greet(name) {\n    return \`Hello, \${name}!\`;\n}\n\nconsole.log(greet("World"));\n`,
  },
  {
    name: "TypeScript",
    id: 74,
    extension: "ts",
    filename: "index.ts",
    starterCode: `// TypeScript (3.7.4)\ninterface User {\n    name: string;\n}\n\nconst user: User = { name: "World" };\nconsole.log(\`Hello, \${user.name}!\`);\n`,
  },
  {
    name: "C#",
    id: 51,
    extension: "cs",
    filename: "Program.cs",
    starterCode: `// C# (Mono 6.6.0.161)\nusing System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}\n`,
  },
  {
    name: "Go",
    id: 60,
    extension: "go",
    filename: "main.go",
    starterCode: `// Go (1.13.5)\npackage main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}\n`,
  },
  {
    name: "Rust",
    id: 73,
    extension: "rs",
    filename: "main.rs",
    starterCode: `// Rust (1.40.0)\nfn main() {\n    println!("Hello, World!");\n}\n`,
  },
  {
    name: "PHP",
    id: 68,
    extension: "php",
    filename: "index.php",
    starterCode: `<?php\n// PHP (7.4.1)\necho "Hello, World!\\n";\n`,
  },
  {
    name: "Ruby",
    id: 72,
    extension: "rb",
    filename: "main.rb",
    starterCode: `# Ruby (2.7.0)\ndef greet(name)\n    "Hello, #{name}!"\nend\n\nputs greet("World")\n`,
  },
  {
    name: "Kotlin",
    id: 78,
    extension: "kt",
    filename: "Main.kt",
    starterCode: `// Kotlin (1.3.70)\nfun main() {\n    println("Hello, World!")\n}\n`,
  },
  {
    name: "Swift",
    id: 83,
    extension: "swift",
    filename: "main.swift",
    starterCode: `// Swift (5.2.3)\nimport Foundation\n\nprint("Hello, World!")\n`,
  },
  {
    name: "SQL (SQLite)",
    id: 82,
    extension: "sql",
    filename: "query.sql",
    starterCode: `-- SQLite (3.27.2)\nCREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, role TEXT);\nINSERT INTO users (name, role) VALUES ('Alice', 'Admin'), ('Bob', 'Developer'), ('Charlie', 'Designer');\nSELECT * FROM users;\n`,
  },
  {
    name: "Bash",
    id: 46,
    extension: "sh",
    filename: "script.sh",
    starterCode: `#!/bin/bash\n# Bash (5.0.0)\nNAME="World"\necho "Hello, $NAME!"\n`,
  },
  {
    name: "HTML/CSS/JS",
    id: "web",
    extension: "html",
    filename: "preview.html",
    starterCode: "",
  },
];

interface ExecutionResult {
  stdout?: string | null;
  stderr?: string | null;
  compile_output?: string | null;
  message?: string | null;
  status?: {
    id: number;
    description: string;
  };
  time?: string | null;
  memory?: number | null;
}

const CompilerPage: React.FC = () => {
  const { state } = useGlobalState();
  const [selectedLanguage, setSelectedLanguage] = useState<LanguageConfig>(LANGUAGES[0]);
  const [code, setCode] = useState<string>(LANGUAGES[0].starterCode);
  const [stdin, setStdin] = useState<string>("");
  const [showStdin, setShowStdin] = useState<boolean>(false);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [result, setResult] = useState<ExecutionResult | null>(null);
  const [rawError, setRawError] = useState<string | null>(null);

  // Web mode state
  const [webTab, setWebTab] = useState<"html" | "css" | "js">("html");
  const [htmlCode, setHtmlCode] = useState("<h1>Hello, World!</h1>\n<p>Welcome to Elevora AI Live Preview.</p>");
  const [cssCode, setCssCode] = useState("body {\n  font-family: sans-serif;\n  padding: 2rem;\n  color: #3b82f6;\n}");
  const [jsCode, setJsCode] = useState('console.log("Interactive web preview loaded");');

  const srcDoc = useMemo(() => {
    return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="utf-8" />
          <style>${cssCode}</style>
        </head>
        <body>
          ${htmlCode}
          <script>${jsCode}</script>
        </body>
      </html>
    `;
  }, [htmlCode, cssCode, jsCode]);

  const handleLanguageChange = (langName: string) => {
    const lang = LANGUAGES.find((l) => l.name === langName);
    if (!lang) return;
    setSelectedLanguage(lang);
    if (lang.id !== "web") {
      setCode(lang.starterCode);
    }
    setResult(null);
    setRawError(null);
  };

  const handleResetCode = () => {
    if (selectedLanguage.id !== "web") {
      setCode(selectedLanguage.starterCode);
    } else {
      setHtmlCode("<h1>Hello, World!</h1>\n<p>Welcome to Elevora AI Live Preview.</p>");
      setCssCode("body {\n  font-family: sans-serif;\n  padding: 2rem;\n  color: #3b82f6;\n}");
      setJsCode('console.log("Interactive web preview loaded");');
    }
    setResult(null);
    setRawError(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Tab") {
      e.preventDefault();
      const target = e.currentTarget;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      const val = target.value;
      const newVal = val.substring(0, start) + "    " + val.substring(end);
      setCode(newVal);
      setTimeout(() => {
        target.selectionStart = target.selectionEnd = start + 4;
      }, 0);
    }
  };

  const handleRun = async () => {
    if (selectedLanguage.id === "web") {
      // In web mode, the iframe automatically updates with srcDoc
      return;
    }

    setIsRunning(true);
    setResult(null);
    setRawError(null);

    try {
      const encodedCode = btoa(unescape(encodeURIComponent(code)));
      const response = await axiosInstance.post("/api/v1/compiler", {
        source_code: encodedCode,
        language_id: selectedLanguage.id,
        stdin: stdin,
        is_base64: true,
      });

      const data = response.data as ExecutionResult;
      setResult(data);
    } catch (error: any) {
      const errorData = error?.response?.data;
      if (errorData && typeof errorData === "object" && (errorData.compile_output || errorData.stderr || errorData.stdout)) {
        setResult(errorData);
      } else {
        const errorMsg =
          errorData?.error ||
          errorData?.message ||
          error?.message ||
          "Execution failed. Please check your network or try again.";
        setRawError(errorMsg);
      }
    } finally {
      setIsRunning(false);
    }
  };

  const getStatusBadge = () => {
    if (isRunning) {
      return (
        <span className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
          <Loader2 className="w-3.5 h-3.5 animate-spin" />
          Running...
        </span>
      );
    }
    if (rawError) {
      return (
        <span className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
          <AlertCircle className="w-3.5 h-3.5" />
          Execution Error
        </span>
      );
    }
    if (result) {
      if (result.compile_output) {
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full bg-rose-500/10 text-rose-400 border border-rose-500/20">
            <AlertCircle className="w-3.5 h-3.5" />
            Compilation Error
          </span>
        );
      }
      if (result.stderr) {
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <AlertCircle className="w-3.5 h-3.5" />
            Runtime Error
          </span>
        );
      }
      return (
        <span className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <CheckCircle2 className="w-3.5 h-3.5" />
          {result.status?.description || "Success"}
        </span>
      );
    }
    return (
      <span className={`px-2.5 py-1 text-xs font-medium rounded-full ${
        state.darkMode ? "bg-gray-800 text-gray-400" : "bg-gray-100 text-gray-600"
      }`}>
        Ready
      </span>
    );
  };

  return (
    <div className={`min-h-screen ${state.darkMode ? "bg-gray-950 text-gray-100" : "bg-gray-50 text-gray-900"}`}>
      <div className="max-w-7xl px-4 py-8 mx-auto space-y-6 sm:px-6 lg:px-8">
        {/* Header Bar */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
          <div>
            <div className="flex items-center gap-2">
              <Code2 className="w-7 h-7 text-blue-500" />
              <h1 className="text-3xl font-bold tracking-tight">Code Compiler</h1>
            </div>
            <p className={`text-sm mt-1 ${state.darkMode ? "text-gray-400" : "text-gray-600"}`}>
              Write, compile, and run code instantly across 15+ supported languages
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleResetCode}
              type="button"
              className={`inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg border transition ${
                state.darkMode
                  ? "border-gray-700 bg-gray-900 text-gray-300 hover:bg-gray-800"
                  : "border-gray-300 bg-white text-gray-700 hover:bg-gray-100"
              }`}
              title="Reset code to starter template"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>

            {selectedLanguage.id !== "web" ? (
              <button
                onClick={handleRun}
                disabled={isRunning}
                type="button"
                className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 shadow-md shadow-blue-500/20"
              >
                {isRunning ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Executing...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-white" />
                    <span>Run Code</span>
                  </>
                )}
              </button>
            ) : (
              <div className="flex items-center gap-1 text-xs text-blue-500 font-medium px-3 py-2 rounded-lg bg-blue-500/10 border border-blue-500/20">
                <Eye className="w-4 h-4" />
                <span>Live Preview Active</span>
              </div>
            )}
          </div>
        </motion.div>

        {/* Language Selector Toolbar */}
        <div
          className={`flex flex-wrap items-center justify-between gap-3 p-3 rounded-xl border ${
            state.darkMode ? "bg-gray-900/90 border-gray-800" : "bg-white border-gray-200"
          } shadow-sm`}
        >
          <div className="flex items-center gap-3">
            <label className="text-xs font-semibold uppercase tracking-wider text-gray-500">
              Language:
            </label>
            <select
              value={selectedLanguage.name}
              onChange={(e) => handleLanguageChange(e.target.value)}
              className={`px-3 py-1.5 text-sm font-medium rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                state.darkMode
                  ? "bg-gray-800 border-gray-700 text-white"
                  : "bg-gray-50 border-gray-300 text-gray-900"
              }`}
            >
              {LANGUAGES.map((lang) => (
                <option key={lang.name} value={lang.name}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-3">
            <span
              className={`text-xs font-mono px-2 py-1 rounded ${
                state.darkMode ? "bg-gray-800 text-gray-400" : "bg-gray-100 text-gray-600"
              }`}
            >
              {selectedLanguage.filename}
            </span>
            {getStatusBadge()}
          </div>
        </div>

        {/* Main IDE Workspace */}
        {selectedLanguage.id === "web" ? (
          /* Web Mode */
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div
              className={`rounded-2xl border overflow-hidden flex flex-col ${
                state.darkMode ? "bg-gray-900 border-gray-800" : "bg-white border-gray-200"
              } shadow-sm`}
            >
              <div
                className={`flex items-center border-b px-4 py-2 gap-2 ${
                  state.darkMode ? "border-gray-800 bg-gray-900/60" : "border-gray-200 bg-gray-50"
                }`}
              >
                {(["html", "css", "js"] as const).map((tab) => (
                  <button
                    key={tab}
                    type="button"
                    onClick={() => setWebTab(tab)}
                    className={`px-3 py-1.5 text-xs font-semibold uppercase rounded-md transition ${
                      webTab === tab
                        ? "bg-blue-600 text-white shadow-sm"
                        : state.darkMode
                        ? "text-gray-400 hover:text-gray-200"
                        : "text-gray-600 hover:text-gray-900"
                    }`}
                  >
                    {tab.toUpperCase()}
                  </button>
                ))}
              </div>

              <div className="p-4 flex-1 min-h-[420px]">
                {webTab === "html" && (
                  <textarea
                    value={htmlCode}
                    onChange={(e) => setHtmlCode(e.target.value)}
                    className={`w-full h-full min-h-[380px] p-3 font-mono text-sm rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none ${
                      state.darkMode ? "bg-gray-950 border-gray-800 text-gray-100" : "bg-gray-50 border-gray-200 text-gray-900"
                    }`}
                    placeholder="Enter HTML markup..."
                  />
                )}
                {webTab === "css" && (
                  <textarea
                    value={cssCode}
                    onChange={(e) => setCssCode(e.target.value)}
                    className={`w-full h-full min-h-[380px] p-3 font-mono text-sm rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none ${
                      state.darkMode ? "bg-gray-950 border-gray-800 text-gray-100" : "bg-gray-50 border-gray-200 text-gray-900"
                    }`}
                    placeholder="Enter CSS styling..."
                  />
                )}
                {webTab === "js" && (
                  <textarea
                    value={jsCode}
                    onChange={(e) => setJsCode(e.target.value)}
                    className={`w-full h-full min-h-[380px] p-3 font-mono text-sm rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none ${
                      state.darkMode ? "bg-gray-950 border-gray-800 text-gray-100" : "bg-gray-50 border-gray-200 text-gray-900"
                    }`}
                    placeholder="Enter JavaScript code..."
                  />
                )}
              </div>
            </div>

            {/* Live Web Preview */}
            <div
              className={`rounded-2xl border overflow-hidden flex flex-col ${
                state.darkMode ? "bg-gray-900 border-gray-800" : "bg-white border-gray-200"
              } shadow-sm`}
            >
              <div
                className={`flex items-center justify-between border-b px-4 py-2.5 ${
                  state.darkMode ? "border-gray-800 bg-gray-900/60" : "border-gray-200 bg-gray-50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Eye className="w-4 h-4 text-blue-500" />
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                    Live Web Preview
                  </span>
                </div>
              </div>
              <div className="flex-1 p-2 bg-white min-h-[420px]">
                <iframe
                  srcDoc={srcDoc}
                  title="live-preview"
                  sandbox="allow-scripts"
                  className="w-full h-full min-h-[400px] border-0 rounded"
                />
              </div>
            </div>
          </div>
        ) : (
          /* Standard Compiler Mode: Two-Column / Split Layout */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left: Code Editor (7 cols) */}
            <div
              className={`lg:col-span-7 rounded-2xl border overflow-hidden flex flex-col ${
                state.darkMode ? "bg-gray-900 border-gray-800" : "bg-white border-gray-200"
              } shadow-sm`}
            >
              <div
                className={`flex items-center justify-between border-b px-4 py-2.5 ${
                  state.darkMode ? "border-gray-800 bg-gray-900/80" : "border-gray-200 bg-gray-50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Code2 className="w-4 h-4 text-blue-500" />
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                    Source Code ({selectedLanguage.name})
                  </span>
                </div>
                <span className="text-xs text-gray-400">
                  {code.split("\n").length} lines
                </span>
              </div>

              <div className="relative flex-1 p-3">
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  onKeyDown={handleKeyDown}
                  spellCheck={false}
                  autoCapitalize="off"
                  autoComplete="off"
                  className={`w-full min-h-[440px] p-4 font-mono text-sm leading-relaxed rounded-xl border focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y ${
                    state.darkMode
                      ? "bg-gray-950 border-gray-800/80 text-gray-100 placeholder-gray-600"
                      : "bg-gray-50 border-gray-200 text-gray-900 placeholder-gray-400"
                  }`}
                  placeholder={`Write your ${selectedLanguage.name} code here...`}
                />
              </div>
            </div>

            {/* Right: Output & Stdin Panel (5 cols) */}
            <div
              className={`lg:col-span-5 rounded-2xl border overflow-hidden flex flex-col ${
                state.darkMode ? "bg-gray-900 border-gray-800" : "bg-white border-gray-200"
              } shadow-sm`}
            >
              <div
                className={`flex items-center justify-between border-b px-4 py-2.5 ${
                  state.darkMode ? "border-gray-800 bg-gray-900/80" : "border-gray-200 bg-gray-50"
                }`}
              >
                <div className="flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-blue-500" />
                  <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                    Terminal Output
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setShowStdin((prev) => !prev)}
                    className={`inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium rounded-md border transition ${
                      showStdin || stdin.trim().length > 0
                        ? "border-blue-500/40 text-blue-400 bg-blue-500/10"
                        : state.darkMode
                        ? "border-gray-700 text-gray-400 hover:text-gray-200"
                        : "border-gray-300 text-gray-600 hover:text-gray-900"
                    }`}
                  >
                    <span>Input (stdin)</span>
                    {stdin.trim().length > 0 && (
                      <span className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                    )}
                    {showStdin ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>

                  {(result || rawError) && (
                    <button
                      type="button"
                      onClick={() => {
                        setResult(null);
                        setRawError(null);
                      }}
                      className="text-xs text-gray-400 hover:text-gray-200"
                    >
                      Clear
                    </button>
                  )}
                </div>
              </div>

              {/* Collapsible Program Input (stdin) Panel */}
              {showStdin && (
                <div
                  className={`p-3 border-b transition-all ${
                    state.darkMode ? "border-gray-800 bg-gray-950/60" : "border-gray-200 bg-gray-50/80"
                  }`}
                >
                  <label className="block mb-1 text-xs font-medium text-gray-400">
                    Standard Input (stdin) — passed to program on run
                  </label>
                  <textarea
                    value={stdin}
                    onChange={(e) => setStdin(e.target.value)}
                    rows={3}
                    placeholder="Provide input arguments or lines for input(), cin, etc..."
                    className={`w-full p-2.5 text-xs font-mono rounded-lg border focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none ${
                      state.darkMode
                        ? "bg-gray-900 border-gray-700 text-gray-100 placeholder-gray-500"
                        : "bg-white border-gray-300 text-gray-900 placeholder-gray-400"
                    }`}
                  />
                </div>
              )}

              {/* Read-Only Terminal Panel */}
              <div className="flex-1 p-3 flex flex-col min-h-[380px]">
                {isRunning ? (
                  <div className="flex-1 flex flex-col items-center justify-center py-16 text-center text-gray-400">
                    <Loader2 className="w-8 h-8 mb-3 text-blue-500 animate-spin" />
                    <p className="text-sm font-medium">Executing code on OnlineCompiler...</p>
                    <p className="text-xs text-gray-500 mt-1">Please wait for execution results</p>
                  </div>
                ) : rawError ? (
                  <div className="p-4 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-300 text-sm font-mono whitespace-pre-wrap">
                    <div className="flex items-center gap-2 mb-2 font-semibold text-rose-400">
                      <AlertCircle className="w-4 h-4" />
                      Execution Failure
                    </div>
                    {rawError}
                  </div>
                ) : result ? (
                  <div className="flex-1 flex flex-col space-y-3 font-mono text-xs">
                    {/* Compilation Errors */}
                    {result.compile_output && (
                      <div className="rounded-xl border border-rose-500/30 bg-rose-950/20 p-3.5 text-rose-300">
                        <div className="flex items-center gap-1.5 font-bold mb-1.5 text-rose-400">
                          <AlertCircle className="w-4 h-4" />
                          <span>Compilation Output</span>
                        </div>
                        <pre className="overflow-x-auto whitespace-pre-wrap font-mono text-xs">
                          {result.compile_output}
                        </pre>
                      </div>
                    )}

                    {/* Standard Error */}
                    {result.stderr && (
                      <div className="rounded-xl border border-amber-500/30 bg-amber-950/20 p-3.5 text-amber-300">
                        <div className="flex items-center gap-1.5 font-bold mb-1.5 text-amber-400">
                          <AlertCircle className="w-4 h-4" />
                          <span>Runtime Error (stderr)</span>
                        </div>
                        <pre className="overflow-x-auto whitespace-pre-wrap font-mono text-xs">
                          {result.stderr}
                        </pre>
                      </div>
                    )}

                    {/* Standard Output */}
                    {result.stdout !== null && result.stdout !== undefined && (
                      <div
                        className={`flex-1 p-4 rounded-xl border overflow-auto ${
                          state.darkMode
                            ? "bg-gray-950 border-gray-800 text-emerald-400"
                            : "bg-gray-900 border-gray-800 text-emerald-400"
                        }`}
                      >
                        <div className="text-[10px] uppercase font-bold text-gray-500 mb-1 select-none">
                          Standard Output
                        </div>
                        <pre className="whitespace-pre-wrap font-mono text-xs">
                          {result.stdout === "" ? "(Program exited with no output)" : result.stdout}
                        </pre>
                      </div>
                    )}

                    {/* Execution Meta */}
                    {(result.time || result.memory) && (
                      <div className="flex items-center justify-end gap-3 text-[11px] text-gray-500 pt-1">
                        {result.time && <span>Time: {result.time}s</span>}
                        {result.memory && <span>Memory: {result.memory} KB</span>}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="flex-1 flex flex-col items-center justify-center text-center p-8 text-gray-500">
                    <Terminal className="w-10 h-10 mb-2 opacity-30" />
                    <p className="text-sm font-medium">No output yet</p>
                    <p className="text-xs text-gray-400 mt-1">
                      Click <strong className="text-blue-500">Run Code</strong> to execute your program
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CompilerPage;
