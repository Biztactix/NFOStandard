#!/usr/bin/env python3
"""
Plex to NFO Standard Exporter
Exports metadata from Plex Media Server to NFO Standard format.
"""

import argparse
import sys
import os
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

try:
    from plexapi.server import PlexServer
    from plexapi.exceptions import NotFound
    HAS_PLEXAPI = True
except ImportError:
    HAS_PLEXAPI = False
    print("Warning: plexapi not installed. Install with: pip install plexapi")


class PlexToNFOExporter:
    """Exports Plex metadata to NFO Standard format."""
    
    NAMESPACE = "NFOStandard"
    SCHEMA_LOCATION = "NFOStandard https://xsd.nfostandard.com/main.xsd"
    
    def __init__(self, plex_url: str, plex_token: str):
        if not HAS_PLEXAPI:
            raise ImportError("plexapi is required. Install with: pip install plexapi")
        
        self.plex = PlexServer(plex_url, plex_token)
        ET.register_namespace("", self.NAMESPACE)
        ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    
    def export_library(self, library_name: str, output_dir: str, 
                      flatten: bool = False) -> Dict[str, bool]:
        """Export an entire Plex library to NFO files."""
        results = {}
        
        try:
            library = self.plex.library.section(library_name)
        except NotFound:
            print(f"Error: Library '{library_name}' not found")
            return results
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Process based on library type
        if library.type == 'movie':
            results = self._export_movies(library, output_dir, flatten)
        elif library.type == 'show':
            results = self._export_shows(library, output_dir, flatten)
        elif library.type == 'artist':
            results = self._export_music(library, output_dir, flatten)
        else:
            print(f"Warning: Unsupported library type '{library.type}'")
        
        return results
    
    def _export_movies(self, library, output_dir: str, flatten: bool) -> Dict[str, bool]:
        """Export movie library."""
        results = {}
        
        for movie in library.all():
            try:
                # Create NFO structure
                nfo_root = self._create_movie_nfo(movie)
                
                # Determine output path
                if flatten:
                    filename = self._sanitize_filename(f"{movie.title} ({movie.year}).nfo")
                    output_path = os.path.join(output_dir, filename)
                else:
                    # Create movie folder
                    movie_dir = self._sanitize_filename(f"{movie.title} ({movie.year})")
                    movie_path = os.path.join(output_dir, movie_dir)
                    os.makedirs(movie_path, exist_ok=True)
                    output_path = os.path.join(movie_path, "movie.nfo")
                
                # Write NFO
                self._write_xml(nfo_root, output_path)
                results[movie.title] = True
                
                # Export images if not flattening
                if not flatten:
                    self._export_images(movie, os.path.dirname(output_path))
                
            except Exception as e:
                print(f"Error exporting '{movie.title}': {e}")
                results[movie.title] = False
        
        return results
    
    def _export_shows(self, library, output_dir: str, flatten: bool) -> Dict[str, bool]:
        """Export TV show library."""
        results = {}
        
        for show in library.all():
            try:
                show_dir = self._sanitize_filename(show.title)
                show_path = os.path.join(output_dir, show_dir)
                os.makedirs(show_path, exist_ok=True)
                
                # Export show NFO
                show_nfo = self._create_tvshow_nfo(show)
                self._write_xml(show_nfo, os.path.join(show_path, "tvshow.nfo"))
                results[show.title] = True
                
                # Export seasons and episodes
                for season in show.seasons():
                    if season.seasonNumber:
                        season_dir = f"Season {season.seasonNumber:02d}"
                        season_path = os.path.join(show_path, season_dir)
                        os.makedirs(season_path, exist_ok=True)
                        
                        # Export episodes
                        for episode in season.episodes():
                            try:
                                episode_nfo = self._create_episode_nfo(episode, show)
                                episode_filename = self._get_episode_filename(show, season, episode)
                                episode_nfo_path = os.path.join(season_path, f"{episode_filename}.nfo")
                                self._write_xml(episode_nfo, episode_nfo_path)
                            except Exception as e:
                                print(f"Error exporting episode '{episode.title}': {e}")
                
                # Export images
                self._export_images(show, show_path)
                
            except Exception as e:
                print(f"Error exporting show '{show.title}': {e}")
                results[show.title] = False
        
        return results
    
    def _export_music(self, library, output_dir: str, flatten: bool) -> Dict[str, bool]:
        """Export music library."""
        results = {}
        
        for artist in library.all():
            try:
                artist_dir = self._sanitize_filename(artist.title)
                artist_path = os.path.join(output_dir, artist_dir)
                os.makedirs(artist_path, exist_ok=True)
                
                # Export albums
                for album in artist.albums():
                    try:
                        album_nfo = self._create_album_nfo(album, artist)
                        album_dir = self._sanitize_filename(album.title)
                        album_path = os.path.join(artist_path, album_dir)
                        os.makedirs(album_path, exist_ok=True)
                        
                        self._write_xml(album_nfo, os.path.join(album_path, "album.nfo"))
                        results[f"{artist.title} - {album.title}"] = True
                        
                        # Export album images
                        self._export_images(album, album_path)
                        
                    except Exception as e:
                        print(f"Error exporting album '{album.title}': {e}")
                        results[f"{artist.title} - {album.title}"] = False
                
            except Exception as e:
                print(f"Error exporting artist '{artist.title}': {e}")
                results[artist.title] = False
        
        return results
    
    def _create_movie_nfo(self, movie) -> ET.Element:
        """Create NFO for a movie."""
        # Create root structure
        root = ET.Element("{%s}root" % self.NAMESPACE)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", self.SCHEMA_LOCATION)
        
        media = ET.SubElement(root, "media")
        movie_elem = ET.SubElement(media, "movie")
        
        # Basic fields
        ET.SubElement(movie_elem, "title").text = movie.title
        if movie.originalTitle:
            ET.SubElement(movie_elem, "originaltitle").text = movie.originalTitle
        if movie.year:
            ET.SubElement(movie_elem, "year").text = str(movie.year)
        if movie.summary:
            ET.SubElement(movie_elem, "plot").text = movie.summary
        if movie.tagline:
            ET.SubElement(movie_elem, "tagline").text = movie.tagline
        if movie.duration:
            ET.SubElement(movie_elem, "runtime").text = str(movie.duration // 60000)  # ms to minutes
        
        # Ratings
        if movie.rating:
            rating = ET.SubElement(movie_elem, "rating")
            rating.set("name", "plex")
            rating.set("value", str(movie.rating))
            rating.set("max", "10")
            rating.set("default", "true")
        
        if movie.audienceRating:
            rating = ET.SubElement(movie_elem, "rating")
            rating.set("name", "audience")
            rating.set("value", str(movie.audienceRating))
            rating.set("max", "10")
        
        # Content rating
        if movie.contentRating:
            content = ET.SubElement(movie_elem, "contentrating")
            content.set("rating", movie.contentRating)
            # Try to determine country/board
            if movie.contentRating in ['G', 'PG', 'PG-13', 'R', 'NC-17']:
                content.set("country", "USA")
                content.set("board", "MPAA")
        
        # Genres
        for genre in movie.genres:
            ET.SubElement(movie_elem, "genre").text = genre.tag
        
        # Countries
        for country in movie.countries:
            ET.SubElement(movie_elem, "country").text = country.tag
        
        # Studios
        if hasattr(movie, 'studio') and movie.studio:
            ET.SubElement(movie_elem, "productioncompany").text = movie.studio
        
        # Collections
        for collection in movie.collections:
            ET.SubElement(movie_elem, "setname").text = collection.tag
        
        # People
        self._add_people(movie, movie_elem)
        
        # IDs
        self._add_guids(movie, movie_elem)
        
        # Library metadata
        library = ET.SubElement(root, "library")
        self._add_library_metadata(movie, library)
        
        return root
    
    def _create_tvshow_nfo(self, show) -> ET.Element:
        """Create NFO for a TV show."""
        root = ET.Element("{%s}root" % self.NAMESPACE)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", self.SCHEMA_LOCATION)
        
        media = ET.SubElement(root, "media")
        show_elem = ET.SubElement(media, "tvshow")
        
        # Basic fields
        ET.SubElement(show_elem, "title").text = show.title
        if show.originalTitle:
            ET.SubElement(show_elem, "originaltitle").text = show.originalTitle
        if show.year:
            ET.SubElement(show_elem, "year").text = str(show.year)
        if show.summary:
            ET.SubElement(show_elem, "plot").text = show.summary
        if hasattr(show, 'tagline') and show.tagline:
            ET.SubElement(show_elem, "tagline").text = show.tagline
        
        # Dates
        if hasattr(show, 'originallyAvailableAt') and show.originallyAvailableAt:
            ET.SubElement(show_elem, "premiered").text = show.originallyAvailableAt.strftime('%Y-%m-%d')
        
        # Studio/Network
        if hasattr(show, 'studio') and show.studio:
            ET.SubElement(show_elem, "studio").text = show.studio
        if hasattr(show, 'network') and show.network:
            ET.SubElement(show_elem, "studio").text = show.network
        
        # Ratings
        if show.rating:
            rating = ET.SubElement(show_elem, "rating")
            rating.set("name", "plex")
            rating.set("value", str(show.rating))
            rating.set("max", "10")
            rating.set("default", "true")
        
        # Content rating
        if show.contentRating:
            content = ET.SubElement(show_elem, "contentrating")
            content.set("rating", show.contentRating)
            if show.contentRating.startswith('TV-'):
                content.set("country", "USA")
                content.set("board", "TV")
        
        # Genres
        for genre in show.genres:
            ET.SubElement(show_elem, "genre").text = genre.tag
        
        # Episode/Season counts
        ET.SubElement(show_elem, "season").text = str(show.childCount)  # Number of seasons
        leaf_count = sum(season.leafCount for season in show.seasons())
        ET.SubElement(show_elem, "episode").text = str(leaf_count)  # Total episodes
        
        # People
        self._add_people(show, show_elem)
        
        # IDs
        self._add_guids(show, show_elem)
        
        # Library metadata
        library = ET.SubElement(root, "library")
        self._add_library_metadata(show, library)
        
        return root
    
    def _create_episode_nfo(self, episode, show) -> ET.Element:
        """Create NFO for an episode."""
        root = ET.Element("{%s}root" % self.NAMESPACE)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", self.SCHEMA_LOCATION)
        
        media = ET.SubElement(root, "media")
        ep_elem = ET.SubElement(media, "episode")
        
        # Basic fields
        ET.SubElement(ep_elem, "title").text = episode.title
        ET.SubElement(ep_elem, "showtitle").text = show.title
        ET.SubElement(ep_elem, "season").text = str(episode.seasonNumber)
        ET.SubElement(ep_elem, "episode").text = str(episode.episodeNumber)
        
        if episode.summary:
            ET.SubElement(ep_elem, "plot").text = episode.summary
        if episode.duration:
            ET.SubElement(ep_elem, "runtime").text = str(episode.duration // 60000)
        
        # Air date
        if hasattr(episode, 'originallyAvailableAt') and episode.originallyAvailableAt:
            ET.SubElement(ep_elem, "aired").text = episode.originallyAvailableAt.strftime('%Y-%m-%d')
        
        # Ratings
        if episode.rating:
            rating = ET.SubElement(ep_elem, "rating")
            rating.set("name", "plex")
            rating.set("value", str(episode.rating))
            rating.set("max", "10")
        
        # Directors/Writers
        for director in episode.directors:
            dir_elem = ET.SubElement(ep_elem, "director")
            ET.SubElement(dir_elem, "name").text = director.tag
        
        for writer in episode.writers:
            writer_elem = ET.SubElement(ep_elem, "writer")
            ET.SubElement(writer_elem, "name").text = writer.tag
        
        # IDs
        self._add_guids(episode, ep_elem)
        
        return root
    
    def _create_album_nfo(self, album, artist) -> ET.Element:
        """Create NFO for a music album."""
        root = ET.Element("{%s}root" % self.NAMESPACE)
        root.set("{http://www.w3.org/2001/XMLSchema-instance}schemaLocation", self.SCHEMA_LOCATION)
        
        media = ET.SubElement(root, "media")
        music_elem = ET.SubElement(media, "music")
        
        # Basic fields
        ET.SubElement(music_elem, "title").text = album.title
        ET.SubElement(music_elem, "artist").text = artist.title
        ET.SubElement(music_elem, "album").text = album.title
        
        if album.year:
            ET.SubElement(music_elem, "year").text = str(album.year)
        
        # Genres
        for genre in album.genres:
            ET.SubElement(music_elem, "genre").text = genre.tag
        
        # Tracks
        for track in album.tracks():
            track_elem = ET.SubElement(music_elem, "track")
            ET.SubElement(track_elem, "position").text = str(track.index)
            ET.SubElement(track_elem, "title").text = track.title
            if track.duration:
                ET.SubElement(track_elem, "duration").text = str(track.duration // 1000)  # ms to seconds
        
        # Rating
        if album.rating:
            rating = ET.SubElement(music_elem, "rating")
            rating.set("name", "plex")
            rating.set("value", str(album.rating))
            rating.set("max", "10")
        
        return root
    
    def _add_people(self, media_item, elem: ET.Element):
        """Add people (actors, directors, etc.) to element."""
        # Actors
        if hasattr(media_item, 'actors'):
            for i, actor in enumerate(media_item.actors):
                actor_elem = ET.SubElement(elem, "actor")
                ET.SubElement(actor_elem, "name").text = actor.tag
                if hasattr(actor, 'role') and actor.role:
                    ET.SubElement(actor_elem, "role").text = actor.role
                ET.SubElement(actor_elem, "order").text = str(i + 1)
                if hasattr(actor, 'thumb') and actor.thumb:
                    ET.SubElement(actor_elem, "thumb").text = actor.thumb
        
        # Directors
        if hasattr(media_item, 'directors'):
            for director in media_item.directors:
                dir_elem = ET.SubElement(elem, "director")
                ET.SubElement(dir_elem, "name").text = director.tag
        
        # Writers
        if hasattr(media_item, 'writers'):
            for writer in media_item.writers:
                writer_elem = ET.SubElement(elem, "writer")
                ET.SubElement(writer_elem, "name").text = writer.tag
    
    def _add_guids(self, media_item, elem: ET.Element):
        """Add unique IDs from Plex GUIDs."""
        if hasattr(media_item, 'guids'):
            default_set = False
            for guid in media_item.guids:
                # Parse GUID format (e.g., "imdb://tt1234567")
                if '://' in guid.id:
                    source, value = guid.id.split('://', 1)
                    uniqueid = ET.SubElement(elem, "uniqueid")
                    uniqueid.set("type", source)
                    uniqueid.text = value
                    
                    if source == 'imdb' and not default_set:
                        uniqueid.set("default", "true")
                        default_set = True
    
    def _add_library_metadata(self, media_item, library_elem: ET.Element):
        """Add Plex-specific library metadata."""
        ET.SubElement(library_elem, "type").text = "plex"
        
        # View count
        if hasattr(media_item, 'viewCount') and media_item.viewCount:
            ET.SubElement(library_elem, "viewcount").text = str(media_item.viewCount)
        
        # Last viewed
        if hasattr(media_item, 'lastViewedAt') and media_item.lastViewedAt:
            ET.SubElement(library_elem, "lastviewed").text = media_item.lastViewedAt.isoformat()
        
        # Added date
        if hasattr(media_item, 'addedAt') and media_item.addedAt:
            ET.SubElement(library_elem, "addeddate").text = media_item.addedAt.isoformat()
        
        # User rating
        if hasattr(media_item, 'userRating') and media_item.userRating:
            ET.SubElement(library_elem, "userrating").text = str(media_item.userRating)
    
    def _export_images(self, media_item, output_dir: str):
        """Export poster and fanart images."""
        try:
            # Poster
            if hasattr(media_item, 'posterUrl') and media_item.posterUrl:
                poster_path = os.path.join(output_dir, "poster.jpg")
                media_item.savePoster(poster_path)
            
            # Fanart/Background
            if hasattr(media_item, 'artUrl') and media_item.artUrl:
                fanart_path = os.path.join(output_dir, "fanart.jpg")
                media_item.saveArt(fanart_path)
            
            # Banner
            if hasattr(media_item, 'bannerUrl') and media_item.bannerUrl:
                banner_path = os.path.join(output_dir, "banner.jpg")
                media_item.saveBanner(banner_path)
            
        except Exception as e:
            print(f"Warning: Could not export images: {e}")
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem."""
        # Remove/replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename.strip()
    
    def _get_episode_filename(self, show, season, episode) -> str:
        """Generate episode filename."""
        return f"{self._sanitize_filename(show.title)} - S{season.seasonNumber:02d}E{episode.episodeNumber:02d}"
    
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


def main():
    parser = argparse.ArgumentParser(
        description="Export Plex metadata to NFO Standard format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --server http://localhost:32400 --token YOUR-TOKEN --library Movies
  %(prog)s --server http://plex.local:32400 --token YOUR-TOKEN --library "TV Shows" --output /nfo/tv/
  %(prog)s --config plex.conf --library Music --flatten
        """
    )
    
    parser.add_argument('--server', help='Plex server URL (e.g., http://localhost:32400)')
    parser.add_argument('--token', help='Plex authentication token')
    parser.add_argument('--config', help='Config file with server and token')
    parser.add_argument('--library', required=True, help='Plex library name to export')
    parser.add_argument('--output', default='./plex_export', 
                       help='Output directory (default: ./plex_export)')
    parser.add_argument('--flatten', action='store_true',
                       help='Export all files to single directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Get server and token
    if args.config:
        # Read from config file
        import configparser
        config = configparser.ConfigParser()
        config.read(args.config)
        server_url = config.get('plex', 'server', fallback=None)
        token = config.get('plex', 'token', fallback=None)
    else:
        server_url = args.server
        token = args.token
    
    if not server_url or not token:
        print("Error: Plex server URL and token are required")
        print("Provide via --server and --token or --config file")
        sys.exit(1)
    
    if not HAS_PLEXAPI:
        print("Error: plexapi is required. Install with: pip install plexapi")
        sys.exit(1)
    
    try:
        # Create exporter
        exporter = PlexToNFOExporter(server_url, token)
        
        # Export library
        print(f"Exporting library '{args.library}' to {args.output}")
        results = exporter.export_library(args.library, args.output, flatten=args.flatten)
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        print(f"\nExport Summary:")
        print(f"  Total items: {len(results)}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {failed}")
        
        if failed > 0 and args.verbose:
            print("\nFailed items:")
            for item, success in results.items():
                if not success:
                    print(f"  - {item}")
        
        sys.exit(0 if failed == 0 else 1)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()