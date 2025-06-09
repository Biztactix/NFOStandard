# NFO Standard Plugin - People/Actors Handling Documentation

## Overview

This document describes the comprehensive people/actors handling implementation for the NFO Standard plugin for Emby 4.8. Based on thorough investigation of the Emby 4.8 API, this implementation provides proper integration with Emby's people management system.

## Key Findings from Emby 4.8 API Investigation

### ILibraryManager People-Related Methods

The plugin integrates with the following Emby 4.8 ILibraryManager methods:

- `Person GetPerson(string name)` - Retrieves a single person by name
- `List<PersonInfo> GetPeople(BaseItem item)` - Gets people associated with an item  
- `List<PersonInfo> GetPeople(InternalPeopleQuery query)` - Gets people using a query
- `List<Person> GetPeopleItems(InternalPeopleQuery query)` - Gets person items
- `List<string> GetPeopleNames(InternalPeopleQuery query)` - Gets person names
- `void UpdatePeople(BaseItem item, List<PersonInfo> people)` - Updates people for an item

### PersonInfo Structure

The `PersonInfo` class contains:
- `Name` - Person's name
- `Role` - Character role (for actors)  
- `Type` - PersonType enum (Actor, Director, Writer, Producer, etc.)
- `ImageUrl` - Person's image/thumb URL
- Additional properties for metadata

## Implementation Components

### 1. Enhanced Metadata Providers

#### NFOStandardMovieProvider
- Extracts people data from movie NFO files
- Supports actors, directors, writers, and producers
- Integrates with ILibraryManager for proper people handling
- Configurable limits and detailed logging

#### NFOStandardSeriesProvider  
- Extracts people data from TV series NFO files
- Supports actors, creators, directors, and producers
- Handles series-level cast and crew information

#### NFOStandardPersonProvider
- Dedicated provider for person-specific metadata
- Handles person.nfo files with biographical information
- Supports birth/death dates, birthplace, provider IDs

### 2. Metadata Writing

#### NFOStandardPeopleWriter
- Writes people information back to NFO files
- Maintains NFO Standard format compliance
- Updates existing files or creates new ones as needed

### 3. Configuration Options

The plugin provides extensive configuration through `PluginConfiguration`:

```csharp
public class PluginConfiguration : BasePluginConfiguration
{
    public bool EnablePeopleExtraction { get; set; } = true;
    public bool EnablePeopleWriting { get; set; } = true;
    public int MaxActors { get; set; } = 50;
    public bool StrictNamespaceValidation { get; set; } = false;
    public bool EnableDetailedLogging { get; set; } = false;
    public bool EnableLegacyFallback { get; set; } = true;
}
```

## How People Are Processed

### 1. Extraction Process

1. NFO file is loaded and parsed
2. People elements are extracted based on type:
   - `<actor>` - Actors with name, role, order, thumb
   - `<director>` - Directors with name, thumb
   - `<writer>` - Writers with name, thumb  
   - `<producer>` - Producers with name, thumb
   - `<creator>` - Creators (treated as producers for series)

3. PersonInfo objects are created with appropriate metadata
4. People are stored in `MetadataResult.People` for Emby processing

### 2. Emby Integration

The plugin properly integrates with Emby's people management:

- Uses `MetadataResult.People` to provide people data to Emby
- Emby's internal systems handle person creation and linking
- People are stored in Emby's database tables (People, TypedBaseItems, PeopleBaseItemMap)
- No direct database manipulation - follows Emby's intended patterns

### 3. Configuration Controls

- **EnablePeopleExtraction**: Controls whether people are extracted from NFO files
- **MaxActors**: Limits the number of actors to prevent performance issues
- **EnableDetailedLogging**: Provides detailed logs for debugging
- **EnableLegacyFallback**: Falls back to non-namespaced elements if NFO Standard format not found

## Supported NFO Format

### Actor Example
```xml
<actor>
    <name>John Doe</name>
    <role>Character Name</role>
    <order>1</order>
    <thumb>http://example.com/actor-image.jpg</thumb>
</actor>
```

### Director Example
```xml
<director>
    <name>Jane Director</name>
    <thumb>http://example.com/director-image.jpg</thumb>
</director>
```

### Writer Example
```xml
<writer>
    <name>Script Writer</name>
    <thumb>http://example.com/writer-image.jpg</thumb>
</writer>
```

## Performance Considerations

1. **Actor Limits**: Configurable maximum to prevent performance issues with large casts
2. **Lazy Loading**: People are only processed when NFO files are parsed
3. **Efficient Processing**: Direct integration with Emby's systems avoids duplicate work
4. **Error Handling**: Graceful handling of malformed people data

## Database Integration

The implementation works with Emby's multi-table people storage:

- **People Table**: Core person entities
- **TypedBaseItems Table**: Person items with metadata
- **PeopleBaseItemMap Table**: Relationships between items and people with roles

## Future Enhancements

Potential areas for future development:

1. **Enhanced Person Metadata**: Birth dates, biographies, additional provider IDs
2. **Image Processing**: Automatic download and caching of person images
3. **Async Operations**: Support for UpdatePeopleAsync in newer versions
4. **Role Ordering**: Preserve and utilize actor ordering information
5. **Episode-Level Cast**: Support for episode-specific cast information

## Troubleshooting

### Common Issues

1. **People Not Appearing**: Check `EnablePeopleExtraction` configuration
2. **Too Many Actors**: Adjust `MaxActors` setting
3. **Performance Issues**: Enable `EnableDetailedLogging` to identify bottlenecks
4. **Format Issues**: Verify NFO Standard namespace compliance

### Logging

Enable detailed logging to see people processing:
```
[NFOStandard] Added actor: John Doe as Character Name
[NFOStandard] Added director: Jane Director  
[NFOStandard] Loaded 15 people for movie: Example Movie (Actors: 12, Directors: 1, Writers: 2, Producers: 0)
```

## Compatibility

- **Emby 4.8+**: Full compatibility with ILibraryManager methods
- **Jellyfin**: Compatible with Jellyfin fork (inherits Emby API)
- **NFO Standard**: Compliant with NFO Standard specification
- **Legacy NFO**: Fallback support for traditional NFO formats