#!/usr/bin/env python3
"""
Emby/Jellyfin NFO to NFO Standard Converter
Converts Emby or Jellyfin NFO files to NFO Standard format.
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


class EmbyToNFOConverter:
    """Converts Emby/Jellyfin NFO files to NFO Standard format."""
    
    NAMESPACE = "NFOStandard"
    SCHEMA_LOCATION = "NFOStandard https://xsd.nfostandard.com/main.xsd"
    
    def __init__(self):
        ET.register_namespace("", self.NAMESPACE)
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    
    def convert_file(self, input_path: str, output_path: Optional[str] = None) -> bool:
        """Convert a single Emby/Jellyfin NFO file to NFO Standard."""
        try:
            # Parse Emby NFO
            tree = ET.parse(input_path)
            emby_root = tree.getroot()
            
            # Determine media type
            media_type = self._determine_media_type(emby_root)
            if not media_type:
                print(f"Warning: Could not determine media type for {input_path}")
                return False
            
            # Create NFO Standard structure
            nfo_root = self._create_nfo_structure(emby_root, media_type)
            
            # Output
            if output_path is None:
                output_path = input_path.replace('.nfo', '_converted.nfo')
            
            self._write_xml(nfo_root, output_path)
            return True
            
        except Exception as e:
            print(f"Error converting {input_path}: {e}")
            return False
    
    def _determine_media_type(self, root: ET.Element) -> Optional[str]:
        """Determine media type from Emby/Jellyfin NFO."""
        tag = root.tag.lower()
        
        # Direct mappings
        if tag in ['movie', 'musicvideo']:
            return tag
        elif tag == 'series':
            return 'tvshow'
        elif tag == 'episode':
            return 'episode'
        elif tag == 'album':
            return 'music'
        elif tag == 'artist':
            return 'artist'
        
        # Check for type indicators
        if root.find('SeriesName') is not None:
            return 'tvshow'
        elif root.find('EpisodeNumber') is not None:
            return 'episode'
        
        return None
    
    def _create_nfo_structure(self, emby_root: ET.Element, media_type: str) -> ET.Element:
        """Create NFO Standard structure from Emby/Jellyfin data."""
        # Create root element
        root = ET.Element("{%s}root" % self.NAMESPACE)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", self.SCHEMA_LOCATION)
        
        # Create media element
        media_elem = ET.SubElement(root, "media")
        media_type_elem = ET.SubElement(media_elem, media_type)
        
        # Convert fields based on media type
        if media_type == 'movie':
            self._convert_movie(emby_root, media_type_elem)
        elif media_type == 'tvshow':
            self._convert_tvshow(emby_root, media_type_elem)
        elif media_type == 'episode':
            self._convert_episode(emby_root, media_type_elem)
        elif media_type == 'music':
            self._convert_music(emby_root, media_type_elem)
        
        # Add library section for Emby-specific data
        library_elem = ET.SubElement(root, "library")
        self._add_library_data(emby_root, library_elem)
        
        return root
    
    def _convert_movie(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert Emby movie fields to NFO Standard."""
        # Direct field mappings
        field_mappings = {
            'title': 'title',
            'originaltitle': 'originaltitle',
            'sorttitle': 'sorttitle',
            'outline': 'outline',
            'plot': 'plot',
            'tagline': 'tagline',
            'runtime': 'runtime',
            'year': 'year',
            'premiered': 'releasedate',
            'releasedate': 'releasedate',
            'genre': 'genre',
            'tag': 'tag',
            'country': 'country',
            'studio': 'productioncompany',
            'director': 'director'
        }
        
        for emby_field, nfo_field in field_mappings.items():
            self._copy_field(emby_elem, nfo_elem, emby_field, nfo_field)
        
        # Special conversions
        self._convert_ratings(emby_elem, nfo_elem)
        self._convert_content_rating(emby_elem, nfo_elem)
        self._convert_ids(emby_elem, nfo_elem)
        self._convert_people(emby_elem, nfo_elem)
        self._convert_images(emby_elem, nfo_elem)
        self._convert_collections(emby_elem, nfo_elem)
    
    def _convert_tvshow(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert Emby TV show fields to NFO Standard."""
        # Handle both 'Series' and 'tvshow' root tags
        field_mappings = {
            'title': 'title',
            'SeriesName': 'title',
            'originaltitle': 'originaltitle',
            'sorttitle': 'sorttitle',
            'plot': 'plot',
            'outline': 'outline',
            'tagline': 'tagline',
            'runtime': 'runtime',
            'year': 'year',
            'premiered': 'premiered',
            'status': 'status',
            'Status': 'status',
            'genre': 'genre',
            'tag': 'tag',
            'country': 'country',
            'studio': 'studio',
            'network': 'studio',
            'Network': 'studio'
        }
        
        for emby_field, nfo_field in field_mappings.items():
            self._copy_field(emby_elem, nfo_elem, emby_field, nfo_field)
        
        # Air time/day
        self._convert_air_schedule(emby_elem, nfo_elem)
        
        # Special conversions
        self._convert_ratings(emby_elem, nfo_elem)
        self._convert_content_rating(emby_elem, nfo_elem)
        self._convert_ids(emby_elem, nfo_elem)
        self._convert_people(emby_elem, nfo_elem)
        self._convert_images(emby_elem, nfo_elem)
    
    def _convert_episode(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert Emby episode fields to NFO Standard."""
        field_mappings = {
            'title': 'title',
            'EpisodeName': 'title',
            'plot': 'plot',
            'runtime': 'runtime',
            'aired': 'aired',
            'FirstAired': 'aired',
            'season': 'season',
            'SeasonNumber': 'season',
            'episode': 'episode',
            'EpisodeNumber': 'episode',
            'director': 'director',
            'writer': 'writer'
        }
        
        for emby_field, nfo_field in field_mappings.items():
            self._copy_field(emby_elem, nfo_elem, emby_field, nfo_field)
        
        self._convert_ratings(emby_elem, nfo_elem)
        self._convert_people(emby_elem, nfo_elem)
        self._convert_images(emby_elem, nfo_elem)
    
    def _convert_music(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert Emby music/album fields to NFO Standard."""
        field_mappings = {
            'title': 'title',
            'album': 'album',
            'artist': 'artist',
            'albumartist': 'albumartist',
            'year': 'year',
            'genre': 'genre',
            'style': 'style',
            'mood': 'mood',
            'compilation': 'compilation',
            'label': 'label',
            'releasedate': 'releasedate'
        }
        
        for emby_field, nfo_field in field_mappings.items():
            self._copy_field(emby_elem, nfo_elem, emby_field, nfo_field)
        
        self._convert_ratings(emby_elem, nfo_elem)
        self._convert_images(emby_elem, nfo_elem)
    
    def _copy_field(self, source: ET.Element, target: ET.Element, 
                    source_field: str, target_field: str):
        """Copy field from source to target, handling multiple values."""
        elements = source.findall(source_field)
        for elem in elements:
            if elem.text and elem.text.strip():
                ET.SubElement(target, target_field).text = elem.text.strip()
    
    def _convert_ratings(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert Emby ratings to NFO Standard format."""
        # Main rating
        rating = emby_elem.find('rating')
        if rating is not None and rating.text:
            rating_elem = ET.SubElement(nfo_elem, 'rating')
            rating_elem.set('name', 'emby')
            rating_elem.set('value', rating.text)
            rating_elem.set('max', '10')
            rating_elem.set('default', 'true')
        
        # Critic rating
        critic_rating = emby_elem.find('criticrating')
        if critic_rating is not None and critic_rating.text:
            rating_elem = ET.SubElement(nfo_elem, 'rating')
            rating_elem.set('name', 'critic')
            rating_elem.set('value', str(float(critic_rating.text) / 10))  # Convert from 0-100 to 0-10
            rating_elem.set('max', '10')
        
        # Custom rating
        custom_rating = emby_elem.find('customrating')
        if custom_rating is not None and custom_rating.text:
            rating_elem = ET.SubElement(nfo_elem, 'rating')
            rating_elem.set('name', 'custom')
            rating_elem.set('value', custom_rating.text)
            rating_elem.set('max', '10')
        
        # User rating
        user_rating = emby_elem.find('userrating')
        if user_rating is not None and user_rating.text:
            ET.SubElement(nfo_elem, 'userrating').text = user_rating.text
    
    def _convert_content_rating(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert content rating/MPAA rating."""
        mpaa = emby_elem.find('mpaa')
        if mpaa is None:
            mpaa = emby_elem.find('contentrating')
        
        if mpaa is not None and mpaa.text:
            content_elem = ET.SubElement(nfo_elem, 'contentrating')
            
            # Try to parse rating
            rating_text = mpaa.text.strip()
            
            # US ratings
            if rating_text in ['G', 'PG', 'PG-13', 'R', 'NC-17']:
                content_elem.set('country', 'USA')
                content_elem.set('board', 'MPAA')
                content_elem.set('rating', rating_text)
            # TV ratings
            elif rating_text.startswith('TV-'):
                content_elem.set('country', 'USA')
                content_elem.set('board', 'TV')
                content_elem.set('rating', rating_text)
            else:
                content_elem.set('rating', rating_text)
    
    def _convert_ids(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert various ID fields."""
        # Direct ID fields
        id_mappings = {
            'imdb': 'imdb',
            'imdbid': 'imdb',
            'tmdb': 'tmdb',
            'tmdbid': 'tmdb',
            'tvdb': 'tvdb',
            'tvdbid': 'tvdb'
        }
        
        default_set = False
        for emby_field, id_type in id_mappings.items():
            elem = emby_elem.find(emby_field)
            if elem is not None and elem.text:
                uniqueid = ET.SubElement(nfo_elem, 'uniqueid')
                uniqueid.set('type', id_type)
                if not default_set and id_type == 'imdb':
                    uniqueid.set('default', 'true')
                    default_set = True
                uniqueid.text = elem.text
        
        # Provider IDs
        provider_ids = emby_elem.findall('provider')
        for provider in provider_ids:
            name = provider.get('name')
            if name and provider.text:
                uniqueid = ET.SubElement(nfo_elem, 'uniqueid')
                uniqueid.set('type', name.lower())
                uniqueid.text = provider.text
    
    def _convert_people(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert people (actors, directors, etc.)."""
        # Actors
        actors = emby_elem.findall('actor')
        for i, actor in enumerate(actors):
            actor_elem = ET.SubElement(nfo_elem, 'actor')
            
            name = actor.find('name')
            if name is not None and name.text:
                ET.SubElement(actor_elem, 'name').text = name.text
            
            role = actor.find('role')
            if role is not None and role.text:
                ET.SubElement(actor_elem, 'role').text = role.text
            
            # Order
            order = actor.find('sortorder')
            if order is not None and order.text:
                ET.SubElement(actor_elem, 'order').text = str(int(order.text) + 1)
            else:
                ET.SubElement(actor_elem, 'order').text = str(i + 1)
            
            # Image
            image = actor.find('imageurl')
            if image is None:
                image = actor.find('thumb')
            if image is not None and image.text:
                ET.SubElement(actor_elem, 'thumb').text = image.text
        
        # Directors
        directors = emby_elem.findall('director')
        for director in directors:
            if director.text:
                director_elem = ET.SubElement(nfo_elem, 'director')
                ET.SubElement(director_elem, 'name').text = director.text
        
        # Writers
        writers = emby_elem.findall('writer')
        for writer in writers:
            if writer.text:
                writer_elem = ET.SubElement(nfo_elem, 'writer')
                ET.SubElement(writer_elem, 'name').text = writer.text
    
    def _convert_images(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert image references."""
        # Poster/thumb
        for field in ['poster', 'thumb']:
            elem = emby_elem.find(field)
            if elem is not None and elem.text:
                thumb = ET.SubElement(nfo_elem, 'thumb')
                thumb.set('type', 'poster')
                thumb.set('url', elem.text)
        
        # Fanart/backdrop
        for field in ['fanart', 'backdrop']:
            elem = emby_elem.find(field)
            if elem is not None and elem.text:
                fanart = ET.SubElement(nfo_elem, 'fanart')
                fanart.set('type', 'background')
                fanart.set('url', elem.text)
        
        # Banner
        banner = emby_elem.find('banner')
        if banner is not None and banner.text:
            banner_elem = ET.SubElement(nfo_elem, 'banner')
            banner_elem.set('type', 'banner')
            banner_elem.set('url', banner.text)
    
    def _convert_collections(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert collection/set information."""
        # Set/collection
        set_elem = emby_elem.find('set')
        if set_elem is not None:
            set_name = set_elem.find('name')
            if set_name is not None and set_name.text:
                ET.SubElement(nfo_elem, 'setname').text = set_name.text
            
            set_overview = set_elem.find('overview')
            if set_overview is not None and set_overview.text:
                ET.SubElement(nfo_elem, 'setoverview').text = set_overview.text
        
        # Collection number/order
        collection_number = emby_elem.find('collectionnumber')
        if collection_number is not None and collection_number.text:
            ET.SubElement(nfo_elem, 'setorder').text = collection_number.text
    
    def _convert_air_schedule(self, emby_elem: ET.Element, nfo_elem: ET.Element):
        """Convert TV show air schedule."""
        air_day = emby_elem.find('Airs_DayOfWeek')
        air_time = emby_elem.find('Airs_Time')
        
        if air_day is not None or air_time is not None:
            schedule = ET.SubElement(nfo_elem, 'schedule')
            
            if air_day is not None and air_day.text:
                ET.SubElement(schedule, 'airday').text = air_day.text
            
            if air_time is not None and air_time.text:
                # Convert time format
                time_text = air_time.text.strip()
                # Try to convert to 24-hour format
                try:
                    from datetime import datetime
                    dt = datetime.strptime(time_text, '%I:%M %p')
                    time_24 = dt.strftime('%H:%M')
                    ET.SubElement(schedule, 'airtime').text = time_24
                except:
                    ET.SubElement(schedule, 'airtime').text = time_text
    
    def _add_library_data(self, emby_elem: ET.Element, library_elem: ET.Element):
        """Add Emby-specific data to library section."""
        # Source type
        ET.SubElement(library_elem, 'type').text = 'emby'
        
        # Locked fields
        locked_fields = emby_elem.find('lockedfields')
        if locked_fields is not None and locked_fields.text:
            locked_elem = ET.SubElement(library_elem, 'lockedfields')
            for field in locked_fields.text.split('|'):
                ET.SubElement(locked_elem, 'field').text = field.strip()
        
        # Added date
        dateadded = emby_elem.find('dateadded')
        if dateadded is not None and dateadded.text:
            ET.SubElement(library_elem, 'dateadded').text = dateadded.text
        
        # Play count
        playcount = emby_elem.find('playcount')
        if playcount is not None and playcount.text:
            ET.SubElement(library_elem, 'playcount').text = playcount.text
        
        # Last played
        lastplayed = emby_elem.find('lastplayed')
        if lastplayed is not None and lastplayed.text:
            ET.SubElement(library_elem, 'lastplayed').text = lastplayed.text
    
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
                backup_path = str(nfo_file) + '.emby.backup'
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
        description="Convert Emby/Jellyfin NFO files to NFO Standard format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s movie.nfo
  %(prog)s tvshow.nfo -o tvshow_standard.nfo
  %(prog)s /path/to/library/ --recursive
  %(prog)s /path/to/library/ --in-place --backup
        """
    )
    
    parser.add_argument('input', help='Input Emby/Jellyfin NFO file or directory')
    parser.add_argument('-o', '--output', help='Output file or directory')
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Process directories recursively')
    parser.add_argument('--in-place', action='store_true',
                       help='Convert files in place (creates .backup files)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    converter = EmbyToNFOConverter()
    
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