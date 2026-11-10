#!/usr/bin/env python3
"""
CLI Task Manager
Part of CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers.
Demonstrates practical Python standard library CLI development with robust
argument parsing, JSON persistence, input validation, and user feedback.

Author: CSE Student Developer
License: MIT
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Any, Optional

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks(filepath: str = DEFAULT_DATA_FILE) -> List[Dict[str, Any]]:
    """
    Safely load task records from a JSON file.
    If the file does not exist, return an empty list.
    If the file contains invalid JSON, handle the error gracefully.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"[Warning] Could not read tasks file ({e}). Starting with empty list.", file=sys.stderr)
        return []


def save_tasks(tasks: List[Dict[str, Any]], filepath: str = DEFAULT_DATA_FILE) -> bool:
    """
    Persist the list of tasks to disk formatted with indentation.
    Returns True upon success, False upon file write error.
    """
    try:
        # Ensure parent directory exists
        parent_dir = os.path.dirname(os.path.abspath(filepath))
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        return True
    except OSError as e:
        print(f"[Error] Failed to save tasks to '{filepath}': {e}", file=sys.stderr)
        return False


def get_next_id(tasks: List[Dict[str, Any]]) -> int:
    """Calculate the next sequential integer ID for a new task."""
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1


def add_task(title: str, priority: str = "medium", filepath: str = DEFAULT_DATA_FILE) -> Optional[Dict[str, Any]]:
    """
    Validate input and append a new task to storage.
    Returns the created task dictionary or None on validation failure.
    """
    cleaned_title = title.strip()
    if not cleaned_title:
        print("[Error] Task title cannot be empty.", file=sys.stderr)
        return None

    valid_priorities = {"low", "medium", "high"}
    normalized_priority = priority.lower().strip()
    if normalized_priority not in valid_priorities:
        print(f"[Error] Invalid priority '{priority}'. Choose from: low, medium, high.", file=sys.stderr)
        return None

    tasks = load_tasks(filepath)
    new_task = {
        "id": get_next_id(tasks),
        "title": cleaned_title,
        "priority": normalized_priority,
        "completed": False
    }
    tasks.append(new_task)
    if save_tasks(tasks, filepath):
        print(f"Task #{new_task['id']} added: \"{new_task['title']}\" [{new_task['priority']}]")
        return new_task
    return None


def list_tasks(status_filter: Optional[str] = None, filepath: str = DEFAULT_DATA_FILE) -> List[Dict[str, Any]]:
    """
    Display a formatted table of all or filtered tasks.
    Returns the list of displayed tasks.
    """
    tasks = load_tasks(filepath)

    if status_filter == "pending":
        tasks = [t for t in tasks if not t.get("completed", False)]
    elif status_filter == "completed":
        tasks = [t for t in tasks if t.get("completed", False)]

    if not tasks:
        msg = f"No {status_filter or ''} tasks found."
        print(msg.strip())
        return []

    print("-" * 65)
    print(f"{'ID':<4} | {'Status':<10} | {'Priority':<8} | {'Title'}")
    print("-" * 65)
    for t in tasks:
        status_symbol = "[X] Done" if t.get("completed") else "[ ] Pending"
        print(f"{t.get('id', 0):<4} | {status_symbol:<10} | {t.get('priority', 'medium').capitalize():<8} | {t.get('title', '')}")
    print("-" * 65)
    return tasks


def complete_task(task_id: int, filepath: str = DEFAULT_DATA_FILE) -> bool:
    """
    Mark an existing task as completed by ID.
    Returns True if task was found and updated, False otherwise.
    """
    if task_id <= 0:
        print("[Error] Task ID must be a positive integer.", file=sys.stderr)
        return False

    tasks = load_tasks(filepath)
    for task in tasks:
        if task.get("id") == task_id:
            if task.get("completed"):
                print(f"Task #{task_id} is already completed.")
                return True
            task["completed"] = True
            save_tasks(tasks, filepath)
            print(f"Task #{task_id} marked as completed.")
            return True

    print(f"[Error] Task #{task_id} not found.", file=sys.stderr)
    return False


def delete_task(task_id: int, filepath: str = DEFAULT_DATA_FILE) -> bool:
    """
    Remove a task by ID.
    Returns True if task was deleted, False otherwise.
    """
    if task_id <= 0:
        print("[Error] Task ID must be a positive integer.", file=sys.stderr)
        return False

    tasks = load_tasks(filepath)
    initial_len = len(tasks)
    remaining_tasks = [t for t in tasks if t.get("id") != task_id]

    if len(remaining_tasks) == initial_len:
        print(f"[Error] Task #{task_id} not found.", file=sys.stderr)
        return False

    save_tasks(remaining_tasks, filepath)
    print(f"Task #{task_id} deleted successfully.")
    return True


def clear_tasks(filepath: str = DEFAULT_DATA_FILE) -> bool:
    """Wipe all tasks from the storage file."""
    if save_tasks([], filepath):
        print("All tasks have been cleared.")
        return True
    return False


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="task_manager",
        description="CLI Task Manager: Organize and track your developer tasks locally."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("title", type=str, help="Description of the task")
    parser_add.add_argument(
        "-p", "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority level (default: medium)"
    )

    # List command
    parser_list = subparsers.add_parser("list", help="List all tasks")
    parser_list.add_argument(
        "--status",
        choices=["pending", "completed"],
        default=None,
        help="Filter tasks by completion status"
    )

    # Complete command
    parser_complete = subparsers.add_parser("complete", help="Mark a task as completed")
    parser_complete.add_argument("id", type=int, help="ID of the task to complete")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a task by ID")
    parser_delete.add_argument("id", type=int, help="ID of the task to delete")

    # Clear command
    subparsers.add_parser("clear", help="Clear all stored tasks")

    return parser


def main() -> None:
    """Entry point for CLI execution."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "add":
        success = add_task(args.title, args.priority)
        sys.exit(0 if success else 1)
    elif args.command == "list":
        list_tasks(status_filter=args.status)
        sys.exit(0)
    elif args.command == "complete":
        success = complete_task(args.id)
        sys.exit(0 if success else 1)
    elif args.command == "delete":
        success = delete_task(args.id)
        sys.exit(0 if success else 1)
    elif args.command == "clear":
        success = clear_tasks()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
