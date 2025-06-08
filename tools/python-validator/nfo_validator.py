#!/usr/bin/env python3
"""
NFO Standard Validator
A Python tool for validating NFO files against the NFO Standard XSD schemas.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Tuple, Optional
import xml.etree.ElementTree as ET
from lxml import etree
import requests
from urllib.parse import urlparse
import json


class NFOValidator:
    """Main validator class for NFO Standard files."""
    
    SCHEMA_BASE_URL = "https://xsd.nfostandard.com/"
    MAIN_SCHEMA = "main.xsd"
    
    def __init__(self, offline: bool = False, schema_dir: Optional[str] = None):
        self.offline = offline
        self.schema_dir = schema_dir
        self.schemas_cache = {}
        self.main_schema = None
        
    def _load_schema(self, schema_url: str) -> etree.XMLSchema:
        """Load and cache XSD schema."""
        if schema_url in self.schemas_cache:
            return self.schemas_cache[schema_url]
            
        if self.offline and self.schema_dir:
            # Load from local directory
            schema_filename = os.path.basename(urlparse(schema_url).path)
            schema_path = os.path.join(self.schema_dir, schema_filename)
            with open(schema_path, 'rb') as f:
                schema_doc = etree.parse(f)
        else:
            # Load from URL
            response = requests.get(schema_url, timeout=10)
            response.raise_for_status()
            schema_doc = etree.fromstring(response.content)
            
        # Create XMLSchema with custom resolver for includes
        schema = etree.XMLSchema(schema_doc)
        self.schemas_cache[schema_url] = schema
        return schema
        
    def validate_file(self, filepath: str, strict: bool = False) -> Tuple[bool, List[str]]:
        """Validate a single NFO file."""
        errors = []
        
        try:
            # Parse the XML file
            with open(filepath, 'rb') as f:
                doc = etree.parse(f)
                
            # Get the schema location from the document
            root = doc.getroot()
            schema_location = root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
            
            if not schema_location:
                errors.append("No xsi:schemaLocation attribute found")
                return False, errors
                
            # Extract schema URL
            parts = schema_location.split()
            if len(parts) >= 2:
                schema_url = parts[1]
            else:
                errors.append("Invalid xsi:schemaLocation format")
                return False, errors
                
            # Load and validate against schema
            try:
                schema = self._load_schema(schema_url)
                schema.assertValid(doc)
                
                # Additional strict validation
                if strict:
                    strict_errors = self._strict_validation(doc)
                    errors.extend(strict_errors)
                    
            except etree.XMLSchemaError as e:
                errors.append(f"Schema validation error: {str(e)}")
                return False, errors
                
        except etree.XMLSyntaxError as e:
            errors.append(f"XML syntax error: {str(e)}")
            return False, errors
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
            return False, errors
            
        return len(errors) == 0, errors
        
    def _strict_validation(self, doc: etree.ElementTree) -> List[str]:
        """Perform additional strict validation checks."""
        errors = []
        root = doc.getroot()
        
        # Check for best practices
        media = root.find('.//{NFOStandard}media')
        if media is not None:
            # Check for recommended fields based on media type
            for media_type in ['movie', 'tvshow', 'music', 'audiobook', 'podcast']:
                element = media.find(f'.//{{{root.nsmap[None]}}}{media_type}')
                if element is not None:
                    errors.extend(self._check_recommended_fields(element, media_type))
                    
        return errors
        
    def _check_recommended_fields(self, element: etree.Element, media_type: str) -> List[str]:
        """Check for recommended fields based on media type."""
        warnings = []
        
        recommended_fields = {
            'movie': ['year', 'runtime', 'genre', 'director', 'actor', 'plot'],
            'tvshow': ['year', 'genre', 'actor', 'plot', 'season', 'episode'],
            'music': ['artist', 'album', 'year', 'genre'],
            'audiobook': ['author', 'narrator', 'publisher', 'year'],
            'podcast': ['author', 'category', 'pubDate', 'duration']
        }
        
        if media_type in recommended_fields:
            for field in recommended_fields[media_type]:
                if element.find(f'.//{{{element.nsmap[None]}}}{field}') is None:
                    warnings.append(f"Warning: Recommended field '{field}' is missing for {media_type}")
                    
        return warnings
        
    def validate_directory(self, directory: str, recursive: bool = False, 
                         pattern: str = "*.nfo") -> List[Tuple[str, bool, List[str]]]:
        """Validate all NFO files in a directory."""
        results = []
        path = Path(directory)
        
        if recursive:
            files = path.rglob(pattern)
        else:
            files = path.glob(pattern)
            
        for filepath in files:
            is_valid, errors = self.validate_file(str(filepath))
            results.append((str(filepath), is_valid, errors))
            
        return results


def format_validation_result(filepath: str, is_valid: bool, errors: List[str], 
                           format_type: str = "text") -> str:
    """Format validation results for output."""
    if format_type == "json":
        return json.dumps({
            "file": filepath,
            "valid": is_valid,
            "errors": errors
        }, indent=2)
    elif format_type == "xml":
        root = ET.Element("validation")
        ET.SubElement(root, "file").text = filepath
        ET.SubElement(root, "valid").text = str(is_valid).lower()
        errors_elem = ET.SubElement(root, "errors")
        for error in errors:
            ET.SubElement(errors_elem, "error").text = error
        return ET.tostring(root, encoding='unicode')
    else:  # text format
        result = f"\n{'='*60}\nFile: {filepath}\n"
        if is_valid:
            result += "Status: VALID ✓\n"
        else:
            result += "Status: INVALID ✗\n"
            result += "Errors:\n"
            for error in errors:
                result += f"  - {error}\n"
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Validate NFO files against the NFO Standard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s movie.nfo
  %(prog)s --strict tvshow.nfo
  %(prog)s --recursive /media/library/
  %(prog)s --format json *.nfo
        """
    )
    
    parser.add_argument('files', nargs='+', help='NFO files or directories to validate')
    parser.add_argument('--strict', action='store_true', 
                       help='Enable strict validation (check recommended fields)')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='Recursively validate directories')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'xml'],
                       default='text', help='Output format')
    parser.add_argument('--offline', action='store_true',
                       help='Use offline validation with local schemas')
    parser.add_argument('--schema-dir', help='Directory containing local schema files')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Only show files with errors')
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = NFOValidator(offline=args.offline, schema_dir=args.schema_dir)
    
    # Process files
    all_valid = True
    for file_path in args.files:
        if os.path.isdir(file_path):
            # Validate directory
            results = validator.validate_directory(file_path, recursive=args.recursive)
            for filepath, is_valid, errors in results:
                if not is_valid:
                    all_valid = False
                if not args.quiet or not is_valid:
                    print(format_validation_result(filepath, is_valid, errors, args.format))
        else:
            # Validate single file
            is_valid, errors = validator.validate_file(file_path, strict=args.strict)
            if not is_valid:
                all_valid = False
            if not args.quiet or not is_valid:
                print(format_validation_result(file_path, is_valid, errors, args.format))
    
    # Exit with appropriate code
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()