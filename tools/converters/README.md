# NFO Standard Converters

This directory contains converters for transforming between XML, JSON, and Protocol Buffers formats for NFO Standard data.

## Format Comparison

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| **XML** | Standard format, human-readable | - Official NFO format<br>- Self-documenting<br>- Wide tool support | - Verbose<br>- Larger file size<br>- Slower parsing |
| **JSON** | Web APIs, JavaScript apps | - Widely supported<br>- Smaller than XML<br>- Fast parsing | - No schema validation<br>- Less human-readable<br>- No comments |
| **Protobuf** | Storage, high-performance apps | - Very compact (30-40% of XML)<br>- Fast parsing<br>- Type-safe | - Binary format<br>- Requires compilation<br>- Not human-readable |

## Available Converters

### JSON to XML (`json-to-xml.py`)

Converts JSON data to NFO Standard compliant XML files.

```bash
# Basic usage
python json-to-xml.py movie.json -o movie.nfo

# From stdin
cat movie.json | python json-to-xml.py -

# Specify media type
python json-to-xml.py data.json --type tvshow
```

### XML to JSON (`xml-to-json.py`)

Converts NFO XML files to JSON format.

```bash
# Basic usage  
python xml-to-json.py movie.nfo -o movie.json

# Compact format
python xml-to-json.py --compact movie.nfo

# Without attributes
python xml-to-json.py --no-attributes movie.nfo

# Simplified structure
python xml-to-json.py --simplify movie.nfo
```

## JSON Format

### Basic Structure

```json
{
  "type": "movie",
  "movie": {
    "title": "The Matrix",
    "year": 1999,
    "runtime": 136,
    "genre": ["Science Fiction", "Action"],
    "rating": {
      "@name": "imdb",
      "@value": "8.7",
      "@votes": "1800000"
    }
  }
}
```

### Attributes

XML attributes are prefixed with `@`:

```json
{
  "rating": {
    "@name": "imdb",
    "@value": "8.7",
    "@votes": "1800000",
    "@default": "true"
  }
}
```

### Multiple Elements

Arrays are used for multiple elements with the same name:

```json
{
  "genre": ["Action", "Drama", "Thriller"],
  "actor": [
    {
      "name": "Actor One",
      "role": "Character One"
    },
    {
      "name": "Actor Two", 
      "role": "Character Two"
    }
  ]
}
```

### Text Content with Attributes

Use `#text` for element text when attributes are present:

```json
{
  "uniqueid": {
    "@type": "imdb",
    "@default": "true",
    "#text": "tt0133093"
  }
}
```

## Examples

See the `examples/` directory for complete JSON examples for each media type.

## Integration

### Python

```python
from json_to_xml import JSONToNFOConverter
from xml_to_json import NFOToJSONConverter

# JSON to XML
converter = JSONToNFOConverter()
xml_output = converter.convert({"type": "movie", "movie": {"title": "Example"}})

# XML to JSON
converter = NFOToJSONConverter(compact=True)
json_output = converter.convert(xml_content)
```

### Command Line

```bash
# Convert all JSON files in a directory
for f in *.json; do
    python json-to-xml.py "$f" -o "${f%.json}.nfo"
done

# Convert all NFO files to JSON
for f in *.nfo; do
    python xml-to-json.py "$f" -o "${f%.nfo}.json"
done
```

## Validation

After conversion, validate the XML output:

```bash
python json-to-xml.py movie.json | nfo-validate -
```

## Format Comparison Tool

Use `format_comparison.py` to analyze size and performance differences:

```bash
# Analyze a single file
python format_comparison.py movie.nfo

# Analyze entire directory
python format_comparison.py /media/library/

# Output example:
# Format          Size    Compressed   Ratio   vs XML
# XML           3,247       1,024    31.5%   100.0%
# JSON          2,891         987    34.1%    89.0%
# JSON (min)    2,455         912    37.1%    75.6%
# Protobuf      1,102         687    62.3%    33.9%
```

## Protobuf Support

See the `protobuf/` directory for Protocol Buffers support:

```bash
# Compile proto files first
cd protobuf
protoc --python_out=. nfo_standard.proto

# Convert between formats
python protobuf_converter.py -f json -t protobuf movie.json -o movie.pb
python protobuf_converter.py -f protobuf -t xml movie.pb -o movie.nfo
```

## Tips

1. **Use compact mode** for cleaner JSON when converting from XML
2. **Validate output** to ensure compliance with NFO Standard
3. **Preserve attributes** when round-tripping between formats
4. **Use type field** to specify media type in JSON
5. **Choose format based on use case**:
   - XML for maximum compatibility
   - JSON for web services
   - Protobuf for storage and performance