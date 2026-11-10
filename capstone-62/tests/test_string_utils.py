#!/usr/bin/env python3
"""
Unit Tests for Blog String Utilities
Part of CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers.
Post 3 Companion Tests: Demonstrates testing pure functions with unittest.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code")))

from string_utils import (
    slugify,
    count_words,
    calculate_reading_time,
    truncate_summary,
)


class TestStringUtils(unittest.TestCase):
    def test_slugify_standard(self):
        """Verify normal title slug generation."""
        self.assertEqual(slugify("Build Your First Python CLI Application!"), "build-your-first-python-cli-application")
        self.assertEqual(slugify("Five Common Python Errors & Solutions"), "five-common-python-errors-solutions")

    def test_slugify_special_characters(self):
        """Verify handling of punctuation, special symbols, and extra spaces."""
        self.assertEqual(slugify("  Hello, World! 100% Guaranteed?? "), "hello-world-100-guaranteed")
        self.assertEqual(slugify("Python 3.12: Features & Improvements"), "python-3-12-features-improvements")

    def test_slugify_invalid_inputs(self):
        """Verify appropriate exceptions for invalid slugify inputs."""
        with self.assertRaises(ValueError):
            slugify("")
        with self.assertRaises(ValueError):
            slugify("   ")
        with self.assertRaises(ValueError):
            slugify("!@#$%^&*()")
        with self.assertRaises(TypeError):
            slugify(12345)  # type: ignore

    def test_count_words(self):
        """Verify word counting accuracy."""
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("   "), 0)
        self.assertEqual(count_words("Python is an awesome programming language."), 6)
        self.assertEqual(count_words("Line one\nLine two\tLine three"), 6)

    def test_calculate_reading_time(self):
        """Verify reading time calculation at standard 200 WPM."""
        self.assertEqual(calculate_reading_time(""), 0)
        # 50 words should ceil to 1 minute
        text_50_words = "word " * 50
        self.assertEqual(calculate_reading_time(text_50_words), 1)
        # 250 words should ceil to 2 minutes
        text_250_words = "word " * 250
        self.assertEqual(calculate_reading_time(text_250_words), 2)
        # 1,000 words should ceil to 5 minutes
        text_1000_words = "word " * 1000
        self.assertEqual(calculate_reading_time(text_1000_words), 5)

    def test_calculate_reading_time_invalid_wpm(self):
        """Verify rejection of zero or negative words_per_minute."""
        with self.assertRaises(ValueError):
            calculate_reading_time("Some text", words_per_minute=0)
        with self.assertRaises(ValueError):
            calculate_reading_time("Some text", words_per_minute=-50)

    def test_truncate_summary(self):
        """Verify text truncation with custom word limits and suffixes."""
        short_text = "Python makes developer automation simple and reliable."
        self.assertEqual(truncate_summary(short_text, max_words=10), short_text)

        long_text = "One two three four five six seven eight nine ten eleven twelve"
        truncated = truncate_summary(long_text, max_words=5, suffix="...")
        self.assertEqual(truncated, "One two three four five...")

    def test_truncate_summary_invalid(self):
        """Verify error handling on invalid max_words."""
        with self.assertRaises(ValueError):
            truncate_summary("Test text", max_words=0)


if __name__ == "__main__":
    unittest.main()
