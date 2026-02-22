#!/usr/bin/env python3
"""
Test: No schema requires more than 2-3 fields (ADR-001 criterion).

Verifies acceptance criterion for US-NFO-3:
  "No schema requires more than 2-3 fields"
"""

import os
import xml.etree.ElementTree as ET

import pytest

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
SKIP = {"common.xsd", "person.xsd", "library.xsd"}
MAX_REQUIRED = 3


def get_primary_type_name(fname):
    base = os.path.splitext(fname)[0]
    return base + "Type"


def get_top_level_required(xsd_path):
    tree = ET.parse(xsd_path)
    root = tree.getroot()
    fname = os.path.basename(xsd_path)
    primary = get_primary_type_name(fname)

    required = []
    for ct in root.findall(f"{XS}complexType"):
        ct_name = ct.get("name", "")
        if ct_name.lower() != primary.lower():
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            min_occurs = elem.get("minOccurs", "1")
            if min_occurs != "0":
                required.append(elem.get("name", "???"))
    return required


def content_schemas():
    schemas = []
    for fname in sorted(os.listdir(SCHEMA_DIR)):
        if fname.endswith(".xsd") and fname not in SKIP:
            schemas.append(fname)
    return schemas


@pytest.mark.parametrize("schema_file", content_schemas())
def test_schema_has_at_most_max_required_fields(schema_file):
    path = os.path.join(SCHEMA_DIR, schema_file)
    required = get_top_level_required(path)
    count = len(required)
    assert count <= MAX_REQUIRED, (
        f"{schema_file} has {count} required fields ({', '.join(required)}), "
        f"max allowed is {MAX_REQUIRED}"
    )
