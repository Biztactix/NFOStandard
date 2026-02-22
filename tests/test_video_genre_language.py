#!/usr/bin/env python3
"""
Test: video.xsd includes genre and language elements.

Verifies acceptance criterion for US-NFO-5:
  "video.xsd includes genre and language elements"
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


def test_video_has_genre_element():
    elements = get_video_elements()
    assert "genre" in elements, (
        "video.xsd is missing 'genre' element in videoType"
    )


def test_video_genre_type_is_string():
    elements = get_video_elements()
    assert elements.get("genre") == "xs:string", (
        f"video.xsd 'genre' should be xs:string, got '{elements.get('genre')}'"
    )


def test_video_genre_is_optional():
    attrs = get_video_element_attrs("genre")
    assert attrs is not None, "genre element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "video.xsd 'genre' should have minOccurs='0'"
    )


def test_video_genre_allows_multiple():
    attrs = get_video_element_attrs("genre")
    assert attrs is not None, "genre element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "video.xsd 'genre' should have maxOccurs='unbounded'"
    )


def test_video_has_language_element():
    elements = get_video_elements()
    assert "language" in elements, (
        "video.xsd is missing 'language' element in videoType"
    )


def test_video_language_type_is_string():
    elements = get_video_elements()
    assert elements.get("language") == "xs:string", (
        f"video.xsd 'language' should be xs:string, got '{elements.get('language')}'"
    )


def test_video_language_is_optional():
    attrs = get_video_element_attrs("language")
    assert attrs is not None, "language element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "video.xsd 'language' should have minOccurs='0'"
    )


def test_video_language_allows_multiple():
    """A video can have multiple languages."""
    attrs = get_video_element_attrs("language")
    assert attrs is not None, "language element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "video.xsd 'language' should have maxOccurs='unbounded'"
    )
