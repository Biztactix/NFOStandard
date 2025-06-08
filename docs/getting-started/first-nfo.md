# Your First NFO File

This guide will walk you through creating your first NFO file using the NFO Standard.

## Basic Structure

Every NFO file starts with the same basic structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <!-- Your media content goes here -->
    </media>
</root>
```

## Creating a Movie NFO

Let's create an NFO file for a movie. Create a file named `movie.nfo`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <!-- Required field -->
            <title>The Matrix</title>
            
            <!-- Optional but recommended fields -->
            <originaltitle>The Matrix</originaltitle>
            <year>1999</year>
            <runtime>136</runtime>
            
            <!-- Ratings from various sources -->
            <rating name="imdb" value="8.7" votes="1800000" default="true"/>
            <rating name="tmdb" value="8.2" votes="20000"/>
            
            <!-- Plot information -->
            <outline>A computer hacker learns about the true nature of reality.</outline>
            <plot>When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.</plot>
            <tagline>Welcome to the Real World</tagline>
            
            <!-- Genre and tags -->
            <genre>Science Fiction</genre>
            <genre>Action</genre>
            <tag>cyberpunk</tag>
            <tag>artificial intelligence</tag>
            
            <!-- Media information -->
            <contentrating country="USA" board="MPAA" rating="R"/>
            
            <!-- Unique identifiers -->
            <uniqueid type="imdb" default="true">tt0133093</uniqueid>
            <uniqueid type="tmdb">603</uniqueid>
            
            <!-- Credits -->
            <director>
                <name>Lana Wachowski</name>
            </director>
            <director>
                <name>Lilly Wachowski</name>
            </director>
            
            <actor>
                <name>Keanu Reeves</name>
                <role>Neo</role>
                <order>1</order>
            </actor>
            <actor>
                <name>Laurence Fishburne</name>
                <role>Morpheus</role>
                <order>2</order>
            </actor>
            <actor>
                <name>Carrie-Anne Moss</name>
                <role>Trinity</role>
                <order>3</order>
            </actor>
            
            <!-- Additional metadata -->
            <country>USA</country>
            <productioncompany>Warner Bros.</productioncompany>
            <releasedate>1999-03-31</releasedate>
        </movie>
    </media>
</root>
```

## Creating a TV Show NFO

For TV shows, create `tvshow.nfo`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" 
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <tvshow>
            <title>Stranger Things</title>
            <originaltitle>Stranger Things</originaltitle>
            <year>2016</year>
            
            <rating name="imdb" value="8.7" votes="1000000"/>
            
            <plot>When a young boy disappears, his mother, a police chief and his friends must confront terrifying supernatural forces in order to get him back.</plot>
            
            <genre>Drama</genre>
            <genre>Fantasy</genre>
            <genre>Horror</genre>
            
            <contentrating country="USA" board="TV" rating="TV-14"/>
            
            <uniqueid type="imdb" default="true">tt4574334</uniqueid>
            <uniqueid type="tvdb">305288</uniqueid>
            
            <studio>Netflix</studio>
            <premiered>2016-07-15</premiered>
            
            <actor>
                <name>Millie Bobby Brown</name>
                <role>Eleven</role>
                <order>1</order>
            </actor>
            
            <season>1</season>
            <episode>1</episode>
            <displayseason>1</displayseason>
            <displayepisode>1</displayepisode>
        </tvshow>
    </media>
</root>
```

## File Naming Conventions

### Movies
- Single file: `MovieName (Year).nfo`
- Example: `The Matrix (1999).nfo`

### TV Shows
- Show info: `tvshow.nfo` (in show folder)
- Season info: `season##.nfo` (in season folder)
- Episode info: `ShowName S##E##.nfo`

## Validation

After creating your NFO file, validate it:

1. **Online**: Use our online validator (coming soon)
2. **Command line**: `nfo-validate movie.nfo`
3. **In your IDE**: If you have the extension installed

## Common Mistakes to Avoid

1. **Missing required fields**: Every media type has required fields (like `title`)
2. **Invalid date formats**: Use `YYYY-MM-DD` format
3. **Wrong encoding**: Always use UTF-8
4. **Incorrect schema location**: Ensure the xsi:schemaLocation points to the correct URL

## Next Steps

- [Learn about validation](validation.md)
- [Explore different media types](../user-guides/movies.md)
- [Add images and artwork](../user-guides/artwork.md)
- [Advanced features](../advanced/extensions.md)