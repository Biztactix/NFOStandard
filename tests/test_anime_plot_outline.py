#!/usr/bin/env python3
"""
Test: anime.xsd includes plot and outline distinction.

Verifies acceptance criterion for US-NFO-6:
  "anime.xsd includes plot and outline distinction"
"""

import os
import xml.etree.ElementTree as ET

import pytest

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
ANIME_XSD = os.path.join(SCHEMA_DIR, "anime.xsd")


def get_anime_elements():
    """Return dict of {element_name: type_name} from animeType sequence."""
    tree = ET.parse(ANIME_XSD)
    root = tree.getroot()
    elements = {}
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "animeType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            name = elem.get("name", "")
            elem_type = elem.get("type", "")
            elements[name] = elem_type
    return elements


def get_anime_element_attrs(field_name):
    """Return dict of XML attributes for a named element in animeType."""
    tree = ET.parse(ANIME_XSD)
    root = tree.getroot()
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "animeType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            if elem.get("name") == field_name:
                return dict(elem.attrib)
    return None


def test_anime_has_outline_element():
    elements = get_anime_elements()
    assert "outline" in elements, (
        "anime.xsd is missing 'outline' element in animeType"
    )


def test_anime_has_plot_element():
    elements = get_anime_elements()
    assert "plot" in elements, (
        "anime.xsd is missing 'plot' element in animeType"
    )


def test_anime_outline_type_is_string():
    elements = get_anime_elements()
    assert elements.get("outline") == "xs:string", (
        f"anime.xsd 'outline' should be xs:string, got '{elements.get('outline')}'"
    )


def test_anime_plot_type_is_string():
    elements = get_anime_elements()
    assert elements.get("plot") == "xs:string", (
        f"anime.xsd 'plot' should be xs:string, got '{elements.get('plot')}'"
    )


def test_anime_outline_is_optional():
    attrs = get_anime_element_attrs("outline")
    assert attrs is not None, "outline element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "anime.xsd 'outline' should have minOccurs='0'"
    )


def test_anime_plot_is_optional():
    attrs = get_anime_element_attrs("plot")
    assert attrs is not None, "plot element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "anime.xsd 'plot' should have minOccurs='0'"
    )


def test_anime_outline_is_singular():
    attrs = get_anime_element_attrs("outline")
    assert attrs is not None, "outline element not found"
    assert attrs.get("maxOccurs", "1") == "1", (
        "anime.xsd 'outline' should have maxOccurs='1'"
    )


def test_anime_plot_is_singular():
    attrs = get_anime_element_attrs("plot")
    assert attrs is not None, "plot element not found"
    assert attrs.get("maxOccurs", "1") == "1", (
        "anime.xsd 'plot' should have maxOccurs='1'"
    )
