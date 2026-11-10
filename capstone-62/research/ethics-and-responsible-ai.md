# Ethics and Responsible AI in Technical Writing
**Project:** CAPSTONE 62 — AI-Powered Technical Blog Writing Series for Developers  
**Author:** Alex Chen (CSE Student Developer)  
**Academic Mentor:** Prof. Sarah Jenkins  
**Date:** October 15, 2026

---

## 1. Guiding Philosophy: AI as a Cognitive Amplifier
In computer science education, Large Language Models must be used as **cognitive amplifiers, not intellectual replacements**. When a student relies on AI to ghostwrite assignments or generate unverified code, they bypass the essential learning process: cognitive struggle, debugging, mental model formation, and technical mastery.

In **CAPSTONE 62**, AI is positioned strictly as an interactive research assistant, brainstorming partner, and editorial critic. The student remains the chief software architect, primary author, and ultimate guarantor of technical correctness.

---

## 2. Core Ethical Principles for Student Developers

### Principle 1: Authentic Understanding Over Auto-Generation
AI should enhance the student’s ability to articulate complex concepts, never mask a lack of understanding. If a student cannot explain every line of code or technical assertion in their article, that section must not be published.

### Principle 2: Mandatory Testing and Zero Fabricated Results
Every code snippet, script, and CLI invocation featured in a technical post must be executed in a physical, verifiable runtime environment. It is unethical to manufacture fake benchmarks, fabricate test outputs, or claim code was tested when it was not. Code that has not been executed must be explicitly marked: `[Status: Untested — Conceptual Demonstration Only]`.

### Principle 3: Rigorous Fact-Checking Against Primary Sources
LLMs are probabilistic token generators susceptible to confident hallucinations. All technical claims, argument names, language specifications, and release dates must be cross-checked against official documentation (such as Python.org, MDN, or the Google Developer Style Guide).

### Principle 4: Attribution and Anti-Plagiarism
Students must never scrape, spin, or paraphrase existing technical blogs (from Real Python, Medium, Dev.to, etc.) and present them as original work. Authoritative references and prior intellectual work must be cited with clear, direct hyperlinks.

### Principle 5: Transparent AI Disclosure
Whenever AI systems are used for outlining, drafting assistance, code generation, or copy-editing, students must provide a transparent, standardized disclosure statement acknowledging the tools used and the human verification undertaken.

### Principle 6: Intellectual Property & Copyright Respect
Code licenses (MIT, Apache 2.0, GPL) and third-party copyrights must be strictly respected. Training data memorization risks must be guarded against by ensuring code samples reflect original architectures tailored to the educational objectives.

### Principle 7: Privacy, Credentials, and Secret Protection
Never input private repository code, proprietary institutional data, API keys, passwords, or personal identifying information (PII) into public AI prompts. Code examples must use generic placeholders (e.g., `user@example.com`, `<API_KEY>`).

### Principle 8: Security and Defensive Programming Standards
Technical blogs have wide reach; published vulnerabilities can be copied by thousands of other learners. Code must model secure practices: avoid raw `eval()`, sanitize user input, use context managers for file descriptors, and validate data types.

### Principle 9: Uncompromising Human-in-the-Loop Governance
Final responsibility for publication rests solely with the human author and reviewer. Automated systems may suggest schedules or flag approaching deadlines, but a human must manually inspect the deliverables and authorize deployment.

---

## 3. Standardized AI-Use Disclosure Badge

The following disclosure format is established by CAPSTONE 62 and embedded at the footer of all articles:

```markdown
---
> **AI-Use Disclosure:** This article was researched and outlined with the assistance of [AI Tool Names, e.g., Google Gemini and ChatGPT] for pedagogical structuring and editorial review. All Python code implementations, exception handlers, and terminal output transcripts were authored, executed, and verified locally by the author on Python 3.12.6. No text or code was copied from third-party blogs.
---
```

---

## 4. Responsible AI Skills Matrix

| AI Competency | Academic & Professional Role | Deliverable Demonstrating Skill |
|---|---|---|
| **1. Prompt Engineering** | Designing constraint-driven, anti-hallucination prompts with strict output schemas. | [`prompts/prompt-library.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/prompts/prompt-library.md) (15 specialized prompts) |
| **2. Research & Information Gathering** | Synthesizing technical requirements and evaluating developer tools across free tiers. | [`research/research-report.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/research/research-report.md) & [`research/references.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/research/references.md) |
| **3. Technical Writing** | Authoring clear, progressive developer tutorials adhering to Google Developer Style Guide. | [`blogs/post-1-python-cli.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-1-python-cli.md) (~1,000 words) |
| **4. Editing & Proofreading** | Refining prose, eliminating passive voice, and optimizing sentence brevity. | [`verification/before-after-analysis.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/verification/before-after-analysis.md) |
| **5. Fact-Checking & Source Verification** | Auditing technical claims and URLs against primary documentation standards. | [`verification/verification-report.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/verification/verification-report.md) |
| **6. Code Generation & Review** | Architecting defensive Python applications and conducting security/correctness audits. | [`code/task_manager.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/task_manager.py) & [`code/error_examples.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/code/error_examples.py) |
| **7. Code Testing & QA** | Writing automated `unittest` test suites covering boundary conditions and corrupt states. | [`tests/test_task_manager.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/tests/test_task_manager.py) (17/17 passing tests) |
| **8. Visual & Presentation Design** | Designing structured executive slide decks with speaker notes and visual card layouts. | [`presentation/five-slide-presentation.pptx`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/presentation/five-slide-presentation.pptx) & [`presentation/presentation-notes.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/presentation/presentation-notes.md) |
| **9. Workflow Automation** | Building scheduled Python automation to monitor deadlines and enforce quality gates. | [`automation/content_calendar_notifier.py`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/automation/content_calendar_notifier.py) |
