# CAPSTONE 62: Final Demonstration Guide
**Project:** AI-Powered Technical Blog Writing Series for Developers  
**Target:** Faculty Evaluators, Peer Reviewers, and Portfolio Examiners  
**Execution Time:** ~3–5 minutes for full end-to-end evaluation

---

## 1. Quick Environment Verification
Verify that your system meets the minimum requirement of Python 3.10+ (Standard Library only):

```bash
# Verify Python version
python --version
```
*Expected:* Python 3.10.x, 3.11.x, or 3.12.x. (Tested on Python 3.12.6).

---

## 2. Step 1: Run the Automated Unit Test Suites
Execute the full test discovery suite to verify all business logic, boundary validation, and error recovery in the companion code:

```bash
python -m unittest discover -s capstone-62/tests -p "test_*.py" -v
```

### Expected Output:
- **17 test cases executed** across `test_task_manager.py` and `test_string_utils.py`.
- Tests verify: task addition, negative ID rejection, empty title checks, JSON persistence, recovery from malformed/corrupted JSON, title slugification, and reading time estimation.
- **Result:** `Ran 17 tests in ~0.3s — OK`.

---

## 3. Step 2: Test the Live CLI Task Manager (Post 1 Companion)
Run the full lifecycle of the command-line application directly from your shell:

```bash
# Navigate to code directory or run directly
python capstone-62/code/task_manager.py clear

# Add tasks with varying priorities
python capstone-62/code/task_manager.py add "Setup virtual environment and git repo" -p high
python capstone-62/code/task_manager.py add "Write unit tests for CLI commands" -p high
python capstone-62/code/task_manager.py add "Draft technical blog article" -p medium
python capstone-62/code/task_manager.py add "Schedule social media announcement" -p low

# Display formatted task table
python capstone-62/code/task_manager.py list

# Mark task #1 as complete
python capstone-62/code/task_manager.py complete 1

# Filter by pending and completed
python capstone-62/code/task_manager.py list --status pending
python capstone-62/code/task_manager.py list --status completed
```

### Expected Output:
- Formatted tabular layout with ID, completion status (`[X] Done` vs `[ ] Pending`), Priority, and Title.
- Persistent state saved to `capstone-62/code/tasks.json`.

---

## 4. Step 3: Run the 5 Python Errors Diagnostic Engine (Post 2 Companion)
Run the automated error demonstration script that safely simulates and catches the five common Python errors:

```bash
python capstone-62/code/error_examples.py
```

### Expected Output:
- Formatted terminal report breaking down:
  1. `SyntaxError` (missing colon)
  2. `NameError` / `UnboundLocalError` (uninitialized variable)
  3. `TypeError` (string concatenation with integer)
  4. `IndexError` (list bounds violation)
  5. `KeyError` (missing dictionary key)
- Shows captured traceback, root cause explanation, and defensive correction for each.

---

## 5. Step 4: Run the Content Calendar Automation Engine (Workflow Demo)
Run the local content calendar automation engine to evaluate schedule status, upcoming deadlines, and verification gates:

```bash
python capstone-62/automation/content_calendar_notifier.py --date 2026-10-15
```

### Expected Output:
- Scans `sample-data.csv` against reference date `2026-10-15`.
- Identifies 1 overdue item (ID 5: *Generators & Iterators*).
- Identifies 2 items due within 3 days (ID 1: *Python CLI App*, ID 4: *Virtual Environments*).
- Identifies 2 verification blockers requiring unit testing sign-off.
- Emits policy reminder: *"100% Manual Human Approval Required Prior to Final Publishing"*.
- Automatically generates:
  - Markdown digest: `automation/notification-digest.md`
  - JSON audit log: `automation/notification-audit.json`

---

## 6. Step 5: Regenerate the Professional Presentation Deck
Regenerate the executive 16:9 widescreen presentation:

```bash
python capstone-62/presentation/generate_presentation.py
```

### Deliverable Produced:
- `presentation/five-slide-presentation.pptx` (saved with executive slate theme, cards, and speaker notes).
- Companion script and markdown notes: `presentation/presentation-notes.md`.

---

## 7. Step 6: Review Technical Documentation and Blog Series
Inspect the published Markdown articles:
1. **Post 1:** [`capstone-62/blogs/post-1-python-cli.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-1-python-cli.md) (~1,000 words, tested code).
2. **Post 2:** [`capstone-62/blogs/post-2-python-errors.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-2-python-errors.md) (5 common errors & fixes).
3. **Post 3:** [`capstone-62/blogs/post-3-functions-testing.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/blogs/post-3-functions-testing.md) (Functions, pure functions, and `unittest`).
4. **Before-and-After Audit:** [`capstone-62/verification/before-after-analysis.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/verification/before-after-analysis.md).
5. **Quality Checklist:** [`capstone-62/checklist/technical-writing-checklist.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/checklist/technical-writing-checklist.md).
6. **Prompt Library:** [`capstone-62/prompts/prompt-library.md`](file:///c:/Users/yohes/OneDrive/Desktop/44/capstone-62/prompts/prompt-library.md) (15 prompt categories).

All tests and deliverables are certified reproducible and fully documented.
