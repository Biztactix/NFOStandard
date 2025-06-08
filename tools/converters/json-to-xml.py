#!/usr/bin/env python3
"""
JSON to NFO XML Converter
Converts JSON data to NFO Standard compliant XML files.
"""

import json
import argparse
import sys
from typing import Dict, Any, List, Union
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime


class JSONToNFOConverter:
    """Converts JSON data to NFO Standard XML format."""
    
    NAMESPACE = "NFOStandard"
    SCHEMA_LOCATION = "NFOStandard https://xsd.nfostandard.com/main.xsd"
    
    def __init__(self):
        # Register namespace
        ET.register_namespace("", self.NAMESPACE)
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    
    def convert(self, json_data: Union[str, Dict], pretty_print: bool = True) -> str:
        """Convert JSON data to NFO XML string."""
        # Parse JSON if string
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        # Create root element
        root = ET.Element("{%s}root" % self.NAMESPACE)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", self.SCHEMA_LOCATION)
        
        # Create media element
        media_elem = ET.SubElement(root, "media")
        
        # Determine media type and create appropriate element
        media_type = data.get('type', 'movie').lower()
        if media_type in ['movie', 'tvshow', 'music', 'audiobook', 'podcast', 'anime', 'adult', 'musicvideo', 'video']:
            media_content = data.get(media_type, data)
            media_type_elem = ET.SubElement(media_elem, media_type)
            self._build_element(media_type_elem, media_content, media_type)
        else:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        # Add library metadata if present
        if 'library' in data:
            library_elem = ET.SubElement(root, "library")
            self._build_element(library_elem, data['library'], 'library')
        
        # Convert to string
        if pretty_print:
            return self._prettify(root)
        else:
            return ET.tostring(root, encoding='unicode')
    
    def _build_element(self, parent: ET.Element, data: Dict[str, Any], context: str = ""):
        """Recursively build XML elements from dictionary data."""
        
        # Special handling for different media types
        if context in ['movie', 'tvshow', 'music', 'audiobook', 'podcast']:
            self._build_media_element(parent, data, context)
        else:
            # Generic building
            for key, value in data.items():
                if value is None:
                    continue
                    
                if isinstance(value, list):
                    # Handle lists (multiple elements with same name)
                    for item in value:
                        elem = ET.SubElement(parent, key)
                        if isinstance(item, dict):
                            self._build_attributes_and_content(elem, item)
                        else:
                            elem.text = str(item)
                elif isinstance(value, dict):
                    elem = ET.SubElement(parent, key)
                    self._build_attributes_and_content(elem, value)
                else:
                    elem = ET.SubElement(parent, key)
                    elem.text = str(value)
    
    def _build_media_element(self, parent: ET.Element, data: Dict[str, Any], media_type: str):
        """Build media-specific elements with proper ordering."""
        
        # Define field order for each media type
        field_orders = {
            'movie': [
                'title', 'originaltitle', 'sorttitle', 'alternatetitle',
                'rating', 'userrating', 'outline', 'plot', 'tagline',
                'runtime', 'banner', 'thumb', 'fanart', 'contentrating',
                'uniqueid', 'genre', 'tag', 'setname', 'setoverview',
                'country', 'productioncompany', 'keyword', 'releasedate',
                'award', 'subtitlelanguage', 'soundtrack', 'parentalguide',
                'actor', 'director', 'writer', 'composer', 'producers',
                'collection', 'intro', 'credits', 'library'
            ],
            'tvshow': [
                'title', 'originaltitle', 'sorttitle', 'alternatetitle',
                'rating', 'userrating', 'outline', 'plot', 'tagline',
                'runtime', 'banner', 'thumb', 'fanart', 'contentrating',
                'uniqueid', 'genre', 'tag', 'country', 'premiered',
                'status', 'studio', 'season', 'episode', 'displayseason',
                'displayepisode', 'actor', 'director', 'writer', 'creator'
            ],
            'music': [
                'title', 'artist', 'albumartist', 'album', 'year',
                'genre', 'style', 'mood', 'rating', 'userrating',
                'compilation', 'label', 'type', 'releasedate',
                'originalreleasedate', 'barcode', 'catalognumber',
                'thumb', 'path', 'track'
            ]
        }
        
        # Get field order for media type
        field_order = field_orders.get(media_type, [])
        
        # Process fields in order
        processed_keys = set()
        for field in field_order:
            if field in data:
                self._add_field(parent, field, data[field])
                processed_keys.add(field)
        
        # Add any remaining fields not in the order
        for key, value in data.items():
            if key not in processed_keys and value is not None:
                self._add_field(parent, key, value)
    
    def _add_field(self, parent: ET.Element, key: str, value: Any):
        """Add a field to the parent element."""
        if isinstance(value, list):
            for item in value:
                elem = ET.SubElement(parent, key)
                if isinstance(item, dict):
                    self._build_attributes_and_content(elem, item)
                else:
                    elem.text = str(item)
        elif isinstance(value, dict):
            elem = ET.SubElement(parent, key)
            self._build_attributes_and_content(elem, value)
        else:
            elem = ET.SubElement(parent, key)
            elem.text = str(value)
    
    def _build_attributes_and_content(self, elem: ET.Element, data: Dict[str, Any]):
        """Build attributes and content for an element."""
        # Separate attributes from content
        attributes = {}
        content = None
        sub_elements = {}
        
        for key, value in data.items():
            if key.startswith('@'):
                # Attribute
                attributes[key[1:]] = str(value)
            elif key == '#text' or key == '_text':
                # Text content
                content = str(value)
            else:
                # Sub-element
                sub_elements[key] = value
        
        # Set attributes
        for attr_name, attr_value in attributes.items():
            elem.set(attr_name, attr_value)
        
        # Set content or build sub-elements
        if sub_elements:
            for key, value in sub_elements.items():
                if isinstance(value, list):
                    for item in value:
                        sub_elem = ET.SubElement(elem, key)
                        if isinstance(item, dict):
                            self._build_attributes_and_content(sub_elem, item)
                        else:
                            sub_elem.text = str(item)
                elif isinstance(value, dict):
                    sub_elem = ET.SubElement(elem, key)
                    self._build_attributes_and_content(sub_elem, value)
                else:
                    sub_elem = ET.SubElement(elem, key)
                    sub_elem.text = str(value)
        elif content:
            elem.text = content
    
    def _prettify(self, elem: ET.Element) -> str:
        """Return a pretty-printed XML string for the Element."""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ", encoding=None)


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON to NFO Standard XML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s movie.json
  %(prog)s movie.json -o movie.nfo
  %(prog)s --type tvshow show.json
  cat movie.json | %(prog)s - 

