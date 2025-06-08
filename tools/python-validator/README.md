# NFO Standard Python Validator

A Python validation tool for NFO Standard files.

## Installation

```bash
pip install nfo-validate
```

Or install from source:

```bash
git clone https://github.com/Biztactix/NFOStandard.git
cd NFOStandard/tools/python-validator
pip install -e .
```

## Usage

### Basic Validation

```bash
# Validate a single file
nfo-validate movie.nfo

# Validate multiple files
nfo-validate movie1.nfo movie2.nfo tvshow.nfo

# Validate with strict mode (checks recommended fields)
nfo-validate --strict movie.nfo
```

### Directory Validation

```bash
# Validate all NFO files in a directory
nfo-validate /path/to/media/

# Recursive validation
nfo-validate --recursive /path/to/media/library/
```

### Output Formats

```bash
# JSON output
nfo-validate --format json movie.nfo

# XML output
nfo-validate --format xml movie.nfo

# Quiet mode (only show errors)
nfo-validate --quiet /media/library/
```

### Offline Validation

```bash
# Download schemas first
wget -r -np -k https://xsd.nfostandard.com/

# Use offline validation
nfo-validate --offline --schema-dir ./xsd.nfostandard.com movie.nfo
```

## Python API

```python
from nfo_validator import NFOValidator

# Create validator instance
validator = NFOValidator()

# Validate a file
is_valid, errors = validator.validate_file("movie.nfo")
if is_valid:
    print("Valid NFO file!")
else:
    for error in errors:
        print(f"Error: {error}")

# Validate with strict mode
is_valid, errors = validator.validate_file("movie.nfo", strict=True)

# Validate directory
results = validator.validate_directory("/media/library", recursive=True)
for filepath, is_valid, errors in results:
    print(f"{filepath}: {'Valid' if is_valid else 'Invalid'}")
```

## Features

- **XSD Schema Validation**: Validates against official NFO Standard schemas
- **Strict Mode**: Checks for recommended fields
- **Multiple Output Formats**: Text, JSON, XML
- **Batch Processing**: Validate entire directories
- **Offline Support**: Use local schema files
- **Detailed Error Messages**: Clear error descriptions with line numbers

## Requirements

- Python 3.7+
- lxml
- requests

## License

This project is licensed under The Unlicense. See the LICENSE file for details.