# NFO Standard Tools

This directory contains various tools for working with NFO Standard files.

## Available Tools

### Python Validator
- Location: `python-validator/`
- Validates NFO files against the XSD schema
- Checks for required fields and proper structure

### JavaScript Validator
- Location: `js-validator/`
- Browser and Node.js compatible validation
- Includes both CLI and library usage

### Format Converters
- Location: `converters/`
- Convert between NFO Standard XML, JSON, and Protobuf formats
- Migration tools from Kodi, Plex, and Emby formats

### Web Importer
- Location: `web-importer/`
- Browser-based tool for importing metadata from IMDB, TMDB, and TheTVDB
- Generate NFO Standard files with a user-friendly interface
- Includes both standalone (mock data) and API server modes

## Quick Start

```bash
# Python validator
cd python-validator
python nfo_validator.py ../examples/movie.xml

# JavaScript validator
cd js-validator
npm install
node cli.js ../examples/tvshow.xml

# Format conversion
cd converters
python json-to-xml.py input.json output.xml

# Web importer
cd web-importer
# For mock data mode:
open index.html
# For API mode:
python api_server.py
```

## Development

Each tool has its own README with specific instructions and examples.