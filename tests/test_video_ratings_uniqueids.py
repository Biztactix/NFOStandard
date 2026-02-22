#!/usr/bin/env python3
"""
Test: video.xsd supports multiple ratings and uniqueIds.

Verifies acceptance criterion for US-NFO-5:
  "video.xsd supports multiple ratings and uniqueIds"
"""

import os
import xml.etree.ElementTree as ET

import pytest

XS = "{http://www.w3.org/2001/XMLSchema}"
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "Schemas")
VIDEO_XSD = os.path.join(SCHEMA_DIR, "video.xsd")


def get_video_element_attrs(field_name):
    """Return dict of XML attributes for a named element in videoType."""
    tree = ET.parse(VIDEO_XSD)
    root = tree.getroot()
    for ct in root.findall(f"{XS}complexType"):
        if ct.get("name") != "videoType":
            continue
        seq = ct.find(f"{XS}sequence")
        if seq is None:
            continue
        for elem in seq.findall(f"{XS}element"):
            if elem.get("name") == field_name:
                return dict(elem.attrib)
    return None


class TestRating:
    def test_rating_element_exists(self):
        attrs = get_video_element_attrs("rating")
        assert attrs is not None, "video.xsd is missing 'rating' element in videoType"

    def test_rating_uses_ratingType(self):
        attrs = get_video_element_attrs("rating")
        assert attrs["type"] == "ratingType", (
            f"rating should use ratingType, got '{attrs['type']}'"
        )

    def test_rating_is_optional(self):
        attrs = get_video_element_attrs("rating")
        assert attrs.get("minOccurs", "1") == "0", (
            "rating should have minOccurs='0'"
        )

    def test_rating_allows_multiple(self):
        attrs = get_video_element_attrs("rating")
        assert attrs.get("maxOccurs", "1") == "unbounded", (
            f"rating should have maxOccurs='unbounded', got '{attrs.get('maxOccurs', '1')}'"
        )


class TestUniqueId:
    def test_uniqueid_element_exists(self):
        attrs = get_video_element_attrs("uniqueId")
        assert attrs is not None, "video.xsd is missing 'uniqueId' element in videoType"

    def test_uniqueid_uses_uniqueidType(self):
        attrs = get_video_element_attrs("uniqueId")
        assert attrs["type"] == "uniqueidType", (
            f"uniqueId should use uniqueidType, got '{attrs['type']}'"
        )

    def test_uniqueid_is_optional(self):
        attrs = get_video_element_attrs("uniqueId")
        assert attrs.get("minOccurs", "1") == "0", (
            "uniqueId should have minOccurs='0'"
        )

    def test_uniqueid_allows_multiple(self):
        attrs = get_video_element_attrs("uniqueId")
        assert attrs.get("maxOccurs", "1") == "unbounded", (
            f"uniqueId should have maxOccurs='unbounded', got '{attrs.get('maxOccurs', '1')}'"
        )
