#!/usr/bin/env python3
"""
Test: anime.xsd isAdult changed from integer to boolean.

Verifies acceptance criterion for US-NFO-6:
  "anime.xsd isAdult changed from integer to boolean"
"""

import os
import xml.etree.ElementTree as ET

import pytest

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
ANIME_XSD = os.path.join(SCHEMA_DIR, "anime.xsd")


def get_anime_element_type(field_name):
    """Return the type attribute for a named element in animeType."""
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
                return elem.get("type", "")
    return None


def test_anime_isadult_exists():
    elem_type = get_anime_element_type("isAdult")
    assert elem_type is not None, (
        "anime.xsd is missing 'isAdult' element in animeType"
    )


def test_anime_isadult_is_boolean():
    elem_type = get_anime_element_type("isAdult")
    assert elem_type == "xs:boolean", (
        f"anime.xsd 'isAdult' should be xs:boolean, got '{elem_type}'"
    )
