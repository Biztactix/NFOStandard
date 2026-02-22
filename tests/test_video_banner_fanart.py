#!/usr/bin/env python3
"""
Test: video.xsd includes banner and fanart image elements.

Verifies acceptance criterion for US-NFO-5:
  "video.xsd includes banner and fanart image elements"
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


# --- banner tests ---

def test_video_has_banner_element():
    elements = get_video_elements()
    assert "banner" in elements, (
        "video.xsd is missing 'banner' element in videoType"
    )


def test_video_banner_type_is_subMediaType():
    elements = get_video_elements()
    assert elements.get("banner") == "subMediaType", (
        f"video.xsd 'banner' should be subMediaType, got '{elements.get('banner')}'"
    )


def test_video_banner_is_optional():
    attrs = get_video_element_attrs("banner")
    assert attrs is not None, "banner element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "video.xsd 'banner' should have minOccurs='0'"
    )


def test_video_banner_allows_multiple():
    attrs = get_video_element_attrs("banner")
    assert attrs is not None, "banner element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "video.xsd 'banner' should have maxOccurs='unbounded'"
    )


# --- fanart tests ---

def test_video_has_fanart_element():
    elements = get_video_elements()
    assert "fanart" in elements, (
        "video.xsd is missing 'fanart' element in videoType"
    )


def test_video_fanart_type_is_subMediaType():
    elements = get_video_elements()
    assert elements.get("fanart") == "subMediaType", (
        f"video.xsd 'fanart' should be subMediaType, got '{elements.get('fanart')}'"
    )


def test_video_fanart_is_optional():
    attrs = get_video_element_attrs("fanart")
    assert attrs is not None, "fanart element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "video.xsd 'fanart' should have minOccurs='0'"
    )


def test_video_fanart_allows_multiple():
    attrs = get_video_element_attrs("fanart")
    assert attrs is not None, "fanart element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "video.xsd 'fanart' should have maxOccurs='unbounded'"
    )
