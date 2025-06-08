# Changelog

All notable changes to the NFO Standard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation website with user guides and API references
- Python validation tool (`nfo-validate`)
- JavaScript/Node.js validation tool (`@nfostandard/validator`)
- Automated XSD validation testing via GitHub Actions
- Versioning strategy and backward compatibility guidelines
- Additional example files for TV shows and music

### Changed
- Updated schema URLs to use versioned paths
- Improved documentation structure

### Fixed
- Schema validation issues in example files

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