# NFO Standard Reference Plugins

This directory contains reference implementation plugins for popular media management systems, demonstrating how to integrate NFO Standard support.

## Available Plugins

### Plex Media Server
- **Location**: `plex/NFOStandard.bundle/`
- **Type**: Metadata Agent (Legacy)
- **Features**: Reads NFO Standard files for movies and TV shows
- **Status**: Works with Plex <= 1.19.x

### Emby/Jellyfin
- **Location**: `emby-jellyfin/NFOStandard/`
- **Type**: .NET Plugin
- **Features**: Full read/write support for NFO Standard
- **Status**: Active development, supports latest versions

## Quick Start

### For Plex Users
```bash
# Copy to Plex plugins directory
cp -r plex/NFOStandard.bundle "/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins/"
# Restart Plex
```

### For Jellyfin Users
```bash
# Build the plugin
cd emby-jellyfin/NFOStandard
dotnet build -c Release
# Copy to Jellyfin plugins
cp -r bin/Release/net5.0 /var/lib/jellyfin/plugins/NFOStandard
# Restart Jellyfin
```

## Plugin Architecture

### Common Features
All plugins implement:
- NFO file discovery
- XML parsing with namespace support
- Field mapping to native metadata
- Multi-rating support
- Provider ID handling

### Integration Points

1. **File Discovery**
   - Look for `movie.nfo` or `[filename].nfo`
   - TV shows: `tvshow.nfo`
   - Episodes: `[episode].nfo`

2. **Metadata Mapping**
   - See [Field Mappings](../docs/field-mappings.md)
   - Preserve unknown fields
   - Handle missing optional fields

3. **Validation**
   - Check for NFO Standard namespace
   - Validate against XSD (optional)
   - Graceful fallback for non-compliant files

## Development Guidelines

### Creating a New Plugin

1. **Choose Integration Method**
   - Native plugin API (preferred)
   - External scanner
   - API wrapper

2. **Implement Core Features**
   ```python
   def find_nfo_file(media_path):
       # Check standard locations
       pass
   
   def parse_nfo(nfo_path):
       # Parse XML with namespace
       pass
   
   def map_metadata(nfo_data, native_format):
       # Map fields according to spec
       pass
   ```

3. **Handle Edge Cases**
   - Missing files
   - Invalid XML
   - Partial metadata
   - Character encoding

4. **Add Logging**
   - Debug NFO discovery
   - Log parsing errors
   - Track field mappings

### Best Practices

1. **Respect User Preferences**
   - Allow disabling NFO reading
   - Configurable field priority
   - Lock field support

2. **Performance**
   - Cache parsed NFO data
   - Monitor file changes
   - Async operations where possible

3. **Compatibility**
   - Support both namespaced and non-namespaced files
   - Graceful degradation
   - Version detection

## Testing

### Test Files
Use the example files in `/examples/`:
- `ExampleMovie.xml`
- `examples/tvshow.xml`
- `examples/anime.xml`

### Validation
```bash
# Validate your NFO files
nfo-validate examples/movie.xml

# Test with the format comparison tool
python tools/converters/format_comparison.py examples/
```

### Integration Tests
1. Place NFO files with media
2. Trigger library scan
3. Verify metadata import
4. Check for errors in logs

## Contributing

To add support for a new media manager:

1. Create a new directory: `plugins/[platform-name]/`
2. Include a README with installation instructions
3. Implement core NFO reading functionality
4. Add examples and tests
5. Submit a pull request

### Plugin Requirements

- Read NFO Standard compliant files
- Map to native metadata format
- Handle errors gracefully
- Include documentation
- Open source license

## Platform-Specific Notes

### Kodi
- Native NFO support (different format)
- Use our converter tools for migration
- Consider XBMC NFO Importer addon

### Plex (New Agent)
- Legacy agents deprecated
- Use Plex Meta Manager instead
- Or implement as scanner

### MediaPortal
- XML-based metadata
- Similar structure to NFO
- Direct mapping possible

### Universal Media Server
- Java-based implementation
- Plugin API available
- Metadata provider interface

## Resources

- [NFO Standard Specification](https://nfostandard.com)
- [Field Mappings](../docs/field-mappings.md)
- [Validation Tools](../tools/python-validator/)
- [Example Files](../examples/)

## Support

For plugin-specific issues:
- Check the plugin's README
- Review platform documentation
- Open an issue on GitHub

For NFO Standard questions:
- See main documentation
- Use validation tools
- Contact maintainers