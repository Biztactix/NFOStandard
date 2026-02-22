#!/usr/bin/env python3
"""
Test: Each content type has its own section with field table.

Verifies acceptance criterion for US-NFO-8:
  "Each content type has its own section with field table"
"""

import os
import re

import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SPEC_PATH = os.path.join(REPO_ROOT, "SPECIFICATION.md")

# The 9 content types and their expected section headings in the spec
CONTENT_TYPE_SECTIONS = {
    "movie": "Movie",
    "tvshow": "TV Show",
    "anime": "Anime",
    "adult": "Adult",
    "video": "Video",
    "music": "Music",
    "musicvideo": "Music Video",
    "audiobook": "Audiobook",
    "podcast": "Podcast",
}


@pytest.fixture(scope="module")
def spec_content():
    assert os.path.isfile(SPEC_PATH), f"SPECIFICATION.md not found at {SPEC_PATH}"
    with open(SPEC_PATH, encoding="utf-8") as f:
        return f.read()


def extract_section(spec_text, heading):
    """Extract the text under a heading (### level) up to the next same-level or higher heading."""
    pattern = rf"^###\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, spec_text, re.MULTILINE)
    if not match:
        return None
    start = match.end()
    # Find the next heading at level ### or higher (##, #)
    next_heading = re.search(r"^#{1,3}\s+", spec_text[start:], re.MULTILINE)
    if next_heading:
        return spec_text[start : start + next_heading.start()]
    return spec_text[start:]


@pytest.mark.parametrize(
    "content_type,heading",
    list(CONTENT_TYPE_SECTIONS.items()),
    ids=list(CONTENT_TYPE_SECTIONS.keys()),
)
def test_content_type_has_section(spec_content, content_type, heading):
    """Each content type must have its own ### section in SPECIFICATION.md."""
    section = extract_section(spec_content, heading)
    assert section is not None, (
        f"SPECIFICATION.md is missing a '### {heading}' section for content type '{content_type}'"
    )


@pytest.mark.parametrize(
    "content_type,heading",
    list(CONTENT_TYPE_SECTIONS.items()),
    ids=list(CONTENT_TYPE_SECTIONS.keys()),
)
def test_content_type_has_field_table(spec_content, content_type, heading):
    """Each content type section must contain a markdown field table."""
    section = extract_section(spec_content, heading)
    assert section is not None, (
        f"Cannot check field table: '### {heading}' section not found"
    )
    # A markdown table has a header row and a separator row like |---|---|
    has_table = bool(re.search(r"\|.*\|.*\|\n\|[-\s|:]+\|", section))
    assert has_table, (
        f"Section '### {heading}' for content type '{content_type}' does not contain a markdown field table"
    )


@pytest.mark.parametrize(
    "content_type,heading",
    list(CONTENT_TYPE_SECTIONS.items()),
    ids=list(CONTENT_TYPE_SECTIONS.keys()),
)
def test_field_table_has_required_columns(spec_content, content_type, heading):
    """Each field table should have standard columns (Element/Attribute, Type, Description)."""
    section = extract_section(spec_content, heading)
    assert section is not None, (
        f"Cannot check columns: '### {heading}' section not found"
    )
    # Find the first table header row
    table_match = re.search(r"^\|(.+)\|$", section, re.MULTILINE)
    assert table_match, (
        f"No table header found in '### {heading}' section"
    )
    header = table_match.group(1).lower()
    # Must have a "type" and "description" column at minimum
    assert "type" in header, (
        f"Field table in '### {heading}' is missing a 'Type' column"
    )
    assert "description" in header, (
        f"Field table in '### {heading}' is missing a 'Description' column"
    )
