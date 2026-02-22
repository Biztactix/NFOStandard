#!/usr/bin/env python3
"""
Test: README includes local validation instructions.

Verifies acceptance criterion for US-NFO-9:
  "README includes local validation instructions"

Checks that the README.md file contains a section describing
how to run schema validation locally.
"""

import os
import re

import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
README_PATH = os.path.join(REPO_ROOT, "README.md")


def read_readme():
    """Read the README.md content."""
    with open(README_PATH) as f:
        return f.read()


def test_readme_exists():
    """README.md must exist in the repository root."""
    assert os.path.isfile(README_PATH), "README.md not found in repository root"


def test_readme_has_validation_section():
    """README must contain a section about validation."""
    content = read_readme()
    # Look for a heading that mentions validation
    has_validation_heading = bool(
        re.search(r"^#+\s+.*[Vv]alidat", content, re.MULTILINE)
    )
    assert has_validation_heading, (
        "README.md must contain a section heading about validation "
        "(e.g., '## Validation', '## Local Validation', '## Schema Validation')"
    )


def test_readme_mentions_running_validation_locally():
    """README must describe how to run validation locally."""
    content = read_readme().lower()
    # Must mention running/executing validation or tests locally
    has_local_instructions = any(
        term in content
        for term in [
            "run validation",
            "validate locally",
            "local validation",
            "run the tests",
            "run tests",
            "pytest",
            "python -m pytest",
        ]
    )
    assert has_local_instructions, (
        "README.md must include instructions for running validation locally "
        "(e.g., mentioning pytest, how to run tests, or how to validate schemas)"
    )


def test_readme_mentions_dependencies():
    """README must mention required dependencies for local validation."""
    content = read_readme().lower()
    has_dependency_info = any(
        term in content
        for term in [
            "pip install",
            "requirements",
            "lxml",
            "dependencies",
        ]
    )
    assert has_dependency_info, (
        "README.md must mention the dependencies needed for local validation "
        "(e.g., pip install, requirements file, or lxml)"
    )
