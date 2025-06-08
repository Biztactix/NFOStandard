# Migrating from Plex to NFO Standard

This guide helps you export metadata from Plex Media Server and convert it to NFO Standard format.

## Overview

Plex stores metadata in its internal database rather than NFO files. This guide shows how to:
1. Export Plex metadata
2. Convert to NFO Standard format
3. Maintain compatibility with Plex

## Plex Metadata Structure

Plex uses:
- SQLite database for metadata
- Local Media Assets for images
- Online agents (TMDB, TVDB, etc.) for metadata

## Export Methods

### Method 1: Using Plex API

```python
# Example script to export Plex metadata
import requests
from plexapi.server import PlexServer

PLEX_URL = 'http://localhost:32400'
PLEX_TOKEN = 'your-plex-token'

plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Export movie metadata
for movie in plex.library.section('Movies').all():
    metadata = {
        'type': 'movie',
        'movie': {
            'title': movie.title,
            'year': movie.year,
            'plot': movie.summary,
            'rating': {
                '@name': 'plex',
                '@value': str(movie.rating),
                '@votes': str(movie.ratingCount) if hasattr(movie, 'ratingCount') else '0'
            },
            'genre': [genre.tag for genre in movie.genres],
            'actor': [{'name': actor.tag, 'role': actor.role} for actor in movie.actors],
            'director': [{'name': director.tag} for director in movie.directors]
        }
    }
    # Convert to NFO using our converter
```

### Method 2: Database Export

Access Plex database directly:
- Windows: `%LOCALAPPDATA%\Plex Media Server\Plug-in Support\Databases\`
- macOS: `~/Library/Application Support/Plex Media Server/Plug-in Support/Databases/`
- Linux: `/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-in Support/Databases/`

## Field Mappings

| Plex Field | NFO Standard Field | Notes |
|------------|-------------------|-------|
| title | `<title>` | Direct mapping |
| originalTitle | `<originaltitle>` | Direct mapping |
| year | `<year>` | Direct mapping |
| summary | `<plot>` | Direct mapping |
| tagline | `<tagline>` | Direct mapping |
| duration | `<runtime>` | Convert milliseconds to minutes |
| rating | `<rating @value>` | Plex uses 0-10 scale |
| contentRating | `<contentrating>` | Map to appropriate board |
| guid | `<uniqueid>` | Extract type and ID |
| addedAt | `<library><addeddate>` | Library metadata |
| viewCount | `<library><viewcount>` | Library metadata |
| lastViewedAt | `<library><lastviewed>` | Library metadata |

## Metadata Agent Mappings

Plex uses various agents that map to NFO Standard:

### Movie Agents
- **Plex Movie**: Generic metadata
- **The Movie Database**: `<uniqueid type="tmdb">`
- **Legacy IMDB**: `<uniqueid type="imdb">`

### TV Agents
- **The Movie Database**: `<uniqueid type="tmdb">`
- **TheTVDB**: `<uniqueid type="tvdb">`

## Converting Collections

Plex Collections → NFO Standard Sets:

```xml
<!-- Plex Collection: Marvel Cinematic Universe -->
<setname>Marvel Cinematic Universe</setname>
<setoverview>The Marvel Cinematic Universe film series</setoverview>
```

## Image Export

Plex stores images in:
- Metadata folder with hashed names
- Local Media Assets (if enabled)

Map to NFO Standard:
```xml
<thumb type="poster" width="1000" height="1500" url="file:///path/to/poster.jpg"/>
<fanart type="background" width="1920" height="1080" url="file:///path/to/fanart.jpg"/>
```

## Migration Script

```bash
# Export Plex library to NFO files
python tools/migration/plex_to_nfo.py \
    --server http://localhost:32400 \
    --token YOUR-PLEX-TOKEN \
    --library "Movies" \
    --output /path/to/nfo/files/
```

## Maintaining Plex Compatibility

To use NFO files with Plex:

1. **Install XBMCnfoMoviesImporter**: Plex agent that reads NFO files
2. **Configure Local Media Assets**: Enable in agent settings
3. **File naming**: Use Plex naming conventions
   - Movies: `MovieName (Year).nfo`
   - TV Shows: `tvshow.nfo` in show folder
   - Episodes: `ShowName - S01E01.nfo`

## Advanced Mappings

### Plex Ratings to NFO Standard

```python
# Plex stores multiple ratings
ratings = []

# Audience rating
if movie.audienceRating:
    ratings.append({
        '@name': 'audience',
        '@value': str(movie.audienceRating),
        '@votes': str(movie.audienceRatingCount)
    })

# Critic rating  
if movie.rating:
    ratings.append({
        '@name': 'critic',
        '@value': str(movie.rating),
        '@default': 'true'
    })
```

### Plex Moods/Styles to Tags

```xml
<!-- Plex moods and styles become tags -->
<tag>Dark</tag>
<tag>Suspenseful</tag>
<tag>Mind Bending</tag>
```

### Plex Chapters

```xml
<!-- Convert Plex chapters -->
<chapters>
    <chapter>
        <starttime>0</starttime>
        <endtime>300</endtime>
        <title>Opening</title>
    </chapter>
</chapters>
```

## TV Show Specifics

### Show Level
```xml
<tvshow>
    <title>Breaking Bad</title>
    <year>2008</year>
    <premiered>2008-01-20</premiered>
    <status>Ended</status>
    <studio>AMC</studio>
    <season>5</season>  <!-- Total seasons -->
    <episode>62</episode>  <!-- Total episodes -->
</tvshow>
```

### Episode Level
```xml
<episodedetails>
    <title>Pilot</title>
    <season>1</season>
    <episode>1</episode>
    <aired>2008-01-20</aired>
    <plot>Episode plot...</plot>
</episodedetails>
```

## Music Library

Plex music metadata to NFO Standard:

```xml
<music>
    <title>Album Title</title>
    <artist>Artist Name</artist>
    <albumartist>Album Artist</albumartist>
    <year>2023</year>
    <genre>Rock</genre>
    <track>
        <position>1</position>
        <title>Track Title</title>
        <duration>245</duration>
    </track>
</music>
```

## Troubleshooting

### Common Issues

1. **Missing metadata**: Plex may not have all fields populated
2. **Agent conflicts**: Different agents provide different data
3. **Image paths**: May need to copy/reorganize images
4. **Special characters**: Ensure proper XML encoding

### Validation

After export, validate all NFO files:
```bash
find /path/to/exports -name "*.nfo" -exec nfo-validate {} \;
```

## Benefits

- **Portability**: Move metadata between systems
- **Backup**: Preserve metadata outside Plex
- **Flexibility**: Use with other media managers
- **Version control**: Track metadata changes