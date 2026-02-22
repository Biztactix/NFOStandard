#!/usr/bin/env python3
"""
Test: Usage guidelines section included.

Verifies acceptance criterion for US-NFO-8:
  "Usage guidelines section included"
"""

import os
import re

import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SPEC_PATH = os.path.join(REPO_ROOT, "SPECIFICATION.md")

# Expected subsections under Usage Guidelines
EXPECTED_SUBSECTIONS = [
    "General Principles",
    "Identifiers",
    "Ratings",
    "Media Assets",
    "People",
    "Library and Stats Sections",
    "Dates",
    "Extensibility",
]


@pytest.fixture(scope="module")
def spec_content():
    assert os.path.isfile(SPEC_PATH), f"SPECIFICATION.md not found at {SPEC_PATH}"
    with open(SPEC_PATH, encoding="utf-8") as f:
        return f.read()


def extract_section(spec_text, heading, level=3):
    """Extract text under a heading up to the next same-level or higher heading."""
    hashes = "#" * level
    pattern = rf"^{hashes}\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, spec_text, re.MULTILINE)
    if not match:
        return None
    start = match.end()
    next_heading = re.search(rf"^#{{1,{level}}}\s+", spec_text[start:], re.MULTILINE)
    if next_heading:
        return spec_text[start : start + next_heading.start()]
    return spec_text[start:]


def test_usage_guidelines_section_exists(spec_content):
    """SPECIFICATION.md must have a 'Usage Guidelines' section."""
    assert re.search(r"^##\s+Usage Guidelines", spec_content, re.MULTILINE), (
        "SPECIFICATION.md is missing a '## Usage Guidelines' section"
    )


def test_usage_guidelines_in_toc(spec_content):
    """Table of Contents must link to Usage Guidelines."""
    assert "Usage Guidelines" in spec_content.split("---")[0], (
        "Usage Guidelines is not listed in the Table of Contents"
    )


@pytest.mark.parametrize("subsection", EXPECTED_SUBSECTIONS)
def test_usage_guideline_subsection_exists(spec_content, subsection):
    """Each expected usage guideline topic must have its own ### subsection."""
    section = extract_section(spec_content, subsection)
    assert section is not None, (
        f"Usage Guidelines is missing a '### {subsection}' subsection"
    )


@pytest.mark.parametrize("subsection", EXPECTED_SUBSECTIONS)
def test_usage_guideline_subsection_has_content(spec_content, subsection):
    """Each usage guideline subsection must have substantive content (>50 chars)."""
    section = extract_section(spec_content, subsection)
    assert section is not None, (
        f"Cannot check content: '### {subsection}' section not found"
    )
    text = section.strip()
    assert len(text) > 50, (
        f"Subsection '### {subsection}' has too little content ({len(text)} chars)"
    )
