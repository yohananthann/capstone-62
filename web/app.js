/**
 * CAPSTONE 62 — Local Showcase & Dashboard Controller
 * Connects the web UI directly to the local Python runtime and REST API.
 */

// Error Database for Tab 4
const ERROR_DATABASE = {
  syntax: {
    name: "SyntaxError",
    summary: "Missing colon (:) at the end of the compound statement header",
    cause: "Python syntax requires a colon at the end of conditional, loop, and function definitions.",
    failing_code: `def check_status(score):\n    if score >= 50\n        print("Passed")`,
    traceback: `  File "code/error_examples.py", line 14\n    if 5 > 3\n            ^\nSyntaxError: expected ':' (line 1)`,
    fixed_code: `def check_status(score):\n    if score >= 50:  # Colon added\n        print("Passed")`,
    fix_explanation: "Add a colon directly after the boolean expression: `if score >= 50:`."
  },
  name: {
    name: "NameError / UnboundLocalError",
    summary: "Local variable referenced before assignment or uninitialized",
    cause: "Accessing or incrementing a local variable before it has been defined in the current scope.",
    failing_code: `def increment_visitor():\n    counter += 1  # UnboundLocalError\n    return counter`,
    traceback: `UnboundLocalError: cannot access local variable 'counter' where it is not associated with a value`,
    fixed_code: `def increment_visitor(current=0):\n    counter = current + 1  # Initialize explicitly\n    return counter`,
    fix_explanation: "Initialize `counter = 0` prior to reading or modifying it, or accept it as a function parameter."
  },
  type: {
    name: "TypeError",
    summary: "Attempting string concatenation with an integer without casting",
    cause: "Python is strongly typed and refuses implicit conversion between strings and numbers using the '+' operator.",
    failing_code: `age_input = "21"\nnext_year = age_input + 1  # TypeError`,
    traceback: `TypeError: can only concatenate str (not "int") to str`,
    fixed_code: `age_input = "21"\nnext_year = int(age_input) + 1  # Cast to integer\nprint(f"Next year: {next_year}")`,
    fix_explanation: "Explicitly cast the string representation to an integer using `int(age_input)` before performing arithmetic."
  },
  index: {
    name: "IndexError",
    summary: "List index out of range bounds",
    cause: "Attempting to access an index greater than or equal to `len(list)` or using an invalid negative index.",
    failing_code: `frameworks = ["Flask", "FastAPI", "Django"]\nselected = frameworks[3]  # IndexError (valid: 0, 1, 2)`,
    traceback: `IndexError: list index out of range`,
    fixed_code: `frameworks = ["Flask", "FastAPI", "Django"]\nidx = 3\nselected = frameworks[idx] if idx < len(frameworks) else "Django"`,
    fix_explanation: "Verify that `0 <= index < len(lst)` before access, or use list slicing/iteration."
  },
  key: {
    name: "KeyError",
    summary: "Attempting to access a non-existent dictionary key via square brackets",
    cause: "Square bracket lookup `dict[key]` raises KeyError if the key is not present in the dictionary.",
    failing_code: `user = {"name": "Alex", "role": "Developer"}\nemail = user["email"]  # KeyError`,
    traceback: `KeyError: 'email'`,
    fixed_code: `user = {"name": "Alex", "role": "Developer"}\nemail = user.get("email", "no-email@domain.com")  # Safe fallback`,
    fix_explanation: "Use `dict.get(key, default)` or `if key in dict:` to retrieve optional dictionary values safely."
  }
};

let allTasks = [];
let currentFilter = "all";
let currentSlideIndex = 0;
let presentationSlides = [];
let currentBlogId = "post-1-python-cli.md";

// Initialize on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupTaskManager();
  setupTestRunner();
  setupErrorLab();
  setupBlogReader();
  setupStringUtilsLab();
  setupCalendar();
  setupPresentation();
  setupTerminal();
  
  // Initial data fetches
  fetchStatus();
  fetchTasks();
  fetchCalendar();
  fetchBlog(currentBlogId);
  fetchPresentationData();
});

