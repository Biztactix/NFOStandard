# Emby 4.8 API Investigation Results - People/Actors Handling

## Executive Summary

This document presents the comprehensive results of investigating the Emby 4.8 API for proper people/actors handling. The investigation uncovered the correct methods, interfaces, and patterns required to implement robust people metadata management in Emby plugins.

## Key API Discoveries

### 1. ILibraryManager Interface Methods

**Primary People-Related Methods Found:**

```csharp
// Core people retrieval methods
Person GetPerson(string name);
List<PersonInfo> GetPeople(BaseItem item);  
List<PersonInfo> GetPeople(InternalPeopleQuery query);
List<Person> GetPeopleItems(InternalPeopleQuery query);
List<string> GetPeopleNames(InternalPeopleQuery query);

// People modification methods  
void UpdatePeople(BaseItem item, List<PersonInfo> people);
Task UpdatePeopleAsync(BaseItem item, IReadOnlyList<PersonInfo> people, CancellationToken cancellationToken);
```

### 2. PersonInfo Structure

**Complete PersonInfo Properties:**
- `Name` - Person's full name
- `Role` - Character role (for actors)
- `Type` - PersonType enum (Actor, Director, Writer, Producer, etc.)
- `ImageUrl` - Person's image/thumbnail URL
- `SortOrder` - Display order (newer versions)
- `ProviderIds` - External metadata provider IDs

### 3. Database Architecture

**Multi-Table Storage System:**
- **People Table** - Core person entities
- **TypedBaseItems Table** - Person items with full metadata
- **PeopleBaseItemMap Table** - Item-to-person relationships with roles

### 4. Integration Patterns

**Correct Plugin Integration:**
1. Use `MetadataResult.People` to provide people data
2. Let Emby's systems handle person creation and database storage
3. Avoid direct database manipulation
4. Follow provider pattern for metadata extraction

## Implementation Architecture

### Enhanced Plugin Components

#### 1. Core Metadata Providers
- **NFOStandardMovieProvider** - Enhanced with ILibraryManager integration
- **NFOStandardSeriesProvider** - TV series people handling
- **NFOStandardPersonProvider** - Person-specific metadata

#### 2. Metadata Writers
- **NFOStandardPeopleWriter** - Writes people data back to NFO files

#### 3. Configuration System
- **PluginConfiguration** - Comprehensive settings for people handling

### Key Features Implemented

#### Advanced People Extraction
- Actors with roles, ordering, and images
- Directors, writers, producers, creators
- Configurable actor limits for performance
- Image URL preservation
- Provider ID mapping

#### Robust Error Handling
- Graceful handling of malformed data
- Configurable logging levels
- Fallback to legacy NFO formats
- Performance monitoring

#### Configuration Control
- Enable/disable people extraction
- Maximum actor limits
- Detailed logging options
- Strict namespace validation
- Legacy format fallback

## Technical Implementation Details

### People Processing Flow

```
1. NFO File Parsing
   ↓
2. People Element Extraction
   ↓  
3. PersonInfo Object Creation
   ↓
4. MetadataResult.People Assignment
   ↓
5. Emby's People Management System
   ↓
6. Database Storage (People, TypedBaseItems, PeopleBaseItemMap)
```

### Supported NFO Elements

```xml
<!-- Actor with full metadata -->
<actor>
    <name>Actor Name</name>
    <role>Character Name</role>
    <order>1</order>
    <thumb>http://example.com/image.jpg</thumb>
</actor>

<!-- Director -->
<director>
    <name>Director Name</name>
    <thumb>http://example.com/director.jpg</thumb>
</director>

<!-- Writer -->
<writer>
    <name>Writer Name</name>
    <thumb>http://example.com/writer.jpg</thumb>
</writer>

<!-- Producer -->
<producer>
    <name>Producer Name</name>
    <thumb>http://example.com/producer.jpg</thumb>
</producer>
```

## Performance Optimizations

### 1. Configurable Limits
- Maximum actors per item (default: 50)
- Prevents performance issues with large casts
- Configurable through plugin settings

### 2. Efficient Processing
- Direct integration with Emby's APIs
- No duplicate person creation
- Lazy loading of people data

### 3. Error Recovery
- Graceful handling of missing data
- Fallback mechanisms for legacy formats
- Detailed logging for troubleshooting

## Extension Methods and Helper Classes

### Custom Extensions Found
- None specifically for people in Emby 4.8 core
- Plugin provides own helper methods for NFO parsing
- Configuration-driven behavior modification

### Repository Integration
- Works with Emby's ItemRepository for people queries
- Integrates with PeopleRepository for person management
- Follows Emby's established patterns

## API Version Compatibility

### Emby 4.8 Specific Features
- ILibraryManager.GetPeople() methods
- PersonInfo structure with all required fields
- MetadataResult.People property for provider integration

### Jellyfin Compatibility
- Inherits same API structure from Emby fork
- UpdatePeopleAsync available in newer versions
- Enhanced people query capabilities

## Best Practices Identified

### 1. Plugin Architecture
- Inject ILibraryManager through dependency injection
- Use MetadataResult.People for people data
- Implement ILocalMetadataProvider pattern correctly

### 2. People Management
- Create PersonInfo objects with complete metadata
- Respect item.SupportsPeople property
- Use appropriate PersonType enums

### 3. Performance
- Implement configurable limits
- Use efficient parsing techniques
- Provide detailed logging for debugging

### 4. Error Handling
- Graceful degradation for missing data
- Comprehensive exception handling
- User-friendly error messages

## Future Enhancement Opportunities

### 1. Advanced Features
- Async people operations (UpdatePeopleAsync)
- Enhanced person metadata (birth dates, biographies)
- Episode-level cast information
- Multiple role support per person

### 2. Performance Improvements
- Batch people operations
- Caching for frequently accessed people
- Background people metadata updates

### 3. Integration Enhancements
- External metadata provider integration
- Automatic image downloading
- People metadata validation

## Conclusion

The investigation successfully identified the complete set of APIs and patterns required for robust people/actors handling in Emby 4.8. The implementation provides:

1. **Complete API Integration** - Proper use of ILibraryManager methods
2. **Robust People Handling** - Full support for all person types
3. **Performance Optimization** - Configurable limits and efficient processing
4. **Error Resilience** - Graceful handling of edge cases
5. **Future Compatibility** - Extensible architecture for enhancements

The solution demonstrates that Emby 4.8 provides comprehensive APIs for people management, and the key is understanding the correct integration patterns and database architecture.

## Files Modified/Created

### Enhanced Existing Files
- `NFOStandardMovieProvider.cs` - Added ILibraryManager integration
- `NFOStandardSeriesProvider.cs` - Enhanced people handling
- `NFOStandardPlugin.cs` - Core plugin structure

### New Files Created
- `NFOStandardPersonProvider.cs` - Person-specific metadata
- `NFOStandardPeopleWriter.cs` - People metadata writing
- `PluginConfiguration.cs` - Comprehensive configuration
- `README_PEOPLE_HANDLING.md` - Implementation documentation

The investigation confirms that Emby 4.8 provides all necessary APIs for people/actors handling, and the implementation demonstrates the correct patterns for plugin integration with the people management system.