#!/usr/bin/env python3
"""
NFO Standard Protobuf Converter
Converts between Protobuf, XML, and JSON formats for NFO Standard data.
"""

import argparse
import sys
import json
import base64
from typing import Dict, Any, Union
from pathlib import Path

# Note: These imports require protobuf installation and compiled proto files
try:
    from google.protobuf import message as protobuf_message
    from google.protobuf import json_format
    HAS_PROTOBUF = True
except ImportError:
    HAS_PROTOBUF = False
    print("Warning: protobuf not installed. Install with: pip install protobuf", file=sys.stderr)

# Import our converters
sys.path.append(str(Path(__file__).parent))
from json_to_xml import JSONToNFOConverter
from xml_to_json import NFOToJSONConverter


class ProtobufConverter:
    """Handles conversion between Protobuf and other formats."""
    
    def __init__(self):
        if not HAS_PROTOBUF:
            raise ImportError("protobuf package is required")
        
        # Import compiled protobuf classes
        try:
            from . import nfo_standard_pb2
            self.pb2 = nfo_standard_pb2
        except ImportError:
            print("Error: Protobuf files not compiled. Run:", file=sys.stderr)
            print("  protoc --python_out=. nfo_standard.proto", file=sys.stderr)
            raise
    
    def json_to_protobuf(self, json_data: Union[str, Dict]) -> bytes:
        """Convert JSON to Protobuf binary format."""
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        # Create root message
        root = self.pb2.NFORoot()
        
        # Determine media type and populate
        media_type = data.get('type', 'movie').lower()
        media_data = data.get(media_type, data)
        
        if media_type == 'movie':
            self._populate_movie(root.media.movie, media_data)
        elif media_type == 'tvshow':
            self._populate_tvshow(root.media.tvshow, media_data)
        elif media_type == 'music':
            self._populate_music(root.media.music, media_data)
        elif media_type == 'audiobook':
            self._populate_audiobook(root.media.audiobook, media_data)
        elif media_type == 'podcast':
            self._populate_podcast(root.media.podcast, media_data)
        elif media_type == 'anime':
            self._populate_anime(root.media.anime, media_data)
        elif media_type == 'adult':
            self._populate_adult(root.media.adult, media_data)
        elif media_type == 'musicvideo':
            self._populate_musicvideo(root.media.musicvideo, media_data)
        elif media_type == 'video':
            self._populate_video(root.media.video, media_data)
        else:
            raise ValueError(f"Unsupported media type: {media_type}")
        
        # Add library metadata if present
        if 'library' in data:
            lib = root.library.add()
            self._populate_library(lib, data['library'])
        
        return root.SerializeToString()
    
    def protobuf_to_json(self, protobuf_data: bytes, compact: bool = False) -> str:
        """Convert Protobuf to JSON."""
        root = self.pb2.NFORoot()
        root.ParseFromString(protobuf_data)
        
        # Use protobuf's JSON formatter
        json_str = json_format.MessageToJson(root, preserving_proto_field_name=True)
        data = json.loads(json_str)
        
        if compact:
            # Extract media type and restructure
            if 'media' in data:
                media = data['media']
                for media_type in ['movie', 'tvshow', 'music', 'audiobook', 
                                 'podcast', 'anime', 'adult', 'musicvideo', 'video']:
                    if media_type in media:
                        result = {
                            'type': media_type,
                            media_type: media[media_type]
                        }
                        if 'library' in data:
                            result['library'] = data['library']
                        return json.dumps(result, indent=2)
        
        return json.dumps(data, indent=2)
    
    def xml_to_protobuf(self, xml_content: str) -> bytes:
        """Convert XML to Protobuf via JSON intermediate."""
        # First convert XML to JSON
        converter = NFOToJSONConverter(compact=True)
        json_str = converter.convert(xml_content)
        
        # Then convert JSON to Protobuf
        return self.json_to_protobuf(json_str)
    
    def protobuf_to_xml(self, protobuf_data: bytes) -> str:
        """Convert Protobuf to XML via JSON intermediate."""
        # First convert Protobuf to JSON
        json_str = self.protobuf_to_json(protobuf_data, compact=True)
        
        # Then convert JSON to XML
        converter = JSONToNFOConverter()
        return converter.convert(json_str)
    
    def _populate_movie(self, movie, data: Dict[str, Any]):
        """Populate movie protobuf message."""
        if 'title' in data:
            movie.title = data['title']
        if 'originaltitle' in data:
            movie.originaltitle = data['originaltitle']
        if 'year' in data:
            movie.year = int(data['year'])
        if 'runtime' in data:
            movie.runtime = int(data['runtime'])
        if 'plot' in data:
            movie.plot = data['plot']
        if 'outline' in data:
            movie.outline = data['outline']
        if 'tagline' in data:
            movie.tagline = data['tagline']
        
        # Handle repeated fields
        for genre in data.get('genre', []):
            movie.genre.append(genre)
        
        for tag in data.get('tag', []):
            movie.tag.append(tag)
        
        # Handle ratings
        ratings = data.get('rating', [])
        if isinstance(ratings, dict):
            ratings = [ratings]
        for rating_data in ratings:
            rating = movie.rating.add()
            self._populate_rating(rating, rating_data)
        
        # Handle actors
        actors = data.get('actor', [])
        if isinstance(actors, dict):
            actors = [actors]
        for actor_data in actors:
            actor = movie.actor.add()
            self._populate_person(actor, actor_data)
    
    def _populate_tvshow(self, tvshow, data: Dict[str, Any]):
        """Populate TV show protobuf message."""
        # Similar to movie but with TV-specific fields
        if 'title' in data:
            tvshow.title = data['title']
        if 'premiered' in data:
            tvshow.premiered = data['premiered']
        if 'status' in data:
            tvshow.status = data['status']
        if 'season' in data:
            tvshow.season = int(data['season'])
        if 'episode' in data:
            tvshow.episode = int(data['episode'])
        
        # Add other fields similar to movie...
    
    def _populate_rating(self, rating, data: Dict[str, Any]):
        """Populate rating message."""
        if '@name' in data:
            rating.name = data['@name']
        elif 'name' in data:
            rating.name = data['name']
            
        if '@value' in data:
            rating.value = float(data['@value'])
        elif 'value' in data:
            rating.value = float(data['value'])
            
        if '@votes' in data:
            rating.votes = int(data['@votes'])
        elif 'votes' in data:
            rating.votes = int(data['votes'])
    
    def _populate_person(self, person, data: Dict[str, Any]):
        """Populate person message."""
        if 'name' in data:
            person.name = data['name']
        if 'role' in data:
            person.role = data['role']
        if 'order' in data:
            person.order = int(data['order'])
        if 'thumb' in data:
            person.thumb = data['thumb']
        if 'bio' in data:
            person.bio = data['bio']
    
    # Add more _populate methods for other types...