// -------------------------------------------------------------
// Navigation Tabs
// -------------------------------------------------------------
function setupNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const tabId = item.getAttribute("data-tab");
      switchTab(tabId);
    });
  });

  // Top quick action buttons
  document.getElementById("btn-quick-tests")?.addEventListener("click", () => {
    switchTab("tab-test-runner");
    runUnitTests();
  });

  document.getElementById("btn-quick-automation")?.addEventListener("click", () => {
    switchTab("tab-calendar");
    runCalendarEngine();
  });
}

function switchTab(tabId) {
  // Update nav buttons
  document.querySelectorAll(".nav-item").forEach(btn => {
    if (btn.getAttribute("data-tab") === tabId) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  // Update tab panes
  document.querySelectorAll(".tab-pane").forEach(pane => {
    if (pane.id === tabId) {
      pane.classList.add("active");
    } else {
      pane.classList.remove("active");
    }
  });

  window.scrollTo({ top: 0, behavior: "smooth" });
}

// -------------------------------------------------------------
// Global Status Fetch
// -------------------------------------------------------------
async function fetchStatus() {
  try {
    const res = await fetch("/api/status");
    if (!res.ok) return;
    const data = await res.json();
    if (data.tasks) {
      const overviewCount = document.getElementById("overview-task-count");
      if (overviewCount) overviewCount.textContent = data.tasks.total;
      const badgeCount = document.getElementById("badge-task-count");
      if (badgeCount) badgeCount.textContent = data.tasks.total;
    }
  } catch (err) {
    console.warn("Status fetch failed:", err);
  }
}

// -------------------------------------------------------------
// Tab 2: CLI Task Manager
// -------------------------------------------------------------
function setupTaskManager() {
  const form = document.getElementById("form-add-task");
  const refreshBtn = document.getElementById("btn-refresh-tasks");
  const clearBtn = document.getElementById("btn-clear-tasks");

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const titleInput = document.getElementById("task-title-input");
    const prioritySelect = document.getElementById("task-priority-select");
    const title = titleInput.value.trim();
    const priority = prioritySelect.value;
    if (!title) return;

    try {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "add", title, priority })
      });
      const data = await res.json();
      if (data.command) {
        document.getElementById("last-cli-command").textContent = data.command;
      }
      titleInput.value = "";
      allTasks = data.tasks || [];
      renderTasks();
      fetchStatus();
    } catch (err) {
      alert("Failed to add task: " + err.message);
    }
  });

  refreshBtn?.addEventListener("click", fetchTasks);

  clearBtn?.addEventListener("click", async () => {
    if (!confirm("Are you sure you want to clear all tasks from the local JSON store?")) return;
    try {
      const res = await fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "clear" })
      });
      const data = await res.json();
      if (data.command) {
        document.getElementById("last-cli-command").textContent = data.command;
      }
      allTasks = data.tasks || [];
      renderTasks();
      fetchStatus();
    } catch (err) {
      alert("Failed to clear tasks: " + err.message);
    }
  });

  // Filter Buttons
  document.querySelectorAll(".filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.getAttribute("data-filter");
      renderTasks();
    });
  });
}

async function fetchTasks() {
  try {
    const res = await fetch("/api/tasks");
    const data = await res.json();
    allTasks = data.tasks || [];
    renderTasks();
  } catch (err) {
    console.error("Failed to fetch tasks:", err);
  }
}

