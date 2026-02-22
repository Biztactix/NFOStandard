#!/usr/bin/env python3
"""
Test: tvshow.xsd includes country and productionCompany.

Verifies acceptance criterion for US-NFO-4:
  "tvshow.xsd includes country and productionCompany"
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


# --- country ---

def test_tvshow_has_country_element():
    elements = get_tvshow_elements()
    assert "country" in elements, (
        "tvshow.xsd is missing 'country' element in tvshowType"
    )


def test_tvshow_country_type_is_string():
    elements = get_tvshow_elements()
    assert elements.get("country") == "xs:string", (
        f"tvshow.xsd 'country' should be xs:string, got '{elements.get('country')}'"
    )


def test_tvshow_country_is_optional():
    attrs = get_tvshow_element_attrs("country")
    assert attrs is not None, "country element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "tvshow.xsd 'country' should have minOccurs='0'"
    )


def test_tvshow_country_allows_multiple():
    attrs = get_tvshow_element_attrs("country")
    assert attrs is not None, "country element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "tvshow.xsd 'country' should have maxOccurs='unbounded'"
    )


# --- productionCompany ---

def test_tvshow_has_productionCompany_element():
    elements = get_tvshow_elements()
    assert "productionCompany" in elements, (
        "tvshow.xsd is missing 'productionCompany' element in tvshowType"
    )


def test_tvshow_productionCompany_type_is_string():
    elements = get_tvshow_elements()
    assert elements.get("productionCompany") == "xs:string", (
        f"tvshow.xsd 'productionCompany' should be xs:string, got '{elements.get('productionCompany')}'"
    )


def test_tvshow_productionCompany_is_optional():
    attrs = get_tvshow_element_attrs("productionCompany")
    assert attrs is not None, "productionCompany element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "tvshow.xsd 'productionCompany' should have minOccurs='0'"
    )


def test_tvshow_productionCompany_allows_multiple():
    attrs = get_tvshow_element_attrs("productionCompany")
    assert attrs is not None, "productionCompany element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "tvshow.xsd 'productionCompany' should have maxOccurs='unbounded'"
    )
