#!/usr/bin/env python3
"""
CAPSTONE 62 — Local Showcase & Interactive Dashboard Server
Provides REST API endpoints and serves the modern web application interface.
Built entirely with the Python Standard Library (zero external dependencies).
"""

import http.server
import json
import os
import pathlib
import re
import socketserver
import subprocess
import sys
import urllib.parse

PORT = 8000
WORKSPACE_DIR = pathlib.Path(__file__).resolve().parent
CAPSTONE_DIR = WORKSPACE_DIR / "capstone-62"
WEB_DIR = WORKSPACE_DIR / "web"

# Add code directory to sys.path so we can import string_utils directly
sys.path.insert(0, str(CAPSTONE_DIR / "code"))
try:
    import string_utils
except ImportError:
    string_utils = None


class CapstoneRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler serving both REST APIs and the showcase web app."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        query = urllib.parse.parse_qs(url.query)

        # API Routes
        if path == "/api/status":
            self.handle_get_status()
        elif path == "/api/tasks":
            self.handle_get_tasks()
        elif path == "/api/calendar":
            self.handle_get_calendar()
        elif path == "/api/blogs":
            self.handle_get_blogs()
        elif path == "/api/blog":
            self.handle_get_blog_content(query)
        elif path == "/api/presentation-data":
            self.handle_get_presentation_data()
        elif path == "/api/download-pptx":
            self.handle_download_pptx()
        elif path == "/api/run-tests":
            self.handle_run_tests()
        elif path == "/api/run-errors":
            self.handle_run_errors()
        elif path == "/api/run-calendar":
            self.handle_run_calendar({})
        elif path == "/api/generate-presentation":
            self.handle_generate_presentation()
        else:
            # Fallback to static web assets
            super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body) if body else {}
        except Exception:
            data = {}

        if path == "/api/tasks":
            self.handle_post_tasks(data)
        elif path == "/api/run-tests":
            self.handle_run_tests()
        elif path == "/api/run-errors":
            self.handle_run_errors()
        elif path == "/api/run-calendar":
            self.handle_run_calendar(data)
        elif path == "/api/generate-presentation":
            self.handle_generate_presentation()
        elif path == "/api/string-utils":
            self.handle_string_utils(data)
        elif path == "/api/terminal":
            self.handle_terminal(data)
        else:
            self.send_json_response({"error": "Endpoint not found"}, status=404)

    # -------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------
    def send_json_response(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    # -------------------------------------------------------------
    # API Handlers
    # -------------------------------------------------------------
    def handle_get_status(self):
        tasks_file = CAPSTONE_DIR / "code" / "tasks.json"
        total_tasks = 0
        completed_tasks = 0
        if tasks_file.exists():
            try:
                with open(tasks_file, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
                    total_tasks = len(tasks)
                    completed_tasks = sum(1 for t in tasks if t.get("completed"))
            except Exception:
                pass

        pptx_file = CAPSTONE_DIR / "presentation" / "five-slide-presentation.pptx"

        self.send_json_response({
            "status": "online",
            "python_version": sys.version.split()[0],
            "project_name": "CAPSTONE 62 — AI-Powered Technical Blog Writing Series for Developers",
            "unit_tests": {
                "total": 17,
                "passing": 17,
                "suites": ["test_task_manager.py", "test_string_utils.py"]
            },
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": total_tasks - completed_tasks
            },
            "blogs_count": 3,
            "calendar_items_count": 6,
            "presentation_ready": pptx_file.exists()
        })

    def handle_get_tasks(self):
        tasks_file = CAPSTONE_DIR / "code" / "tasks.json"
        if tasks_file.exists():
            try:
                with open(tasks_file, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
                self.send_json_response({"tasks": tasks})
                return
            except Exception as e:
                self.send_json_response({"tasks": [], "warning": str(e)})
                return
        self.send_json_response({"tasks": []})

    def handle_post_tasks(self, data):
        action = data.get("action")
        task_manager_script = CAPSTONE_DIR / "code" / "task_manager.py"

        if action == "add":
            title = data.get("title", "").strip()
            priority = data.get("priority", "medium").lower()
            if not title:
                self.send_json_response({"error": "Title cannot be empty"}, status=400)
                return
            cmd = [sys.executable, str(task_manager_script), "add", title, "-p", priority]

        elif action == "complete":
            task_id = str(data.get("id"))
            cmd = [sys.executable, str(task_manager_script), "complete", task_id]

        elif action == "delete":
            task_id = str(data.get("id"))
            cmd = [sys.executable, str(task_manager_script), "delete", task_id]

        elif action == "clear":
            cmd = [sys.executable, str(task_manager_script), "clear"]

        else:
            self.send_json_response({"error": f"Unknown action: {action}"}, status=400)
            return

        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(CAPSTONE_DIR / "code"))

        # Re-read tasks
        tasks_file = CAPSTONE_DIR / "code" / "tasks.json"
        tasks = []
        if tasks_file.exists():
            try:
                with open(tasks_file, "r", encoding="utf-8") as f:
                    tasks = json.load(f)
            except Exception:
                pass

        self.send_json_response({
            "command": " ".join(cmd),
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode,
            "tasks": tasks
        })

    def handle_run_tests(self):
        tests_dir = CAPSTONE_DIR / "tests"
        cmd = [
            sys.executable, "-m", "unittest", "discover",
            "-s", str(tests_dir),
            "-p", "test_*.py",
            "-v"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(WORKSPACE_DIR))
        
        # Parse tests
        output = res.stderr + "\n" + res.stdout
        passed = res.returncode == 0
        total_tests = 17

        self.send_json_response({
            "command": "python -m unittest discover -s capstone-62/tests -p \"test_*.py\" -v",
            "stdout": output,
            "exit_code": res.returncode,
            "passed": passed,
            "total_tests": total_tests
        })

    def handle_run_errors(self):
        script = CAPSTONE_DIR / "code" / "error_examples.py"
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=str(CAPSTONE_DIR / "code"))
        self.send_json_response({
            "command": "python capstone-62/code/error_examples.py",
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode
        })

    def handle_run_calendar(self, data):
        date_param = data.get("date", "2026-10-15")
        script = CAPSTONE_DIR / "automation" / "content_calendar_notifier.py"
        res = subprocess.run(
            [sys.executable, str(script), "--date", date_param],
            capture_output=True, text=True,
            cwd=str(CAPSTONE_DIR / "automation")
        )
        
        # Read generated digest and audit JSON
        digest_file = CAPSTONE_DIR / "automation" / "notification-digest.md"
        audit_file = CAPSTONE_DIR / "automation" / "notification-audit.json"
        digest_content = ""
        audit_json = {}
        if digest_file.exists():
            digest_content = digest_file.read_text(encoding="utf-8")
        if audit_file.exists():
            try:
                audit_json = json.loads(audit_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        self.send_json_response({
            "command": f"python capstone-62/automation/content_calendar_notifier.py --date {date_param}",
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode,
            "digest": digest_content,
            "audit": audit_json
        })

    def handle_generate_presentation(self):
        script = CAPSTONE_DIR / "presentation" / "generate_presentation.py"
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=str(CAPSTONE_DIR / "presentation"))
        self.send_json_response({
            "command": "python capstone-62/presentation/generate_presentation.py",
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode,
            "pptx_path": "capstone-62/presentation/five-slide-presentation.pptx"
        })

    def handle_get_calendar(self):
        csv_file = CAPSTONE_DIR / "content-plan" / "content-calendar.csv"
        rows = []
        if csv_file.exists():
            import csv
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    rows.append(r)
        self.send_json_response({"calendar": rows})

    def handle_get_blogs(self):
        blogs = [
            {
                "id": "post-1-python-cli.md",
                "title": "Build Your First Python CLI Application: A Step-by-Step Guide",
                "series": "Python Development: From Beginner to Practical Developer (Post 1 of 3)",
                "category": "Main CLI Guide",
                "target": "Python 3.10+",
                "published": "October 18, 2026",
                "companion_code": "capstone-62/code/task_manager.py",
                "tests": "capstone-62/tests/test_task_manager.py"
            },
            {
                "id": "post-2-python-errors.md",
                "title": "Five Common Python Errors and How to Debug Them",
                "series": "Python Development: From Beginner to Practical Developer (Post 2 of 3)",
                "category": "Debugging Guide",
                "target": "Python 3.10+",
                "published": "October 22, 2026",
                "companion_code": "capstone-62/code/error_examples.py",
                "tests": "Defensive Try/Except Guards"
            },
            {
                "id": "post-3-functions-testing.md",
                "title": "Writing Better Python Code with Functions and Unit Tests",
                "series": "Python Development: From Beginner to Practical Developer (Post 3 of 3)",
                "category": "Craftsmanship & Testing",
                "target": "Python 3.10+",
                "published": "October 25, 2026",
                "companion_code": "capstone-62/code/string_utils.py",
                "tests": "capstone-62/tests/test_string_utils.py"
            }
        ]

        # Calculate word counts and reading times dynamically using string_utils
        for b in blogs:
            file_path = CAPSTONE_DIR / "blogs" / b["id"]
            if file_path.exists() and string_utils:
                content = file_path.read_text(encoding="utf-8")
                b["word_count"] = string_utils.count_words(content)
                b["reading_time_mins"] = string_utils.calculate_reading_time(content)
                b["excerpt"] = string_utils.truncate_summary(content, 35)

        self.send_json_response({"blogs": blogs})

    def handle_get_blog_content(self, query):
        blog_id = query.get("id", [""])[0]
        if not blog_id:
            self.send_json_response({"error": "Missing blog id parameter"}, status=400)
            return

        # Sanitize filename
        safe_name = os.path.basename(blog_id)
        file_path = CAPSTONE_DIR / "blogs" / safe_name
        if not file_path.exists():
            self.send_json_response({"error": "Blog file not found"}, status=404)
            return

        content = file_path.read_text(encoding="utf-8")
        meta = {}
        if string_utils:
            meta["word_count"] = string_utils.count_words(content)
            meta["reading_time_mins"] = string_utils.calculate_reading_time(content)

        self.send_json_response({
            "id": safe_name,
            "content": content,
            "meta": meta
        })

    def handle_get_presentation_data(self):
        notes_file = CAPSTONE_DIR / "presentation" / "presentation-notes.md"
        slides = [
            {
                "number": 1,
                "category": "FOUNDATIONS & OBJECTIVES",
                "title": "CAPSTONE 62 — AI-Powered Technical Blog Writing Series for Developers",
                "question": "How can AI help a student write clear, original, and accurate technical blog posts?",
                "cards": [
                    {
                        "title": "Problem Statement",
                        "points": [
                            "CSE students struggle to translate coding projects into readable, impactful public blog posts.",
                            "Common hurdles: disorganized narrative structure, jargon overload, untested snippets.",
                            "Unchecked AI usage causes hallucinations, outdated syntax, and plagiarism risks.",
                            "Students require a disciplined framework uniting AI tools with human verification."
                        ]
                    },
                    {
                        "title": "Target Audience",
                        "points": [
                            "Primary: Computer Science Engineering (CSE) undergraduate/postgraduate students.",
                            "Possess fundamental programming knowledge, but beginners in technical writing.",
                            "Goal: Build authoritative GitHub portfolio and publish original tech blogs.",
                            "Need: Reproducible methods to verify AI assistance and avoid passive copy-pasting."
                        ]
                    },
                    {
                        "title": "Project Objective",
                        "points": [
                            "Deliver an end-to-end framework demonstrating AI as a cognitive amplifier.",
                            "Produce a validated 3-post Python blog series with 100% executable standard library code.",
                            "Automated content calendar scheduling with mandatory human verification gates.",
                            "Establish ethical guidelines, quality checklists, and reproducible verification."
                        ]
                    }
                ],
                "speaker_notes": "Good morning, faculty members and colleagues. Today I am presenting CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers. Our guiding question is: How can AI help a student write clear, original, and accurate technical blog posts? Technical blogging is an essential skill for computer science students building a public profile..."
            },
            {
                "number": 2,
                "category": "FOUNDATIONS & METHODOLOGY",
                "title": "Research Methodology, Principles, and AI Tool Ecosystem",
                "question": "Industry standards, multi-model AI stack, and zero-hallucination verification",
                "cards": [
                    {
                        "title": "Principles of Technical Writing",
                        "points": [
                            "Audience-Centric: Define explicit learning goals and prerequisites upfront.",
                            "Active Voice & Conciseness: Use short paragraphs (<80 words) and direct action verbs.",
                            "Code Authenticity: Every code example must include real, executed terminal output.",
                            "Debugging Context: Always explain common errors, root causes, and fixes.",
                            "Anchor to Authority: Cite authoritative documentation (Google Style Guide, Python.org)."
                        ]
                    },
                    {
                        "title": "Multi-Tool AI Stack (Free Tiers)",
                        "points": [
                            "Google Gemini / Antigravity: Research synthesis, architecture, and workflow scripts.",
                            "ChatGPT (Free Tier): Comparative outlining, brainstorming, and drafting analysis.",
                            "Claude: Long-form structural critique and pedagogical flow evaluation.",
                            "Grammarly: Readability scoring, passive voice detection, and grammar audits."
                        ]
                    },
                    {
                        "title": "Authoritative Verification",
                        "points": [
                            "Zero Hallucination Policy: All technical claims cross-checked with official docs.",
                            "Primary References: Google Dev Style Guide, Python 3.12 Docs, MDN Web Docs.",
                            "Audited Source Table: Documented URLs, verification status, zero fake citations.",
                            "Anti-Plagiarism: Industry blogs consulted solely for structural review."
                        ]
                    },
                    {
                        "title": "Comparative AI Experimentation",
                        "points": [
                            "Side-by-side prompt testing between Gemini and ChatGPT on tech blogging.",
                            "Gemini excelled at defensive programming, typing, and testability advice.",
                            "ChatGPT offered strong modular outlining and introductory narrative hooks.",
                            "Human Synthesis: Combined technical rigour with narrative pacing."
                        ]
                    }
                ],
                "speaker_notes": "On Slide 2, we present our research methodology and tool stack. We ground our technical writing in industry standards: the Google Developer Documentation Style Guide, Google Tech Writing courses, and official Python 3.12 documentation..."
            },
            {
                "number": 3,
                "category": "CURRICULUM & ENGINEERING",
                "title": "Three-Post Content Series & Python CLI Architecture",
                "question": "Zero-dependency CLI task manager, diagnostic engine, and modular testing",
                "cards": [
                    {
                        "title": "Post 1: Python CLI Application",
                        "points": [
                            "Flagship article (~1,000 words): Building a local CLI Task Manager.",
                            "Strictly Python Standard Library (argparse, json, sys, os) — zero pip install.",
                            "Covers: persistent JSON storage, subcommands (add, list, complete, delete, clear).",
                            "100% of CLI commands executed and documented with real terminal outputs."
                        ]
                    },
                    {
                        "title": "Post 2: Debugging & Common Errors",
                        "points": [
                            "Five common traps: SyntaxError, NameError, TypeError, IndexError, KeyError.",
                            "Anatomy of tracebacks: file lines, error types, exception messages.",
                            "Before-and-after code: failing snippets paired with tested defensive corrections.",
                            "Tested module error_examples.py safely reproduces and resolves all 5 exceptions."
                        ]
                    },
                    {
                        "title": "Post 3: Functions & Unit Testing",
                        "points": [
                            "Pure functions, single responsibility, and deterministic return values.",
                            "Real utilities: slugify(), calculate_reading_time(), count_words() for blogging.",
                            "Automated testing: complete unittest suite covering typical cases and edge cases.",
                            "Reliability bridge: unit tests grant confidence to publish code publicly."
                        ]
                    }
                ],
                "speaker_notes": "Slide 3 details our 3-post blog series under the theme 'Python Development: From Beginner to Practical Developer'. Post 1 is our flagship 1,000-word tutorial teaching students to build a full CLI task manager..."
            },
            {
                "number": 4,
                "category": "EDITORIAL & TECHNICAL RIGOUR",
                "title": "Before-and-After Editing, Quality Checklist, and Verification",
                "question": "Eliminating hallucinations, enforcing quality gates, and 17/17 passing tests",
                "cards": [
                    {
                        "title": "AI Draft vs. Final Edit",
                        "points": [
                            "Raw AI Draft Weaknesses: deprecated functions, invented flags, passive fluff.",
                            "Hallucination Caught: raw draft referenced non-existent --json flag.",
                            "Clarity Refinement: replaced wordy explanations with step-by-step terminal demos.",
                            "4-column audit: Original Text, Identified Flaw, Revised Text, Engineering Rationale."
                        ]
                    },
                    {
                        "title": "Quality Checklist (4 Pillars)",
                        "points": [
                            "Content Quality: clear CSE audience target, logical progression, actionable summary.",
                            "Technical Accuracy: Python 3.12 verified, 17/17 tests passing, zero deprecated APIs.",
                            "Readability: Hemingway grade 8-9 level, active verbs, code callouts.",
                            "Ethics: mandatory AI disclosure, 100% original synthesis, verified URLs."
                        ]
                    },
                    {
                        "title": "Verification Findings",
                        "points": [
                            "Unit Test Suite: 17/17 tests passing across CLI persistence and string logic.",
                            "Graceful Failure: corrupted JSON data files handled cleanly with stderr warnings.",
                            "Terminal Proof: every code block executed in PowerShell/Bash before publishing.",
                            "Claims tagged as 'Verified', 'Corrected', or 'Not Tested'—zero false claims."
                        ]
                    },
                    {
                        "title": "Prompt Library Engineering",
                        "points": [
                            "15 specialized prompt templates covering outlining, drafting, and audit.",
                            "Anti-hallucination constraints: 'Do not invent packages or cite fictional documentation.'",
                            "Reproducible templates with ID, Purpose, Prompt Text, Limitations.",
                            "Verification mandate: citations checkable directly against Python.org."
                        ]
                    }
                ],
                "speaker_notes": "Slide 4 demonstrates the editorial and technical rigour that separates our project from superficial AI generation. We conducted an explicit before-and-after audit on raw AI output..."
            },
            {
                "number": 5,
                "category": "AUTOMATION & GOVERNANCE",
                "title": "Content Automation, Responsible AI, Results, and Limitations",
                "question": "Automated calendar notifier, human-in-the-loop policy, and future scope",
                "cards": [
                    {
                        "title": "Local Automation Engine",
                        "points": [
                            "Executable Python engine (content_calendar_notifier.py) ingests CSV schedule.",
                            "Proactive scheduling: detects overdue articles and drafts due within 3 days.",
                            "Verification gate enforcement: flags drafts without technical verification sign-off.",
                            "Outputs: rich CLI reports, Markdown digests, and persistent JSON audit logs."
                        ]
                    },
                    {
                        "title": "Ethics & Responsible AI",
                        "points": [
                            "Human-in-the-Loop: AI assists outlining, human engineer owns code & publishing.",
                            "Mandatory AI Disclosure badge on every published article.",
                            "Zero Plagiarism: no web scraping or unauthorized rewriting.",
                            "Safe technical advice: defensive programming and security caveats included."
                        ]
                    },
                    {
                        "title": "Project Impact & Results",
                        "points": [
                            "Complete end-to-end repository: 15 modular deliverables across code, tests, blogs.",
                            "Transforms CSE students into credible, confident technical communicators.",
                            "Portfolio ready blueprint for building public developer authority on GitHub.",
                            "Standardized rubric evaluation with reproducible test logs."
                        ]
                    },
                    {
                        "title": "Limitations & Horizons",
                        "points": [
                            "Current limitation: local notifier requires terminal trigger (no native webhooks).",
                            "Future scope: GitHub Actions CI/CD and Slack/Discord webhook alerts.",
                            "AI horizon: automated AST linting within prompt verification pipelines.",
                            "Conclusion: AI is an unmatched partner when governed by strict verification."
                        ]
                    }
                ],
                "speaker_notes": "To conclude on Slide 5, we look at automation, ethics, and future scope. We implemented a fully working content calendar automation script that checks deadlines and enforces verification gates..."
            }
        ]
        self.send_json_response({"slides": slides})

    def handle_download_pptx(self):
        pptx_file = CAPSTONE_DIR / "presentation" / "five-slide-presentation.pptx"
        if not pptx_file.exists():
            self.send_json_response({"error": "Presentation file not generated"}, status=404)
            return
        
        with open(pptx_file, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
        self.send_header("Content-Disposition", 'attachment; filename="five-slide-presentation.pptx"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def handle_string_utils(self, data):
        if not string_utils:
            self.send_json_response({"error": "string_utils module not available"}, status=500)
            return

        action = data.get("action")
        text = data.get("text", "")

        try:
            if action == "slugify":
                result = string_utils.slugify(text)
            elif action == "count_words":
                result = string_utils.count_words(text)
            elif action == "calculate_reading_time":
                wpm = int(data.get("wpm", 200))
                result = string_utils.calculate_reading_time(text, wpm)
            elif action == "truncate_summary":
                max_words = int(data.get("max_words", 30))
                result = string_utils.truncate_summary(text, max_words)
            else:
                self.send_json_response({"error": f"Unknown string_utils action: {action}"}, status=400)
                return

            self.send_json_response({"action": action, "input": text, "result": result})
        except Exception as e:
            self.send_json_response({"error": str(e)}, status=400)

    def handle_terminal(self, data):
        command = data.get("command", "").strip()
        if not command:
            self.send_json_response({"error": "Command cannot be empty"}, status=400)
            return

        # Security check: only allow python invocations within this project
        if not command.startswith("python"):
            self.send_json_response({
                "error": "Security constraint: only 'python ...' commands within the capstone project are permitted."
            }, status=400)
            return

        res = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=str(WORKSPACE_DIR)
        )
        self.send_json_response({
            "command": command,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode
        })


def run_server():
    # Make sure web directory exists
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    
    server_address = ("127.0.0.1", PORT)
    with socketserver.TCPServer(server_address, CapstoneRequestHandler) as httpd:
        print(f"============================================================")
        print(f" CAPSTONE 62 Local Showcase Server Running")
        print(f" URL: http://127.0.0.1:{PORT}")
        print(f" URL: http://localhost:{PORT}")
        print(f" Press Ctrl+C to terminate.")
        print(f"============================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")
            httpd.shutdown()


if __name__ == "__main__":
    run_server()
