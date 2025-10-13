#!/bin/bash

# NFOStandard Example File Fixer
# This script fixes common validation issues in example files

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

echo -e "${BLUE}NFOStandard Example File Fixer${NC}"
echo "==============================="
echo ""

# Function to fix a single XML file
fix_xml_file() {
    local file="$1"
    local filename=$(basename "$file")
    
    echo -n "  Fixing $filename... "
    
    # Create backup
    cp "$file" "$file.backup"
    
    # Fix contentRating structure from attributes to elements
    # Pattern: <contentRating country="XX" board="YY" rating="ZZ" image="URL"/>
    # To: <contentRating country="XX" board="YY"><rating>ZZ</rating><image>URL</image></contentRating>
    sed -i 's|<contentRating country="\([^"]*\)" board="\([^"]*\)" rating="\([^"]*\)" image="\([^"]*\)"/>|<contentRating country="\1" board="\2"><rating>\3</rating><image>\4</image></contentRating>|g' "$file"
    
    # Fix contentRating without image
    sed -i 's|<contentRating country="\([^"]*\)" board="\([^"]*\)" rating="\([^"]*\)"/>|<contentRating country="\1" board="\2"><rating>\3</rating></contentRating>|g' "$file"
    
    # Fix country codes to ISO 3166-1 alpha-2
    sed -i 's|country="USA"|country="US"|g' "$file"
    sed -i 's|country="Japan"|country="JP"|g' "$file"
    sed -i 's|country="United Kingdom"|country="GB"|g' "$file"
    sed -i 's|country="Germany"|country="DE"|g' "$file"
    sed -i 's|country="France"|country="FR"|g' "$file"
    sed -i 's|country="Canada"|country="CA"|g' "$file"
    
    # Fix media file elements from attributes to content+attributes
    # Pattern: <banner type="X" width="Y" height="Z" url="URL"/>
    # To: <banner type="X" width="Y" height="Z" url="URL">Content</banner>
    
    # Fix banner elements
    sed -i 's|<banner type="\([^"]*\)" width="\([^"]*\)" height="\([^"]*\)" url="\([^"]*\)"/>|<banner type="banner" width="\2" height="\3" url="\4">Banner Image</banner>|g' "$file"
    
    # Fix thumb elements
    sed -i 's|<thumb type="\([^"]*\)" width="\([^"]*\)" height="\([^"]*\)" url="\([^"]*\)"/>|<thumb type="thumb" width="\2" height="\3" url="\4">Thumbnail Image</thumb>|g' "$file"
    
    # Fix fanart elements
    sed -i 's|<fanart type="\([^"]*\)" width="\([^"]*\)" height="\([^"]*\)" url="\([^"]*\)"/>|<fanart type="fanart" width="\2" height="\3" url="\4">Fanart Image</fanart>|g' "$file"
    
    # Fix cover elements
    sed -i 's|<cover type="\([^"]*\)" width="\([^"]*\)" height="\([^"]*\)" url="\([^"]*\)"/>|<cover type="poster" width="\2" height="\3" url="\4">Cover Image</cover>|g' "$file"
    
    # Fix thumbnail elements
    sed -i 's|<thumbnail type="\([^"]*\)" width="\([^"]*\)" height="\([^"]*\)" url="\([^"]*\)"/>|<thumbnail type="thumb" width="\2" height="\3" url="\4">Thumbnail Image</thumbnail>|g' "$file"
    
    # Fix language codes to ISO 639-1 format for subtitle languages
    sed -i 's|<subtitlelanguage>English</subtitlelanguage>|<subtitlelanguage>en</subtitlelanguage>|g' "$file"
    sed -i 's|<subtitlelanguage>Spanish</subtitlelanguage>|<subtitlelanguage>es</subtitlelanguage>|g' "$file"
    sed -i 's|<subtitlelanguage>French</subtitlelanguage>|<subtitlelanguage>fr</subtitlelanguage>|g' "$file"
    sed -i 's|<subtitlelanguage>German</subtitlelanguage>|<subtitlelanguage>de</subtitlelanguage>|g' "$file"
    sed -i 's|<subtitlelanguage>Japanese</subtitlelanguage>|<subtitlelanguage>ja</subtitlelanguage>|g' "$file"
    
    echo -e "${GREEN}✓ FIXED${NC}"
}

# Fix all example files
echo -e "${YELLOW}Fixing example files...${NC}"

# Fix root-level examples
for file in "$PROJECT_ROOT"/*.xml; do
    if [ -f "$file" ]; then
        fix_xml_file "$file"
    fi
done

# Fix examples directory
if [ -d "$PROJECT_ROOT/examples" ]; then
    for file in "$PROJECT_ROOT/examples"/*.xml; do
        if [ -f "$file" ]; then
            fix_xml_file "$file"
        fi
    done
fi

# Fix test files (but only the valid ones, leave invalid ones alone)
if [ -d "$PROJECT_ROOT/tests/valid" ]; then
    for file in "$PROJECT_ROOT/tests/valid"/*.xml; do
        if [ -f "$file" ]; then
            fix_xml_file "$file"
        fi
    done
fi

# Fix edge cases (these should be valid but with edge cases)
if [ -d "$PROJECT_ROOT/tests/edge-cases" ]; then
    for file in "$PROJECT_ROOT/tests/edge-cases"/*.xml; do
        if [ -f "$file" ]; then
            fix_xml_file "$file"
        fi
    done
fi

echo ""
echo -e "${GREEN}Example file fixes complete!${NC}"
echo ""
echo -e "${YELLOW}Running validation to check results...${NC}"

# Run the test script to verify fixes
if [ -f "$SCRIPT_DIR/test_schemas.sh" ]; then
    "$SCRIPT_DIR/test_schemas.sh"
else
    echo -e "${RED}Test script not found. Please run test_schemas.sh manually to verify fixes.${NC}"
fi