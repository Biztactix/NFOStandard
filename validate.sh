#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export XML_CATALOG_FILES="$SCRIPT_DIR/catalog.xml"

pass=0
fail=0
failed_files=()

echo "=== XSD Well-formedness Check ==="
for xsd in "$SCRIPT_DIR"/main.xsd "$SCRIPT_DIR"/Schemas/*.xsd; do
    name="$(basename "$xsd")"
    if xmllint --noout "$xsd" 2>/dev/null; then
        echo "  PASS  $name"
        pass=$((pass + 1))
    else
        echo "  FAIL  $name"
        failed_files+=("$name")
        fail=$((fail + 1))
    fi
done

echo ""
echo "=== XML Schema Validation ==="
xml_files=()
for pattern in "$SCRIPT_DIR"/Example*.xml "$SCRIPT_DIR"/Sample*.xml; do
    [ -e "$pattern" ] && xml_files+=("$pattern")
done

if [ ${#xml_files[@]} -eq 0 ]; then
    echo "  No Example*.xml or Sample*.xml files found."
else
    for xml in "${xml_files[@]}"; do
        name="$(basename "$xml")"
        if xmllint --noout --schema "$SCRIPT_DIR/main.xsd" "$xml" 2>/dev/null; then
            echo "  PASS  $name"
            pass=$((pass + 1))
        else
            echo "  FAIL  $name"
            failed_files+=("$name")
            fail=$((fail + 1))
        fi
    done
fi

echo ""
echo "=== Results ==="
echo "  Passed: $pass"
echo "  Failed: $fail"

if [ $fail -gt 0 ]; then
    echo ""
    echo "  Failed files:"
    for f in "${failed_files[@]}"; do
        echo "    - $f"
    done
    exit 1
fi

echo "  All checks passed."
exit 0
