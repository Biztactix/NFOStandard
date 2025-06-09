# Movie Metadata Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Elements](#core-elements)
- [Titles and Sorting](#titles-and-sorting)
- [Ratings and Reviews](#ratings-and-reviews)
- [Cast and Crew](#cast-and-crew)
- [Artwork and Images](#artwork-and-images)
- [Collections and Sets](#collections-and-sets)
- [Advanced Features](#advanced-features)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

The movie metadata format in NFOStandard provides comprehensive support for film information, from basic details like title and year to complex metadata like multiple ratings, international titles, and detailed cast information.

## Quick Start

Here's a minimal movie NFO file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>The Matrix</title>
            <year>1999</year>
            <plot>A computer hacker learns about the true nature of reality.</plot>
        </movie>
    </media>
</root>
```

## Core Elements

### Required Fields

| Element | Type | Description | Example |
|---------|------|-------------|---------|
| `title` | string | The movie's title | `<title>Inception</title>` |

### Essential Fields

| Element | Type | Description | Example |
|---------|------|-------------|---------|
| `year` | integer | Release year | `<year>2010</year>` |
| `plot` | string | Full plot description | `<plot>A thief who steals...</plot>` |
| `outline` | string | Brief plot summary | `<outline>Dream heist thriller</outline>` |
| `tagline` | string | Marketing tagline | `<tagline>Your mind is the scene of the crime</tagline>` |
| `runtime` | integer | Duration in minutes | `<runtime>148</runtime>` |
| `releasedate` | date | Release date | `<releasedate>2010-07-16</releasedate>` |

## Titles and Sorting

### Title Variations

```xml
<movie>
    <title>The Dark Knight</title>
    <originaltitle>The Dark Knight</originaltitle>
    <sorttitle>Dark Knight, The</sorttitle>
    <alternatetitle>Batman: The Dark Knight</alternatetitle>
    <alternatetitle lang="es">El Caballero Oscuro</alternatetitle>
    <alternatetitle lang="fr">Le Chevalier Noir</alternatetitle>
</movie>
```

### Title Guidelines
- `title`: Display title in your library's primary language
- `originaltitle`: Original release title
- `sorttitle`: For proper alphabetical sorting (move articles to end)
- `alternatetitle`: Alternative or international titles

## Ratings and Reviews

### Multiple Rating Systems

```xml
<movie>
    <!-- Primary rating -->
    <rating name="imdb" max="10" default="true">
        <value>8.8</value>
        <votes>2300000</votes>
    </rating>
    
    <!-- Additional ratings -->
    <rating name="tmdb" max="10">
        <value>8.4</value>
        <votes>25000</votes>
    </rating>
    
    <rating name="metacritic" max="100">
        <value>74</value>
    </rating>
    
    <rating name="rottentomatoes" max="100">
        <value>87</value>
    </rating>
    
    <!-- User's personal rating -->
    <userrating>9.0</userrating>
</movie>
```

### Content Ratings

```xml
<movie>
    <contentrating country="USA" board="MPAA">
        <rating>PG-13</rating>
        <reason>Intense sequences of violence and action</reason>
        <image>mpaa_pg13.png</image>
    </contentrating>
    
    <contentrating country="UK" board="BBFC">
        <rating>12A</rating>
    </contentrating>
</movie>
```

## Cast and Crew

### Actors

```xml
<movie>
    <actor>
        <name>Leonardo DiCaprio</name>
        <role>Dom Cobb</role>
        <order>1</order>
        <thumb>https://image.tmdb.org/t/p/original/actor1.jpg</thumb>
        <bio>Leonardo Wilhelm DiCaprio is an American actor...</bio>
        <birthdate>1974-11-11</birthdate>
        <birthplace>Los Angeles, California, USA</birthplace>
        <tmdbid>6193</tmdbid>
        <imdbid>nm0000138</imdbid>
    </actor>
    
    <actor>
        <name>Marion Cotillard</name>
        <role>Mal</role>
        <order>2</order>
        <thumb>https://image.tmdb.org/t/p/original/actor2.jpg</thumb>
    </actor>
</movie>
```

### Crew Members

```xml
<movie>
    <director>
        <name>Christopher Nolan</name>
        <thumb>https://image.tmdb.org/t/p/original/director.jpg</thumb>
        <tmdbid>525</tmdbid>
    </director>
    
    <writer>
        <name>Christopher Nolan</name>
    </writer>
    
    <producer>
        <name>Emma Thomas</name>
    </producer>
    
    <composer>
        <name>Hans Zimmer</name>
    </composer>
    
    <cinematographer>
        <name>Wally Pfister</name>
    </cinematographer>
    
    <editor>
        <name>Lee Smith</name>
    </editor>
</movie>
```

## Artwork and Images

### Image Types

```xml
<movie>
    <!-- Main poster -->
    <poster>
        <url>https://image.tmdb.org/t/p/original/poster.jpg</url>
        <width>1000</width>
        <height>1500</height>
        <language>en</language>
    </poster>
    
    <!-- Background/fanart -->
    <fanart>
        <url>https://image.tmdb.org/t/p/original/backdrop.jpg</url>
        <width>1920</width>
        <height>1080</height>
    </fanart>
    
    <!-- Banner -->
    <banner>
        <url>https://image.tmdb.org/t/p/original/banner.jpg</url>
        <width>1000</width>
        <height>185</height>
    </banner>
    
    <!-- Landscape thumb -->
    <landscape>
        <url>https://image.tmdb.org/t/p/original/landscape.jpg</url>
        <width>1920</width>
        <height>1080</height>
    </landscape>
    
    <!-- Logo/clearart -->
    <clearlogo>
        <url>https://fanart.tv/logo.png</url>
    </clearlogo>
    
    <!-- Disc art -->
    <discart>
        <url>https://fanart.tv/disc.png</url>
    </discart>
</movie>
```

## Collections and Sets

```xml
<movie>
    <set>
        <name>The Dark Knight Collection</name>
        <overview>Christopher Nolan's Batman trilogy</overview>
        <order>2</order>  <!-- Position in set -->
    </set>
    
    <!-- Alternative collection format -->
    <collection tmdbid="263">
        <name>The Dark Knight Collection</name>
        <poster>https://image.tmdb.org/t/p/original/collection.jpg</poster>
    </collection>
</movie>
```

## Advanced Features

### Identifiers

```xml
<movie>
    <uniqueid type="imdb" default="true">tt1375666</uniqueid>
    <uniqueid type="tmdb">27205</uniqueid>
    <uniqueid type="tmdb-movie">27205</uniqueid>
</movie>
```

### Genre and Tags

```xml
<movie>
    <genre>Action</genre>
    <genre>Science Fiction</genre>
    <genre>Thriller</genre>
    
    <tag>Mind-bending</tag>
    <tag>Heist</tag>
    <tag>Dreams</tag>
    <tag>IMAX</tag>
</movie>
```

### Production Information

```xml
<movie>
    <studio>Warner Bros. Pictures</studio>
    <studio>Legendary Pictures</studio>
    <studio>Syncopy</studio>
    
    <country>United States</country>
    <country>United Kingdom</country>
    
    <language>en</language>
    <language>ja</language>
    <language>fr</language>
    
    <budget currency="USD">160000000</budget>
    <revenue currency="USD">836848102</revenue>
</movie>
```

### Technical Details

```xml
<movie>
    <quality>
        <resolution>2160</resolution>  <!-- 4K -->
        <hdr>true</hdr>
        <codec>h265</codec>
        <audio>DTS-HD MA 5.1</audio>
    </quality>
    
    <source>Blu-ray</source>
    <edition>Director's Cut</edition>
</movie>
```

### Awards

```xml
<movie>
    <awards>
        <award>
            <name>Academy Award for Best Cinematography</name>
            <year>2011</year>
            <won>true</won>
        </award>
        <award>
            <name>Academy Award for Best Picture</name>
            <year>2011</year>
            <won>false</won>
            <nominated>true</nominated>
        </award>
    </awards>
</movie>
```

## Examples

### Minimal Movie

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>The Shawshank Redemption</title>
            <year>1994</year>
            <plot>Two imprisoned men bond over years, finding redemption.</plot>
            <uniqueid type="imdb">tt0111161</uniqueid>
        </movie>
    </media>
</root>
```

### Standard Movie

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>Blade Runner 2049</title>
            <originaltitle>Blade Runner 2049</originaltitle>
            <sorttitle>Blade Runner 2049</sorttitle>
            <year>2017</year>
            <rating name="imdb" max="10" default="true">
                <value>8.0</value>
                <votes>500000</votes>
            </rating>
            <plot>A young blade runner discovers a secret that leads him to track down former blade runner Rick Deckard.</plot>
            <runtime>164</runtime>
            <contentrating country="USA" board="MPAA">
                <rating>R</rating>
            </contentrating>
            <genre>Science Fiction</genre>
            <genre>Drama</genre>
            <director>
                <name>Denis Villeneuve</name>
            </director>
            <actor>
                <name>Ryan Gosling</name>
                <role>K</role>
                <order>1</order>
            </actor>
            <actor>
                <name>Harrison Ford</name>
                <role>Rick Deckard</role>
                <order>2</order>
            </actor>
            <uniqueid type="imdb" default="true">tt1856101</uniqueid>
            <uniqueid type="tmdb">335984</uniqueid>
            <poster>
                <url>https://image.tmdb.org/t/p/original/poster.jpg</url>
            </poster>
            <fanart>
                <url>https://image.tmdb.org/t/p/original/backdrop.jpg</url>
            </fanart>
        </movie>
    </media>
</root>
```

### Complete Movie

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>Inception</title>
            <originaltitle>Inception</originaltitle>
            <sorttitle>Inception</sorttitle>
            <alternatetitle lang="fr">Origine</alternatetitle>
            <alternatetitle lang="es">El Origen</alternatetitle>
            
            <set>
                <name>Christopher Nolan Collection</name>
                <overview>Films by Christopher Nolan</overview>
            </set>
            
            <year>2010</year>
            <releasedate>2010-07-16</releasedate>
            
            <rating name="imdb" max="10" default="true">
                <value>8.8</value>
                <votes>2300000</votes>
            </rating>
            <rating name="tmdb" max="10">
                <value>8.4</value>
                <votes>33000</votes>
            </rating>
            <rating name="metacritic" max="100">
                <value>74</value>
            </rating>
            <userrating>9.5</userrating>
            
            <outline>A thief who enters dreams takes on one last job.</outline>
            <plot>Dom Cobb is a skilled thief, the absolute best in the dangerous art of extraction: stealing valuable secrets from deep within the subconscious during the dream state when the mind is at its most vulnerable. Cobb's rare ability has made him a coveted player in this treacherous new world of corporate espionage, but it has also made him an international fugitive and cost him everything he has ever loved.</plot>
            <tagline>Your mind is the scene of the crime</tagline>
            
            <runtime>148</runtime>
            
            <contentrating country="USA" board="MPAA">
                <rating>PG-13</rating>
                <reason>Sequences of violence and action throughout</reason>
            </contentrating>
            <contentrating country="UK" board="BBFC">
                <rating>12A</rating>
            </contentrating>
            
            <genre>Action</genre>
            <genre>Science Fiction</genre>
            <genre>Thriller</genre>
            
            <tag>Dreams</tag>
            <tag>Heist</tag>
            <tag>Mind-bending</tag>
            <tag>IMAX</tag>
            <tag>Nonlinear</tag>
            
            <studio>Warner Bros. Pictures</studio>
            <studio>Legendary Pictures</studio>
            <studio>Syncopy</studio>
            
            <country>United States</country>
            <country>United Kingdom</country>
            
            <language>en</language>
            <language>ja</language>
            <language>fr</language>
            
            <budget currency="USD">160000000</budget>
            <revenue currency="USD">836848102</revenue>
            
            <director>
                <name>Christopher Nolan</name>
                <thumb>https://image.tmdb.org/t/p/original/nolan.jpg</thumb>
                <tmdbid>525</tmdbid>
                <imdbid>nm0634240</imdbid>
            </director>
            
            <writer>
                <name>Christopher Nolan</name>
            </writer>
            
            <producer>
                <name>Emma Thomas</name>
            </producer>
            <producer>
                <name>Christopher Nolan</name>
            </producer>
            
            <composer>
                <name>Hans Zimmer</name>
            </composer>
            
            <cinematographer>
                <name>Wally Pfister</name>
            </cinematographer>
            
            <editor>
                <name>Lee Smith</name>
            </editor>
            
            <actor>
                <name>Leonardo DiCaprio</name>
                <role>Dom Cobb</role>
                <order>1</order>
                <thumb>https://image.tmdb.org/t/p/original/leo.jpg</thumb>
                <tmdbid>6193</tmdbid>
                <imdbid>nm0000138</imdbid>
            </actor>
            <actor>
                <name>Marion Cotillard</name>
                <role>Mal</role>
                <order>2</order>
                <thumb>https://image.tmdb.org/t/p/original/marion.jpg</thumb>
                <tmdbid>8293</tmdbid>
            </actor>
            <actor>
                <name>Elliot Page</name>
                <role>Ariadne</role>
                <order>3</order>
                <thumb>https://image.tmdb.org/t/p/original/elliot.jpg</thumb>
                <tmdbid>27578</tmdbid>
            </actor>
            
            <uniqueid type="imdb" default="true">tt1375666</uniqueid>
            <uniqueid type="tmdb">27205</uniqueid>
            
            <poster>
                <url>https://image.tmdb.org/t/p/original/poster.jpg</url>
                <width>1000</width>
                <height>1500</height>
                <language>en</language>
            </poster>
            <poster>
                <url>https://image.tmdb.org/t/p/original/poster_fr.jpg</url>
                <language>fr</language>
            </poster>
            
            <fanart>
                <url>https://image.tmdb.org/t/p/original/backdrop1.jpg</url>
                <width>1920</width>
                <height>1080</height>
            </fanart>
            <fanart>
                <url>https://image.tmdb.org/t/p/original/backdrop2.jpg</url>
                <width>1920</width>
                <height>1080</height>
            </fanart>
            
            <banner>
                <url>https://image.tmdb.org/t/p/original/banner.jpg</url>
            </banner>
            
            <clearlogo>
                <url>https://fanart.tv/logo.png</url>
            </clearlogo>
            
            <quality>
                <resolution>2160</resolution>
                <hdr>true</hdr>
                <codec>h265</codec>
                <audio>DTS-HD MA 5.1</audio>
            </quality>
            
            <source>UHD Blu-ray</source>
            <edition>Special Edition</edition>
            
            <awards>
                <award>
                    <name>Academy Award for Best Cinematography</name>
                    <year>2011</year>
                    <won>true</won>
                </award>
                <award>
                    <name>Academy Award for Best Visual Effects</name>
                    <year>2011</year>
                    <won>true</won>
                </award>
            </awards>
            
            <trailer>https://www.youtube.com/watch?v=YoHD9XEInc0</trailer>
            
            <watched>true</watched>
            <playcount>3</playcount>
            <lastplayed>2023-12-15</lastplayed>
        </movie>
    </media>
</root>
```

## Troubleshooting

### Common Issues

1. **Validation Errors**
   - Ensure required `<title>` element is present
   - Check date formats (YYYY-MM-DD)
   - Verify rating values are within max range

2. **Image Display Issues**
   - Use absolute URLs for remote images
   - Check image accessibility
   - Verify correct aspect ratios

3. **Character Encoding**
   - Always use UTF-8 encoding
   - Properly escape special characters
   - Use language attributes for international titles

### Best Practices

1. **Identifiers**
   - Always include at least one unique identifier
   - Prefer IMDB ID as primary for movies
   - Include TMDB ID for artwork

2. **Titles**
   - Use sorttitle for proper ordering
   - Include original title if different
   - Add international titles with language codes

3. **Ratings**
   - Mark one rating as default
   - Include vote counts when available
   - Separate user ratings from critic ratings

4. **Images**
   - Provide multiple image types
   - Include dimensions for proper display
   - Use high-quality sources

## Related Topics

- [TV Shows Guide](tvshows.md)
- [Artwork Specifications](artwork.md)
- [Internationalization](../advanced/i18n.md)
- [Migration from Other Formats](../migration/)