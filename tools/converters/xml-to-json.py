#!/usr/bin/env python3
"""
NFO XML to JSON Converter
Converts NFO Standard XML files to JSON format.
"""

import json
import argparse
import sys
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Union
from collections import defaultdict


class NFOToJSONConverter:
    """Converts NFO Standard XML to JSON format."""
    
    def __init__(self, compact: bool = False):
        self.compact = compact
        self.namespaces = {
            'nfo': 'NFOStandard',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }
    
    def convert(self, xml_content: str, include_attributes: bool = True) -> str:
        """Convert NFO XML to JSON string."""
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML: {e}")
        
        # Convert to dictionary
        result = self._element_to_dict(root, include_attributes)
        
        # Extract media type and structure
        if 'media' in result.get('root', {}):
            media = result['root']['media']
            # Find the media type
            media_type = None
            for mtype in ['movie', 'tvshow', 'music', 'audiobook', 'podcast', 
                         'anime', 'adult', 'musicvideo', 'video']:
                if mtype in media:
                    media_type = mtype
                    break
            
            if media_type and self.compact:
                # Compact format: just the media content with type
                output = {
                    'type': media_type,
                    media_type: media[media_type]
                }
                # Add library if present
                if 'library' in result.get('root', {}):
                    output['library'] = result['root']['library']
            else:
                # Full format
                output = result
        else:
            output = result
        
        # Convert to JSON
        if self.compact:
            return json.dumps(output, indent=2, ensure_ascii=False)
        else:
            return json.dumps(output, indent=2, ensure_ascii=False)
    
    def _element_to_dict(self, element: ET.Element, include_attributes: bool = True) -> Dict[str, Any]:
        """Convert an XML element to a dictionary."""
        result = {}
        
        # Get the tag without namespace
        tag = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        
        # Initialize the element's dictionary
        elem_dict = {}
        
        # Add attributes
        if include_attributes and element.attrib:
            for key, value in element.attrib.items():
                # Skip namespace declarations
                if key.startswith('{'):
                    attr_name = '@' + key.split('}')[-1]
                else:
                    attr_name = '@' + key
                
                # Skip schemaLocation for compact mode
                if self.compact and 'schemaLocation' in attr_name:
                    continue
                    
                elem_dict[attr_name] = value
        
        # Process child elements
        children = list(element)
        if children:
            # Group children by tag
            child_dict = defaultdict(list)
            for child in children:
                child_tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                child_data = self._element_to_dict(child, include_attributes)
                
                # Extract the child data
                if child_tag in child_data:
                    child_dict[child_tag].append(child_data[child_tag])
                else:
                    child_dict[child_tag].append(child_data)
            
            # Add children to element dict
            for child_tag, child_list in child_dict.items():
                if len(child_list) == 1:
                    # Single child - don't use array
                    elem_dict[child_tag] = child_list[0]
                else:
                    # Multiple children - use array
                    elem_dict[child_tag] = child_list
        
        # Add text content if present
        if element.text and element.text.strip():
            if elem_dict:
                # Has attributes or children - add text as special key
                elem_dict['#text'] = element.text.strip()
            else:
                # Just text - return as string
                return {tag: element.text.strip()}
        
        # Return result
        if elem_dict or not element.text:
            result[tag] = elem_dict if elem_dict else None
        
        return result
    
    def convert_file(self, filepath: str, include_attributes: bool = True) -> str:
        """Convert an NFO XML file to JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            xml_content = f.read()
        return self.convert(xml_content, include_attributes)


def simplify_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """Simplify JSON structure by removing empty values and flattening where possible."""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if value is not None and value != {} and value != []:
                simplified = simplify_json(value)
                if simplified is not None:
                    result[key] = simplified
        return result if result else None
    elif isinstance(data, list):
        result = [simplify_json(item) for item in data if item is not None]
        return result if result else None
    else:
        return data


def main():
    parser = argparse.ArgumentParser(
        description="Convert NFO Standard XML to JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s movie.nfo
  %(prog)s movie.nfo -o movie.json
  %(prog)s --compact movie.nfo
  cat movie.nfo | %(prog)s -

Output formats:
  Default: Full JSON representation
  Compact: Simplified JSON with just media content
        """
    )
    
    parser.add_argument('input', help='Input XML file (use "-" for stdin)')
    parser.add_argument('-o', '--output', help='Output JSON file (default: stdout)')
    parser.add_argument('-c', '--compact', action='store_true',
                       help='Use compact JSON format')
    parser.add_argument('--no-attributes', action='store_true',
                       help='Exclude XML attributes from output')
    parser.add_argument('--simplify', action='store_true',
                       help='Remove empty values and simplify structure')
    
    args = parser.parse_args()
    
    # Read input
    if args.input == '-':
        xml_content = sys.stdin.read()
    else:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                xml_content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found - {args.input}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: Could not read file - {e}", file=sys.stderr)
            sys.exit(1)
    
    # Convert to JSON
    converter = NFOToJSONConverter(compact=args.compact)
    try:
        json_output = converter.convert(xml_content, include_attributes=not args.no_attributes)
        
        # Simplify if requested
        if args.simplify:
            data = json.loads(json_output)
            simplified = simplify_json(data)
            json_output = json.dumps(simplified, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error: Conversion failed - {e}", file=sys.stderr)
        sys.exit(1)
    
    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"Successfully converted to {args.output}")
        except Exception as e:
            print(f"Error: Could not write file - {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(json_output)


if __name__ == "__main__":
    main()