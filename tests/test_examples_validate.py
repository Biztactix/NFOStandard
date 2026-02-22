#!/usr/bin/env python3
"""
Test: All examples validate against their respective schemas.

Verifies acceptance criterion for US-NFO-7:
  "All examples validate against their respective schemas"

Uses lxml to perform full XSD validation of each example XML file
against the local schema files, rewriting remote URLs to local paths.
"""

import glob
import os
import xml.etree.ElementTree as ET

import pytest
from lxml import etree

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
SCHEMA_DIR = os.path.join(REPO_ROOT, "Schemas")
MAIN_XSD = os.path.join(REPO_ROOT, "main.xsd")
NS = "NFOStandard"
REMOTE_PREFIX = "https://xsd.nfostandard.com/"


def build_local_schema():
    """Build an XMLSchema from the local main.xsd, resolving remote includes locally."""

    class LocalResolver(etree.Resolver):
        def resolve(self, system_url, public_id, context):
            if system_url.startswith(REMOTE_PREFIX):
                local_path = system_url[len(REMOTE_PREFIX) :]
                local_file = os.path.join(REPO_ROOT, local_path)
                if os.path.exists(local_file):
                    return self.resolve_filename(local_file, context)
            return None

    parser = etree.XMLParser()
    parser.resolvers.add(LocalResolver())

    with open(MAIN_XSD, "rb") as f:
        schema_doc = etree.parse(f, parser)

    return etree.XMLSchema(schema_doc)


def find_example_xmls():
    """Find all example XML files in the repo root."""
    xml_files = glob.glob(os.path.join(REPO_ROOT, "*.xml"))
    results = []
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            media = root.find(f"{{{NS}}}media")
            if media is not None and len(media) > 0:
                content_type = media[0].tag.replace(f"{{{NS}}}", "")
                results.append((xml_file, content_type))
        except ET.ParseError:
            continue
    return results


EXAMPLES = find_example_xmls()


@pytest.mark.parametrize(
    "xml_file,content_type",
    EXAMPLES,
    ids=[f"{os.path.basename(f)}({t})" for f, t in EXAMPLES],
)
def test_example_validates_against_schema(xml_file, content_type):
    schema = build_local_schema()
    doc = etree.parse(xml_file)
    is_valid = schema.validate(doc)
    if not is_valid:
        errors = "\n".join(str(e) for e in schema.error_log)
        pytest.fail(
            f"{os.path.basename(xml_file)} (type={content_type}) failed XSD validation:\n{errors}"
        )
