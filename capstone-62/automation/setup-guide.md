# Content Calendar Automation: Setup & Operations Guide
**Project:** CAPSTONE 62 — AI-Powered Technical Blog Writing Series for Developers  
**Target:** Local Execution, OS Schedulers, and Free-Tier Cloud Integrations  
**Security Policy:** Never hardcode API keys, tokens, or personal credentials.

---

## 1. Quickstart: Local Standalone Execution (Zero Setup)
The content calendar engine is designed to run out-of-the-box on any system with Python 3.10+ installed.

### Step 1: Clone or Navigate to the Repository
Open your terminal and ensure you are in the project root:
```bash
cd capstone-62
```

### Step 2: Run the Notifier with Default Sample Data
```bash
python automation/content_calendar_notifier.py
```

### Step 3: Run with a Custom or Simulated Date
To test deadline alerts against a specific point in time (for example, mid-month evaluation):
```bash
python automation/content_calendar_notifier.py --date 2026-10-15 --days 3
```

### Step 4: Inspect Generated Deliverables
After running, verify the generated files:
- Markdown Executive Digest: `automation/notification-digest.md`
- JSON Audit Log: `automation/notification-audit.json`

---

## 2. Scheduling Daily Automations (Free-Tier & Local)

### Option A: Windows Task Scheduler (Local Automated Run)
To run the draft reminder automatically every morning at 09:00 AM on Windows:

1. Open **Windows PowerShell** as Administrator.
2. Register a scheduled task pointing to your Python interpreter and the notifier script:
```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" `
  -Argument "C:\Users\yohes\OneDrive\Desktop\44\capstone-62\automation\content_calendar_notifier.py" `
  -WorkingDirectory "C:\Users\yohes\OneDrive\Desktop\44\capstone-62"

$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM

Register-ScheduledTask -TaskName "CAPSTONE62_ContentNotifier" -Action $action -Trigger $trigger -Description "Daily Content Calendar Reminder"
```
3. The script will execute automatically in the background and update `notification-digest.md` daily.

---

### Option B: Linux / macOS Cron Job
On Unix systems, add a daily cron entry:
```bash
# Open crontab editor
crontab -e

# Run every weekday at 09:00 AM
0 9 * * 1-5 cd /path/to/capstone-62 && python3 automation/content_calendar_notifier.py >> automation/cron.log 2>&1
```

---

## 3. Notion & Cloud Integration Setup (Optional Free Tier)
If your team manages content planning in Notion or Google Sheets, you can synchronize the calendar into this workflow.

### Notion Database Schema Mapping:
Create a Notion Database named **"Technical Content Calendar"** with properties matching our schema:
- `Title` -> Title property
- `Topic` -> Select property
- `Planned Date` -> Date property
- `Status` -> Status property (`Idea`, `Drafting`, `In Review`, `Ready for Publish`, `Published`)
- `Verification Status` -> Select property (`Pending Verification`, `Action Needed`, `Verified`)
- `Author` -> Person / Text property
- `Reviewer` -> Person / Text property

### Secure API Synchronization (Make.com or Notion SDK):
If using Make.com or a Python webhook:
1. Create a Notion Internal Integration at [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations).
2. Store your token safely in an environment variable:
   ```bash
   # Windows PowerShell
   $env:NOTION_API_KEY = "secret_your_token_here"
   
   # Linux / macOS
   export NOTION_API_KEY="secret_your_token_here"
   ```
3. **NEVER** commit API keys or passwords to Git. Always include `.env` in your `.gitignore` file.
4. Export the database to CSV or use the Notion API to dump records to `automation/sample-data.csv` prior to running `content_calendar_notifier.py`.

---

## 4. Human-in-the-Loop Approval Protocol
The automation engine strictly enforces the **Human-in-the-Loop** policy:
1. The script will **never** automatically change a status to `Published`.
2. A human author and faculty reviewer must physically complete the **Technical-Writing Quality Checklist** (`checklist/technical-writing-checklist.md`).
3. Only after the code is tested and the checklist signed off may a post be deployed to a public platform.
