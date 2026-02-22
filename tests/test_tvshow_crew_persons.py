#!/usr/bin/env python3
"""
Test: tvshow.xsd includes director/writer/composer person elements.

Verifies acceptance criterion for US-NFO-4:
  "tvshow.xsd includes director/writer/composer person elements"
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


@pytest.mark.parametrize("field", ["director", "writer", "composer"])
def test_tvshow_has_crew_person_element(field):
    elements = get_tvshow_elements()
    assert field in elements, (
        f"tvshow.xsd is missing '{field}' element in tvshowType"
    )
    assert elements[field] == "personType", (
        f"tvshow.xsd '{field}' should use personType, got '{elements[field]}'"
    )


@pytest.mark.parametrize("field", ["director", "writer", "composer"])
def test_tvshow_crew_allows_multiple(field):
    """Crew fields should allow unbounded occurrences."""
    tree = ET.parse(TVSHOW_XSD)
    root = tree.getroot()
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "tvshowType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            if elem.get("name") == field:
                max_occurs = elem.get("maxOccurs", "1")
                assert max_occurs == "unbounded", (
                    f"tvshow.xsd '{field}' should have maxOccurs='unbounded', "
                    f"got '{max_occurs}'"
                )
                return
    pytest.fail(f"tvshow.xsd '{field}' element not found")


@pytest.mark.parametrize("field", ["director", "writer", "composer"])
def test_tvshow_crew_is_optional(field):
    """Crew fields should be optional (minOccurs=0)."""
    tree = ET.parse(TVSHOW_XSD)
    root = tree.getroot()
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "tvshowType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            if elem.get("name") == field:
                min_occurs = elem.get("minOccurs", "1")
                assert min_occurs == "0", (
                    f"tvshow.xsd '{field}' should have minOccurs='0', "
                    f"got '{min_occurs}'"
                )
                return
    pytest.fail(f"tvshow.xsd '{field}' element not found")
