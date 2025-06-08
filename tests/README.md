# NFO Standard Test Suite

This directory contains comprehensive test cases for validating NFO Standard implementations.

## Directory Structure

- `valid/` - Valid NFO files that should pass validation
- `invalid/` - Invalid NFO files that should fail validation with specific errors
- `edge-cases/` - Edge cases and complex scenarios

## Test Categories

### Valid Tests
- Basic examples for each media type
- Files with all optional fields
- Minimal files with only required fields
- International characters and special encoding
- Multiple ratings, genres, actors
- Complex nested structures

### Invalid Tests
- Missing required fields
- Invalid data types
- Malformed XML
- Wrong schema references
- Invalid date formats
- Out-of-range values

### Edge Cases
- Very large files
- Deeply nested structures
- Unicode edge cases
- Maximum field lengths
- Unusual but valid combinations

## Running Tests

### Python
```bash
cd tools/python-validator
python test_suite.py ../../tests/
```

### JavaScript
```bash
cd tools/js-validator
npm test
```

### Manual Testing
```bash
# Test all valid files should pass
for f in tests/valid/*.xml; do
    nfo-validate "$f" || echo "FAILED: $f"
done

# Test all invalid files should fail
for f in tests/invalid/*.xml; do
    nfo-validate "$f" && echo "SHOULD HAVE FAILED: $f"
done
```

## Adding New Tests

1. Create a descriptive filename: `media-type_test-description.xml`
2. Add comments explaining what the test validates
3. For invalid tests, add a comment with expected error
4. Update this README with test description

## Test Naming Convention

- `movie_minimal.xml` - Minimal valid movie
- `movie_complete.xml` - Movie with all fields
- `movie_missing_title.xml` - Invalid: missing required field
- `movie_invalid_runtime.xml` - Invalid: wrong data type
- `movie_unicode_edge.xml` - Edge case: unicode handling