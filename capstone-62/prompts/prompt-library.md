# CAPSTONE 62: Prompt Engineering Library
**Project:** AI-Powered Technical Blog Writing Series for Developers  
**Policy:** Every prompt embeds explicit anti-fabrication constraints prohibiting hallucinations, fake sources, invented execution results, and plagiarism.

---

## Prompt Engineering Standard Architecture
Each prompt in this library follows a rigorous 4-part structure:
1. **System Persona:** Defines domain authority (e.g., Principal Technical Writer, Senior Software Engineer).
2. **Context & Objective:** Outlines audience level, scope, and target deliverable.
3. **Negative Constraints (Zero-Hallucination Policy):** Explicit prohibitions against making up APIs, copying external blogs, or faking tests.
4. **Output Schema:** Dictates structured Markdown output for automated parsing and human auditing.

---

## Complete Prompt Registry (15 Categories)

### 1. Topic Selection
- **Prompt ID:** `PRM-01-TOPIC`
- **Purpose:** Brainstorm practical, portfolio-worthy technical blogging themes tailored for CSE students.
- **Full Prompt:**
  ```text
  You are an experienced Computer Science educator and developer advocate.
  Propose three distinct technical blogging themes for a 3rd-year CSE undergraduate student.
  Requirements:
  - Theme must focus on core Python software development.
  - The topic must be practical and lead to an executable GitHub project.
  - Assume the reader knows loops and functions but has never built a production CLI or test suite.
  Constraint: Do not propose generic "hello world" calculators or machine learning buzzwords without concrete code. Do not promise guaranteed career outcomes.
  Format your response as a numbered list with: Theme Title, Target Problem, Planned Technical Deliverable, and Portfolio Impact.
  ```
- **Expected Output:** 3 structured themes comparing CLI engineering, debugging, and testing workflows.
- **Verification Method:** Faculty review against academic syllabus and curriculum standards.
- **Known Limitations:** AI suggestions often gravitate toward high-level web frameworks unless constrained to the standard library.

---

### 2. Audience Analysis
- **Prompt ID:** `PRM-02-AUDIENCE`
- **Purpose:** Define persona profiles, baseline prerequisites, and common cognitive friction points.
- **Full Prompt:**
  ```text
  You are a technical writing curriculum designer specializing in developer education.
  Perform an audience persona analysis for a technical blog post titled "Build Your First Python CLI Application".
  Analyze:
  1. Primary Reader Persona: 3rd-year CSE student building a public developer profile.
  2. Technical Prerequisite Baseline: What do they already know? What do they NOT yet know?
  3. Cognitive Friction Points: Where do beginner CLI developers typically get confused?
  4. Reader Motivation: Why would a recruiter or hiring manager care about this article?
  Constraint: Be realistic. Do not assume readers know Unix piping, shell environments, or advanced packaging.
  ```
- **Expected Output:** Structured profile detailing reader knowledge, friction points (e.g. `sys.argv` confusion), and motivations.
- **Verification Method:** Cross-checked against student peer feedback from actual lab courses.
- **Known Limitations:** May overestimate student familiarity with terminal commands on Windows vs. Linux.

---

### 3. Technical Research
- **Prompt ID:** `PRM-03-RESEARCH`
- **Purpose:** Extract official language features, documentation references, and architectural best practices.
- **Full Prompt:**
  ```text
  You are a Python standard library documentation specialist.
  Summarize the core architectural design for building a local Command-Line Interface using Python 3.12's `argparse` module.
  Cover:
  - Subcommand parsing using `add_subparsers()`.
  - Distinguishing positional arguments from optional flags.
  - Graceful exit codes using `sys.exit()` and streaming errors to `sys.stderr`.
  Constraint: Cite only official Python 3 documentation (docs.python.org). Do not reference third-party libraries (e.g., Click, Typer). Do not invent non-existent flags or methods.
  ```
- **Expected Output:** Accurate technical architectural breakdown grounded exclusively in official Python documentation.
- **Verification Method:** Cross-referenced directly against `https://docs.python.org/3/library/argparse.html`.
- **Known Limitations:** LLMs may inadvertently blend `argparse` syntax with `optparse` (deprecated) or third-party libraries if not strictly prompted.

---