JSON Format:
  {
    "type": "movie",
    "movie": {
      "title": "Example Movie",
      "year": 2023,
      "rating": {
        "@name": "imdb",
        "@value": "8.5",
        "@votes": "1000"
      },
      "genre": ["Action", "Drama"],
      "actor": [
        {
          "name": "John Doe",
          "role": "Main Character",
          "order": 1
        }
      ]
    }
  }
        """
    )
    
    parser.add_argument('input', help='Input JSON file (use "-" for stdin)')
    parser.add_argument('-o', '--output', help='Output XML file (default: stdout)')
    parser.add_argument('-t', '--type', help='Media type if not specified in JSON',
                       choices=['movie', 'tvshow', 'music', 'audiobook', 'podcast', 
                               'anime', 'adult', 'musicvideo', 'video'])
    parser.add_argument('--no-pretty', action='store_true',
                       help='Disable pretty printing')
    
    args = parser.parse_args()
    
    # Read input
    if args.input == '-':
        json_data = sys.stdin.read()
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            json_data = f.read()
    
    # Parse JSON
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)
    
    # Override type if specified
    if args.type and 'type' not in data:
        data['type'] = args.type
    
    # Convert to XML
    converter = JSONToNFOConverter()
    try:
        xml_output = converter.convert(data, pretty_print=not args.no_pretty)
    except Exception as e:
        print(f"Error: Conversion failed - {e}", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(xml_output)
        print(f"Successfully converted to {args.output}")
    else:
        print(xml_output)


if __name__ == "__main__":
    main()