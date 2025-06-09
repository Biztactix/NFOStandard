# NFO Standard Versioning Strategy

## Overview

The NFO Standard follows [Semantic Versioning 2.0.0](https://semver.org/) with specific guidelines for maintaining backward compatibility and managing schema evolution.

## Version Format

`MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

## Current Version

**2.0.0** (Enhanced Schema with Breaking Changes)

## Versioning Rules

### Major Version Changes (Breaking Changes)

Increment MAJOR version when:
- Removing existing elements or attributes
- Changing element cardinality from optional to required
- Changing data types in incompatible ways
- Restructuring the schema hierarchy
- Removing support for a media type

### Minor Version Changes (New Features)

Increment MINOR version when:
- Adding new optional elements or attributes
- Adding new media types
- Adding new enumeration values
- Relaxing validation constraints
- Adding new schema files

### Patch Version Changes (Bug Fixes)

Increment PATCH version when:
- Fixing typos in documentation
- Correcting validation logic errors
- Clarifying ambiguous specifications
- Updating examples

## Backward Compatibility Guidelines

### Guaranteed Compatibility

1. **Reading Forward**: Applications supporting version X.Y must be able to read files from version X.0 through X.Y
2. **Writing Backward**: Applications should write files compatible with the lowest version they claim to support
3. **Unknown Elements**: Applications must ignore unknown elements rather than failing

### Compatibility Matrix

| NFO Version | Can Read | Can Write |
|-------------|----------|-----------|
| 1.0.0 | 1.0.x | 1.0.0 |
| 1.1.0 | 1.0.x - 1.1.x | 1.0.0 or 1.1.0 |
| 2.0.0 | 2.0.x | 2.0.0 |

## Schema Versioning

### URL Structure

Schemas are versioned in their URLs:
```
https://xsd.nfostandard.com/v1/main.xsd
https://xsd.nfostandard.com/v1/Schemas/movie.xsd
```

### Version Negotiation

NFO files specify their version through the schema location:
```xml
xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/v1/main.xsd"
```

### Legacy Support

- Version 1.x schemas remain available indefinitely at their original URLs
- A `latest` alias points to the current stable version
- Deprecated versions are marked but remain functional

## Migration Path

### Minor Version Updates

No migration required. New features are optional:
```xml
<!-- Version 1.0 -->
<movie>
    <title>Example</title>
</movie>

<!-- Version 1.1 (with new optional field) -->
<movie>
    <title>Example</title>
    <awards>Oscar Winner</awards> <!-- New in 1.1 -->
</movie>
```

### Major Version Updates

Provide migration tools and guides:
1. Automated converter tools
2. Field mapping documentation
3. Validation for both versions during transition

## Release Process

### 1. Pre-release

- Version: `X.Y.Z-alpha.N` or `X.Y.Z-beta.N`
- Duration: 30-90 days
- Purpose: Community testing and feedback

### 2. Release Candidate

- Version: `X.Y.Z-rc.N`
- Duration: 14-30 days
- Purpose: Final testing, no new features

### 3. Stable Release

- Version: `X.Y.Z`
- Announcement: Blog post, GitHub release, mailing list

### 4. Long-term Support

- LTS versions: Every major version
- Support period: 3 years minimum
- Security fixes: 5 years

## Deprecation Policy

### Deprecation Timeline

1. **Announcement**: Feature marked deprecated in version X.Y
2. **Warning Period**: Remains functional for entire X.* series
3. **Removal**: Can be removed in version (X+1).0

### Deprecation Marking

In XSD:
```xml
<xs:element name="oldfield" type="xs:string">
    <xs:annotation>
        <xs:documentation>
            DEPRECATED since v1.2.0. Use 'newfield' instead.
            Will be removed in v2.0.0.
        </xs:documentation>
    </xs:annotation>
</xs:element>
```

In Documentation:
```
⚠️ **Deprecated**: This field is deprecated since v1.2.0 and will be removed in v2.0.0. Please use `newfield` instead.
```

## Version Discovery

Applications can discover the NFO Standard version through:

1. **Schema URL**: Extract version from schema location
2. **Version Attribute**: Optional version attribute on root element
3. **Feature Detection**: Check for presence of version-specific elements

## Experimental Features

Experimental features use the `x-` prefix:
```xml
<movie>
    <title>Example</title>
    <x-experimental-field>Value</x-experimental-field>
</movie>
```

Rules:
- May change or be removed without notice
- Not included in stable schema validation
- Graduate to stable features in minor releases

## Change Log

All changes are documented in `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/) format.

## Version Support Matrix

| Version | Status | Released | EOL | Notes |
|---------|--------|----------|-----|-------|
| 1.0.x | Legacy | 2024-01 | 2027-01 | Initial release, LTS |
| 2.0.x | Current | 2024-12 | 2027-12 | Enhanced schema, breaking changes, LTS |
| 2.1.x | Planned | 2025-06 | 2026-06 | New media types |
| 3.0.x | Future | 2026-01 | 2029-01 | Future enhancements |

## Implementation Requirements

### For Schema Authors

1. Never break backward compatibility in minor releases
2. Document all changes in CHANGELOG
3. Provide migration examples for breaking changes
4. Test with multiple validator versions

### for Application developers

1. Declare supported NFO Standard versions
2. Implement forward compatibility (ignore unknown elements)
3. Validate against specific version, not latest
4. Plan for migration between major versions

## Questions?

- GitHub Issues: https://github.com/Biztactix/NFOStandard/issues
- Mailing List: dev@nfostandard.com