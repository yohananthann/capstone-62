# AI Draft Versus Final Edit: Before-and-After Analysis
**Project:** CAPSTONE 62 — AI-Powered Technical Blog Writing Series for Developers  
**Author:** Alex Chen (Student Author) & Prof. Sarah Jenkins (Reviewer)  
**Sample Note:** *This before-and-after case study is based on a recorded initial generation session using an unconstrained LLM prompt, illustrating typical AI failure modes (hallucinated CLI flags, passive fluff, unhandled exceptions, and missing dependencies) and demonstrating the rigorous human engineering review required to transform raw AI output into publication-grade technical documentation.*

---

## 1. Context & The "Raw AI Draft"
When prompting an AI with a general request like *"Write a tutorial explaining how to build a Python CLI task manager"*, the model often generates code that *looks* syntactically plausible but suffers from critical flaws:
- Inventing non-existent command-line arguments (hallucinations).
- Omitting file existence checks, causing fatal crashes on fresh installations.
- Using wordy, passive, and unengaging introductory prose.
- Making unsubstantiated performance claims.

Below is an authentic sample of an unedited, raw AI draft for the introductory section and task-loading code of Post 1.

---

## 2. The Original Raw AI Draft (Unedited)

```markdown
### Introduction to Python CLIs
In the modern world of programming today, command-line interfaces are utilized extensively by various developers across many companies. It is well known that building a CLI in Python will make your programs run 10x faster and will guarantee you an interview at top tech companies. You can just utilize Python's `argparse` module which is very easy and simple for everyone to use.

### Loading Tasks from File
To load your tasks, you should simply read the `tasks.json` file. Here is the code to do that:

```python
import json

def load_tasks():
    # Load tasks from file
    f = open("tasks.json")
    data = json.loads(f.read())
    return data
```

When you run `python task_manager.py --json --load-all`, it will automatically parse the database and output all the tasks in a formatted table for you.
```

---

## 3. Systematic Problem Identification

1. **Technical Inaccuracy & Hallucinations:**
   - **File Handling Bug:** `open("tasks.json")` opens without a context manager (`with`), risking file descriptor leaks.
   - **Missing File Crash:** If `tasks.json` does not exist on the user's machine (as is true on any clean install), Python throws an unhandled `FileNotFoundError` and crashes immediately.
   - **Inefficient Reading:** Using `json.loads(f.read())` is less efficient than the standard library `json.load(f)`.
   - **Hallucinated CLI Arguments:** The draft tells the user to run `python task_manager.py --json --load-all`. Neither `--json` nor `--load-all` was ever defined in the code! Running this command produces `unrecognized arguments: --json --load-all` and exits with an error.

2. **Clarity & Tone Deficiencies:**
   - **Wordy Passive Fluff:** Phrases like *"In the modern world of programming today, command-line interfaces are utilized extensively..."* add cognitive clutter without technical substance.
   - **Condescending Jargon:** Calling `argparse` *"very easy and simple for everyone to use"* alienates beginner students who may find argument parsing challenging.

3. **Source Verification & Ethical Issues:**
   - **Wild, Unsubstantiated Claims:** The draft claims building a CLI *"will make your programs run 10x faster and will guarantee you an interview at top tech companies."* This is ethically irresponsible, factually untrue, and damages developer credibility.

---

## 4. The Revised Final Version (Publication-Grade)

```markdown
### 1. Introduction: Why Command-Line Tools Matter
Every software engineer spends significant time in the terminal. Whether deploying containerized services, managing Git repositories, or automating repetitive workflows, command-line interfaces (CLIs) remain the backbone of developer tooling.

Learning to build command-line applications in Python teaches you how operating systems handle argument passing, stream separation, and local data persistence. These fundamental systems skills directly strengthen your public developer portfolio.

### 2. Loading Tasks Safely with Defensive JSON Handling
When reading local application data, your code must anticipate edge cases: what if the data file does not exist yet? What if another process edited the file with invalid syntax?

Here is the robust, production-tested implementation using Python's standard library:

```python
import json
import os
import sys
from typing import List, Dict, Any

DEFAULT_DATA_FILE = "tasks.json"

def load_tasks(filepath: str = DEFAULT_DATA_FILE) -> List[Dict[str, Any]]:
    """
    Safely load task records from a JSON file.
    Returns an empty list if the file is missing or contains invalid JSON.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError) as e:
        print(f"[Warning] Could not parse tasks file ({e}). Starting with empty list.", file=sys.stderr)
        return []
```

To list your active tasks, run the verified subcommand:
```bash
python task_manager.py list
```
```

---

## 5. Direct Comparison Table

| Original Raw Text | Identified Problem | Revised Text | Reason for Change |
|---|---|---|---|
| *"In the modern world of programming today, command-line interfaces are utilized extensively by various developers..."* | Wordy, passive opening with redundant filler words. Violates Google Developer Style Guide. | *"Every software engineer spends significant time in the terminal. Whether deploying containerized services, managing Git repositories..."* | Replaced passive throat-clearing with a direct, active hook illustrating real developer workflows. |
| *"...will make your programs run 10x faster and will guarantee you an interview at top tech companies."* | Unsubstantiated speed claim and ethically irresponsible promise of guaranteed employment. | *"...teaches you how operating systems handle argument passing, stream separation, and local data persistence. These fundamental systems skills directly strengthen your public developer portfolio."* | Replaced fabricated hype with realistic, verifiable pedagogical value and portfolio benefits. |
| *"You can just utilize Python's `argparse` module which is very easy and simple for everyone to use."* | Dismissive language ("just", "easy", "simple") that alienates struggling beginners. | *"We structure command-line commands cleanly using Python's built-in `argparse` module."* | Neutral, objective instructional tone adhering to MDN and Google technical writing standards. |
| `f = open("tasks.json")`<br>`data = json.loads(f.read())` | **Fatal crash bug:** Unhandled `FileNotFoundError` on first run; file descriptor leak; inefficient string buffer loading. | `if not os.path.exists(filepath): return []`<br>`with open(filepath, "r", encoding="utf-8") as f:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`data = json.load(f)` | Enforced defensive programming: verifies file presence, uses context manager (`with`), specifies UTF-8 encoding, and uses direct stream parsing. |
| *No error handling on corrupt JSON.* | Corrupted or partially written JSON files crash the CLI with an unhandled `json.decoder.JSONDecodeError`. | `except (json.JSONDecodeError, OSError) as e:`<br>&nbsp;&nbsp;&nbsp;&nbsp;`print(f"[Warning]...", file=sys.stderr)`<br>&nbsp;&nbsp;&nbsp;&nbsp;`return []` | Prevents crashes; warns the user cleanly via `sys.stderr` and safely falls back to a clean state. |
| *"When you run `python task_manager.py --json --load-all`..."* | **Hallucination:** Neither `--json` nor `--load-all` was implemented in the argument parser. Command fails immediately. | *"To list your active tasks, run the verified subcommand: `python task_manager.py list`"* | Aligned tutorial documentation with the exact `argparse` subcommands physically implemented in the verified code. |

---

## 6. Key Takeaways for Student Writers
1. **Never Trust Unexecuted Code:** LLMs generate statistically likely tokens, not compiled binaries. If you do not run the snippet in your own terminal, consider it broken.
2. **Eliminate Fluff & Hyperbole:** Good technical writing is concise, objective, and empathetic. Respect the reader's time by getting straight to the problem and solution.
3. **Be Transparent:** Acknowledge AI tools as research assistants, but own every single line of code and prose you put your name on.
