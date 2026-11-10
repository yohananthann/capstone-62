# CAPSTONE 62 — AI-Powered Technical Blog Writing Series for Developers

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Tests Passing](https://img.shields.io/badge/Tests-17%2F17%20Passed-brightgreen.svg)](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests)
[![Editorial Standard](https://img.shields.io/badge/Style-Google%20Dev%20Docs-orange.svg)](https://developers.google.com/style)

> **Main Project Question:**  
> *How can Artificial Intelligence help a Computer Science Engineering (CSE) student write clear, original, and technically accurate technical blog posts while maintaining ethical writing practices?*

---

## Executive Summary
For Computer Science Engineering (CSE) students, publishing clear, original, and verified technical blog posts is one of the most effective strategies to build developer authority on GitHub, demonstrate engineering depth to recruiters, and contribute meaningfully to the open-source ecosystem.

However, beginner student writers face steep barriers: structural ambiguity, cognitive overload from technical jargon, untested code snippets, and poor editorial pacing. While Large Language Models (LLMs) offer unprecedented assistance, unguided AI usage introduces grave risks: code hallucinations, fabricated documentation citations, outdated APIs, and passive plagiarism.

**CAPSTONE 62** delivers an end-to-end, academic and practical framework demonstrating how AI tools—when paired with strict software engineering verification, human-in-the-loop oversight, and professional technical writing principles—empower CSE students to write clear, original, and technically verified developer content.

---

## Master File Index & Repository Structure

```text
capstone-62/
├── README.md                              # Master project overview, file index, and evaluation rubric
├── research/
│   ├── research-report.md                 # Foundational research report, tools comparison, and writing principles
│   ├── references.md                      # Verified authoritative source references table (no fake citations)
│   └── ethics-and-responsible-ai.md       # Ethical guidelines, principles, and 9-skill matrix
├── checklist/
│   └── technical-writing-checklist.md     # 25-point quality checklist across Content, Accuracy, Readability, Ethics
├── content-plan/
│   ├── topic-series.md                    # Curriculum plan, pedagogical rationale, and post blueprints
│   └── content-calendar.csv               # Standardized content calendar with status, deadlines, and verification gates
├── blogs/
│   ├── post-1-python-cli.md               # Flagship article (~1,000 words): Python CLI Task Manager with code
│   ├── post-2-python-errors.md            # Diagnostic article: Five Common Python Errors and How to Debug Them
│   └── post-3-functions-testing.md        # Craftsmanship article: Writing Better Code with Functions & Unit Tests
├── code/
│   ├── task_manager.py                    # Complete CLI Task Manager (argparse, JSON persistence, error handling)
│   ├── error_examples.py                  # Reproducible test harness for 5 common Python exceptions
│   └── string_utils.py                    # Modular, pure functions for blog text processing
├── tests/
│   ├── test_task_manager.py               # Automated unittest suite for task_manager.py (9 test cases)
│   └── test_string_utils.py               # Automated unittest suite for string_utils.py (8 test cases)
├── social/
│   └── social-posts.md                    # 5 original educational/promotional posts (LinkedIn, X, Instagram)
├── presentation/
│   ├── five-slide-presentation.pptx       # Professional 16:9 widescreen presentation deck
│   ├── presentation-notes.md              # Complete slide layouts and verbatim speaker notes
│   └── generate_presentation.py           # Reproducible script using python-pptx to generate the deck
├── automation/
│   ├── content_calendar_notifier.py       # Standalone Python automation engine for reminders and gatekeeping
│   ├── workflow.md                        # Workflow architecture diagram, triggers, actions, and schema
│   ├── setup-guide.md                     # Setup instructions for local execution, OS schedulers, and Notion
│   ├── sample-data.csv                    # Sample content calendar dataset for testing
│   ├── notification-digest.md             # Auto-generated markdown alert report
│   └── notification-audit.json            # Auto-generated JSON audit log
├── verification/
│   ├── verification-report.md             # Systematic 11-dimension AI output verification report
│   └── before-after-analysis.md           # Before-and-after case study with 4-column comparison table
└── demo/
    └── final-demo-guide.md                # Quickstart 5-minute evaluation guide for faculty and reviewers
```

---

## Clickable Deliverable Directory

| Deliverable Name | File Link | Primary Scope & Summary |
|---|---|---|
| **Research Report** | [research-report.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/research/research-report.md) | Technical writing principles, 13-stage developer blog structure, audience analysis, and Gemini vs. ChatGPT comparative experiments. |
| **Authoritative References** | [references.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/research/references.md) | Source table with verified URLs, findings, and access dates. Zero fabricated citations. |
| **Ethics & Responsible AI** | [ethics-and-responsible-ai.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/research/ethics-and-responsible-ai.md) | Core ethical tenets, human-in-the-loop governance, standardized AI disclosure badge, and 9-skill matrix. |
| **Quality Checklist** | [technical-writing-checklist.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/checklist/technical-writing-checklist.md) | 25-point audit across Content Quality, Technical Accuracy, Readability, and Ethics. |
| **Topic Series Plan** | [topic-series.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/content-plan/topic-series.md) | Multi-post curriculum: "Python Development: From Beginner to Practical Developer." |
| **Content Calendar CSV** | [content-calendar.csv](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/content-plan/content-calendar.csv) | Machine-readable content planning calendar with dates, assignees, and verification statuses. |
| **Post 1 (Main Article)** | [post-1-python-cli.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-1-python-cli.md) | Flagship 1,000-word tutorial building a CLI Task Manager using Python standard library. |
| **Post 2 (Errors & Debugging)** | [post-2-python-errors.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-2-python-errors.md) | Explains SyntaxError, NameError, TypeError, IndexError, KeyError with verified fixes. |
| **Post 3 (Functions & Testing)** | [post-3-functions-testing.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-3-functions-testing.md) | Pure functions, parameter design, and automated `unittest` test suite construction. |
| **CLI Task Manager Code** | [task_manager.py](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/task_manager.py) | Fully functional Python standard library CLI (`argparse`, `json`, `sys`, `os`). |
| **Common Errors Harness** | [error_examples.py](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/error_examples.py) | Executable test harness reproducing and resolving 5 common Python exceptions safely. |
| **Blog String Utilities** | [string_utils.py](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/string_utils.py) | Reusable, pure Python string functions (`slugify`, `count_words`, `calculate_reading_time`). |
| **Unit Test Suite (Task Manager)** | [test_task_manager.py](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests/test_task_manager.py) | 9 automated unit tests verifying CLI arguments, persistence, and corrupted file handling. |
| **Unit Test Suite (String Utils)** | [test_string_utils.py](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests/test_string_utils.py) | 8 automated unit tests verifying pure function boundaries and exception guards. |
| **Social Media Posts** | [social-posts.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/social/social-posts.md) | 5 original educational and promotional posts for LinkedIn, X, Instagram, and Dev communities. |
| **5-Slide Presentation Deck** | [five-slide-presentation.pptx](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/presentation/five-slide-presentation.pptx) | Professional 16:9 widescreen presentation in executive dark slate theme. |
| **Presentation Notes** | [presentation-notes.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/presentation/presentation-notes.md) | Card layouts and verbatim speaker notes for all 5 slides. |
| **Slide Deck Generator** | [generate_presentation.py](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/presentation/generate_presentation.py) | Python script that programmatically compiles the slide deck using `python-pptx`. |
| **Automation Workflow** | [workflow.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/automation/workflow.md) | Mermaid flowchart, triggers, actions, error-handling strategy, and approval gates. |
| **Automation Setup Guide** | [setup-guide.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/automation/setup-guide.md) | Step-by-step setup for local CLI runs, Windows Task Scheduler, cron, and Notion API. |
| **Automation Notifier Engine** | [content_calendar_notifier.py](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/automation/content_calendar_notifier.py) | Standalone Python automation engine parsing CSV, detecting deadlines, and checking gates. |
| **Prompt Library (15 Categories)** | [prompt-library.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/prompts/prompt-library.md) | 15 specialized prompts with anti-hallucination constraints, expected outputs, and limitations. |
| **Verification Report** | [verification-report.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/verification/verification-report.md) | 11-dimension risk audit table and live test execution logs. |
| **Before-and-After Analysis** | [before-after-analysis.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/verification/before-after-analysis.md) | 4-column comparative table analyzing raw AI draft vs. verified final tutorial edit. |
| **Final Demonstration Guide** | [final-demo-guide.md](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/demo/final-demo-guide.md) | 5-minute evaluator guide with exact CLI commands to test and verify the entire project. |

---

## The Three-Post Blog Series Overview

| Post ID | Title | Word Count | Key Skills & Concepts | Verified Companion Code |
|---|---|---|---|---|
| **Post 1** | *Build Your First Python CLI Application: A Step-by-Step Guide* | **972 prose words** (2,087 total with code) | `argparse`, subcommands, JSON persistence, input validation, exit codes, stderr. | [`code/task_manager.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/task_manager.py) & [`tests/test_task_manager.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests/test_task_manager.py) |
| **Post 2** | *Five Common Python Errors and How to Debug Them* | **~650 words** | `SyntaxError`, `NameError`, `TypeError`, `IndexError`, `KeyError`, traceback reading, defensive coding. | [`code/error_examples.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/error_examples.py) |
| **Post 3** | *Writing Better Python Code with Functions and Unit Tests* | **~750 words** | Pure functions, single responsibility, type hints, `unittest.TestCase`, test fixtures, regression prevention. | [`code/string_utils.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/string_utils.py) & [`tests/test_string_utils.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests/test_string_utils.py) |

---

## Automated Test Suite & Verification Results
All companion code was tested and executed in the local Windows Python 3.12.6 environment:

```text
$ python -m unittest discover -s capstone-62/tests -p "test_*.py" -v

test_calculate_reading_time (test_string_utils.TestStringUtils.test_calculate_reading_time) ... ok
test_calculate_reading_time_invalid_wpm (test_string_utils.TestStringUtils.test_calculate_reading_time_invalid_wpm) ... ok
test_count_words (test_string_utils.TestStringUtils.test_count_words) ... ok
test_slugify_invalid_inputs (test_string_utils.TestStringUtils.test_slugify_invalid_inputs) ... ok
test_slugify_special_characters (test_string_utils.TestStringUtils.test_slugify_special_characters) ... ok
test_slugify_standard (test_string_utils.TestStringUtils.test_slugify_standard) ... ok
test_truncate_summary (test_string_utils.TestStringUtils.test_truncate_summary) ... ok
test_truncate_summary_invalid (test_string_utils.TestStringUtils.test_truncate_summary_invalid) ... ok
test_add_task_empty_title_rejected (test_task_manager.TestTaskManager.test_add_task_empty_title_rejected) ... ok
test_add_task_invalid_priority_rejected (test_task_manager.TestTaskManager.test_add_task_invalid_priority_rejected) ... ok
test_add_task_success (test_task_manager.TestTaskManager.test_add_task_success) ... ok
test_clear_tasks (test_task_manager.TestTaskManager.test_clear_tasks) ... ok
test_complete_task_lifecycle (test_task_manager.TestTaskManager.test_complete_task_lifecycle) ... ok
test_corrupted_json_recovery (test_task_manager.TestTaskManager.test_corrupted_json_recovery) ... ok
test_delete_task (test_task_manager.TestTaskManager.test_delete_task) ... ok
test_id_increments_sequentially (test_task_manager.TestTaskManager.test_id_increments_sequentially) ... ok
test_list_tasks_filtering (test_task_manager.TestTaskManager.test_list_tasks_filtering) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.362s

OK (100% Pass Rate)
```

---

## Required AI Skills Matrix

| AI Competency | Demonstrated Capability | Project Evidence Deliverable |
|---|---|---|
| **1. Prompt Engineering** | Authoring structured, constraint-driven prompts with negative rules preventing fake citations. | [`prompts/prompt-library.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/prompts/prompt-library.md) (15 distinct categories) |
| **2. Research & Synthesis** | Multi-tool ecosystem analysis and comparative prompt experiments between Gemini and ChatGPT. | [`research/research-report.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/research/research-report.md) & [`research/references.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/research/references.md) |
| **3. Technical Writing** | 13-stage developer blog architecture, Google Developer Style Guide, active voice, short paragraphs. | [`blogs/post-1-python-cli.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-1-python-cli.md) |
| **4. Editing & Proofreading** | Transforming flawed raw AI prose into concise, publication-grade developer documentation. | [`verification/before-after-analysis.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/verification/before-after-analysis.md) |
| **5. Fact-Checking & Verification** | Auditing technical claims, deprecated APIs, and documentation URLs across 11 risk dimensions. | [`verification/verification-report.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/verification/verification-report.md) |
| **6. Code Generation & Review** | Developing a single-file CLI Task Manager with JSON persistence, subcommands, and defensive checks. | [`code/task_manager.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/task_manager.py) & [`code/error_examples.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/error_examples.py) |
| **7. Code Testing & QA** | Implementing automated `unittest` suites testing typical inputs, boundary cases, and corrupted data. | [`tests/test_task_manager.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests/test_task_manager.py) & [`tests/test_string_utils.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests/test_string_utils.py) |
| **8. Visual & Presentation Design** | Designing an executive 5-slide widescreen presentation deck with speaker notes and visual cards. | [`presentation/five-slide-presentation.pptx`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/presentation/five-slide-presentation.pptx) & [`presentation/presentation-notes.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/presentation/presentation-notes.md) |
| **9. Workflow Automation** | Building an automated content calendar notifier engine enforcing technical verification gates. | [`automation/content_calendar_notifier.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/automation/content_calendar_notifier.py) & [`automation/workflow.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/automation/workflow.md) |

---

## 5-Minute Evaluation Quickstart for Faculty Reviewers

To verify the entire capstone project in under 5 minutes:

```bash
# 1. Run all automated unit tests (17 tests)
python -m unittest discover -s capstone-62/tests -p "test_*.py" -v

# 2. Run the interactive CLI Task Manager workflow
python capstone-62/code/task_manager.py clear
python capstone-62/code/task_manager.py add "Build portfolio CLI tool" -p high
python capstone-62/code/task_manager.py add "Write unit tests" -p high
python capstone-62/code/task_manager.py list
python capstone-62/code/task_manager.py complete 1
python capstone-62/code/task_manager.py list

# 3. Run the 5 Python Errors demonstration
python capstone-62/code/error_examples.py

# 4. Run the Content Calendar Automation Engine (simulated run on 2026-10-15)
python capstone-62/automation/content_calendar_notifier.py --date 2026-10-15

# 5. Regenerate the 5-slide presentation deck
python capstone-62/presentation/generate_presentation.py
```

---

## Ethical Declaration & AI Disclosure
In accordance with ethical academic and professional engineering practices:
1. **AI as Cognitive Amplifier:** AI tools (Google Gemini, ChatGPT, Claude) were used strictly for research synthesis, structural outlining, and editorial critique.
2. **Zero Fabricated Results:** Every code snippet, CLI terminal transcript, and unit test result documented in this repository reflects real, local executions on Python 3.12.6.
3. **No Plagiarism:** All text and architecture are 100% original student-authored works. Third-party blogs were consulted solely for qualitative structure analysis; zero code or text was copied.
4. **Human Ownership:** The human student author and academic reviewer maintain full responsibility for the technical accuracy and integrity of all published content.
