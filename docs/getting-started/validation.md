# NFO Validation Guide

## Why Validate?

Validation ensures your NFO files:
- Follow the correct schema structure
- Contain all required fields
- Use proper data types
- Will work with NFO-compatible applications

## Validation Methods

### 1. Online Validator

The easiest way to validate your NFO files is using our online validator:

1. Visit [https://nfostandard.com/validator](https://nfostandard.com/validator) (coming soon)
2. Upload your NFO file or paste its contents
3. Click "Validate"
4. Review any errors or warnings

### 2. Command Line Tools

#### Python Validator

```bash
# Install
pip install nfo-validate

# Basic validation
nfo-validate movie.nfo

# Strict validation (checks optional fields)
nfo-validate --strict movie.nfo

# Validate multiple files
nfo-validate *.nfo

# Validate directory recursively
nfo-validate --recursive /media/library/
```

#### Node.js Validator

```bash
# Install
npm install -g @nfostandard/validator

# Basic validation
nfo-validator movie.nfo

# Watch mode (auto-validates on change)
nfo-validator --watch movie.nfo

# Output formats
nfo-validator --format json movie.nfo
nfo-validator --format xml movie.nfo
```

### 3. Programmatic Validation

#### Python

```python
from nfostandard import NFOValidator

validator = NFOValidator()

# Validate file
result = validator.validate_file("movie.nfo")
if result.is_valid:
    print("Valid NFO!")
else:
    for error in result.errors:
        print(f"Error: {error.message} at line {error.line}")

# Validate string
nfo_content = open("movie.nfo").read()
result = validator.validate_string(nfo_content)
```

#### JavaScript

```javascript
const { NFOValidator } = require('nfostandard');

const validator = new NFOValidator();

// Validate file
const result = await validator.validateFile('movie.nfo');
if (result.isValid) {
    console.log('Valid NFO!');
} else {
    result.errors.forEach(error => {
        console.log(`Error: ${error.message} at line ${error.line}`);
    });
}
```

## Understanding Validation Errors

### Common Errors

#### Missing Required Field
```
Error: Required field 'title' is missing
Location: /root/media/movie
```

**Fix**: Add the missing field:
```xml
<movie>
    <title>Movie Title</title>
    <!-- other fields -->
</movie>
```

#### Invalid Data Type
```
Error: Invalid integer value '2h30m' for field 'runtime'
Location: /root/media/movie/runtime
```

**Fix**: Use correct data type (runtime is in minutes):
```xml
<runtime>150</runtime>
```

#### Invalid Date Format
```
Error: Invalid date format '07/15/2023' for field 'releasedate'
Location: /root/media/movie/releasedate
```

**Fix**: Use ISO date format (YYYY-MM-DD):
```xml
<releasedate>2023-07-15</releasedate>
```

#### Unknown Element
```
Error: Element 'customfield' is not allowed
Location: /root/media/movie/customfield
```

**Fix**: Remove unknown elements or use proper extension mechanism.

### Validation Levels

#### 1. Schema Validation (Default)
- Checks XML structure
- Validates against XSD schema
- Ensures required fields exist
- Validates data types

#### 2. Strict Validation
- All schema validation checks
- Validates optional field formats
- Checks for deprecated fields
- Warns about best practices

#### 3. Content Validation
- All strict validation checks
- Validates URLs are accessible
- Checks image dimensions
- Verifies external IDs (IMDB, TMDB)

## IDE Integration

### Visual Studio Code

With the NFO Standard extension installed:

1. Open any `.nfo` file
2. Errors appear in the Problems panel
3. Hover over underlined elements for error details
4. Use Quick Fix (Ctrl+.) for automatic fixes

### IntelliJ IDEA

1. Right-click on `.nfo` file
2. Select "Validate NFO"
3. View results in the Validation panel

## Continuous Integration

### GitHub Actions

```yaml
name: Validate NFO Files
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: nfostandard/validate-action@v1
        with:
          files: '**/*.nfo'
          strict: true
```

### GitLab CI

```yaml
validate_nfo:
  image: python:3.9
  script:
    - pip install nfo-validate
    - nfo-validate --recursive .
  only:
    changes:
      - "**/*.nfo"
```

## Best Practices

1. **Validate Early**: Check files as you create them
2. **Use Strict Mode**: For production libraries
3. **Automate**: Set up CI/CD validation
4. **Fix Warnings**: They may become errors in future versions
5. **Keep Updated**: Use the latest validator version

## Troubleshooting

### "Schema not found" Error

Ensure your NFO file has the correct schema location:
```xml
xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd"
```

### "Connection timeout" Error

The validator needs internet access to fetch schemas. For offline validation:
```bash
nfo-validate --offline --schema-dir ./schemas movie.nfo
```

### Performance Issues

For large libraries:
```bash
# Use parallel processing
nfo-validate --parallel --threads 4 /media/library/

# Skip content validation
nfo-validate --skip-content /media/library/
```

## Next Steps

- [Create media-specific NFO files](../user-guides/movies.md)
- [Learn about extensions](../advanced/extensions.md)
- [Set up automated workflows](../advanced/automation.md)