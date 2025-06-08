# Installation Guide

## Overview

The NFO Standard is a specification that doesn't require installation itself, but you'll want tools to validate and work with NFO files.

## Schema Files

The NFO Standard schemas are hosted at `https://xsd.nfostandard.com/` and are automatically referenced in your NFO files. No local installation is needed.

## Validation Tools

### Online Validator

Visit our online validator (coming soon) to validate your NFO files directly in your browser.

### Command Line Tools

#### Python Validator (nfo-validate)

```bash
pip install nfo-validate
```

Usage:
```bash
nfo-validate movie.nfo
nfo-validate --strict tvshow.nfo
nfo-validate --batch /path/to/nfo/files/
```

#### Node.js Validator

```bash
npm install -g @nfostandard/validator
```

Usage:
```bash
nfo-validator movie.nfo
nfo-validator --watch /media/library/
```

### IDE Support

#### Visual Studio Code

Install the NFO Standard extension:
1. Open VS Code
2. Press `Ctrl+Shift+X` (Extensions)
3. Search for "NFO Standard"
4. Click Install

Features:
- Syntax highlighting
- Schema validation
- Auto-completion
- Snippets

#### JetBrains IDEs

The NFO Standard plugin is available for:
- IntelliJ IDEA
- PyCharm
- WebStorm
- PHPStorm

Install from: Settings → Plugins → Marketplace → Search "NFO Standard"

## Library Integration

### Python

```bash
pip install nfostandard
```

```python
from nfostandard import NFOParser, NFOValidator

# Parse NFO file
parser = NFOParser()
movie = parser.parse_file("movie.nfo")
print(movie.title)

# Validate NFO
validator = NFOValidator()
if validator.validate_file("movie.nfo"):
    print("Valid NFO file!")
```

### JavaScript/Node.js

```bash
npm install nfostandard
```

```javascript
const { parseNFO, validateNFO } = require('nfostandard');

// Parse NFO file
const movie = await parseNFO('movie.nfo');
console.log(movie.title);

// Validate NFO
const isValid = await validateNFO('movie.nfo');
```

### Java

```xml
<dependency>
    <groupId>com.nfostandard</groupId>
    <artifactId>nfostandard</artifactId>
    <version>1.0.0</version>
</dependency>
```

### C#/.NET

```bash
dotnet add package NFOStandard
```

## Next Steps

- [Create Your First NFO File](first-nfo.md)
- [Learn About Validation](validation.md)
- [Explore Media Types](../user-guides/movies.md)