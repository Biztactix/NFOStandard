# NFO Standard Protocol Buffers Support

This directory contains Protocol Buffers (protobuf) definitions for the NFO Standard, providing a binary serialization format that's compact and efficient. Files use the `.nfpb` extension (NFO Protocol Buffer).

## Why Protobuf?

- **Space Efficient**: NFPB format uses 50-80% less space than XML
- **Fast Parsing**: 20-100x faster parsing than XML
- **Type Safety**: Strongly typed with schema validation
- **Language Support**: Native libraries for most programming languages
- **Backward Compatible**: Protobuf's field numbering allows schema evolution

## Current Implementations

### ✅ C# (.NET) - Complete
- Full implementation with bidirectional XML ↔ Protocol Buffer conversion
- Command-line tool: `nfo-protobuf`
- NuGet package: `NFOStandard.Protobuf`
- Comprehensive unit tests
- See [csharp/README.md](csharp/README.md) for detailed documentation

### 🚧 Python - In Progress
- Basic converter implementation available
- See usage examples below

### 📋 Planned
- Java/Android
- Go
- JavaScript/TypeScript
- Rust

## Setup

### 1. Install Protocol Buffers Compiler

```bash
# Ubuntu/Debian
sudo apt-get install protobuf-compiler

# macOS
brew install protobuf

# Or download from: https://github.com/protocolbuffers/protobuf/releases
```

### 2. Install Python Protobuf Library

```bash
pip install protobuf
```

### 3. Compile Proto Files

```bash
# Generate Python code
protoc --python_out=. nfo_standard.proto

# Generate for other languages
protoc --java_out=. nfo_standard.proto
protoc --csharp_out=. nfo_standard.proto
protoc --go_out=. nfo_standard.proto
protoc --js_out=. nfo_standard.proto
```

## Usage

### Command Line Converter

```bash
# JSON to Protobuf
python ../protobuf_converter.py -f json -t protobuf movie.json -o movie.nfpb

# Protobuf to JSON
python ../protobuf_converter.py -f protobuf -t json movie.nfpb -o movie.json

# XML to Protobuf
python ../protobuf_converter.py -f xml -t protobuf movie.nfo -o movie.nfpb

# Protobuf to XML
python ../protobuf_converter.py -f protobuf -t xml movie.nfpb -o movie.nfo

# Base64 encoding (for text transport)
python ../protobuf_converter.py -f json -t protobuf --base64 movie.json
```

### Python API

```python
import nfo_standard_pb2

# Create a movie
movie = nfo_standard_pb2.Movie()
movie.title = "The Matrix"
movie.year = 1999
movie.runtime = 136

# Add genres
movie.genre.extend(["Science Fiction", "Action"])

# Add rating
rating = movie.rating.add()
rating.name = "imdb"
rating.value = 8.7
rating.votes = 1800000

# Add actor
actor = movie.actor.add()
actor.name = "Keanu Reeves"
actor.role = "Neo"
actor.order = 1

# Create root and serialize
root = nfo_standard_pb2.NFORoot()
root.media.movie.CopyFrom(movie)

# Serialize to binary
binary_data = root.SerializeToString()

# Deserialize
new_root = nfo_standard_pb2.NFORoot()
new_root.ParseFromString(binary_data)
print(new_root.media.movie.title)
```

### Java Example

```java
import com.nfostandard.protobuf.NfoStandard;

// Create movie
NfoStandard.Movie.Builder movieBuilder = NfoStandard.Movie.newBuilder()
    .setTitle("The Matrix")
    .setYear(1999)
    .setRuntime(136);

// Add genres
movieBuilder.addGenre("Science Fiction");
movieBuilder.addGenre("Action");

// Create root
NfoStandard.NFORoot root = NfoStandard.NFORoot.newBuilder()
    .setMedia(NfoStandard.Media.newBuilder()
        .setMovie(movieBuilder))
    .build();

// Serialize
byte[] data = root.toByteArray();

// Deserialize
NfoStandard.NFORoot parsed = NfoStandard.NFORoot.parseFrom(data);
```

### C# Example

```csharp
using NFOStandard.Protobuf;

// Create movie
var movie = new Movie
{
    Title = "The Matrix",
    Year = 1999,
    Runtime = 136
};

movie.Genre.Add("Science Fiction");
movie.Genre.Add("Action");

// Create root
var root = new NFORoot
{
    Media = new Media { Movie = movie }
};

// Serialize to .nfpb file
using var output = File.Create("movie.nfpb");
root.WriteTo(output);

// Deserialize from .nfpb file
using var input = File.OpenRead("movie.nfpb");
var parsed = NFORoot.Parser.ParseFrom(input);
```

## Size Comparison

Example movie with full metadata:

| Format | Size | Relative |
|--------|------|----------|
| XML (.nfo) | 3,247 bytes | 100% |
| JSON | 2,891 bytes | 89% |
| NFO Protobuf (.nfpb) | 1,102 bytes | 34% |
| NFPB+gzip | 687 bytes | 21% |

## Schema Evolution

Protobuf allows backward-compatible schema changes:

### Safe Changes
- Adding new optional fields
- Adding new repeated fields
- Adding new message types
- Adding new enum values

### Unsafe Changes
- Changing field numbers
- Changing field types
- Removing required fields
- Renaming fields (number stays same)

## Best Practices

1. **Use for Storage**: Store NFO data as .nfpb files for space efficiency
2. **Convert for Display**: Convert to XML/JSON when human readability needed
3. **Transport**: Use base64 encoding for text-based transport
4. **Streaming**: Protobuf supports streaming for large collections
5. **Validation**: Always validate after conversion

## Language Support

Official protobuf support for:
- C++
- Java
- Python
- Go
- C#
- JavaScript/TypeScript
- Ruby
- PHP
- Dart
- Swift
- Rust (third-party)

## Performance Tips

1. **Reuse Messages**: Clear and reuse message objects
2. **Lazy Parsing**: Use lazy parsing for large messages
3. **Field Presence**: Use `has_field()` before accessing
4. **Repeated Fields**: Pre-allocate capacity when known
5. **Binary Wire**: Use binary format, not text format

## Troubleshooting

### "Module not found" Error
```bash
# Make sure proto files are compiled
protoc --python_out=. nfo_standard.proto
```

### "Unknown field" Warning
- Normal when parsing newer messages with older schema
- Protobuf preserves unknown fields by default

### Size Not Reduced
- Ensure using binary format, not text format
- Consider compression for network transport
- Remove unnecessary repeated fields