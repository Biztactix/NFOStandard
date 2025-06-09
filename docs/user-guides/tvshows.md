# TV Show Metadata Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Show vs Episode Structure](#show-vs-episode-structure)
- [TV Show Metadata](#tv-show-metadata)
- [Episode Metadata](#episode-metadata)
- [Season Organization](#season-organization)
- [Special Episodes](#special-episodes)
- [Cast Management](#cast-management)
- [Artwork Guidelines](#artwork-guidelines)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

NFOStandard supports comprehensive TV show metadata with separate structures for shows and episodes. This guide covers both series-level information and individual episode details.

## Quick Start

### Minimal TV Show NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <tvshow>
            <title>Breaking Bad</title>
            <year>2008</year>
            <plot>A high school chemistry teacher turned methamphetamine producer.</plot>
        </tvshow>
    </media>
</root>
```

### Minimal Episode NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <episode>
            <title>Pilot</title>
            <season>1</season>
            <episode>1</episode>
            <plot>Walter White, a struggling high school chemistry teacher...</plot>
        </episode>
    </media>
</root>
```

## Show vs Episode Structure

### File Organization
```
TV Shows/
├── Breaking Bad/
│   ├── tvshow.nfo          # Series metadata
│   ├── poster.jpg          # Series poster
│   ├── fanart.jpg          # Series backdrop
│   ├── Season 1/
│   │   ├── S01E01.mkv
│   │   ├── S01E01.nfo      # Episode metadata
│   │   ├── S01E02.mkv
│   │   ├── S01E02.nfo
│   │   └── season01-poster.jpg
│   └── Season 2/
│       ├── S02E01.mkv
│       └── S02E01.nfo
```

## TV Show Metadata

### Core Show Elements

```xml
<tvshow>
    <!-- Required -->
    <title>Breaking Bad</title>
    
    <!-- Essential -->
    <originaltitle>Breaking Bad</originaltitle>
    <sorttitle>Breaking Bad</sorttitle>
    <year>2008</year>  <!-- First aired year -->
    <endyear>2013</endyear>  <!-- Final year -->
    <plot>A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine...</plot>
    <outline>Chemistry teacher becomes meth kingpin</outline>
    
    <!-- Status -->
    <status>Ended</status>  <!-- Continuing, Ended, Canceled -->
    <episodeguide>
        <url>https://api.thetvdb.com/series/81189/episodes</url>
    </episodeguide>
</tvshow>
```

### Ratings and Classification

```xml
<tvshow>
    <rating name="imdb" max="10" default="true">
        <value>9.5</value>
        <votes>1800000</votes>
    </rating>
    
    <rating name="tvdb" max="10">
        <value>9.4</value>
        <votes>5000</votes>
    </rating>
    
    <contentrating country="USA" board="TV">
        <rating>TV-MA</rating>
        <reason>Violence, language, drug content</reason>
    </contentrating>
    
    <contentrating country="UK" board="BBFC">
        <rating>18</rating>
    </contentrating>
</tvshow>
```

### Production Information

```xml
<tvshow>
    <studio>AMC</studio>
    <studio>Sony Pictures Television</studio>
    
    <network>AMC</network>
    <distributor>Sony Pictures Television</distributor>
    
    <country>United States</country>
    <language>en</language>
    <language>es</language>
    
    <genre>Crime</genre>
    <genre>Drama</genre>
    <genre>Thriller</genre>
    
    <tag>Drug Trade</tag>
    <tag>Cancer</tag>
    <tag>Family Drama</tag>
    <tag>Neo-Western</tag>
</tvshow>
```

### Series Identifiers

```xml
<tvshow>
    <uniqueid type="tvdb" default="true">81189</uniqueid>
    <uniqueid type="imdb">tt0903747</uniqueid>
    <uniqueid type="tmdb">1396</uniqueid>
    <uniqueid type="tvmaze">169</uniqueid>
</tvshow>
```

### Show Runtime

```xml
<tvshow>
    <runtime>45</runtime>  <!-- Typical episode duration in minutes -->
    <totalseasons>5</totalseasons>
    <totalepisodes>62</totalepisodes>
</tvshow>
```

## Episode Metadata

### Core Episode Elements

```xml
<episode>
    <!-- Required -->
    <title>Ozymandias</title>
    <season>5</season>
    <episode>14</episode>
    
    <!-- Essential -->
    <plot>Walt goes on the run. Jesse is taken hostage...</plot>
    <aired>2013-09-15</aired>
    <runtime>48</runtime>
    
    <!-- Episode numbering -->
    <displayseason>5</displayseason>  <!-- For split seasons -->
    <displayepisode>14</displayepisode>
    <absolute>60</absolute>  <!-- Absolute episode number -->
    <dvd_season>5</dvd_season>  <!-- DVD ordering -->
    <dvd_episode>14</dvd_episode>
</episode>
```

### Episode Ratings

```xml
<episode>
    <rating name="imdb" max="10">
        <value>10.0</value>
        <votes>180000</votes>
    </rating>
    
    <rating name="tvdb" max="10">
        <value>9.9</value>
    </rating>
    
    <userrating>10.0</userrating>
</episode>
```

### Episode Production

```xml
<episode>
    <director>
        <name>Rian Johnson</name>
    </director>
    
    <writer>
        <name>Moira Walley-Beckett</name>
    </writer>
    
    <credits>Peter Gould</credits>  <!-- Additional credits -->
    <credits>Sam Catlin</credits>
</episode>
```

### Episode Identifiers

```xml
<episode>
    <uniqueid type="tvdb" default="true">4589771</uniqueid>
    <uniqueid type="imdb">tt2301451</uniqueid>
    <uniqueid type="tmdb">62161</uniqueid>
</episode>
```

## Season Organization

### Season Metadata (in show NFO)

```xml
<tvshow>
    <seasons>
        <season number="1">
            <aired>2008-01-20</aired>
            <episodes>7</episodes>
            <poster>season01-poster.jpg</poster>
        </season>
        <season number="2">
            <aired>2009-03-08</aired>
            <episodes>13</episodes>
            <poster>season02-poster.jpg</poster>
        </season>
    </seasons>
</tvshow>
```

### Multi-Part Episodes

```xml
<episode>
    <title>To'hajiilee</title>
    <season>5</season>
    <episode>13</episode>
    <part>1</part>  <!-- Part 1 of 2 -->
    <partcount>2</partcount>
</episode>
```

## Special Episodes

### Special Episode Types

```xml
<episode>
    <title>Breaking Bad: The Movie</title>
    <season>0</season>  <!-- Specials are season 0 -->
    <episode>1</episode>
    <specialtype>movie</specialtype>  <!-- movie, recap, behind-the-scenes -->
    <plot>Feature-length conclusion to the series...</plot>
</episode>
```

### Crossover Episodes

```xml
<episode>
    <title>Crossover Special</title>
    <crossover>
        <show>Better Call Saul</show>
        <season>1</season>
        <episode>1</episode>
    </crossover>
</episode>
```

## Cast Management

### Series Regular Cast

```xml
<tvshow>
    <actor>
        <name>Bryan Cranston</name>
        <role>Walter White</role>
        <order>1</order>
        <thumb>https://image.tmdb.org/t/p/original/bryan.jpg</thumb>
        <seasons>1,2,3,4,5</seasons>  <!-- Appears in these seasons -->
    </actor>
    
    <actor>
        <name>Aaron Paul</name>
        <role>Jesse Pinkman</role>
        <order>2</order>
        <thumb>https://image.tmdb.org/t/p/original/aaron.jpg</thumb>
        <seasons>1,2,3,4,5</seasons>
    </actor>
</tvshow>
```

### Guest Stars (Episode-specific)

```xml
<episode>
    <actor>
        <name>Robert Forster</name>
        <role>Ed Galbraith</role>
        <order>10</order>  <!-- Guest star order -->
        <guest>true</guest>
    </actor>
</episode>
```

## Artwork Guidelines

### Show Artwork

```xml
<tvshow>
    <!-- Series poster -->
    <poster>
        <url>https://image.tmdb.org/t/p/original/series-poster.jpg</url>
        <season>all</season>
    </poster>
    
    <!-- Season-specific posters -->
    <poster>
        <url>https://image.tmdb.org/t/p/original/season1-poster.jpg</url>
        <season>1</season>
    </poster>
    
    <!-- Series fanart -->
    <fanart>
        <url>https://image.tmdb.org/t/p/original/series-backdrop.jpg</url>
    </fanart>
    
    <!-- Banner -->
    <banner>
        <url>https://artworks.thetvdb.com/banners/graphical/81189-g.jpg</url>
        <type>graphical</type>
    </banner>
    
    <!-- Clear logo -->
    <clearlogo>
        <url>https://fanart.tv/fanart/tv/81189/hdtvlogo/breaking-bad.png</url>
    </clearlogo>
</tvshow>
```

### Episode Artwork

```xml
<episode>
    <!-- Episode still/screenshot -->
    <thumb>
        <url>https://image.tmdb.org/t/p/original/episode-still.jpg</url>
        <width>1920</width>
        <height>1080</height>
    </thumb>
</episode>
```

## Examples

### Complete TV Show Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <tvshow>
            <title>Stranger Things</title>
            <originaltitle>Stranger Things</originaltitle>
            <sorttitle>Stranger Things</sorttitle>
            
            <year>2016</year>
            <status>Continuing</status>
            
            <plot>When a young boy disappears, his mother, a police chief and his friends must confront terrifying supernatural forces in order to get him back.</plot>
            <outline>Kids in 1980s Indiana encounter supernatural forces</outline>
            
            <runtime>50</runtime>
            <totalseasons>4</totalseasons>
            <totalepisodes>42</totalepisodes>
            
            <rating name="imdb" max="10" default="true">
                <value>8.7</value>
                <votes>1200000</votes>
            </rating>
            
            <contentrating country="USA" board="TV">
                <rating>TV-14</rating>
            </contentrating>
            
            <genre>Drama</genre>
            <genre>Fantasy</genre>
            <genre>Horror</genre>
            
            <tag>1980s</tag>
            <tag>Supernatural</tag>
            <tag>Kids</tag>
            <tag>Mystery</tag>
            
            <studio>21 Laps Entertainment</studio>
            <network>Netflix</network>
            
            <country>United States</country>
            <language>en</language>
            
            <creator>
                <name>Matt Duffer</name>
            </creator>
            <creator>
                <name>Ross Duffer</name>
            </creator>
            
            <actor>
                <name>Millie Bobby Brown</name>
                <role>Eleven</role>
                <order>1</order>
                <thumb>https://image.tmdb.org/t/p/original/millie.jpg</thumb>
            </actor>
            <actor>
                <name>Finn Wolfhard</name>
                <role>Mike Wheeler</role>
                <order>2</order>
                <thumb>https://image.tmdb.org/t/p/original/finn.jpg</thumb>
            </actor>
            
            <uniqueid type="tvdb" default="true">305288</uniqueid>
            <uniqueid type="imdb">tt4574334</uniqueid>
            <uniqueid type="tmdb">66732</uniqueid>
            
            <poster>
                <url>https://image.tmdb.org/t/p/original/poster.jpg</url>
            </poster>
            <fanart>
                <url>https://image.tmdb.org/t/p/original/fanart.jpg</url>
            </fanart>
            <clearlogo>
                <url>https://fanart.tv/fanart/tv/305288/hdtvlogo/stranger-things.png</url>
            </clearlogo>
        </tvshow>
    </media>
</root>
```

### Complete Episode Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <episode>
            <title>Chapter One: The Vanishing of Will Byers</title>
            <showtitle>Stranger Things</showtitle>
            
            <season>1</season>
            <episode>1</episode>
            <absolute>1</absolute>
            
            <plot>On his way home from a friend's house, young Will sees something terrifying. Nearby, a sinister secret lurks in the depths of a government lab.</plot>
            
            <aired>2016-07-15</aired>
            <runtime>49</runtime>
            
            <rating name="imdb" max="10">
                <value>8.6</value>
                <votes>45000</votes>
            </rating>
            
            <director>
                <name>Matt Duffer</name>
            </director>
            <director>
                <name>Ross Duffer</name>
            </director>
            
            <writer>
                <name>Matt Duffer</name>
            </writer>
            <writer>
                <name>Ross Duffer</name>
            </writer>
            
            <credits>The Duffer Brothers</credits>
            
            <actor>
                <name>Millie Bobby Brown</name>
                <role>Eleven</role>
                <order>1</order>
            </actor>
            <actor>
                <name>Matthew Modine</name>
                <role>Dr. Martin Brenner</role>
                <order>15</order>
                <guest>true</guest>
            </actor>
            
            <uniqueid type="tvdb" default="true">5741523</uniqueid>
            <uniqueid type="imdb">tt4635282</uniqueid>
            
            <thumb>
                <url>https://image.tmdb.org/t/p/original/episode-still.jpg</url>
            </thumb>
            
            <watched>true</watched>
            <playcount>2</playcount>
            <lastplayed>2023-10-31</lastplayed>
        </episode>
    </media>
</root>
```

### Anime Series Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <tvshow>
            <title>Attack on Titan</title>
            <originaltitle>進撃の巨人</originaltitle>
            <sorttitle>Attack on Titan</sorttitle>
            <alternatetitle lang="ja-romaji">Shingeki no Kyojin</alternatetitle>
            
            <year>2013</year>
            <endyear>2023</endyear>
            <status>Ended</status>
            
            <plot>Humanity fights for survival against giant humanoid Titans.</plot>
            
            <anime>true</anime>
            <totalseasons>4</totalseasons>
            <totalepisodes>87</totalepisodes>
            
            <studio>Wit Studio</studio>
            <studio>MAPPA</studio>
            
            <genre>Action</genre>
            <genre>Drama</genre>
            <genre>Fantasy</genre>
            
            <tag>Post-Apocalyptic</tag>
            <tag>Military</tag>
            <tag>Shounen</tag>
            
            <uniqueid type="anidb">9541</uniqueid>
            <uniqueid type="mal">16498</uniqueid>
            <uniqueid type="tvdb">267440</uniqueid>
        </tvshow>
    </media>
</root>
```

## Troubleshooting

### Common Issues

1. **Episode Ordering**
   - Use `displayseason`/`displayepisode` for split seasons
   - Use `absolute` for anime absolute numbering
   - Use `dvd_season`/`dvd_episode` for DVD order

2. **Missing Episodes**
   - Ensure consistent numbering
   - Check for special episodes in season 0
   - Verify episode count matches metadata

3. **Cast Information**
   - Differentiate series regulars from guest stars
   - Use season lists for recurring characters
   - Include character names in role field

### Best Practices

1. **File Naming**
   - Use consistent naming: `S01E01.nfo`
   - Place `tvshow.nfo` in series root
   - Keep season posters with episodes

2. **Metadata Completeness**
   - Always include show title in episodes
   - Add aired dates for proper ordering
   - Include unique identifiers

3. **Artwork**
   - Provide season-specific posters
   - Include episode thumbnails
   - Use appropriate aspect ratios

4. **Special Handling**
   - Use season 0 for specials
   - Document multi-part episodes
   - Track crossover information

## Related Topics

- [Movies Guide](movies.md)
- [Anime Guide](anime.md)
- [Artwork Specifications](artwork.md)
- [Migration from Other Formats](../migration/)