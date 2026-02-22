#!/usr/bin/env python3
"""
Test: Shared types (common.xsd / person.xsd) documented.

Verifies acceptance criterion for US-NFO-8:
  "Shared types (common.xsd / person.xsd) documented"
"""

import os
import re

import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SPEC_PATH = os.path.join(REPO_ROOT, "SPECIFICATION.md")

# Types defined in common.xsd
COMMON_TYPES = [
    "ratingType",
    "uniqueidType",
    "contentRatingType",
    "serviceLinksType",
    "subMediaType",
]

# Types defined in person.xsd
PERSON_TYPES = [
    "personType",
]

ALL_SHARED_TYPES = COMMON_TYPES + PERSON_TYPES


@pytest.fixture(scope="module")
def spec_content():
    assert os.path.isfile(SPEC_PATH), f"SPECIFICATION.md not found at {SPEC_PATH}"
    with open(SPEC_PATH, encoding="utf-8") as f:
        return f.read()


def extract_section(spec_text, heading):
    """Extract text under a ### heading up to the next same-level or higher heading."""
    pattern = rf"^###\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, spec_text, re.MULTILINE)
    if not match:
        return None
    start = match.end()
    next_heading = re.search(r"^#{1,3}\s+", spec_text[start:], re.MULTILINE)
    if next_heading:
        return spec_text[start : start + next_heading.start()]
    return spec_text[start:]


def test_shared_types_section_exists(spec_content):
    """SPECIFICATION.md must have a 'Shared Types' section."""
    assert re.search(r"^##\s+Shared Types", spec_content, re.MULTILINE), (
        "SPECIFICATION.md is missing a '## Shared Types' section"
    )


def test_shared_types_mentions_source_files(spec_content):
    """The Shared Types section should reference common.xsd and person.xsd."""
    assert "common.xsd" in spec_content, (
        "SPECIFICATION.md does not mention 'common.xsd'"
    )
    assert "person.xsd" in spec_content, (
        "SPECIFICATION.md does not mention 'person.xsd'"
    )


@pytest.mark.parametrize("type_name", ALL_SHARED_TYPES)
def test_shared_type_has_subsection(spec_content, type_name):
    """Each shared type must have its own ### subsection."""
    section = extract_section(spec_content, type_name)
    assert section is not None, (
        f"SPECIFICATION.md is missing a '### {type_name}' subsection"
    )


@pytest.mark.parametrize("type_name", ALL_SHARED_TYPES)
def test_shared_type_has_table(spec_content, type_name):
    """Each shared type subsection must contain a markdown table."""
    section = extract_section(spec_content, type_name)
    assert section is not None, (
        f"Cannot check table: '### {type_name}' section not found"
    )
    has_table = bool(re.search(r"\|.*\|.*\|\n\|[-\s|:]+\|", section))
    assert has_table, (
        f"Section '### {type_name}' does not contain a markdown table"
    )


@pytest.mark.parametrize("type_name", ALL_SHARED_TYPES)
def test_shared_type_table_has_type_and_description(spec_content, type_name):
    """Each shared type table must have Type and Description columns."""
    section = extract_section(spec_content, type_name)
    assert section is not None, (
        f"Cannot check columns: '### {type_name}' section not found"
    )
    table_match = re.search(r"^\|(.+)\|$", section, re.MULTILINE)
    assert table_match, f"No table header found in '### {type_name}' section"
    header = table_match.group(1).lower()
    assert "type" in header, (
        f"Table in '### {type_name}' is missing a 'Type' column"
    )
    assert "description" in header, (
        f"Table in '### {type_name}' is missing a 'Description' column"
    )


@pytest.mark.parametrize("type_name", COMMON_TYPES)
def test_common_type_references_common_xsd(spec_content, type_name):
    """Types from common.xsd should indicate their source file."""
    section = extract_section(spec_content, type_name)
    assert section is not None, (
        f"Cannot check source ref: '### {type_name}' section not found"
    )
    assert "common.xsd" in section, (
        f"Section '### {type_name}' does not reference 'common.xsd' as its source"
    )


@pytest.mark.parametrize("type_name", PERSON_TYPES)
def test_person_type_references_person_xsd(spec_content, type_name):
    """Types from person.xsd should indicate their source file."""
    section = extract_section(spec_content, type_name)
    assert section is not None, (
        f"Cannot check source ref: '### {type_name}' section not found"
    )
    assert "person.xsd" in section, (
        f"Section '### {type_name}' does not reference 'person.xsd' as its source"
    )
