# NFO Standard Plugin for Emby/Jellyfin

This plugin enables Emby and Jellyfin to read and write NFO files following the NFO Standard specification.

## Features

- Full NFO Standard compliance
- Reads all metadata fields including ratings, people, and provider IDs
- Supports movies, TV shows, episodes, and more
- Automatic file monitoring for changes
- Compatible with both Emby and Jellyfin

## Installation

### Jellyfin

1. Download the latest release `NFOStandard.dll`
2. Create folder: `NFOStandard` in your plugins directory:
   - **Windows**: `%ProgramData%\Jellyfin\Server\plugins\`
   - **Linux**: `/var/lib/jellyfin/plugins/`
   - **Docker**: `/config/plugins/`
3. Copy the DLL and plugin.xml to the folder
4. Restart Jellyfin
5. Enable in Dashboard → Plugins

### Emby

1. Download the latest release
2. Go to Settings → Plugins → Manual Plugin Installation
3. Browse and select the plugin file
4. Restart Emby Server

### Building from Source

Requirements:
- .NET Core SDK 5.0 or higher
- Visual Studio 2019+ or VS Code

```bash
cd plugins/emby-jellyfin/NFOStandard
dotnet build -c Release
```

The compiled plugin will be in `bin/Release/net5.0/`

## Configuration

1. Go to Dashboard → Plugins → NFO Standard
2. Configure settings:
   - Enable for Movies
   - Enable for TV Shows
   - Enable for Episodes
   - File naming preferences

## File Structure

The plugin looks for NFO files in standard locations:

### Movies
- Same name as movie: `MovieName (Year).nfo`
- In folder: `movie.nfo`

### TV Shows
- Show folder: `tvshow.nfo`
- Season folder: `season.nfo` (optional)
- Episodes: `ShowName S01E01.nfo`

## NFO Format

Example movie NFO:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>The Matrix</title>
            <year>1999</year>
            <plot>A computer hacker learns about the true nature of reality.</plot>
            <rating name="imdb" value="8.7" votes="1800000" default="true"/>
            <contentrating country="USA" board="MPAA" rating="R"/>
            <genre>Science Fiction</genre>
            <genre>Action</genre>
            <uniqueid type="imdb" default="true">tt0133093</uniqueid>
            <uniqueid type="tmdb">603</uniqueid>
        </movie>
    </media>
</root>
```

## Supported Metadata

### Movies
- Titles (main, original, sort)
- Year, runtime
- Plot, outline, tagline
- Multiple ratings with sources
- Content ratings by country
- Genres and tags
- Studios/production companies
- Collections
- People (actors, directors, writers)
- Provider IDs (IMDB, TMDB, etc.)
- Release dates

### TV Shows
- All movie fields plus:
- Status (ended, continuing)
- Premiered date
- Air schedule
- Season/episode information
- Network/studio

### Episodes
- Title and episode numbers
- Air date
- Plot
- Guest stars
- Directors and writers

## Provider Priority

The plugin integrates with Jellyfin/Emby's provider system:

1. Local NFO files (highest priority)
2. Online providers (TMDB, TVDB, etc.)
3. Embedded metadata

## Writing NFO Files

The plugin can also save metadata back to NFO files:

1. Enable in plugin settings
2. Use "Save metadata" option in item menu
3. Files are saved in NFO Standard format

## Troubleshooting

### Plugin not loading
- Check .NET version compatibility
- Verify file permissions
- Check server logs for errors

### NFO files not detected
- Ensure files are named correctly
- Validate XML syntax
- Check file encoding (UTF-8)

### Metadata not updating
- Refresh metadata for the item
- Check "Lock metadata" settings
- Verify NFO file is newer than last scan

## Advanced Features

### Custom Fields

The plugin preserves Jellyfin/Emby-specific fields in the library section:

```xml
<library>
    <type>jellyfin</type>
    <dateadded>2023-01-01T00:00:00</dateadded>
    <playcount>5</playcount>
    <lastplayed>2023-12-01T20:30:00</lastplayed>
</library>
```

### Locked Fields

Prevent specific fields from being overwritten:

```xml
<library>
    <lockedfields>
        <field>OfficialRating</field>
        <field>Genres</field>
    </lockedfields>
</library>
```

## Performance

- Async file operations
- Caching of parsed NFO files
- Minimal overhead on library scans
- Change monitoring for updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Include tests for new features

## Support

- GitHub Issues: https://github.com/Biztactix/NFOStandard/issues
- Jellyfin Forum: https://forum.jellyfin.org/
- Emby Community: https://emby.media/community/

## License

This plugin is released under The Unlicense, making it free for everyone to use and modify.