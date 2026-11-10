#!/usr/bin/env python3
"""
Unit Tests for CLI Task Manager
Part of CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers.

Tests verify:
- Adding tasks with default and custom priorities.
- Rejection of empty titles and invalid priorities.
- Sequential ID assignment.
- Listing tasks with and without filters.
- Completing tasks (existing, already completed, non-existent).
- Deleting tasks (existing, non-existent, negative IDs).
- Clearing tasks and handling corrupted JSON files.
"""

import json
import os
import tempfile
import unittest
import sys

# Ensure code directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code")))

from task_manager import (
    load_tasks,
    save_tasks,
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    clear_tasks,
    get_next_id,
)


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """Create a temporary file for isolated test state."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_file.close()
        self.test_filepath = self.temp_file.name
        # Initialize with empty list
        save_tasks([], self.test_filepath)

    def tearDown(self):
        """Clean up temporary test file."""
        if os.path.exists(self.test_filepath):
            try:
                os.remove(self.test_filepath)
            except OSError:
                pass

    def test_add_task_success(self):
        """Verify successful addition of a task with valid title and priority."""
        task = add_task("Finish CAPSTONE 62 Deliverables", priority="high", filepath=self.test_filepath)
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Finish CAPSTONE 62 Deliverables")
        self.assertEqual(task["priority"], "high")
        self.assertFalse(task["completed"])

        tasks = load_tasks(self.test_filepath)
        self.assertEqual(len(tasks), 1)

    def test_add_task_empty_title_rejected(self):
        """Verify that empty or whitespace-only task titles are rejected."""
        result = add_task("   ", priority="low", filepath=self.test_filepath)
        self.assertIsNone(result)
        tasks = load_tasks(self.test_filepath)
        self.assertEqual(len(tasks), 0)

    def test_add_task_invalid_priority_rejected(self):
        """Verify that invalid priority strings are rejected."""
        result = add_task("Valid Title", priority="urgent", filepath=self.test_filepath)
        self.assertIsNone(result)
        tasks = load_tasks(self.test_filepath)
        self.assertEqual(len(tasks), 0)

    def test_id_increments_sequentially(self):
        """Verify that sequential IDs are allocated correctly."""
        t1 = add_task("Task One", filepath=self.test_filepath)
        t2 = add_task("Task Two", filepath=self.test_filepath)
        t3 = add_task("Task Three", filepath=self.test_filepath)
        self.assertEqual(t1["id"], 1)
        self.assertEqual(t2["id"], 2)
        self.assertEqual(t3["id"], 3)

    def test_list_tasks_filtering(self):
        """Verify filtering by pending and completed statuses."""
        add_task("Pending Task", filepath=self.test_filepath)
        t2 = add_task("Done Task", filepath=self.test_filepath)
        complete_task(t2["id"], filepath=self.test_filepath)

        all_tasks = list_tasks(filepath=self.test_filepath)
        self.assertEqual(len(all_tasks), 2)

        pending_tasks = list_tasks(status_filter="pending", filepath=self.test_filepath)
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0]["title"], "Pending Task")

        completed_tasks = list_tasks(status_filter="completed", filepath=self.test_filepath)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0]["title"], "Done Task")

    def test_complete_task_lifecycle(self):
        """Verify completing existing tasks, idempotent completion, and missing IDs."""
        task = add_task("Write unit test", filepath=self.test_filepath)
        task_id = task["id"]

        # Complete task
        self.assertTrue(complete_task(task_id, filepath=self.test_filepath))
        updated = load_tasks(self.test_filepath)[0]
        self.assertTrue(updated["completed"])

        # Idempotent completion
        self.assertTrue(complete_task(task_id, filepath=self.test_filepath))

        # Non-existent task
        self.assertFalse(complete_task(999, filepath=self.test_filepath))

        # Invalid ID (negative)
        self.assertFalse(complete_task(-5, filepath=self.test_filepath))

    def test_delete_task(self):
        """Verify task deletion and handling of invalid IDs."""
        t1 = add_task("Keep this", filepath=self.test_filepath)
        t2 = add_task("Delete this", filepath=self.test_filepath)

        # Delete existing task
        self.assertTrue(delete_task(t2["id"], filepath=self.test_filepath))
        remaining = load_tasks(self.test_filepath)
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0]["id"], t1["id"])

        # Delete non-existent ID
        self.assertFalse(delete_task(999, filepath=self.test_filepath))

        # Delete invalid zero/negative ID
        self.assertFalse(delete_task(0, filepath=self.test_filepath))

    def test_clear_tasks(self):
        """Verify clearing all tasks."""
        add_task("T1", filepath=self.test_filepath)
        add_task("T2", filepath=self.test_filepath)
        self.assertTrue(clear_tasks(filepath=self.test_filepath))
        self.assertEqual(len(load_tasks(self.test_filepath)), 0)

    def test_corrupted_json_recovery(self):
        """Verify that corrupted JSON file is safely caught without crashing."""
        with open(self.test_filepath, "w", encoding="utf-8") as f:
            f.write("{ invalid json formatting !!!")

        tasks = load_tasks(self.test_filepath)
        self.assertEqual(tasks, [])


if __name__ == "__main__":
    unittest.main()