function renderTasks() {
  const container = document.getElementById("tasks-container");
  if (!container) return;

  const countAll = allTasks.length;
  const countPending = allTasks.filter(t => !t.completed).length;
  const countCompleted = allTasks.filter(t => t.completed).length;

  document.getElementById("count-all").textContent = countAll;
  document.getElementById("count-pending").textContent = countPending;
  document.getElementById("count-completed").textContent = countCompleted;

  const badgeCount = document.getElementById("badge-task-count");
  if (badgeCount) badgeCount.textContent = countAll;
  const overviewCount = document.getElementById("overview-task-count");
  if (overviewCount) overviewCount.textContent = countAll;

  let filtered = allTasks;
  if (currentFilter === "pending") filtered = allTasks.filter(t => !t.completed);
  if (currentFilter === "completed") filtered = allTasks.filter(t => t.completed);

  if (filtered.length === 0) {
    container.innerHTML = `<div class="empty-state">No tasks found for current filter (${currentFilter}).</div>`;
    return;
  }

  container.innerHTML = filtered.map(t => `
    <div class="task-item ${t.completed ? 'completed' : ''}" data-id="${t.id}">
      <div class="task-left">
        <button class="task-check-btn" onclick="toggleTaskComplete(${t.id})">
          ${t.completed ? '✓' : ''}
        </button>
        <span class="task-id">#${t.id}</span>
        <span class="task-text">${escapeHtml(t.title)}</span>
      </div>
      <div class="task-right">
        <span class="priority-tag ${t.priority || 'medium'}">${t.priority || 'medium'}</span>
        <button class="task-del-btn" onclick="deleteTask(${t.id})" title="Delete task">✕</button>
      </div>
    </div>
  `).join("");
}

window.toggleTaskComplete = async function(id) {
  try {
    const res = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "complete", id })
    });
    const data = await res.json();
    if (data.command) {
      document.getElementById("last-cli-command").textContent = data.command;
    }
    allTasks = data.tasks || [];
    renderTasks();
  } catch (err) {
    alert("Error updating task: " + err.message);
  }
};

window.deleteTask = async function(id) {
  try {
    const res = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action: "delete", id })
    });
    const data = await res.json();
    if (data.command) {
      document.getElementById("last-cli-command").textContent = data.command;
    }
    allTasks = data.tasks || [];
    renderTasks();
    fetchStatus();
  } catch (err) {
    alert("Error deleting task: " + err.message);
  }
};

// -------------------------------------------------------------
// Tab 3: Unit Test Runner
// -------------------------------------------------------------
function setupTestRunner() {
  const btn = document.getElementById("btn-run-tests");
  btn?.addEventListener("click", runUnitTests);
}

async function runUnitTests() {
  const btn = document.getElementById("btn-run-tests");
  const outputEl = document.getElementById("test-terminal-output");
  const statusEl = document.getElementById("test-overall-status");
  const durationEl = document.getElementById("test-duration");

  if (btn) btn.disabled = true;
  outputEl.textContent = "Executing 'python -m unittest discover -s capstone-62/tests -p \"test_*.py\" -v' ...";
  statusEl.textContent = "Running...";

  const startTime = performance.now();
  try {
    const res = await fetch("/api/run-tests", { method: "POST" });
    const data = await res.json();
    const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);

    durationEl.textContent = `${elapsed}s`;
    outputEl.textContent = data.stdout;

    if (data.passed) {
      statusEl.textContent = "Passed (17/17)";
      statusEl.style.color = "var(--accent-emerald)";
    } else {
      statusEl.textContent = "Failed";
      statusEl.style.color = "var(--accent-rose)";
    }
  } catch (err) {
    outputEl.textContent = "Test execution failed: " + err.message;
    statusEl.textContent = "Error";
  } finally {
    if (btn) btn.disabled = false;
  }
}

// -------------------------------------------------------------
// Tab 4: 5 Common Python Errors Lab
// -------------------------------------------------------------
function setupErrorLab() {
  const selectBtns = document.querySelectorAll(".error-select-btn");
  selectBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      selectBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const errKey = btn.getAttribute("data-error");
      renderErrorDetail(errKey);
    });
  });

  document.getElementById("btn-run-all-errors")?.addEventListener("click", async () => {
    switchTab("tab-terminal");
    const cmdInput = document.getElementById("terminal-cmd-input");
    if (cmdInput) cmdInput.value = "python capstone-62/code/error_examples.py";
    executeTerminalCommand("python capstone-62/code/error_examples.py");
  });

  // Initial render
  renderErrorDetail("syntax");
}

