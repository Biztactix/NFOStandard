#!/usr/bin/env python3
"""
Test: All XSD files compile successfully.

Verifies acceptance criterion for US-NFO-9:
  "Validation script exists that checks all XSD files compile"

Parses each XSD file individually and also compiles the combined
main.xsd schema to ensure all schema definitions are valid.
"""

import glob
import os

import pytest
from lxml import etree

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SCHEMA_DIR = os.path.join(REPO_ROOT, "Schemas")
MAIN_XSD = os.path.join(REPO_ROOT, "main.xsd")
REMOTE_PREFIX = "https://xsd.nfostandard.com/"


class LocalResolver(etree.Resolver):
    """Resolve remote schema URLs to local files."""

    def resolve(self, system_url, public_id, context):
        if system_url.startswith(REMOTE_PREFIX):
            local_path = system_url[len(REMOTE_PREFIX):]
            local_file = os.path.join(REPO_ROOT, local_path)
            if os.path.exists(local_file):
                return self.resolve_filename(local_file, context)
        return None


def find_all_xsd_files():
    """Find all XSD files in the repo (main.xsd + Schemas/*.xsd)."""
    xsd_files = [MAIN_XSD]
    xsd_files.extend(sorted(glob.glob(os.path.join(SCHEMA_DIR, "*.xsd"))))
    return xsd_files


XSD_FILES = find_all_xsd_files()


@pytest.mark.parametrize(
    "xsd_file",
    XSD_FILES,
    ids=[os.path.relpath(f, REPO_ROOT) for f in XSD_FILES],
)
def test_xsd_parses_as_valid_xml(xsd_file):
    """Each XSD file must be well-formed XML."""
    doc = etree.parse(xsd_file)
    assert doc.getroot().tag == "{http://www.w3.org/2001/XMLSchema}schema", (
        f"{os.path.basename(xsd_file)} root element is not xs:schema"
    )


def test_main_xsd_compiles_as_schema():
    """The combined main.xsd must compile into a valid XMLSchema."""
    parser = etree.XMLParser()
    parser.resolvers.add(LocalResolver())

    with open(MAIN_XSD, "rb") as f:
        schema_doc = etree.parse(f, parser)

    try:
        etree.XMLSchema(schema_doc)
    except etree.XMLSchemaParseError as e:
        pytest.fail(f"main.xsd failed to compile as XMLSchema:\n{e}")
