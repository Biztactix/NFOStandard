#!/usr/bin/env python3
"""
Test: video.xsd includes duration element.

Verifies acceptance criterion for US-NFO-5:
  "video.xsd includes duration element"
"""

import os
import xml.etree.ElementTree as ET

import pytest

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
VIDEO_XSD = os.path.join(SCHEMA_DIR, "video.xsd")


def get_video_elements():
    """Return dict of {element_name: type_name} from videoType sequence."""
    tree = ET.parse(VIDEO_XSD)
    root = tree.getroot()
    elements = {}
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "videoType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            name = elem.get("name", "")
            elem_type = elem.get("type", "")
            elements[name] = elem_type
    return elements


def get_video_element_attrs(field_name):
    """Return dict of XML attributes for a named element in videoType."""
    tree = ET.parse(VIDEO_XSD)
    root = tree.getroot()
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "videoType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            if elem.get("name") == field_name:
                return dict(elem.attrib)
    return None


def test_video_has_duration_element():
    elements = get_video_elements()
    assert "duration" in elements, (
        "video.xsd is missing 'duration' element in videoType"
    )


def test_video_duration_type_is_integer():
    elements = get_video_elements()
    assert elements.get("duration") == "xs:integer", (
        f"video.xsd 'duration' should be xs:integer, got '{elements.get('duration')}'"
    )


def test_video_duration_is_optional():
    attrs = get_video_element_attrs("duration")
    assert attrs is not None, "duration element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "video.xsd 'duration' should have minOccurs='0'"
    )


def test_video_duration_is_single():
    """Duration should allow at most one value."""
    attrs = get_video_element_attrs("duration")
    assert attrs is not None, "duration element not found"
    assert attrs.get("maxOccurs", "1") == "1", (
        "video.xsd 'duration' should have maxOccurs='1'"
    )
