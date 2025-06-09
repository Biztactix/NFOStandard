# NFO Standard Plex Metadata Agent

This is a Plex metadata agent that reads NFO Standard compliant files and imports metadata into Plex Media Server.

## Features

- Reads NFO Standard XML files for movies and TV shows
- Imports all metadata including titles, plots, ratings, genres, and people
- Supports multiple rating sources (IMDB, TMDB, etc.)
- Handles collections/sets
- Episode-level metadata for TV shows

## Installation

### Method 1: Manual Installation

1. Download the `NFOStandard.bundle` folder
2. Copy it to your Plex plugins directory:
   - **Windows**: `%LOCALAPPDATA%\Plex Media Server\Plug-ins\`
   - **macOS**: `~/Library/Application Support/Plex Media Server/Plug-ins/`
   - **Linux**: `/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/`
3. Restart Plex Media Server
4. The agent will appear in Settings → Agents

### Method 2: Git Clone

```bash
cd "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/"
git clone https://github.com/Biztactix/NFOStandard.git
cd NFOStandard/plugins/plex
cp -r NFOStandard.bundle ../../../
```

## Configuration

1. Go to Settings → Server → Agents
2. Select Movies or TV Shows
3. Enable "NFO Standard" agent
4. Move it to the top of the list to prioritize it

## File Naming

The agent looks for NFO files in these locations:

### Movies
- Same name as movie file: `MovieName (Year).nfo`
- In movie folder: `movie.nfo`

### TV Shows
- In show folder: `tvshow.nfo`
- Episode files: `ShowName - S01E01.nfo`

## NFO File Structure

Movie example:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>Movie Title</title>
            <year>2023</year>
            <plot>Movie plot...</plot>
            <rating name="imdb" value="8.5" votes="10000" default="true"/>
            <genre>Action</genre>
            <genre>Drama</genre>
        </movie>
    </media>
</root>
```

## Supported Fields

### Movies
- title, originaltitle, sorttitle
- year, runtime
- plot, tagline
- rating (multiple sources)
- contentrating
- genre, tag, country
- productioncompany
- setname (collections)
- actor, director, writer, producer
- releasedate
- uniqueid (IMDB, TMDB, etc.)

### TV Shows
- All movie fields plus:
- premiered, status
- studio/network
- season/episode counts
- air schedule

## Limitations

- Plex agents are deprecated in favor of new scanner/agent system
- This agent works with Plex Media Server up to version 1.19.x
- For newer Plex versions, consider using the Plex Meta Manager with NFO support

## Troubleshooting

### Agent not appearing
1. Check the plugin is in the correct directory
2. Ensure proper permissions on the plugin folder
3. Check Plex logs for errors

### Metadata not updating
1. Ensure NFO files are properly formatted
2. Check file permissions
3. Try "Refresh Metadata" on the item
4. Enable debug logging in Plex

### Validation
Validate your NFO files:
```bash
nfo-validate movie.nfo
```

## Contributing

Please submit issues and pull requests to the main NFOStandard repository.

## License

This plugin is released under The Unlicense, same as the NFO Standard project.