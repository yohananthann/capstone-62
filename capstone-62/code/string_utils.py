#!/usr/bin/env python3
"""
Blog String Utilities & Pure Functions
Part of CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers.
Post 3 Companion Code: Demonstrates writing modular, testable Python functions.

Functions include:
- slugify: converts blog titles into URL-safe slugs.
- calculate_reading_time: calculates estimated reading time in minutes.
- count_words: counts non-whitespace words in a markdown or text document.
- truncate_summary: generates an excerpt truncated at a maximum word count.
"""

import re
from typing import Optional


def slugify(title: str) -> str:
    """
    Convert a blog post title into a URL-friendly slug.

    Rules:
    - Convert to lowercase.
    - Replace non-alphanumeric characters with hyphens.
    - Remove consecutive hyphens and strip leading/trailing hyphens.

    Raises:
        ValueError: If title is empty or contains no alphanumeric characters.

    Examples:
        >>> slugify("Build Your First CLI App!")
        'build-your-first-cli-app'
    """
    if not isinstance(title, str):
        raise TypeError("Title must be a string.")

    cleaned = title.strip().lower()
    if not cleaned:
        raise ValueError("Title cannot be empty.")

    # Replace any non-alphanumeric character with hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", cleaned)
    # Strip leading and trailing hyphens
    slug = slug.strip("-")

    if not slug:
        raise ValueError(f"Title '{title}' does not contain any valid alphanumeric characters.")

    return slug


def count_words(text: str) -> int:
    """
    Count the number of words in a given text block.
    Splits on whitespace. Returns 0 for empty or whitespace-only strings.
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    words = text.split()
    return len(words)


def calculate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Calculate estimated reading time in minutes based on average reading speed.
    Always rounds up to at least 1 minute if there is content.
    Returns 0 if text is empty.
    """
    if words_per_minute <= 0:
        raise ValueError("words_per_minute must be greater than zero.")

    total_words = count_words(text)
    if total_words == 0:
        return 0

    minutes = (total_words + words_per_minute - 1) // words_per_minute  # ceiling division
    return max(1, minutes)


def truncate_summary(text: str, max_words: int = 30, suffix: str = "...") -> str:
    """
    Truncate text to a maximum word count, appending suffix if truncated.
    """
    if max_words <= 0:
        raise ValueError("max_words must be greater than zero.")

    words = text.split()
    if len(words) <= max_words:
        return " ".join(words)

    return " ".join(words[:max_words]) + suffix
