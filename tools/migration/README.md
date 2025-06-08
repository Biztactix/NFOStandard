# NFO Standard Migration Tools

This directory contains tools for migrating from various media manager formats to NFO Standard.

## Available Converters

### Kodi/XBMC → NFO Standard (`kodi_to_nfo.py`)

Converts Kodi/XBMC NFO files to NFO Standard format.

```bash
# Single file
python kodi_to_nfo.py movie.nfo -o movie_standard.nfo

# Directory (recursive)
python kodi_to_nfo.py /path/to/kodi/library/ --recursive

# In-place conversion (creates backups)
python kodi_to_nfo.py /path/to/library/ --in-place --recursive
```

**Features:**
- Preserves all metadata
- Converts ratings to multi-source format
- Handles all media types (movies, TV shows, episodes)
- Creates backup files when converting in-place

### Emby/Jellyfin → NFO Standard (`emby_to_nfo.py`)

Converts Emby or Jellyfin NFO files to NFO Standard format.

```bash
# Single file
python emby_to_nfo.py movie.nfo -o movie_standard.nfo

# Directory conversion
python emby_to_nfo.py /path/to/emby/library/ --recursive

# In-place with backups
python emby_to_nfo.py /path/to/library/ --in-place --recursive
```

**Features:**
- Handles Emby-specific fields (locked fields, custom ratings)
- Converts multiple rating types
- Preserves collection information
- Supports all Emby/Jellyfin media types

### Plex → NFO Standard (`plex_to_nfo.py`)

Exports metadata from Plex Media Server to NFO Standard files.

```bash
# Export movie library
python plex_to_nfo.py \
    --server http://localhost:32400 \
    --token YOUR-PLEX-TOKEN \
    --library "Movies" \
    --output /path/to/export/

# Export TV shows
python plex_to_nfo.py \
    --server http://plex.local:32400 \
    --token YOUR-TOKEN \
    --library "TV Shows"

# Use config file
python plex_to_nfo.py \
    --config plex.conf \
    --library "Music" \
    --flatten
```

**Config file format (plex.conf):**
```ini
[plex]
server = http://localhost:32400
token = YOUR-PLEX-TOKEN
```

**Features:**
- Direct export from Plex database
- Exports all metadata including ratings, collections, and people
- Downloads poster and fanart images
- Supports movies, TV shows, and music
- Maintains Plex library structure

## Installation

### Requirements

```bash
# Basic requirements
pip install lxml

# For Plex export
pip install plexapi

# For image handling (optional)
pip install pillow requests
```

### Getting Your Plex Token

1. Sign in to Plex Web App
2. Browse to a library item
3. Click "..." → "Get Info" → "View XML"
4. Look for `X-Plex-Token` in the URL

Or use this command:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"user": {"login": "YOUR_EMAIL", "password": "YOUR_PASSWORD"}}' \
  https://plex.tv/users/sign_in.json
```

## Field Mappings

### Common Mappings

| Source Field | NFO Standard Field | Notes |
|--------------|-------------------|-------|
| title | title | Direct mapping |
| year | year | Extracted from dates if needed |
| plot/summary | plot | Direct mapping |
| rating | rating[@value] | Converted to multi-rating |
| mpaa | contentrating | Enhanced structure |
| id/guid | uniqueid | Multiple ID support |

### Rating Conversions

**Kodi/Emby:**
```xml
<!-- Source -->
<rating>8.5</rating>
<votes>12345</votes>

<!-- NFO Standard -->
<rating name="imdb" value="8.5" votes="12345" max="10" default="true"/>
```

**Plex:**
```xml
<!-- Multiple ratings preserved -->
<rating name="critic" value="8.5" max="10"/>
<rating name="audience" value="9.0" max="10"/>
<rating name="plex" value="8.7" max="10" default="true"/>
```

## Batch Processing

### Convert entire library
```bash
# Kodi library
find /media/kodi -name "*.nfo" -type f | while read file; do
    python kodi_to_nfo.py "$file"
done

# Emby/Jellyfin library  
python emby_to_nfo.py /var/lib/jellyfin/metadata/ --recursive

# Export all Plex libraries
for lib in "Movies" "TV Shows" "Music"; do
    python plex_to_nfo.py --config plex.conf --library "$lib"
done
```

### Validation after conversion
```bash
# Validate all converted files
find /path/to/converted -name "*.nfo" -exec nfo-validate {} \;
```

## Advanced Usage

### Custom Field Mapping

Edit the converter scripts to add custom field mappings:

```python
# In kodi_to_nfo.py
FIELD_MAPPINGS = {
    'movie': {
        'customfield': 'targetfield',
        # Add your mappings
    }
}
```

### Preserve Original Files

Always recommended:
```bash
# Create backup before conversion
cp -r /media/library /media/library.backup

# Or use built-in backup
python kodi_to_nfo.py /media/library --in-place --recursive
# Creates .kodi.backup files
```

### Logging

Enable verbose output:
```bash
python emby_to_nfo.py /path/to/library --verbose --recursive > conversion.log 2>&1
```

## Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements.txt
```

### Plex Connection Issues
- Ensure Plex server is running
- Check token is valid
- Try local IP instead of hostname
- Disable SSL verification if using self-signed cert

### Character Encoding
- All converters use UTF-8
- Source files with different encoding may need preprocessing
- Use `iconv` to convert if needed

### Large Libraries
- Use `--flatten` for Plex to avoid deep directory structures
- Process in batches for very large libraries
- Monitor disk space when exporting images

## Contributing

To add support for a new format:

1. Create new converter script
2. Follow existing patterns for structure
3. Map fields to NFO Standard
4. Add tests and documentation
5. Submit pull request

## Support

- GitHub Issues: https://github.com/Biztactix/NFOStandard/issues
- Documentation: https://nfostandard.com/docs/migration/