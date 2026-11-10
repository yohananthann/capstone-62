#!/usr/bin/env python3
"""
Python Common Errors & Debugging Demonstrations
Part of CAPSTONE 62: AI-Powered Technical Blog Writing Series for Developers.
Post 2 Companion Code: Explains SyntaxError, NameError, TypeError, IndexError, KeyError.

This module provides reproducible functions illustrating both the faulty code
(wrapped safely to capture the error) and the corrected implementation.
"""

from typing import Tuple, Any, Dict, List


def demonstrate_syntax_error() -> Dict[str, str]:
    """
    Demonstrates SyntaxError: Missing colon in an if-statement or unclosed parenthesis.
    Note: A raw SyntaxError prevents compilation, so we demonstrate it using eval()/compile()
    to safely capture and explain the traceback during runtime testing.
    """
    bad_code = "if 5 > 3\n    print('Greater')"
    error_msg = ""
    try:
        compile(bad_code, "<string>", "exec")
    except SyntaxError as e:
        error_msg = f"{type(e).__name__}: {e.msg} (line {e.lineno})"

    # Corrected code
    good_code = "if 5 > 3:\n    result = 'Greater'"
    compiled_good = compile(good_code, "<string>", "exec")
    local_scope: Dict[str, Any] = {}
    exec(compiled_good, {}, local_scope)

    return {
        "error_type": "SyntaxError",
        "cause": "Missing colon (:) at the end of the compound statement header.",
        "captured_error": error_msg,
        "correction": "Add a colon after the boolean expression: `if 5 > 3:`.",
        "result": local_scope.get("result", "")
    }


def demonstrate_name_error() -> Dict[str, str]:
    """
    Demonstrates NameError: Accessing a variable before definition or misspelled variable name.
    """
    error_msg = ""
    try:
        # Intentionally referencing an undefined variable 'counter'
        return_val = counter + 1  # type: ignore # noqa: F821
    except NameError as e:
        error_msg = f"{type(e).__name__}: {e}"

    # Corrected code: initialize before accessing
    counter = 0
    counter = counter + 1

    return {
        "error_type": "NameError",
        "cause": "Variable 'counter' referenced before assignment or misspelled.",
        "captured_error": error_msg,
        "correction": "Initialize `counter = 0` before reading or incrementing it.",
        "result": f"counter is {counter}"
    }


def demonstrate_type_error() -> Dict[str, str]:
    """
    Demonstrates TypeError: Attempting an unsupported operation between incompatible types (e.g. str + int).
    """
    error_msg = ""
    try:
        age_input = "21"
        next_year = age_input + 1  # type: ignore
    except TypeError as e:
        error_msg = f"{type(e).__name__}: {e}"

    # Corrected code: explicitly cast string to int
    age_input = "21"
    next_year = int(age_input) + 1

    return {
        "error_type": "TypeError",
        "cause": "Can only concatenate str (not 'int') to str, or unsupported operand + for str and int.",
        "captured_error": error_msg,
        "correction": "Cast the string representation to integer using `int(age_input)` before addition.",
        "result": f"next_year is {next_year}"
    }


def demonstrate_index_error() -> Dict[str, str]:
    """
    Demonstrates IndexError: Attempting to access an index out of bounds on a list.
    """
    error_msg = ""
    frameworks: List[str] = ["FastAPI", "Flask", "Django"]
    try:
        # Accessing index 3 when valid indices are 0, 1, 2
        selected = frameworks[3]
    except IndexError as e:
        error_msg = f"{type(e).__name__}: {e}"

    # Corrected code: verify boundary with len() or use safe retrieval
    target_idx = 3
    if 0 <= target_idx < len(frameworks):
        selected = frameworks[target_idx]
    else:
        selected = frameworks[-1]  # fallback or default

    return {
        "error_type": "IndexError",
        "cause": "List index out of range: list has 3 elements (indices 0..2), requested index 3.",
        "captured_error": error_msg,
        "correction": "Verify `0 <= index < len(lst)` or use list slicing/iteration.",
        "result": f"selected framework fallback: {selected}"
    }


def demonstrate_key_error() -> Dict[str, str]:
    """
    Demonstrates KeyError: Looking up a non-existent key in a dictionary using bracket notation.
    """
    error_msg = ""
    user_profile = {"username": "alex_dev", "role": "student"}
    try:
        email = user_profile["email"]
    except KeyError as e:
        error_msg = f"{type(e).__name__}: {e}"

    # Corrected code: use dict.get() with fallback or check key presence with `in`
    email_safe = user_profile.get("email", "no-email-provided@domain.com")

    return {
        "error_type": "KeyError",
        "cause": "Attempted to access non-existent dictionary key 'email' using square brackets.",
        "captured_error": error_msg,
        "correction": "Use `dict.get('email', default_value)` or `if 'email' in user_profile:` guard.",
        "result": f"email resolved to: {email_safe}"
    }


def run_all_demonstrations() -> None:
    """Execute and display all 5 error demonstrations."""
    demos = [
        demonstrate_syntax_error(),
        demonstrate_name_error(),
        demonstrate_type_error(),
        demonstrate_index_error(),
        demonstrate_key_error()
    ]
    print("=" * 70)
    print("CAPSTONE 62 — Python Common Errors & Debugging Demonstrations")
    print("=" * 70)
    for i, d in enumerate(demos, 1):
        print(f"\n[{i}] {d['error_type']}")
        print(f"    Cause:          {d['cause']}")
        print(f"    Captured Trace: {d['captured_error']}")
        print(f"    Correction:     {d['correction']}")
        print(f"    Result:         {d['result']}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_all_demonstrations()