### 4. Blog Outlining
- **Prompt ID:** `PRM-04-OUTLINE`
- **Purpose:** Generate a scannable, pedagogically progressive blog post outline following the 13-part developer blog structure.
- **Full Prompt:**
  ```text
  You are a senior technical writer following the Google Developer Documentation Style Guide.
  Create a detailed 13-stage outline for an approximately 1,000-word tutorial titled:
  "Build Your First Python CLI Application: A Step-by-Step Guide".
  Required Structure:
  1. Title & Meta, 2. Introduction, 3. Problem Statement, 4. Prerequisites, 5. Learning Objectives, 
  6. Architecture Overview, 7. Code Implementation, 8. Running the Program, 9. Expected Output, 
  10. Code Deep Dive, 11. Error Handling, 12. Testing Instructions, 13. Conclusion & Official References.
  Constraint: Ensure headings are descriptive and action-oriented. Do not include pseudocode; reserve code sections for complete runnable Python.
  ```
- **Expected Output:** Hierarchical Markdown outline matching the 13-stage developer blog structure.
- **Verification Method:** Checked against the Technical-Writing Quality Checklist (`CQ-3`).
- **Known Limitations:** AI sometimes attempts to compress sections 8–10 into a single generic heading.

---

### 5. Article Drafting
- **Prompt ID:** `PRM-05-DRAFT`
- **Purpose:** Draft concise, engaging tutorial sections in the active voice adhering to Google Style standards.
- **Full Prompt:**
  ```text
  You are a technical blog author writing for undergraduate developers.
  Draft Sections 1, 2, and 5 of the tutorial "Build Your First Python CLI Application: A Step-by-Step Guide".
  Guidelines:
  - Use active voice and second-person pronouns ("you", "your").
  - Keep paragraphs short (maximum 3–4 sentences, under 80 words).
  - Clearly explain the problem: why terminal context switching hurts developer productivity.
  - Formulate 5 measurable learning objectives starting with action verbs (Understand, Structure, Persist, Implement, Execute).
  Constraint: Avoid conversational filler ("In this fast-paced world...", "Needless to say..."). Do not make exaggerated career claims.
  ```
- **Expected Output:** Clean, crisp technical prose with clear learning objectives and a compelling problem statement.
- **Verification Method:** Audited using Grammarly Free for active voice and sentence length.
- **Known Limitations:** Tends to produce introductory fluff sentences unless explicitly prohibited.

---

### 6. Code Generation
- **Prompt ID:** `PRM-06-CODEGEN`
- **Purpose:** Produce production-grade, defensive Python standard library code for the CLI application.
- **Full Prompt:**
  ```text
  You are a principal software engineer writing reference code for a computer science tutorial.
  Write a complete, single-file Python script named `task_manager.py`.
  Requirements:
  1. Standard library ONLY: `argparse`, `json`, `os`, `sys`, `typing`.
  2. Implement subcommands: `add`, `list`, `complete`, `delete`, `clear`.
  3. Store tasks in a local `tasks.json` file.
  4. Defensive coding: handle missing files, corrupted JSON, empty titles, and invalid numeric IDs cleanly.
  5. Print errors to `sys.stderr` and use proper exit codes (`sys.exit(0)` on success, `sys.exit(1)` on error).
  Constraint: Provide the COMPLETE runnable script. No omitted lines, no `# TODO`, no pseudocode. Code must pass Python 3.12 syntax compilation.
  ```
- **Expected Output:** 100% syntactically valid Python code with complete function implementations and type hints.
- **Verification Method:** Executed directly in local interpreter: `python -m py_compile task_manager.py`.
- **Known Limitations:** AI models frequently attempt to truncate long code blocks with comments like `# ... rest of code unchanged ...`.

---

### 7. Code Review
- **Prompt ID:** `PRM-07-CODEREVIEW`
- **Purpose:** Audit generated Python code for security bugs, edge cases, and PEP 8 compliance.
- **Full Prompt:**
  ```text
  You are a senior code reviewer conducting a security and reliability audit on the following Python script.
  [Insert task_manager.py source code]
  Audit the code for:
  1. Unhandled exceptions or crash vectors (e.g., missing files, negative integer IDs, corrupt JSON).
  2. Resource leaks (unclosed file handles).
  3. Security pitfalls (unsafe input evaluation, arbitrary code execution).
  4. Adherence to PEP 8 naming and type annotations.
  Constraint: For every vulnerability identified, provide the exact line number, explain the failure mode, and supply the defensive code patch.
  ```
- **Expected Output:** Line-by-line security and bug audit with defensive replacement snippets.
- **Verification Method:** Verified identified edge cases by writing automated regression tests in `test_task_manager.py`.
- **Known Limitations:** Can occasionally flag harmless idiomatic constructs as theoretical risks.

---

