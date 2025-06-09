# NFO Standard Plugin for Emby - Deployment Instructions

## Important: NFO File Naming Convention

**This plugin follows the NFO Standard specification for file naming:**
- NFO files MUST have the same name as the video file with .nfo extension
- Example: `The Matrix (1999).mkv` → `The Matrix (1999).nfo`
- This differs from Emby's default which uses generic names like `movie.nfo`

## Current Status
The plugin is built for Emby Server 4.8.x and provides:
- NFO file reading for Movies and TV Shows
- NFO file writing (saving) for Movies and TV Shows
- Configuration page in Emby settings

## Installation

1. **Download the DLL**
   - Navigate to: `/home/ClaudeCodeRepos/NFOStandard/plugins/emby/NFOStandard/bin/Release/net6.0/`
   - Copy `NFOStandard.dll`

2. **Install in Emby**
   - Copy the DLL to your Emby plugins folder:
     - Windows: `%AppData%\Emby-Server\programdata\plugins\`
     - Linux: `/var/lib/emby/plugins/`
   - Restart Emby Server

3. **Configure**
   - Go to Settings → Plugins → NFO Standard
   - Enable for Movies and/or TV Shows
   - Enable saving metadata if desired

## Usage

### As a Metadata Reader
1. In your library settings, go to "Metadata downloaders"
2. Enable "NFO Standard" 
3. Move it to the top of the list if you want it to take priority

### As a Metadata Saver
1. In your library settings, go to "Metadata savers"
2. Enable "NFO Standard"
3. This will save metadata in NFO Standard format when you save metadata

## Known Limitations

Due to API differences between Emby versions and Jellyfin:
- Some fields may not be fully supported (e.g., collections, sort order for actors)
- The plugin uses Emby's native logging system
- People/cast information is read but not written (Emby handles this separately)

## Troubleshooting

If the plugin doesn't appear:
1. Check Emby logs for loading errors
2. Ensure the DLL is in the correct location
3. Verify .NET 6.0 runtime is installed
4. Try placing the DLL in the system plugins folder instead

## Version Information
- Plugin Version: 1.0.0
- Target Emby Version: 4.8.0.50+
- .NET Version: 6.0