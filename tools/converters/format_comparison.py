#!/usr/bin/env python3
"""
Format Comparison Tool
Compares size and performance of XML, JSON, and Protobuf formats for NFO data.
"""

import argparse
import sys
import time
import gzip
import json
from pathlib import Path
import statistics

# Import converters
from json_to_xml import JSONToNFOConverter
from xml_to_json import NFOToJSONConverter

try:
    from protobuf_converter import ProtobufConverter
    HAS_PROTOBUF = True
except ImportError:
    HAS_PROTOBUF = False


def compress_data(data: bytes) -> bytes:
    """Compress data using gzip."""
    return gzip.compress(data)


def get_size_info(data: bytes, label: str) -> dict:
    """Get size information for data."""
    compressed = compress_data(data)
    return {
        'format': label,
        'size': len(data),
        'compressed_size': len(compressed),
        'compression_ratio': len(compressed) / len(data) * 100
    }


def benchmark_conversions(xml_content: str, iterations: int = 100) -> dict:
    """Benchmark conversion performance."""
    results = {}
    
    # XML to JSON
    start = time.time()
    for _ in range(iterations):
        converter = NFOToJSONConverter(compact=True)
        json_str = converter.convert(xml_content)
    results['xml_to_json'] = (time.time() - start) / iterations * 1000  # ms
    
    # JSON to XML
    json_data = json.loads(json_str)
    start = time.time()
    for _ in range(iterations):
        converter = JSONToNFOConverter()
        xml_str = converter.convert(json_data)
    results['json_to_xml'] = (time.time() - start) / iterations * 1000  # ms
    
    if HAS_PROTOBUF:
        pb_converter = ProtobufConverter()
        
        # JSON to Protobuf
        start = time.time()
        for _ in range(iterations):
            pb_data = pb_converter.json_to_protobuf(json_data)
        results['json_to_protobuf'] = (time.time() - start) / iterations * 1000
        
        # Protobuf to JSON
        start = time.time()
        for _ in range(iterations):
            json_str2 = pb_converter.protobuf_to_json(pb_data)
        results['protobuf_to_json'] = (time.time() - start) / iterations * 1000
    
    return results


def analyze_file(filepath: str) -> None:
    """Analyze an NFO file and show format comparison."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath}")
    print(f"{'='*60}\n")
    
    # Read XML
    with open(filepath, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Convert to different formats
    sizes = []
    
    # XML
    xml_bytes = xml_content.encode('utf-8')
    sizes.append(get_size_info(xml_bytes, 'XML'))
    
    # JSON
    converter = NFOToJSONConverter(compact=True)
    json_str = converter.convert(xml_content)
    json_bytes = json_str.encode('utf-8')
    sizes.append(get_size_info(json_bytes, 'JSON'))
    
    # JSON (minified)
    json_min = json.dumps(json.loads(json_str), separators=(',', ':'))
    json_min_bytes = json_min.encode('utf-8')
    sizes.append(get_size_info(json_min_bytes, 'JSON (min)'))
    
    # Protobuf
    if HAS_PROTOBUF:
        pb_converter = ProtobufConverter()
        pb_data = pb_converter.json_to_protobuf(json_str)
        sizes.append(get_size_info(pb_data, 'Protobuf'))
    
    # Display size comparison
    print("Size Comparison:")
    print(f"{'Format':<15} {'Size':>10} {'Compressed':>10} {'Ratio':>8} {'vs XML':>8}")
    print("-" * 60)
    
    xml_size = sizes[0]['size']
    for info in sizes:
        ratio_vs_xml = info['size'] / xml_size * 100
        print(f"{info['format']:<15} {info['size']:>10,} {info['compressed_size']:>10,} "
              f"{info['compression_ratio']:>7.1f}% {ratio_vs_xml:>7.1f}%")
    
    # Benchmark conversions
    print("\n\nConversion Performance (average over 100 iterations):")
    print("-" * 40)
    
    benchmarks = benchmark_conversions(xml_content, iterations=100)
    for conversion, time_ms in benchmarks.items():
        print(f"{conversion:<20} {time_ms:>8.2f} ms")
    
    # Content analysis
    print("\n\nContent Analysis:")
    print("-" * 40)
    
    data = json.loads(json_str)
    media_type = data.get('type', 'unknown')
    media_data = data.get(media_type, {})
    
    field_count = count_fields(media_data)
    print(f"Media Type: {media_type}")
    print(f"Total Fields: {field_count}")
    
    # Count specific elements
    counts = {
        'genres': len(media_data.get('genre', [])),
        'actors': len(media_data.get('actor', [])),
        'ratings': len(media_data.get('rating', [])),
        'images': len(media_data.get('thumb', [])) + len(media_data.get('fanart', [])) + len(media_data.get('banner', []))
    }
    
    for key, count in counts.items():
        if count > 0:
            print(f"{key.capitalize()}: {count}")


def count_fields(obj, count=0):
    """Recursively count fields in object."""
    if isinstance(obj, dict):
        count += len(obj)
        for value in obj.values():
            count = count_fields(value, count)
    elif isinstance(obj, list):
        for item in obj:
            count = count_fields(item, count)
    return count


def compare_directory(directory: str) -> None:
    """Compare all NFO files in a directory."""
    path = Path(directory)
    nfo_files = list(path.glob("**/*.nfo")) + list(path.glob("**/*.xml"))
    
    if not nfo_files:
        print(f"No NFO/XML files found in {directory}")
        return
    
    print(f"\nFound {len(nfo_files)} files to analyze")
    
    total_sizes = {'XML': 0, 'JSON': 0, 'Protobuf': 0}
    
    for filepath in nfo_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            
            # Get sizes
            total_sizes['XML'] += len(xml_content.encode('utf-8'))
            
            converter = NFOToJSONConverter(compact=True)
            json_str = converter.convert(xml_content)
            total_sizes['JSON'] += len(json_str.encode('utf-8'))
            
            if HAS_PROTOBUF:
                pb_converter = ProtobufConverter()
                pb_data = pb_converter.json_to_protobuf(json_str)
                total_sizes['Protobuf'] += len(pb_data)
                
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("Directory Summary")
    print(f"{'='*60}\n")
    
    print(f"{'Format':<15} {'Total Size':>15} {'vs XML':>10}")
    print("-" * 45)
    
    xml_total = total_sizes['XML']
    for format_name, size in total_sizes.items():
        if size > 0:
            ratio = size / xml_total * 100
            print(f"{format_name:<15} {size:>15,} {ratio:>9.1f}%")


def main():
    parser = argparse.ArgumentParser(
        description="Compare XML, JSON, and Protobuf formats for NFO files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s movie.nfo
  %(prog)s /path/to/media/library/
  %(prog)s --benchmark movie.nfo
        """
    )
    
    parser.add_argument('input', help='NFO file or directory to analyze')
    parser.add_argument('--benchmark', action='store_true',
                       help='Run performance benchmarks')
    
    args = parser.parse_args()
    
    if not HAS_PROTOBUF:
        print("Warning: protobuf not available. Install with: pip install protobuf")
        print("Comparing only XML and JSON formats.\n")
    
    path = Path(args.input)
    
    if path.is_file():
        analyze_file(args.input)
    elif path.is_dir():
        compare_directory(args.input)
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()