### 8. Code Testing
- **Prompt ID:** `PRM-08-TESTGEN`
- **Purpose:** Generate a comprehensive `unittest` suite covering normal execution, boundaries, and errors.
- **Full Prompt:**
  ```text
  You are a Quality Assurance engineer specializing in Python automated testing.
  Write a comprehensive `unittest` test suite named `test_task_manager.py` to test `task_manager.py`.
  Requirements:
  - Inherit from `unittest.TestCase`.
  - Use `tempfile.NamedTemporaryFile` in `setUp()` and `tearDown()` so tests never touch production data.
  - Test cases: successful add, rejection of empty title, rejection of invalid priority, sequential ID allocation, listing with/without filters, completing tasks, idempotent completion, deleting tasks, handling non-existent IDs, and recovery from corrupted JSON files.
  Constraint: Do not use third-party test runners like pytest. Code must execute with `python -m unittest`.
  ```
- **Expected Output:** Complete, runnable `unittest` file with fixtures and assertions.
- **Verification Method:** Executed via: `python -m unittest discover tests -v`. Result: 17/17 tests passing.
- **Known Limitations:** AI may mock file operations instead of testing real file read/writes unless instructed to use `tempfile`.

---

### 9. Grammar & Style Editing
- **Prompt ID:** `PRM-09-STYLE`
- **Purpose:** Refine drafted technical prose according to the Google Developer Documentation Style Guide.
- **Full Prompt:**
  ```text
  You are a copy editor enforcing the Google Developer Documentation Style Guide.
  Review the following draft excerpt:
  [Insert draft paragraph]
  Rules:
  1. Convert passive voice to active voice.
  2. Eliminate redundant words (e.g., replace "in order to" with "to", "utilize" with "use").
  3. Replace vague pronouns ("this is because...") with explicit subjects.
  4. Ensure technical terms are formatted with markdown backticks (`argparse`, `tasks.json`).
  Provide your output as: 1. Revised Text, 2. List of Specific Changes Made with Justification.
  ```
- **Expected Output:** Polished prose with active phrasing and an explicit rationale for each grammatical change.
- **Verification Method:** Readability scoring and grammar checks via Grammarly Free.
- **Known Limitations:** May occasionally remove necessary technical nuance if prompted too aggressively for brevity.

---

### 10. Source Verification
- **Prompt ID:** `PRM-10-FACTCHECK`
- **Purpose:** Audit all citations and documentation links in an article against primary sources.
- **Full Prompt:**
  ```text
  You are a technical fact-checker and source auditor.
  Review the following list of technical claims and references cited in our Python CLI article:
  [Insert claims and URLs]
  For each item:
  1. Confirm whether the URL points to an active, official documentation domain (e.g., docs.python.org, developers.google.com).
  2. Verify whether the technical behavior described matches the official Python 3.12 documentation.
  3. Flag any third-party blog citations that should be replaced with primary documentation.
  Constraint: Do NOT invent documentation pages or cite fictional RFCs. If a feature or flag does not exist in standard Python 3.12, flag it as UNVERIFIED.
  ```
- **Expected Output:** Source audit table detailing URL validity, accuracy, and official documentation anchors.
- **Verification Method:** Manual HTTP checking and reading of Python 3.12 documentation pages.
- **Known Limitations:** AI cannot physically ping live URLs; its domain knowledge is limited to training cutoffs.

---

### 11. Hallucination Detection
- **Prompt ID:** `PRM-11-HALLUCINATION`
- **Purpose:** Scan draft technical blogs to detect hallucinated CLI flags, non-existent methods, or fake features.
- **Full Prompt:**
  ```text
  You are an adversarial AI auditor tasked with detecting hallucinations in developer tutorials.
  Analyze the following tutorial text and code snippet:
  [Insert tutorial text and code]
  Search aggressively for:
  1. Mentions of CLI flags or parameters in the text that are NOT present in the code.
  2. Functions or methods imported from the standard library that do not actually exist in Python 3.12.
  3. Terminal commands described in the text that would fail if typed into a real shell.
  Format findings as: Claim/Command in Text | Code Reality | Verdict (Accurate vs Hallucination) | Recommended Correction.
  ```
- **Expected Output:** Structured audit identifying discrepancies between prose instructions and actual code.
- **Verification Method:** Verified by copying terminal commands into Windows PowerShell / Bash and checking exit codes.
- **Known Limitations:** May fail to catch subtle platform-specific discrepancies (e.g., Windows path separators vs. Unix slashes).

---

