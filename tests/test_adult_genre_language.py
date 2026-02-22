#!/usr/bin/env python3
"""
Test: adult.xsd includes genre and language elements.

Verifies acceptance criterion for US-NFO-6:
  "adult.xsd includes genre and language elements"
"""

import os
import xml.etree.ElementTree as ET

import pytest

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
ADULT_XSD = os.path.join(SCHEMA_DIR, "adult.xsd")


def get_adult_elements():
    """Return dict of {element_name: type_name} from adultType sequence."""
    tree = ET.parse(ADULT_XSD)
    root = tree.getroot()
    elements = {}
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "adultType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            name = elem.get("name", "")
            elem_type = elem.get("type", "")
            elements[name] = elem_type
    return elements


def get_adult_element_attrs(field_name):
    """Return dict of XML attributes for a named element in adultType."""
    tree = ET.parse(ADULT_XSD)
    root = tree.getroot()
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "adultType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            if elem.get("name") == field_name:
                return dict(elem.attrib)
    return None


def test_adult_has_genre_element():
    elements = get_adult_elements()
    assert "genre" in elements, (
        "adult.xsd is missing 'genre' element in adultType"
    )


def test_adult_genre_type_is_string():
    elements = get_adult_elements()
    assert elements.get("genre") == "xs:string", (
        f"adult.xsd 'genre' should be xs:string, got '{elements.get('genre')}'"
    )


def test_adult_genre_is_optional():
    attrs = get_adult_element_attrs("genre")
    assert attrs is not None, "genre element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "adult.xsd 'genre' should have minOccurs='0'"
    )


def test_adult_genre_allows_multiple():
    attrs = get_adult_element_attrs("genre")
    assert attrs is not None, "genre element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "adult.xsd 'genre' should have maxOccurs='unbounded'"
    )


def test_adult_has_language_element():
    elements = get_adult_elements()
    assert "language" in elements, (
        "adult.xsd is missing 'language' element in adultType"
    )


def test_adult_language_type_is_string():
    elements = get_adult_elements()
    assert elements.get("language") == "xs:string", (
        f"adult.xsd 'language' should be xs:string, got '{elements.get('language')}'"
    )


def test_adult_language_is_optional():
    attrs = get_adult_element_attrs("language")
    assert attrs is not None, "language element not found"
    assert attrs.get("minOccurs", "1") == "0", (
        "adult.xsd 'language' should have minOccurs='0'"
    )


def test_adult_language_allows_multiple():
    """An adult video can have multiple languages."""
    attrs = get_adult_element_attrs("language")
    assert attrs is not None, "language element not found"
    assert attrs.get("maxOccurs", "1") == "unbounded", (
        "adult.xsd 'language' should have maxOccurs='unbounded'"
    )
