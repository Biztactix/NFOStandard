#!/usr/bin/env python3
"""
Test: tvshow.xsd includes outline for short descriptions.

Verifies acceptance criterion for US-NFO-4:
  "tvshow.xsd includes outline for short descriptions"
"""

import os
import xml.etree.ElementTree as ET

import pytest

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
TVSHOW_XSD = os.path.join(SCHEMA_DIR, "tvshow.xsd")


def get_tvshow_elements():
    """Return dict of {element_name: type_name} from tvshowType sequence."""
    tree = ET.parse(TVSHOW_XSD)
    root = tree.getroot()
    elements = {}
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "tvshowType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            name = elem.get("name", "")
            elem_type = elem.get("type", "")
            elements[name] = elem_type
    return elements


def get_tvshow_element_attrs(field_name):
    """Return dict of XML attributes for a named element in tvshowType."""
    tree = ET.parse(TVSHOW_XSD)
    root = tree.getroot()
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "tvshowType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            if elem.get("name") == field_name:
                return dict(elem.attrib)
    return None


def test_tvshow_has_outline_element():
    elements = get_tvshow_elements()
    assert "outline" in elements, (
        "tvshow.xsd is missing 'outline' element in tvshowType"
    )


def test_tvshow_outline_type_is_string():
    elements = get_tvshow_elements()
    assert elements.get("outline") == "xs:string", (
        f"tvshow.xsd 'outline' should be xs:string, got '{elements.get('outline')}'"
    )


def test_tvshow_outline_is_optional():
    attrs = get_tvshow_element_attrs("outline")
    assert attrs is not None, "outline element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "tvshow.xsd 'outline' should have minOccurs='0'"
    )


def test_tvshow_outline_is_singular():
    attrs = get_tvshow_element_attrs("outline")
    assert attrs is not None, "outline element not found"
    assert attrs.get("maxOccurs", "1") == "1", (
        "tvshow.xsd 'outline' should have maxOccurs='1'"
    )