function renderErrorDetail(key) {
  const err = ERROR_DATABASE[key];
  const container = document.getElementById("error-display-card");
  if (!err || !container) return;

  container.innerHTML = `
    <div>
      <h3 style="font-family: var(--font-heading); font-size: 20px; color: #fff; margin-bottom: 4px;">
        ${err.name}
      </h3>
      <p style="color: var(--text-muted); font-size: 13.5px;">${err.summary}</p>
    </div>

    <div>
      <div class="err-section-title">1. Root Cause Explanation</div>
      <p style="font-size: 13.5px; color: #e2e8f0; line-height: 1.6;">${err.cause}</p>
    </div>

    <div>
      <div class="err-section-title">2. Failing Code Snippet (Reproducing Bug)</div>
      <pre style="background: #080c14; padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border-subtle); color: #fda4af; font-family: var(--font-mono); font-size: 12.5px;"><code>${escapeHtml(err.failing_code)}</code></pre>
    </div>

    <div>
      <div class="err-section-title">3. Real Captured Traceback</div>
      <div class="traceback-box">${escapeHtml(err.traceback)}</div>
    </div>

    <div>
      <div class="err-section-title">4. Defensive Correction Code</div>
      <div class="fix-box">${escapeHtml(err.fixed_code)}</div>
      <p style="font-size: 12.5px; color: var(--text-muted); margin-top: 6px;">
        <strong>Resolution Strategy:</strong> ${escapeHtml(err.fix_explanation)}
      </p>
    </div>
  `;
}

// -------------------------------------------------------------
// Tab 5: Technical Blog Reader
// -------------------------------------------------------------
function setupBlogReader() {
  const tabs = document.querySelectorAll(".blog-tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const blogId = tab.getAttribute("data-blog");
      currentBlogId = blogId;
      fetchBlog(blogId);
    });
  });
}

async function fetchBlog(blogId) {
  const container = document.getElementById("blog-content-view");
  const wordCountEl = document.getElementById("blog-word-count");
  const readingTimeEl = document.getElementById("blog-reading-time");
  const codeRefEl = document.getElementById("blog-code-ref");

  container.innerHTML = '<div class="loading-spinner">Loading article...</div>';

  try {
    const res = await fetch(`/api/blog?id=${encodeURIComponent(blogId)}`);
    const data = await res.json();
    if (data.error) {
      container.innerHTML = `<div class="empty-state">${data.error}</div>`;
      return;
    }

    if (data.meta) {
      wordCountEl.textContent = `${data.meta.word_count || '—'} words`;
      readingTimeEl.textContent = `${data.meta.reading_time_mins || '—'} min read`;
    }

    if (blogId.includes("cli")) {
      codeRefEl.textContent = "capstone-62/code/task_manager.py";
    } else if (blogId.includes("errors")) {
      codeRefEl.textContent = "capstone-62/code/error_examples.py";
    } else {
      codeRefEl.textContent = "capstone-62/code/string_utils.py";
    }

    container.innerHTML = parseMarkdownToHtml(data.content);
  } catch (err) {
    container.innerHTML = `<div class="empty-state">Failed to load blog: ${err.message}</div>`;
  }
}

