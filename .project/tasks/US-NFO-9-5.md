---
assignee: claude
created: '2026-02-22'
id: US-NFO-9-5
points: 3
status: done
story_id: US-NFO-9
title: Create validation script with XML catalog for local schema resolution
updated: '2026-02-22'
---

Create a validation script and XML catalog file that enables local XSD compilation and XML validation.

Files to create:

**catalog.xml** — XML catalog that redirects remote schema URLs to local paths:
- Rewrite `https://xsd.nfostandard.com/` → `./` (or appropriate relative path)
- This allows xmllint to resolve `<xs:include schemaLocation="https://xsd.nfostandard.com/Schemas/common.xsd"/>` to local `./Schemas/common.xsd`

**validate.sh** — Bash script that:
1. Sets `XML_CATALOG_FILES` to point to `catalog.xml`
2. Checks all XSD files are well-formed XML: `xmllint --noout main.xsd Schemas/*.xsd`
3. Validates each example XML against the schema: `xmllint --noout --schema main.xsd Example*.xml Sample*.xml`
4. Reports pass/fail for each file
5. Exits 0 if all pass, non-zero on any failure

The script should:
- Be executable (chmod +x)
- Work from the repo root directory
- Use `xmllint` from libxml2-utils (widely available)
- Print clear output showing which files pass/fail
- Handle the case where no example files match the glob

Files: validate.sh, catalog.xml