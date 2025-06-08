#!/usr/bin/env python3
"""
Kodi NFO to NFO Standard Converter
Converts Kodi/XBMC NFO files to NFO Standard format.
"""

import argparse
import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any, Optional
import re
from datetime import datetime


class KodiToNFOConverter:
    """Converts Kodi NFO files to NFO Standard format."""
    
    NAMESPACE = "NFOStandard"
    SCHEMA_LOCATION = "NFOStandard https://xsd.nfostandard.com/main.xsd"
    
    # Field mappings from Kodi to NFO Standard
    FIELD_MAPPINGS = {
        'movie': {
            'title': 'title',
            'originaltitle': 'originaltitle',
            'sorttitle': 'sorttitle',
            'set': 'setname',
            'year': 'year',
            'trailer': 'trailer',
            'outline': 'outline',
            'plot': 'plot',
            'tagline': 'tagline',
            'runtime': 'runtime',
            'releasedate': 'releasedate',
            'studio': 'productioncompany',
            'genre': 'genre',
            'tag': 'tag',
            'country': 'country',
            'credits': 'writer',
            'director': 'director',
            'actor': 'actor'
        },
        'tvshow': {
            'title': 'title',
            'showtitle': 'title',
            'originaltitle': 'originaltitle',
            'sorttitle': 'sorttitle',
            'year': 'year',
            'plot': 'plot',
            'outline': 'outline',
            'tagline': 'tagline',
            'runtime': 'runtime',
            'premiered': 'premiered',
            'status': 'status',
            'studio': 'studio',
            'genre': 'genre',
            'tag': 'tag',
            'actor': 'actor'
        }
    }
    
    def __init__(self):
        ET.register_namespace("", self.NAMESPACE)
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    
    def convert_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Convert a single Kodi NFO file to NFO Standard."""
        try:
            # Parse Kodi NFO
            tree = ET.parse(input_path)
            kodi_root = tree.getroot()
            
            # Determine media type
            media_type = kodi_root.tag.lower()
            if media_type not in ['movie', 'tvshow', 'episodedetails', 'musicvideo']:
                print(f"Warning: Unknown media type '{media_type}'")
                return False
            
            # Create NFO Standard structure
            nfo_root = self._create_nfo_structure(kodi_root, media_type)
            
            # Output
            if output_path is None:
                output_path = input_path.replace('.nfo', '_converted.nfo')
            
            self._write_xml(nfo_root, output_path)
            return True
            
        except Exception as e:
            print(f"Error converting {input_path}: {e}")
            return False
    
    def _create_nfo_structure(self, kodi_root: ET.Element, media_type: str) -> ET.Element:
        """Create NFO Standard structure from Kodi data."""
        # Create root element
        root = ET.Element("{%s}root" % self.NAMESPACE)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", self.SCHEMA_LOCATION)
        
        # Create media element
        media_elem = ET.SubElement(root, "media")
        
        # Create media type element
        if media_type == 'episodedetails':
            media_type_elem = ET.SubElement(media_elem, 'episode')
        else:
            media_type_elem = ET.SubElement(media_elem, media_type)
        
        # Convert fields
        self._convert_fields(kodi_root, media_type_elem, media_type)
        
        # Add library section for Kodi-specific data
        library_elem = ET.SubElement(root, "library")
        self._add_library_data(kodi_root, library_elem)
        
        return root
    
    def _convert_fields(self, kodi_elem: ET.Element, nfo_elem: ET.Element, media_type: str):
        """Convert Kodi fields to NFO Standard."""
        mappings = self.FIELD_MAPPINGS.get(media_type, {})
        
        for kodi_field, nfo_field in mappings.items():
            kodi_values = kodi_elem.findall(kodi_field)
            for value in kodi_values:
                if value.text:
                    ET.SubElement(nfo_elem, nfo_field).text = value.text
        
        # Special field conversions
        self._convert_rating(kodi_elem, nfo_elem)
        self._convert_mpaa(kodi_elem, nfo_elem)
        self._convert_uniqueids(kodi_elem, nfo_elem)
        self._convert_artwork(kodi_elem, nfo_elem)
        self._convert_actors(kodi_elem, nfo_elem)
        self._convert_fileinfo(kodi_elem, nfo_elem)
    
    def _convert_rating(self, kodi_elem: ET.Element, nfo_elem: ET.Element):
        """Convert Kodi rating to NFO Standard rating structure."""
        rating = kodi_elem.find('rating')
        votes = kodi_elem.find('votes')
        
        if rating is not None and rating.text:
            rating_elem = ET.SubElement(nfo_elem, 'rating')
            rating_elem.set('name', 'imdb')
            rating_elem.set('value', rating.text)
            rating_elem.set('max', '10')
            rating_elem.set('default', 'true')
            
            if votes is not None and votes.text:
                rating_elem.set('votes', votes.text)
        
        # User rating
        userrating = kodi_elem.find('userrating')
        if userrating is not None and userrating.text:
            ET.SubElement(nfo_elem, 'userrating').text = userrating.text
    
    def _convert_mpaa(self, kodi_elem: ET.Element, nfo_elem: ET.Element):
        """Convert MPAA rating to content rating structure."""
        mpaa = kodi_elem.find('mpaa')
        if mpaa is not None and mpaa.text:
            content_rating = ET.SubElement(nfo_elem, 'contentrating')
            
            # Try to parse country and rating
            mpaa_text = mpaa.text.strip()
            if mpaa_text.startswith('Rated '):
                mpaa_text = mpaa_text[6:]
            
            # Common patterns
            if mpaa_text in ['G', 'PG', 'PG-13', 'R', 'NC-17']:
                content_rating.set('country', 'USA')
                content_rating.set('board', 'MPAA')
                content_rating.set('rating', mpaa_text)
            else:
                # Try to extract country
                content_rating.set('rating', mpaa_text)
    
    def _convert_uniqueids(self, kodi_elem: ET.Element, nfo_elem: ET.Element):
        """Convert various ID fields to uniqueid structure."""
        # IMDB ID
        for field in ['id', 'imdbid', 'imdb']:
            elem = kodi_elem.find(field)
            if elem is not None and elem.text:
                uniqueid = ET.SubElement(nfo_elem, 'uniqueid')
                uniqueid.set('type', 'imdb')
                uniqueid.set('default', 'true')
                uniqueid.text = elem.text
                break
        
        # TMDB ID
        tmdbid = kodi_elem.find('tmdbid')
        if tmdbid is not None and tmdbid.text:
            uniqueid = ET.SubElement(nfo_elem, 'uniqueid')
            uniqueid.set('type', 'tmdb')
            uniqueid.text = tmdbid.text
        
        # TVDB ID
        tvdbid = kodi_elem.find('tvdbid')
        if tvdbid is not None and tvdbid.text:
            uniqueid = ET.SubElement(nfo_elem, 'uniqueid')
            uniqueid.set('type', 'tvdb')
            uniqueid.text = tvdbid.text
    
    def _convert_artwork(self, kodi_elem: ET.Element, nfo_elem: ET.Element):
        """Convert Kodi artwork to NFO Standard format."""
        # Thumb/Poster
        thumbs = kodi_elem.findall('thumb')
        for thumb in thumbs:
            if thumb.text:
                thumb_elem = ET.SubElement(nfo_elem, 'thumb')
                thumb_elem.set('type', 'poster')
                thumb_elem.set('url', thumb.text)
                
                # Try to get aspect from attributes
                aspect = thumb.get('aspect')
                if aspect:
                    thumb_elem.set('aspect', aspect)
        
        # Fanart
        fanart = kodi_elem.find('fanart')
        if fanart is not None:
            fanart_thumbs = fanart.findall('thumb')
            for ft in fanart_thumbs:
                if ft.text:
                    fanart_elem = ET.SubElement(nfo_elem, 'fanart')
                    fanart_elem.set('type', 'background')
                    fanart_elem.set('url', ft.text)
    
    def _convert_actors(self, kodi_elem: ET.Element, nfo_elem: ET.Element):
        """Convert actor information."""
        actors = kodi_elem.findall('actor')
        for i, actor in enumerate(actors):
            actor_elem = ET.SubElement(nfo_elem, 'actor')
            
            name = actor.find('name')
            if name is not None and name.text:
                ET.SubElement(actor_elem, 'name').text = name.text
            
            role = actor.find('role')
            if role is not None and role.text:
                ET.SubElement(actor_elem, 'role').text = role.text
            
            thumb = actor.find('thumb')
            if thumb is not None and thumb.text:
                ET.SubElement(actor_elem, 'thumb').text = thumb.text
            
            # Add order
            order = actor.find('order')
            if order is not None and order.text:
                ET.SubElement(actor_elem, 'order').text = order.text
            else:
                ET.SubElement(actor_elem, 'order').text = str(i + 1)
    
    def _convert_fileinfo(self, kodi_elem: ET.Element, nfo_elem: ET.Element):
        """Convert file info and stream details."""
        fileinfo = kodi_elem.find('fileinfo')
        if fileinfo is not None:
            # This should go in library section, not media section
            pass
    
    def _add_library_data(self, kodi_elem: ET.Element, library_elem: ET.Element):
        """Add Kodi-specific data to library section."""
        # Source type
        ET.SubElement(library_elem, 'type').text = 'kodi'
        
        # Play count
        playcount = kodi_elem.find('playcount')
        if playcount is not None and playcount.text:
            ET.SubElement(library_elem, 'playcount').text = playcount.text
        
        # Last played
        lastplayed = kodi_elem.find('lastplayed')
        if lastplayed is not None and lastplayed.text:
            ET.SubElement(library_elem, 'lastplayed').text = lastplayed.text
        
        # File path
        filenameandpath = kodi_elem.find('filenameandpath')
        if filenameandpath is not None and filenameandpath.text:
            ET.SubElement(library_elem, 'filepath').text = filenameandpath.text
        
        # Date added
        dateadded = kodi_elem.find('dateadded')
        if dateadded is not None and dateadded.text:
            ET.SubElement(library_elem, 'dateadded').text = dateadded.text
    
    def _write_xml(self, root: ET.Element, output_path: str):
        """Write XML with pretty formatting."""
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ", encoding=None)
        
        # Remove extra blank lines
        lines = pretty_xml.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        pretty_xml = '\n'.join(non_empty_lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
    
    def convert_directory(self, input_dir: str, output_dir: Optional[str] = None, 
                         recursive: bool = False, in_place: bool = False) -> Dict[str, bool]:
        """Convert all NFO files in a directory."""
        results = {}
        path = Path(input_dir)
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        pattern = '**/*.nfo' if recursive else '*.nfo'
        for nfo_file in path.glob(pattern):
            if in_place:
                output_path = str(nfo_file)
                # Backup original
                backup_path = str(nfo_file) + '.kodi.backup'
                import shutil
                shutil.copy2(nfo_file, backup_path)
            elif output_dir:
                rel_path = nfo_file.relative_to(path)
                output_path = os.path.join(output_dir, rel_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
            else:
                output_path = None
            
            success = self.convert_file(str(nfo_file), output_path)
            results[str(nfo_file)] = success
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Convert Kodi/XBMC NFO files to NFO Standard format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s movie.nfo
  %(prog)s movie.nfo -o movie_standard.nfo
  %(prog)s /path/to/library/ --recursive
  %(prog)s /path/to/library/ --in-place --backup
        """
    )
    
    parser.add_argument('input', help='Input Kodi NFO file or directory')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Process directories recursively')
    parser.add_argument('--in-place', action='store_true',
                       help='Convert files in place (creates .backup files)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    converter = KodiToNFOConverter()
    
    if os.path.isfile(args.input):
        # Single file conversion
        success = converter.convert_file(args.input, args.output)
        if success:
            print(f"Successfully converted: {args.input}")
            if args.output:
                print(f"Output saved to: {args.output}")
        else:
            print(f"Failed to convert: {args.input}")
            sys.exit(1)
    
    elif os.path.isdir(args.input):
        # Directory conversion
        results = converter.convert_directory(
            args.input, 
            args.output,
            recursive=args.recursive,
            in_place=args.in_place
        )
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        print(f"\nConversion Summary:")
        print(f"  Total files: {len(results)}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        
        if failed > 0 and args.verbose:
            print("\nFailed files:")
            for file, success in results.items():
                if not success:
                    print(f"  - {file}")
        
        sys.exit(0 if failed == 0 else 1)
    
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()