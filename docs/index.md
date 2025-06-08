# NFO Standard Documentation

Welcome to the comprehensive documentation for the NFO Standard - an open, unified metadata format for media files.

## Quick Start

The NFO Standard provides a consistent way to store metadata for various media types including movies, TV shows, music, audiobooks, podcasts, and more.

### Basic Structure

Every NFO file follows this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <!-- Media type content here -->
    </media>
</root>
```

## Documentation Sections

### Getting Started
- [Installation Guide](getting-started/installation.md)
- [Your First NFO File](getting-started/first-nfo.md)
- [Validation](getting-started/validation.md)

### User Guides
- [Movies](user-guides/movies.md)
- [TV Shows](user-guides/tvshows.md)
- [Music](user-guides/music.md)
- [Audiobooks](user-guides/audiobooks.md)
- [Podcasts](user-guides/podcasts.md)
- [Anime](user-guides/anime.md)

### Developer Resources
- [API Reference](api-reference/index.md)
- [Schema Documentation](api-reference/schemas.md)
- [Validation Libraries](api-reference/validation.md)
- [Integration Guide](api-reference/integration.md)

### Migration
- [From Kodi NFO](migration/kodi.md)
- [From Plex](migration/plex.md)
- [From Emby](migration/emby.md)

### Advanced Topics
- [Internationalization](advanced/i18n.md)
- [Custom Extensions](advanced/extensions.md)
- [Best Practices](advanced/best-practices.md)

## Why NFO Standard?

- **Unified Format**: One standard for all media types
- **Extensible**: Easy to add custom fields
- **Well-Documented**: Comprehensive schemas and examples
- **Open Source**: Free to use and contribute

## Quick Examples

### Movie NFO
```xml
<movie>
    <title>Inception</title>
    <year>2010</year>
    <rating name="imdb" value="8.8" votes="2000000"/>
    <genre>Sci-Fi</genre>
    <genre>Action</genre>
    <director>
        <name>Christopher Nolan</name>
    </director>
</movie>
```

### TV Show NFO
```xml
<tvshow>
    <title>Breaking Bad</title>
    <year>2008</year>
    <rating name="imdb" value="9.5" votes="1500000"/>
    <genre>Drama</genre>
    <genre>Crime</genre>
    <season>1</season>
    <episode>1</episode>
</tvshow>
```

## Contributing

We welcome contributions! See our [Contributing Guide](contributing.md) for details.

## Support

- [GitHub Issues](https://github.com/Biztactix/NFOStandard/issues)
- [Community Forum](#) (Coming Soon)