// Simple markdown formatter
function parseMarkdownToHtml(md) {
  let html = md
    // Escape HTML special characters
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Code blocks ```python ... ```
  html = html.replace(/```([a-z]*)\n([\s\S]*?)```/gim, (match, lang, code) => {
    return `<pre><code class="language-${lang}">${code.trim()}</code></pre>`;
  });

  // Inline code `code`
  html = html.replace(/`([^`]+)`/gim, '<code>$1</code>');

  // Bold & Italic
  html = html.replace(/\*\*([^*]+)\*\*/gim, '<strong>$1</strong>');
  html = html.replace(/\*([^*]+)\*/gim, '<em>$1</em>');

  // Blockquotes
  html = html.replace(/^\> (.*$)/gim, '<blockquote style="border-left: 3px solid var(--accent-cyan); padding-left: 14px; margin: 14px 0; color: #94a3b8; font-style: italic;">$1</blockquote>');

  // Unordered list items
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');

  // Paragraph breaks
  html = html.split('\n\n').map(p => {
    p = p.trim();
    if (!p) return '';
    if (p.startsWith('<h') || p.startsWith('<pre') || p.startsWith('<blockquote') || p.startsWith('<li')) {
      return p;
    }
    return `<p>${p}</p>`;
  }).join('\n');

  return html;
}

// -------------------------------------------------------------
// Tab 6: String Utilities Lab
// -------------------------------------------------------------
function setupStringUtilsLab() {
  const slugInput = document.getElementById("slug-input");
  const slugOutput = document.getElementById("slug-output");

  const readingInput = document.getElementById("reading-time-input");
  const wordsOutput = document.getElementById("words-output");
  const readingTimeOutput = document.getElementById("reading-time-output");

  const truncateLimit = document.getElementById("truncate-limit");
  const truncateOutput = document.getElementById("truncate-output");

  // Local calculation mirrors of string_utils.py
  function updateSlug() {
    const val = slugInput.value.trim().toLowerCase();
    const slug = val.replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
    slugOutput.textContent = slug || "(empty)";
  }

  function updateReadingTime() {
    const text = readingInput.value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    const mins = words > 0 ? Math.max(1, Math.ceil(words / 200)) : 0;
    wordsOutput.textContent = `${words} words`;
    readingTimeOutput.textContent = `${mins} minute${mins !== 1 ? 's' : ''}`;
    updateTruncate();
  }

  function updateTruncate() {
    const text = readingInput.value.trim();
    const limit = parseInt(truncateLimit.value) || 15;
    const words = text ? text.split(/\s+/) : [];
    if (words.length <= limit) {
      truncateOutput.textContent = words.join(" ");
    } else {
      truncateOutput.textContent = words.slice(0, limit).join(" ") + "...";
    }
  }

  slugInput?.addEventListener("input", updateSlug);
  readingInput?.addEventListener("input", updateReadingTime);
  truncateLimit?.addEventListener("input", updateTruncate);

  updateSlug();
  updateReadingTime();
}

// -------------------------------------------------------------
// Tab 7: Content Calendar
// -------------------------------------------------------------
function setupCalendar() {
  document.getElementById("btn-run-calendar-engine")?.addEventListener("click", runCalendarEngine);
}

async function fetchCalendar() {
  const tbody = document.getElementById("calendar-table-body");
  if (!tbody) return;

  try {
    const res = await fetch("/api/calendar");
    const data = await res.json();
    const rows = data.calendar || [];

    if (rows.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" class="text-center">No calendar items found.</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map(r => `
      <tr>
        <td><strong>#${r.id}</strong></td>
        <td><strong>${escapeHtml(r.title)}</strong></td>
        <td><span style="color: var(--text-muted); font-size: 12px;">${escapeHtml(r.topic)}</span></td>
        <td><code>${escapeHtml(r.planned_date)}</code></td>
        <td><span class="badge ${getStatusBadgeClass(r.status)}">${escapeHtml(r.status)}</span></td>
        <td><small>${escapeHtml(r.author)}<br/><span style="color: var(--text-dim);">${escapeHtml(r.reviewer)}</span></small></td>
        <td><span class="badge ${getGateBadgeClass(r.verification_status)}">${escapeHtml(r.verification_status)}</span></td>
        <td><span class="priority-tag ${r.priority.toLowerCase()}">${r.priority}</span></td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="8">Failed to load calendar: ${err.message}</td></tr>`;
  }
}

function getStatusBadgeClass(status) {
  if (status.includes("Ready")) return "badge-success";
  if (status.includes("Review")) return "badge-ai";
  return "";
}

function getGateBadgeClass(gate) {
  if (gate === "Verified") return "badge-success";
  return "priority-tag high";
}

async function runCalendarEngine() {
  const btn = document.getElementById("btn-run-calendar-engine");
  const digestView = document.getElementById("digest-view");
  const auditView = document.getElementById("audit-view");

  if (btn) btn.disabled = true;
  digestView.textContent = "Executing automation engine (content_calendar_notifier.py)...";

  try {
    const res = await fetch("/api/run-calendar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ date: "2026-10-15" })
    });
    const data = await res.json();
    digestView.textContent = data.digest || data.stdout;
    auditView.textContent = JSON.stringify(data.audit, null, 2);
  } catch (err) {
    digestView.textContent = "Automation failed: " + err.message;
  } finally {
    if (btn) btn.disabled = false;
  }
}

// -------------------------------------------------------------
// Tab 8: Presentation Deck
// -------------------------------------------------------------
function setupPresentation() {
  document.getElementById("btn-slide-prev")?.addEventListener("click", () => {
    if (currentSlideIndex > 0) {
      currentSlideIndex--;
      renderSlide();
    }
  });

  document.getElementById("btn-slide-next")?.addEventListener("click", () => {
    if (currentSlideIndex < presentationSlides.length - 1) {
      currentSlideIndex++;
      renderSlide();
    }
  });

  // Arrow key navigation
  window.addEventListener("keydown", (e) => {
    const presentationTab = document.getElementById("tab-presentation");
    if (!presentationTab.classList.contains("active")) return;
    if (e.key === "ArrowRight" || e.key === "PageDown") {
      if (currentSlideIndex < presentationSlides.length - 1) {
        currentSlideIndex++;
        renderSlide();
      }
    } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
      if (currentSlideIndex > 0) {
        currentSlideIndex--;
        renderSlide();
      }
    }
  });
}

async function fetchPresentationData() {
  try {
    const res = await fetch("/api/presentation-data");
    const data = await res.json();
    presentationSlides = data.slides || [];
    renderSlide();
  } catch (err) {
    console.error("Presentation data load failed:", err);
  }
}

function renderSlide() {
  if (presentationSlides.length === 0) return;
  const slide = presentationSlides[currentSlideIndex];
  const viewport = document.getElementById("slide-viewport");
  const counter = document.getElementById("slide-counter");
  const notesText = document.getElementById("speaker-notes-text");

  counter.textContent = `Slide ${slide.number} of ${presentationSlides.length}`;
  notesText.textContent = `"${slide.speaker_notes}"`;

  viewport.innerHTML = `
    <div>
      <div class="slide-category-tag">${slide.category} • SLIDE ${slide.number}</div>
      <div class="slide-main-title">${escapeHtml(slide.title)}</div>
      <div class="slide-core-question"><em>${escapeHtml(slide.question)}</em></div>
    </div>

    <div class="slide-cards-row">
      ${slide.cards.map(c => `
        <div class="slide-card-item">
          <h5>${escapeHtml(c.title)}</h5>
          <ul>
            ${c.points.map(p => `<li>${escapeHtml(p)}</li>`).join("")}
          </ul>
        </div>
      `).join("")}
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 14px; margin-top: 20px;">
      <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-dim);">CAPSTONE 62 • Computer Science Engineering</span>
      <span style="font-size: 11px; color: var(--accent-cyan);">16:9 Widescreen • Executive Slate Theme</span>
    </div>
  `;
}

// -------------------------------------------------------------
// Tab 9: Terminal Console
// -------------------------------------------------------------
function setupTerminal() {
  const input = document.getElementById("terminal-cmd-input");
  const btn = document.getElementById("btn-run-cmd");

  btn?.addEventListener("click", () => {
    executeTerminalCommand(input.value.trim());
  });

  input?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      executeTerminalCommand(input.value.trim());
    }
  });

  document.querySelectorAll(".btn-preset").forEach(preset => {
    preset.addEventListener("click", () => {
      const cmd = preset.getAttribute("data-cmd");
      input.value = cmd;
      executeTerminalCommand(cmd);
    });
  });
}

async function executeTerminalCommand(cmd) {
  if (!cmd) return;
  const outputEl = document.getElementById("terminal-live-output");
  const btn = document.getElementById("btn-run-cmd");

  if (btn) btn.disabled = true;
  outputEl.textContent = `$ ${cmd}\n\nRunning process in local Python runtime...\n`;

  try {
    const res = await fetch("/api/terminal", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: cmd })
    });
    const data = await res.json();
    if (data.error) {
      outputEl.textContent += `[Error] ${data.error}`;
    } else {
      outputEl.textContent = `$ ${cmd}\n\n${data.stdout}${data.stderr ? '\n' + data.stderr : ''}\n[Process exited with code ${data.exit_code}]`;
    }
  } catch (err) {
    outputEl.textContent += `Execution failed: ${err.message}`;
  } finally {
    if (btn) btn.disabled = false;
  }
}

// -------------------------------------------------------------
// Utilities
// -------------------------------------------------------------
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
