#!/usr/bin/env python3
"""
Verify ADR-001: Required vs Optional Field Policy

Policy:
  1. title (or equivalent) is always required
  2. No schema should require more than 2-3 fields at the top level
  3. Default to optional

Checks all content-type XSD schemas and reports compliance.
"""

import os
import sys
import xml.etree.ElementTree as ET

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
SKIP = {"common.xsd", "person.xsd", "library.xsd"}
MAX_REQUIRED = 3

results = {"PASS": 0, "WARN": 0, "FAIL": 0}
details = []


def get_primary_type_name(fname):
    """Derive the expected primary type name from filename (e.g. movie.xsd -> movieType)."""
    base = os.path.splitext(fname)[0]
    return base + "Type"


def get_top_level_required(xsd_path):
    """Return list of required field names from the primary complexType sequence."""
    tree = ET.parse(xsd_path)
    root = tree.getroot()
    fname = os.path.basename(xsd_path)
    primary = get_primary_type_name(fname)

    required = []
    for ct in root.findall(f"{XS}complexType"):
        ct_name = ct.get("name", "")
        # Only check the primary content type (e.g. movieType, musicType)
        if ct_name.lower() != primary.lower():
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        # Only check direct children (not nested complex types)
        for elem in seq.findall(f"{XS}element"):
            min_occurs = elem.get("minOccurs", "1")  # XSD default is 1
            if min_occurs != "0":
                name = elem.get("name", "???")
                required.append(name)
    return required


for fname in sorted(os.listdir(SCHEMA_DIR)):
    if not fname.endswith(".xsd") or fname in SKIP:
        continue

    path = os.path.join(SCHEMA_DIR, fname)
    required = get_top_level_required(path)
    count = len(required)

    has_title = any(f in required for f in ("title", "name"))

    if not has_title:
        status = "FAIL"
        notes = "Missing required 'title' field"
    elif count > MAX_REQUIRED:
        status = "FAIL"
        notes = f"Too many required fields ({count} > {MAX_REQUIRED} max)"
    elif count > 1:
        status = "WARN"
        notes = f"{count} required fields (policy prefers title-only)"
    else:
        status = "PASS"
        notes = ""

    results[status] += 1
    req_str = ", ".join(required) if required else "(none)"
    line = f"{fname:<20s} [{status}]  Required({count}): {req_str}"
    if notes:
        line += f"  -- {notes}"
    details.append(line)

print("=== ADR-001 Compliance Check: Required vs Optional Field Policy ===")
print()
for line in details:
    print(line)
print()
print("=== Summary ===")
print(f"PASS: {results['PASS']}  WARN: {results['WARN']}  FAIL: {results['FAIL']}")
print()

if results["FAIL"] > 0:
    print(f"RESULT: NON-COMPLIANT -- {results['FAIL']} schema(s) violate ADR-001")
    print("See tasks US-NFO-3-5 and US-NFO-3-6 for required fixes.")
    sys.exit(1)
else:
    print("RESULT: COMPLIANT -- All schemas follow ADR-001")
    sys.exit(0)