def main():
    parser = argparse.ArgumentParser(
        description="Convert between Protobuf, JSON, and XML for NFO Standard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # JSON to Protobuf
  %(prog)s -f json -t protobuf movie.json -o movie.pb
  
  # Protobuf to JSON
  %(prog)s -f protobuf -t json movie.pb -o movie.json
  
  # XML to Protobuf
  %(prog)s -f xml -t protobuf movie.nfo -o movie.pb
  
  # Protobuf to XML
  %(prog)s -f protobuf -t xml movie.pb -o movie.nfo
  
  # Base64 encoding for transport
  %(prog)s -f json -t protobuf --base64 movie.json

Formats:
  - json: JSON format
  - xml: NFO XML format  
  - protobuf: Binary protobuf format
  - protobuf-text: Text protobuf format (human readable)
        """
    )
    
    parser.add_argument('input', help='Input file (use "-" for stdin)')
    parser.add_argument('-f', '--from', dest='from_format', required=True,
                       choices=['json', 'xml', 'protobuf', 'protobuf-text'],
                       help='Input format')
    parser.add_argument('-t', '--to', dest='to_format', required=True,
                       choices=['json', 'xml', 'protobuf', 'protobuf-text'],
                       help='Output format')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--base64', action='store_true',
                       help='Use base64 encoding for protobuf I/O')
    parser.add_argument('--compact', action='store_true',
                       help='Use compact JSON format')
    
    args = parser.parse_args()
    
    if not HAS_PROTOBUF:
        print("Error: protobuf package is required", file=sys.stderr)
        sys.exit(1)
    
    # Read input
    if args.input == '-':
        if args.from_format == 'protobuf' and not args.base64:
            input_data = sys.stdin.buffer.read()
        else:
            input_data = sys.stdin.read()
    else:
        if args.from_format == 'protobuf' and not args.base64:
            with open(args.input, 'rb') as f:
                input_data = f.read()
        else:
            with open(args.input, 'r', encoding='utf-8') as f:
                input_data = f.read()
    
    # Handle base64 decoding for protobuf input
    if args.from_format == 'protobuf' and args.base64:
        input_data = base64.b64decode(input_data)
    
    # Convert
    converter = ProtobufConverter()
    
    try:
        if args.from_format == 'json' and args.to_format == 'protobuf':
            output_data = converter.json_to_protobuf(input_data)
        elif args.from_format == 'protobuf' and args.to_format == 'json':
            output_data = converter.protobuf_to_json(input_data, compact=args.compact)
        elif args.from_format == 'xml' and args.to_format == 'protobuf':
            output_data = converter.xml_to_protobuf(input_data)
        elif args.from_format == 'protobuf' and args.to_format == 'xml':
            output_data = converter.protobuf_to_xml(input_data)
        elif args.from_format == args.to_format:
            output_data = input_data
        else:
            # Convert via intermediate format
            if args.from_format == 'json' and args.to_format == 'xml':
                conv = JSONToNFOConverter()
                output_data = conv.convert(input_data)
            elif args.from_format == 'xml' and args.to_format == 'json':
                conv = NFOToJSONConverter(compact=args.compact)
                output_data = conv.convert(input_data)
            else:
                print(f"Error: Conversion from {args.from_format} to {args.to_format} not supported", 
                      file=sys.stderr)
                sys.exit(1)
    except Exception as e:
        print(f"Error: Conversion failed - {e}", file=sys.stderr)
        sys.exit(1)
    
    # Handle base64 encoding for protobuf output
    if args.to_format == 'protobuf' and args.base64:
        output_data = base64.b64encode(output_data).decode('ascii')
    
    # Write output
    if args.output:
        if args.to_format == 'protobuf' and not args.base64:
            with open(args.output, 'wb') as f:
                f.write(output_data)
        else:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_data)
        print(f"Successfully converted to {args.output}")
    else:
        if args.to_format == 'protobuf' and not args.base64:
            sys.stdout.buffer.write(output_data)
        else:
            print(output_data)


if __name__ == "__main__":
    main()