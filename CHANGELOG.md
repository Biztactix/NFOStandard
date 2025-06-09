# Changelog

All notable changes to the NFO Standard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2024-12-09

### 🚨 **BREAKING CHANGES**

This is a major release with significant breaking changes that improve schema quality, validation, and internationalization support.

### Added
- Comprehensive schema annotations and documentation for all types
- Schema versioning with `version` attributes in all XSD files
- Robust data validation with proper constraints and patterns
- ISO standards compliance (ISO 3166-1 country codes, ISO 639-1 language codes, ISO 8601 dates)
- New reusable types: `DateType`, `YearType`, `RuntimeType`, `UserRatingType`
- Enhanced PersonType with gender enumeration and proper constraints
- Automated testing framework (`test_schemas.sh`)
- Example file validation and fixer tools (`fix_examples.sh`)
- Protocol Buffer implementation with C# support
- Complete user guide documentation for all media types
- Implementation plan and roadmap documentation

### Changed
- **BREAKING**: Updated all type names to UpperCamelCase (e.g., `ratingType` → `RatingType`)
- **BREAKING**: ContentRatingType structure changed from attributes to child elements
- **BREAKING**: MediaFileType enhanced structure for banner/thumb/fanart elements
- **BREAKING**: Enhanced data validation with stricter constraints
- **BREAKING**: Country codes must use ISO 3166-1 alpha-2 format (e.g., "USA" → "US")
- **BREAKING**: Language codes must use ISO 639-1 format for subtitle languages
- **BREAKING**: Rating values limited to 1 decimal place precision
- **BREAKING**: Person order values limited to reasonable ranges (max 1000)
- Enhanced schema documentation with comprehensive field descriptions
- Improved element ordering and sequence requirements

### Fixed
- All example files now validate successfully (100% compliance)
- Schema type reference consistency across all media types
- ContentRating structure alignment with actual usage patterns
- Element ordering in TV show and movie schemas
- Unicode character support in example files
- Data type constraints and validation patterns

### Migration from v1.0.0
- Update ContentRating from `<contentRating country="US" rating="PG-13"/>` to:
  ```xml
  <contentRating country="US" board="MPAA">
    <rating>PG-13</rating>
  </contentRating>
  ```
- Update country codes to ISO 3166-1 alpha-2 format
- Update type references in custom schemas to UpperCamelCase
- Validate rating precision (max 1 decimal place)
- Check element ordering in movie/TV show schemas

### Technical Details
- Schema files: 13 schemas with comprehensive validation
- Example files: 10 media types with 100% validation success
- Test coverage: Valid, invalid, and edge case test files
- Documentation: Complete user guides for all media types

## [1.0.0] - 2024-01-15

### Added
- Initial release of NFO Standard
- XSD schemas for multiple media types:
  - Movies (`movie.xsd`)
  - TV Shows (`tvshow.xsd`)
  - Music (`music.xsd`)
  - Audiobooks (`audiobook.xsd`)
  - Podcasts (`podcast.xsd`)
  - Anime (`anime.xsd`)
  - Adult content (`adult.xsd`)
  - Music Videos (`musicvideo.xsd`)
  - Generic videos (`video.xsd`)
- Common schemas:
  - Common types (`common.xsd`)
  - Person types (`person.xsd`)
  - Library metadata (`library.xsd`)
- Master schema (`main.xsd`)
- Example NFO files for movies and podcasts
- Basic README documentation
- The Unlicense license

### Security
- No known security issues

## Version History

- **1.0.0** - Initial stable release (2024-01-15)

[Unreleased]: https://github.com/Biztactix/NFOStandard/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Biztactix/NFOStandard/releases/tag/v1.0.0