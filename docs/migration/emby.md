# Migrating from Emby/Jellyfin to NFO Standard

This guide covers migrating from Emby or Jellyfin NFO files to NFO Standard format. Since Jellyfin is a fork of Emby, they share the same NFO format.

## Overview

Emby/Jellyfin NFO format is based on Kodi's format with some extensions. The migration process is similar to Kodi migration with additional considerations.

## Key Differences

### 1. Root Structure

Emby/Jellyfin uses the same flat structure as Kodi:

**Emby/Jellyfin:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<movie>
    <title>Movie Title</title>
    <lockedfields>OfficialRating|Genres|Studios</lockedfields>
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
        </movie>
    </media>
    <library>
        <lockedfields>OfficialRating|Genres|Studios</lockedfields>
    </library>
</root>
```

### 2. Emby/Jellyfin Specific Fields

| Emby/Jellyfin Field | NFO Standard Location | Notes |
|---------------------|----------------------|-------|
| `<lockedfields>` | `<library>` section | Metadata lock info |
| `<criticrating>` | `<rating name="critic">` | Separate rating type |
| `<customrating>` | `<rating name="custom">` | User-defined rating |
| `<collectionnumber>` | `<setorder>` | Order in collection |
| `<tmdbcollectionid>` | `<setid type="tmdb">` | Collection ID |
| `<providerId>` | `<uniqueid>` | Various provider IDs |
| `<imdb>` | `<uniqueid type="imdb">` | IMDB ID |
| `<tmdb>` | `<uniqueid type="tmdb">` | TMDB ID |
| `<tvdb>` | `<uniqueid type="tvdb">` | TVDB ID |

### 3. Multiple Ratings

**Emby/Jellyfin:**
```xml
<rating>8.5</rating>
<criticrating>85</criticrating>
<customrating>9</customrating>
```

**NFO Standard:**
```xml
<rating name="imdb" value="8.5" votes="100000" default="true"/>
<rating name="critic" value="8.5" max="10"/>
<rating name="custom" value="9" max="10"/>
<userrating>9</userrating>
```

### 4. Provider IDs

**Emby/Jellyfin:**
```xml
<imdb>tt1234567</imdb>
<tmdb>12345</tmdb>
<tvdb>98765</tvdb>
```

**NFO Standard:**
```xml
<uniqueid type="imdb" default="true">tt1234567</uniqueid>
<uniqueid type="tmdb">12345</uniqueid>
<uniqueid type="tvdb">98765</uniqueid>
```

## Special Emby/Jellyfin Features

### 1. Locked Fields

Emby/Jellyfin allows locking specific metadata fields:

```xml
<!-- In library section -->
<library>
    <type>emby</type>
    <lockedfields>
        <field>OfficialRating</field>
        <field>Genres</field>
        <field>Studios</field>
    </lockedfields>
</library>
```

### 2. Display Preferences

**Emby/Jellyfin:**
```xml
<displayorder>MovieName</displayorder>
<primaryimagetag>abc123</primaryimagetag>
```

**NFO Standard:**
```xml
<library>
    <displaypreferences>
        <sortorder>title</sortorder>
        <primaryimage>abc123</primaryimage>
    </displaypreferences>
</library>
```

### 3. Multiple Studios

Both formats support multiple studios similarly:
```xml
<studio>Studio 1</studio>
<studio>Studio 2</studio>
```

## TV Show Considerations

### Series Level

**Emby/Jellyfin tvshow.nfo:**
```xml
<Series>
    <SeriesName>Breaking Bad</SeriesName>
    <Status>Ended</Status>
    <Network>AMC</Network>
    <Airs_DayOfWeek>Sunday</Airs_DayOfWeek>
    <Airs_Time>9:00 PM</Airs_Time>
</Series>
```

**NFO Standard:**
```xml
<tvshow>
    <title>Breaking Bad</title>
    <status>Ended</status>
    <studio>AMC</studio>
    <schedule>
        <airday>Sunday</airday>
        <airtime>21:00</airtime>
        <timezone>America/New_York</timezone>
    </schedule>
</tvshow>
```

### Episode Level

Episode structure is very similar, with main difference being the root element.

## Migration Script

```bash
# Single file conversion
python tools/migration/emby_to_nfo.py movie.nfo -o movie_converted.nfo

# Batch conversion
python tools/migration/emby_to_nfo.py /path/to/library/ --recursive --in-place
```

## Advanced Features

### 1. Subtitles and Audio Streams

**Emby/Jellyfin:**
```xml
<streamdetails>
    <subtitle>
        <language>eng</language>
        <isdefault>true</isdefault>
        <isforced>false</isforced>
    </subtitle>
</streamdetails>
```

**NFO Standard:** (in library section)
```xml
<library>
    <mediainfo>
        <subtitle>
            <language>eng</language>
            <default>true</default>
            <forced>false</forced>
            <codec>srt</codec>
        </subtitle>
    </mediainfo>
</library>
```

### 2. Collections

**Emby/Jellyfin:**
```xml
<set>
    <name>Marvel Cinematic Universe</name>
    <overview>The MCU film series</overview>
</set>
<collectionnumber>5</collectionnumber>
```

**NFO Standard:**
```xml
<setname>Marvel Cinematic Universe</setname>
<setoverview>The MCU film series</setoverview>
<setorder>5</setorder>
```

### 3. People Enhancement

Emby/Jellyfin stores additional person data:

```xml
<actor>
    <name>Actor Name</name>
    <role>Character</role>
    <type>Actor</type>
    <sortorder>0</sortorder>
    <imageurl>http://example.com/actor.jpg</imageurl>
</actor>
```

NFO Standard equivalent:
```xml
<actor>
    <name>Actor Name</name>
    <role>Character</role>
    <order>1</order>
    <thumb>http://example.com/actor.jpg</thumb>
    <type>Actor</type>
</actor>
```

## Maintaining Compatibility

To maintain compatibility with Emby/Jellyfin:

1. **Keep original NFO files**: Store in `.backup` folder
2. **Use compatible naming**: Follow Emby naming conventions
3. **Preserve provider IDs**: Essential for metadata refreshing
4. **Export images**: Maintain poster/fanart structure

## Image Handling

Emby/Jellyfin image storage:
- `folder.jpg` - Primary poster
- `backdrop.jpg` - Fanart
- `logo.png` - Clear logo
- `banner.jpg` - Banner image

Map to NFO Standard:
```xml
<thumb type="poster" url="folder.jpg"/>
<fanart type="background" url="backdrop.jpg"/>
<banner type="logo" url="logo.png"/>
<banner type="banner" url="banner.jpg"/>
```

## Music Metadata

**Emby/Jellyfin album.nfo:**
```xml
<album>
    <title>Album Title</title>
    <artist>Artist Name</artist>
    <year>2023</year>
    <genre>Rock</genre>
</album>
```

Maps directly to NFO Standard `<music>` type.

## Validation

After migration:
```bash
# Validate all converted files
find /path/to/converted -name "*.nfo" -type f | while read file; do
    echo "Validating: $file"
    nfo-validate "$file"
done
```

## Common Issues

1. **Special characters**: Ensure proper UTF-8 encoding
2. **Date formats**: Convert to ISO 8601
3. **Missing required fields**: Add title if missing
4. **Custom fields**: Move to library section
5. **Image paths**: Update relative to absolute paths

## Benefits of Migration

- **Schema validation**: Catch errors early
- **Richer metadata**: Additional fields available
- **Better portability**: Works with more systems
- **Format flexibility**: Export to JSON/Protobuf
- **Future-proof**: Versioned standard