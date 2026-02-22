#!/usr/bin/env python3
"""
Test: Example XML files exist for all 9 content types.

Verifies acceptance criterion for US-NFO-7:
  "Example XML files exist for all 9 content types"
"""

import glob
import os
import xml.etree.ElementTree as ET

import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
NS = "NFOStandard"

CONTENT_TYPES = [
    "movie",
    "tvshow",
    "adult",
    "anime",
    "video",
    "music",
    "audiobook",
    "podcast",
    "musicvideo",
]


def find_example_for_type(content_type):
    """Find an example XML file whose <media> child matches the content type."""
    xml_files = glob.glob(os.path.join(REPO_ROOT, "*.xml"))
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            media = root.find(f"{{{NS}}}media")
            if media is not None and media.find(f"{{{NS}}}{content_type}") is not None:
                return xml_file
        except ET.ParseError:
            continue
    return None


@pytest.mark.parametrize("content_type", CONTENT_TYPES)
def test_example_xml_exists(content_type):
    match = find_example_for_type(content_type)
    assert match is not None, (
        f"No example XML file found for content type '{content_type}'. "
        f"Expected an XML file in the repo root with <media><{content_type}>...</{content_type}></media>"
    )
