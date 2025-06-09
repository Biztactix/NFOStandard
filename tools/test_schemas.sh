#!/bin/bash

# NFOStandard Schema Testing Script
# This script creates a local testing environment for schema validation

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEST_DIR="$PROJECT_ROOT/test_output"
SCHEMAS_DIR="$PROJECT_ROOT/Schemas"
EXAMPLES_DIR="$PROJECT_ROOT/examples"
TESTS_DIR="$PROJECT_ROOT/tests"

echo -e "${BLUE}NFOStandard Schema Testing Framework${NC}"
echo "======================================"
echo "Project Root: $PROJECT_ROOT"
echo "Test Directory: $TEST_DIR"
echo ""

# Clean and create test directory
echo -e "${YELLOW}Setting up test environment...${NC}"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR/schemas"
mkdir -p "$TEST_DIR/examples"
mkdir -p "$TEST_DIR/tests"

# Copy schema files and update URLs
echo -e "${YELLOW}Copying and localizing schema files...${NC}"

# Copy all XSD files
cp "$PROJECT_ROOT/main.xsd" "$TEST_DIR/schemas/"
cp "$SCHEMAS_DIR"/*.xsd "$TEST_DIR/schemas/"

# Function to update schema URLs to local paths
update_schema_urls() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo "  Updating URLs in $filename"
    
    # Update include statements to use local paths
    sed -i 's|https://xsd\.nfostandard\.com/v2/Schemas/|./|g' "$file"
    sed -i 's|https://xsd\.nfostandard\.com/v2/main\.xsd|./main.xsd|g' "$file"
    # Also handle legacy v1 URLs for backward compatibility testing
    sed -i 's|https://xsd\.nfostandard\.com/Schemas/|./|g' "$file"
    sed -i 's|https://xsd\.nfostandard\.com/main\.xsd|./main.xsd|g' "$file"
}

# Update all schema files
for schema_file in "$TEST_DIR/schemas"/*.xsd; do
    update_schema_urls "$schema_file"
done

# Copy example files and update schema locations
echo -e "${YELLOW}Copying and updating example files...${NC}"

# Copy example files
if [ -d "$EXAMPLES_DIR" ]; then
    cp "$EXAMPLES_DIR"/*.xml "$TEST_DIR/examples/" 2>/dev/null || true
fi

# Copy test files
if [ -d "$TESTS_DIR" ]; then
    mkdir -p "$TEST_DIR/tests/valid" "$TEST_DIR/tests/invalid" "$TEST_DIR/tests/edge-cases"
    find "$TESTS_DIR/valid" -name "*.xml" -exec cp {} "$TEST_DIR/tests/valid/" \; 2>/dev/null || true
    find "$TESTS_DIR/invalid" -name "*.xml" -exec cp {} "$TEST_DIR/tests/invalid/" \; 2>/dev/null || true
    find "$TESTS_DIR/edge-cases" -name "*.xml" -exec cp {} "$TEST_DIR/tests/edge-cases/" \; 2>/dev/null || true
fi

# Copy root-level example files
cp "$PROJECT_ROOT"/*.xml "$TEST_DIR/examples/" 2>/dev/null || true

# Function to update example schema locations
update_example_schema_location() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo "  Updating schema location in $filename"
    
    # Update schema location to point to local test schemas
    sed -i 's|https://xsd\.nfostandard\.com/v2/main\.xsd|./schemas/main.xsd|g' "$file"
    sed -i 's|xsi:schemaLocation="NFOStandard https://xsd\.nfostandard\.com/v2/main\.xsd"|xsi:schemaLocation="NFOStandard ./schemas/main.xsd"|g' "$file"
    # Also handle legacy v1 URLs for backward compatibility testing
    sed -i 's|https://xsd\.nfostandard\.com/main\.xsd|./schemas/main.xsd|g' "$file"
    sed -i 's|xsi:schemaLocation="NFOStandard https://xsd\.nfostandard\.com/main\.xsd"|xsi:schemaLocation="NFOStandard ./schemas/main.xsd"|g' "$file"
}

# Update all example files
for example_file in "$TEST_DIR/examples"/*.xml; do
    if [ -f "$example_file" ]; then
        update_example_schema_location "$example_file"
    fi
done

# Update test files
for test_file in "$TEST_DIR/tests/valid"/*.xml "$TEST_DIR/tests/invalid"/*.xml "$TEST_DIR/tests/edge-cases"/*.xml; do
    if [ -f "$test_file" ]; then
        update_example_schema_location "$test_file"
    fi
done

echo -e "${GREEN}Test environment setup complete!${NC}"
echo ""

# Function to validate a single XML file
validate_xml_file() {
    local xml_file="$1"
    local schema_file="$2"
    local filename=$(basename "$xml_file")
    
    echo -n "  Testing $filename... "
    
    if xmllint --noout --schema "$schema_file" "$xml_file" 2>/dev/null; then
        echo -e "${GREEN}✓ VALID${NC}"
        return 0
    else
        echo -e "${RED}✗ INVALID${NC}"
        echo -e "${RED}    Error details:${NC}"
        xmllint --noout --schema "$schema_file" "$xml_file" 2>&1 | sed 's/^/      /'
        return 1
    fi
}

# Test schema syntax first
echo -e "${YELLOW}Testing schema syntax...${NC}"
schema_valid=true

# Test main schema
echo -n "  main.xsd... "
if xmllint --noout "$TEST_DIR/schemas/main.xsd" 2>/dev/null; then
    echo -e "${GREEN}✓ VALID SYNTAX${NC}"
else
    echo -e "${RED}✗ INVALID SYNTAX${NC}"
    xmllint --noout "$TEST_DIR/schemas/main.xsd" 2>&1 | sed 's/^/    /'
    schema_valid=false
fi

# Test individual schemas
for schema_file in "$TEST_DIR/schemas"/*.xsd; do
    if [ "$(basename "$schema_file")" != "main.xsd" ]; then
        filename=$(basename "$schema_file")
        echo -n "  $filename... "
        if xmllint --noout "$schema_file" 2>/dev/null; then
            echo -e "${GREEN}✓ VALID SYNTAX${NC}"
        else
            echo -e "${RED}✗ INVALID SYNTAX${NC}"
            xmllint --noout "$schema_file" 2>&1 | sed 's/^/    /'
            schema_valid=false
        fi
    fi
done

if [ "$schema_valid" = false ]; then
    echo -e "${RED}Schema syntax errors found. Fix schemas before testing examples.${NC}"
    exit 1
fi

echo ""

# Test examples against schemas
echo -e "${YELLOW}Testing example files against schemas...${NC}"
main_schema="$TEST_DIR/schemas/main.xsd"
total_files=0
valid_files=0
invalid_files=0

# Test example files
if [ -d "$TEST_DIR/examples" ] && [ "$(ls -A "$TEST_DIR/examples"/*.xml 2>/dev/null)" ]; then
    echo -e "${BLUE}Example files:${NC}"
    for xml_file in "$TEST_DIR/examples"/*.xml; do
        if [ -f "$xml_file" ]; then
            total_files=$((total_files + 1))
            if validate_xml_file "$xml_file" "$main_schema"; then
                valid_files=$((valid_files + 1))
            else
                invalid_files=$((invalid_files + 1))
            fi
        fi
    done
    echo ""
fi

# Test valid test files (should pass)
if [ -d "$TEST_DIR/tests" ] && [ "$(ls -A "$TEST_DIR/tests"/valid/*.xml 2>/dev/null)" ]; then
    echo -e "${BLUE}Valid test files (should pass):${NC}"
    for xml_file in "$TEST_DIR/tests"/valid/*.xml; do
        if [ -f "$xml_file" ]; then
            total_files=$((total_files + 1))
            if validate_xml_file "$xml_file" "$main_schema"; then
                valid_files=$((valid_files + 1))
            else
                invalid_files=$((invalid_files + 1))
            fi
        fi
    done
    echo ""
fi

# Test invalid test files (should fail)
if [ -d "$TEST_DIR/tests" ] && [ "$(ls -A "$TEST_DIR/tests"/invalid/*.xml 2>/dev/null)" ]; then
    echo -e "${BLUE}Invalid test files (should fail):${NC}"
    for xml_file in "$TEST_DIR/tests"/invalid/*.xml; do
        if [ -f "$xml_file" ]; then
            total_files=$((total_files + 1))
            echo -n "  $(basename "$xml_file")... "
            if xmllint --noout --schema "$main_schema" "$xml_file" 2>/dev/null; then
                echo -e "${RED}✗ UNEXPECTEDLY VALID${NC}"
                invalid_files=$((invalid_files + 1))
            else
                echo -e "${GREEN}✓ CORRECTLY INVALID${NC}"
                valid_files=$((valid_files + 1))
            fi
        fi
    done
    echo ""
fi

# Test edge case files (should pass but test edge cases)
if [ -d "$TEST_DIR/tests" ] && [ "$(ls -A "$TEST_DIR/tests"/edge-cases/*.xml 2>/dev/null)" ]; then
    echo -e "${BLUE}Edge case test files (should pass):${NC}"
    for xml_file in "$TEST_DIR/tests"/edge-cases/*.xml; do
        if [ -f "$xml_file" ]; then
            total_files=$((total_files + 1))
            if validate_xml_file "$xml_file" "$main_schema"; then
                valid_files=$((valid_files + 1))
            else
                invalid_files=$((invalid_files + 1))
            fi
        fi
    done
    echo ""
fi

# Summary
echo -e "${BLUE}Test Summary:${NC}"
echo "============="
echo "Total files tested: $total_files"
echo -e "Valid/Expected: ${GREEN}$valid_files${NC}"
echo -e "Invalid/Unexpected: ${RED}$invalid_files${NC}"

if [ $invalid_files -eq 0 ]; then
    echo -e "${GREEN}All tests passed! ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. ✗${NC}"
    exit 1
fi