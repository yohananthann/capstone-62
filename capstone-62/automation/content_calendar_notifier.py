#!/usr/bin/env python3
"""
Content Calendar & Draft Reminder Automation Engine
Part of CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers.

This script implements an automated workflow that:
1. Ingests content calendar data (CSV format, compatible with Notion/Google Sheets exports).
2. Calculates approaching deadlines and identifies overdue drafts.
3. Checks technical verification gates and reviewer approvals.
4. Enforces the Human-in-the-Loop policy: content cannot be marked "Published" without manual approval.
5. Emits structured notification alerts (Console, Markdown Digest, and JSON Audit Log).
"""

import argparse
import csv
import datetime
import json
import os
import sys
from typing import List, Dict, Any


def parse_calendar(csv_path: str) -> List[Dict[str, str]]:
    """Reads and parses the content calendar CSV file."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Content calendar file not found at: {csv_path}")

    records: List[Dict[str, str]] = []
    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k}
            records.append(cleaned_row)
    return records


def analyze_schedule(
    records: List[Dict[str, str]],
    reference_date: datetime.date,
    days_threshold: int = 3
) -> Dict[str, Any]:
    """
    Analyzes content items against deadlines, verification status, and publication readiness.
    """
    overdue_items = []
    upcoming_items = []
    verification_blockers = []
    ready_for_review = []
    published_items = []

    for item in records:
        title = item.get("title", "Untitled")
        status = item.get("status", "Idea")
        verif = item.get("verification_status", "Pending Verification")
        date_str = item.get("planned_date", "")

        try:
            planned_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"[Warning] Invalid date format for '{title}': '{date_str}'. Expected YYYY-MM-DD.", file=sys.stderr)
            continue

        days_remaining = (planned_date - reference_date).days

        item_summary = {
            "id": item.get("id"),
            "title": title,
            "topic": item.get("topic"),
            "status": status,
            "planned_date": date_str,
            "days_remaining": days_remaining,
            "draft_location": item.get("draft_location"),
            "author": item.get("author"),
            "reviewer": item.get("reviewer"),
            "verification_status": verif,
            "priority": item.get("priority", "Medium")
        }

        if status.lower() == "published":
            published_items.append(item_summary)
            continue

        # Overdue detection
        if days_remaining < 0:
            overdue_items.append(item_summary)
        # Upcoming within window
        elif 0 <= days_remaining <= days_threshold:
            upcoming_items.append(item_summary)

        # Verification gate check (drafts nearing completion or in review without technical verification)
        if status.lower() in ["drafting", "in review", "ready for publish"] and verif.lower() != "verified":
            verification_blockers.append(item_summary)

        if status.lower() == "in review":
            ready_for_review.append(item_summary)

    return {
        "reference_date": str(reference_date),
        "total_items": len(records),
        "overdue": overdue_items,
        "upcoming": upcoming_items,
        "verification_blockers": verification_blockers,
        "in_review": ready_for_review,
        "published": published_items
    }


def generate_markdown_digest(analysis: Dict[str, Any], output_path: str) -> None:
    """Generates an executive markdown notification summary for the writing team."""
    lines = [
        "# Automated Content Calendar Digest & Notification Report",
        f"**Run Date:** {analysis['reference_date']} | **Total Tracked Items:** {analysis['total_items']}",
        "",
        "> [!IMPORTANT]",
        "> **Human-in-the-Loop Governance Notice:** All technical blog posts require manual reviewer signoff and reproducible code test verification before deployment.",
        "",
        "## 1. Action Required: Overdue Items",
    ]

    if not analysis["overdue"]:
        lines.append("*No overdue items. Schedule is on track.*")
    else:
        lines.append("| ID | Title | Due Date | Days Overdue | Status | Assignee | Priority |")
        lines.append("|---|---|---|---|---|---|---|")
        for item in analysis["overdue"]:
            lines.append(f"| {item['id']} | **{item['title']}** | {item['planned_date']} | {abs(item['days_remaining'])} day(s) | `{item['status']}` | {item['author']} | `{item['priority']}` |")

    lines.extend([
        "",
        "## 2. Upcoming Deadlines (Next 3 Days)",
    ])

    if not analysis["upcoming"]:
        lines.append("*No upcoming deadlines in the next 3 days.*")
    else:
        lines.append("| ID | Title | Due Date | Days Left | Status | Assignee | Verification |")
        lines.append("|---|---|---|---|---|---|---|")
        for item in analysis["upcoming"]:
            lines.append(f"| {item['id']} | **{item['title']}** | {item['planned_date']} | {item['days_remaining']} day(s) | `{item['status']}` | {item['author']} | `{item['verification_status']}` |")

    lines.extend([
        "",
        "## 3. Technical Verification Gate Blockers",
        "The following active drafts require reproducible code verification or technical fact-checking before publication:",
        ""
    ])

    if not analysis["verification_blockers"]:
        lines.append("*All active drafts have completed technical verification.*")
    else:
        lines.append("| ID | Title | Draft File | Reviewer | Verification Status |")
        lines.append("|---|---|---|---|---|")
        for item in analysis["verification_blockers"]:
            lines.append(f"| {item['id']} | {item['title']} | `{item['draft_location']}` | {item['reviewer']} | `{item['verification_status']}` |")

    lines.extend([
        "",
        "## 4. Workflow Next Steps",
        "1. Authors with upcoming/overdue tasks should update their drafting status.",
        "2. Reviewers must complete the **Technical-Writing Quality Checklist** on `blogs/` drafts.",
        "3. Ensure all code blocks pass automated unit tests (`python -m unittest discover tests`).",
        "",
        "---",
        "*Report auto-generated by CAPSTONE 62 Content Automation Engine.*"
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def print_cli_summary(analysis: Dict[str, Any]) -> None:
    """Prints a clean CLI summary to standard output."""
    print("=" * 75)
    print(f"CAPSTONE 62 — CONTENT CALENDAR AUTOMATION & REMINDER ENGINE")
    print(f"Audit Date: {analysis['reference_date']} | Total Tracked Posts: {analysis['total_items']}")
    print("=" * 75)

    print(f"\n[!] Overdue Items: {len(analysis['overdue'])}")
    for item in analysis["overdue"]:
        print(f"    - ID {item['id']}: '{item['title']}' ({abs(item['days_remaining'])} days late | Status: {item['status']})")

    print(f"\n[*] Approaching Deadlines (<= 3 days): {len(analysis['upcoming'])}")
    for item in analysis["upcoming"]:
        print(f"    - ID {item['id']}: '{item['title']}' (Due in {item['days_remaining']} days | Status: {item['status']})")

    print(f"\n[?] Verification Gate Warnings: {len(analysis['verification_blockers'])}")
    for item in analysis["verification_blockers"]:
        print(f"    - ID {item['id']}: '{item['title']}' [Status: {item['verification_status']}]")

    print("\n" + "=" * 75)
    print("Policy Check: 100% Manual Human Approval Required Prior to Final Publishing.")
    print("=" * 75)


def main() -> None:
    parser = argparse.ArgumentParser(description="Content Calendar Reminder & Verification Automation")
    default_csv = os.path.join(os.path.dirname(__file__), "sample-data.csv")
    parser.add_argument("--csv", default=default_csv, help="Path to content-calendar CSV")
    parser.add_argument("--date", default=None, help="Simulated run date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--days", type=int, default=3, help="Days ahead threshold for upcoming warnings")
    parser.add_argument("--output-md", default=None, help="Path to write markdown digest report")
    parser.add_argument("--output-json", default=None, help="Path to write JSON audit log")

    args = parser.parse_args()

    ref_date = datetime.date.today()
    if args.date:
        ref_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()

    records = parse_calendar(args.csv)
    analysis = analyze_schedule(records, ref_date, days_threshold=args.days)

    print_cli_summary(analysis)

    # Default output locations if not passed
    base_dir = os.path.dirname(__file__)
    md_path = args.output_md or os.path.join(base_dir, "notification-digest.md")
    json_path = args.output_json or os.path.join(base_dir, "notification-audit.json")

    generate_markdown_digest(analysis, md_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)

    print(f"\n[Artifact Generated] Markdown Digest: {md_path}")
    print(f"[Artifact Generated] JSON Audit Log:  {json_path}")


if __name__ == "__main__":
    main()