### 12. Before-and-After Comparison
- **Prompt ID:** `PRM-12-BEFOREAFTER`
- **Purpose:** Construct an educational before-and-after case study contrasting raw AI output with human-edited code.
- **Full Prompt:**
  ```text
  You are a computer science pedagogy researcher.
  Take the following flawed raw AI draft:
  [Insert raw draft]
  And compare it with our human-verified publication-grade version:
  [Insert revised version]
  Create a 4-column Markdown table with:
  | Original Raw Text | Identified Problem | Revised Text | Reason for Change |
  Categorize each problem under: Technical Inaccuracy, Tone/Clarity Flaw, or Ethical/Source Issue.
  ```
- **Expected Output:** Detailed comparative table breaking down structural, syntactic, and tone improvements.
- **Verification Method:** Cross-checked against the Before-and-After Analysis document (`verification/before-after-analysis.md`).
- **Known Limitations:** Must be provided with both versions; AI should not be asked to invent fictional errors without real context.

---

### 13. Social Media Writing
- **Prompt ID:** `PRM-13-SOCIAL`
- **Purpose:** Craft professional, educational social media posts for LinkedIn, X, and developer communities.
- **Full Prompt:**
  ```text
  You are a developer advocate writing educational social media content.
  Draft 5 distinct social media posts promoting our Python Development blog series.
  Platforms: LinkedIn, X (Twitter), Instagram (Carousel text), Developer Communities.
  Required Topics:
  1. Series Announcement, 2. Post 1 Promotion (CLI App), 3. Debugging Tip (Post 2), 
  4. Unit Testing Tip (Post 3), 5. Portfolio Building Advice.
  Each post MUST include: Platform, Short Hook, Main Message, Practical Takeaway, Call to Action, Relevant Hashtags.
  Constraint: Do not make exaggerated claims. Do not promise guaranteed jobs or salaries. Focus on practical software craftsmanship.
  ```
- **Expected Output:** 5 well-crafted, platform-native social media posts with clear takeaways and hashtags.
- **Verification Method:** Reviewed for adherence to tone, length constraints, and anti-hyperbole rules.
- **Known Limitations:** Frequently adds excessive emojis unless specifically instructed to maintain professional restraint.

---

### 14. Presentation Creation
- **Prompt ID:** `PRM-14-SLIDES`
- **Purpose:** Formulate executive slide deck content and verbatim speaker notes for academic evaluation.
- **Full Prompt:**
  ```text
  You are an academic presentation coach preparing a 5-slide capstone defence presentation.
  Create the slide structure and verbatim speaker notes for CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers.
  Slide Breakdown:
  Slide 1: Title, Problem Statement, Target Audience, Objective.
  Slide 2: Research Methodology, Technical-Writing Principles, Source Verification, AI Stack.
  Slide 3: Content Plan and Python CLI Project Architecture.
  Slide 4: Before-and-After Editing Case Study, Quality Checklist, Verification Results.
  Slide 5: Automation Workflow, Ethics & Responsible AI, Results, Limitations & Conclusion.
  Constraint: Exactly 5 slides. For each slide, provide: Visual Card Breakdown (3-4 bullet cards) and complete, professional Speaker Notes.
  ```
- **Expected Output:** 5-slide executive presentation outline paired with comprehensive speaker notes.
- **Verification Method:** Implemented and rendered via `presentation/generate_presentation.py` into `five-slide-presentation.pptx`.
- **Known Limitations:** Slide content can become text-heavy if not constrained to 3–4 concise cards per slide.

---

### 15. Content Calendar Automation
- **Prompt ID:** `PRM-15-AUTOMATION`
- **Purpose:** Design Python automation scripts for content calendar tracking, deadline warnings, and verification gates.
- **Full Prompt:**
  ```text
  You are a DevOps automation engineer designing a local content pipeline.
  Write a Python script named `content_calendar_notifier.py` that:
  1. Ingests a content calendar CSV containing: id, title, topic, planned_date, status, draft_location, author, reviewer, verification_status, priority.
  2. Analyzes dates against a reference date to identify overdue posts and items due in <= 3 days.
  3. Enforces a Technical Verification Gate: warns if any post in Drafting/In Review lacks "Verified" status.
  4. Enforces Human-in-the-Loop policy: prohibits automated status changes to "Published" without manual approval.
  5. Outputs formatted terminal alerts, an executive Markdown digest, and a JSON audit log.
  Constraint: Use Python standard library only (`csv`, `datetime`, `json`, `argparse`, `os`, `sys`).
  ```
- **Expected Output:** Fully functional, standalone automation script with CSV parsing, reporting, and audit capabilities.
- **Verification Method:** Tested with simulated dates on `sample-data.csv`: script executed with exit code 0 and generated all reports.
- **Known Limitations:** Local automation requires manual invocation or OS-level scheduling (Task Scheduler / cron) rather than cloud webhooks.
