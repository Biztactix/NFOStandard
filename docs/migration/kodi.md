# Migrating from Kodi NFO to NFO Standard

This guide helps you migrate your existing Kodi (XBMC) NFO files to the NFO Standard format.

## Overview

Kodi NFO files and NFO Standard share many similarities, but there are key differences in structure, naming conventions, and supported fields.

## Key Differences

### 1. Root Structure

**Kodi NFO:**
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<movie>
    <title>Movie Title</title>
    <!-- content -->
</movie>
```

**NFO Standard:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>Movie Title</title>
            <!-- content -->
        </movie>
    </media>
</root>
```

### 2. Field Mappings

| Kodi Field | NFO Standard Field | Notes |
|------------|-------------------|-------|
| `<title>` | `<title>` | Direct mapping |
| `<originaltitle>` | `<originaltitle>` | Direct mapping |
| `<sorttitle>` | `<sorttitle>` | Direct mapping |
| `<set>` | `<setname>` | Renamed field |
| `<year>` | `<year>` or within `<releasedate>` | Can be extracted from releasedate |
| `<top250>` | Not supported | Use ratings instead |
| `<trailer>` | `<trailer>` | Enhanced with attributes |
| `<votes>` | Within `<rating>` element | Part of rating structure |
| `<rating>` | `<rating @value>` | Different structure |
| `<mpaa>` | `<contentrating>` | Enhanced structure |
| `<playcount>` | In `<library>` section | Moved to library metadata |
| `<lastplayed>` | In `<library>` section | Moved to library metadata |
| `<id>` | `<uniqueid>` | Enhanced structure |
| `<filenameandpath>` | Not in media section | Use library metadata |

### 3. Ratings Structure

**Kodi:**
```xml
<rating>8.5</rating>
<votes>12345</votes>
```

**NFO Standard:**
```xml
<rating name="imdb" value="8.5" votes="12345" max="10" default="true"/>
<rating name="tmdb" value="8.3" votes="5000" max="10"/>
```

### 4. Content Ratings

**Kodi:**
```xml
<mpaa>PG-13</mpaa>
```

**NFO Standard:**
```xml
<contentrating country="USA" board="MPAA" rating="PG-13" image="mpaa_pg13.png"/>
```

### 5. Unique IDs

**Kodi:**
```xml
<id>tt1234567</id>
<imdbid>tt1234567</imdbid>
<tmdbid>12345</tmdbid>
```

**NFO Standard:**
```xml
<uniqueid type="imdb" default="true">tt1234567</uniqueid>
<uniqueid type="tmdb">12345</uniqueid>
```

## Migration Script

Use our migration tool to automatically convert your Kodi NFO files:

```bash
python tools/migration/kodi_to_nfo.py input.nfo -o output.nfo
```

For batch conversion:
```bash
python tools/migration/kodi_to_nfo.py /path/to/kodi/library/ --recursive
```

## Manual Migration Steps

### 1. Movies

1. Wrap existing content in NFO Standard structure
2. Convert ratings to new format
3. Update content ratings
4. Convert unique IDs
5. Move library-specific data

### 2. TV Shows

**Kodi tvshow.nfo:**
```xml
<tvshow>
    <title>Breaking Bad</title>
    <season>-1</season>
    <episode>-1</episode>
</tvshow>
```

**NFO Standard:**
```xml
<tvshow>
    <title>Breaking Bad</title>
    <season>5</season>  <!-- Total seasons -->
    <episode>62</episode>  <!-- Total episodes -->
    <displayseason>-1</displayseason>  <!-- For display purposes -->
    <displayepisode>-1</displayepisode>
</tvshow>
```

### 3. Episodes

Kodi and NFO Standard episode structures are similar, but NFO Standard adds:
- Multiple ratings support
- Enhanced actor information
- Better streaming metadata

## Special Considerations

### 1. Artwork

Kodi stores artwork URLs differently:

**Kodi:**
```xml
<thumb>http://example.com/poster.jpg</thumb>
<fanart>
    <thumb>http://example.com/fanart1.jpg</thumb>
    <thumb>http://example.com/fanart2.jpg</thumb>
</fanart>
```

**NFO Standard:**
```xml
<thumb type="poster" width="1000" height="1500" url="http://example.com/poster.jpg"/>
<fanart type="background" width="1920" height="1080" url="http://example.com/fanart1.jpg"/>
<fanart type="background" width="1920" height="1080" url="http://example.com/fanart2.jpg"/>
```

### 2. Actor Images

**Kodi:**
```xml
<actor>
    <name>Actor Name</name>
    <role>Character</role>
    <thumb>http://example.com/actor.jpg</thumb>
</actor>
```

**NFO Standard:** (same structure, but can add more fields)
```xml
<actor>
    <name>Actor Name</name>
    <role>Character</role>
    <order>1</order>
    <thumb>http://example.com/actor.jpg</thumb>
    <bio>Actor biography...</bio>
    <url>https://www.imdb.com/name/nm0000123/</url>
</actor>
```

### 3. File Paths

Kodi includes file paths in NFO files. NFO Standard separates this:

```xml
<!-- In library section, not media section -->
<library>
    <type>kodi</type>
    <filepath>/media/movies/movie.mkv</filepath>
    <playcount>2</playcount>
    <lastplayed>2023-12-01T20:30:00</lastplayed>
</library>
```

## Validation

After migration, validate your files:

```bash
nfo-validate migrated-movie.nfo
```

## Common Issues

1. **Missing required fields**: Ensure `<title>` is present
2. **Invalid date formats**: Convert to ISO 8601 (YYYY-MM-DD)
3. **Unrecognized elements**: Remove Kodi-specific fields like `<top250>`
4. **Character encoding**: Ensure UTF-8 encoding

## Benefits of Migration

- **Better compatibility** across different media managers
- **Richer metadata** with enhanced field support  
- **Validation support** with XSD schemas
- **Future-proof** format with versioning
- **Multi-format support** (XML, JSON, Protobuf)