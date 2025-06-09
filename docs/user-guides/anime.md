# Anime Metadata Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Anime-Specific Elements](#anime-specific-elements)
- [Title Handling](#title-handling)
- [Season and Episode Organization](#season-and-episode-organization)
- [Studio and Production](#studio-and-production)
- [Character and Voice Acting](#character-and-voice-acting)
- [Anime Categories](#anime-categories)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

Anime metadata in NFOStandard extends the TV show format with specific elements for Japanese animation. This guide covers the unique aspects of documenting anime series, movies, and OVAs.

## Quick Start

### Minimal Anime Series NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <anime>
            <title>Steins;Gate</title>
            <originaltitle>シュタインズ・ゲート</originaltitle>
            <year>2011</year>
            <type>TV</type>
            <episodes>24</episodes>
        </anime>
    </media>
</root>
```

### Minimal Anime Episode NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <episode>
            <title>Turning Point</title>
            <titlejp>境界面上のシュタインズゲート</titlejp>
            <anime>Steins;Gate</anime>
            <season>1</season>
            <episode>1</episode>
            <absolute>1</absolute>
        </episode>
    </media>
</root>
```

## Anime-Specific Elements

### Core Anime Information

```xml
<anime>
    <!-- Type classification -->
    <type>TV</type>  <!-- TV, Movie, OVA, ONA, Special -->
    <subtype>Series</subtype>  <!-- Series, Film, Short -->
    
    <!-- Episode information -->
    <episodes>24</episodes>
    <episodelength>24</episodelength>  <!-- minutes per episode -->
    <status>Finished Airing</status>  <!-- Airing, Finished Airing, Not Yet Aired -->
    
    <!-- Source material -->
    <source>Visual Novel</source>  <!-- Manga, Light Novel, Visual Novel, Original, Game -->
    <adaptation>Full</adaptation>  <!-- Full, Partial, Original Story -->
</anime>
```

### Anime Identifiers

```xml
<anime>
    <anidbid>7729</anidbid>
    <malid>9253</malid>  <!-- MyAnimeList ID -->
    <anilistid>9253</anilistid>
    <animenewsnetworkid>11770</animenewsnetworkid>
    <kitsu>steins-gate</kitsu>
    
    <!-- Alternative IDs -->
    <tvdbid>247926</tvdbid>
    <tmdbid>61557</tmdbid>
    <imdbid>tt1910272</imdbid>
</anime>
```

### Broadcast Information

```xml
<anime>
    <aired>
        <from>2011-04-06</from>
        <to>2011-09-14</to>
    </aired>
    
    <broadcast>
        <day>Wednesday</day>
        <time>02:05</time>  <!-- JST -->
        <timezone>JST</timezone>
    </broadcast>
    
    <season>Spring 2011</season>  <!-- Anime season -->
    <premiered>Spring 2011</premiered>
</anime>
```

## Title Handling

### Multiple Title Formats

```xml
<anime>
    <!-- Display title (localized) -->
    <title>Attack on Titan</title>
    
    <!-- Original Japanese title -->
    <originaltitle>進撃の巨人</originaltitle>
    
    <!-- Romanized title -->
    <titlejp>Shingeki no Kyojin</titlejp>
    
    <!-- English title variations -->
    <titleeng>Attack on Titan</titleeng>
    <alternatetitle>Advancing Giants</alternatetitle>
    
    <!-- Other languages -->
    <alternatetitle lang="de">Angriff auf die Titanen</alternatetitle>
    <alternatetitle lang="fr">L'Attaque des Titans</alternatetitle>
    
    <!-- Synonyms -->
    <synonym>AoT</synonym>
    <synonym>SnK</synonym>
</anime>
```

### Title Guidelines
- Use the most common English title as `<title>`
- Always include `<originaltitle>` in Japanese
- Add `<titlejp>` for romaji (romanized Japanese)
- Include common abbreviations as synonyms

## Season and Episode Organization

### Anime Seasons (Cours)

```xml
<anime>
    <!-- For split-cour series -->
    <seasons>
        <season number="1">
            <title>First Cour</title>
            <episodes>12</episodes>
            <aired>
                <from>2023-04-01</from>
                <to>2023-06-24</to>
            </aired>
        </season>
        <season number="2">
            <title>Second Cour</title>
            <episodes>12</episodes>
            <aired>
                <from>2023-10-07</from>
                <to>2023-12-23</to>
            </aired>
        </season>
    </seasons>
</anime>
```

### Episode Numbering

```xml
<episode>
    <!-- Standard numbering -->
    <season>1</season>
    <episode>5</episode>
    
    <!-- Absolute numbering (important for anime) -->
    <absolute>5</absolute>
    
    <!-- For long-running series -->
    <arc>Water 7</arc>
    <arcnumber>3</arcnumber>
    
    <!-- Special episodes -->
    <special>false</special>
    <specialtype>OVA</specialtype>  <!-- OVA, ONA, Special, Recap -->
</episode>
```

## Studio and Production

### Animation Studios

```xml
<anime>
    <studios>
        <studio primary="true">
            <name>Wit Studio</name>
            <role>Animation Production</role>
            <seasons>1-3</seasons>
        </studio>
        <studio>
            <name>MAPPA</name>
            <role>Animation Production</role>
            <seasons>4</seasons>
        </studio>
        <studio>
            <name>Production I.G</name>
            <role>Production Cooperation</role>
        </studio>
    </studios>
</anime>
```

### Production Committee

```xml
<anime>
    <producers>
        <producer>Pony Canyon</producer>
        <producer>Dentsu</producer>
        <producer>Mainichi Broadcasting System</producer>
        <producer>Pony Canyon Enterprise</producer>
    </producers>
    
    <licensors>
        <licensor region="NA">Funimation</licensor>
        <licensor region="EU">Anime Limited</licensor>
        <licensor region="AU">Madman Entertainment</licensor>
    </licensors>
</anime>
```

## Character and Voice Acting

### Character Information

```xml
<anime>
    <characters>
        <character>
            <name>Eren Yeager</name>
            <namejp>エレン・イェーガー</namejp>
            <role>Main</role>  <!-- Main, Supporting, Minor -->
            <description>A young man who dreams of the world beyond the walls...</description>
            <image>https://cdn.myanimelist.net/images/characters/eren.jpg</image>
        </character>
        <character>
            <name>Mikasa Ackerman</name>
            <namejp>ミカサ・アッカーマン</namejp>
            <role>Main</role>
        </character>
    </characters>
</anime>
```

### Voice Actors (Seiyuu)

```xml
<anime>
    <voiceactors>
        <voiceactor>
            <character>Eren Yeager</character>
            <actor>Yoshimasa Hosoya</actor>
            <actorjp>細谷佳正</actorjp>
            <language>Japanese</language>
            <image>https://cdn.myanimelist.net/images/voiceactors/hosoya.jpg</image>
        </voiceactor>
        <voiceactor>
            <character>Eren Yeager</character>
            <actor>Bryce Papenbrook</actor>
            <language>English</language>
        </voiceactor>
    </voiceactors>
</anime>
```

## Anime Categories

### Genre Classification

```xml
<anime>
    <!-- Standard genres -->
    <genre>Action</genre>
    <genre>Drama</genre>
    <genre>Fantasy</genre>
    
    <!-- Anime-specific genres -->
    <animegenre>Shounen</animegenre>  <!-- Demographic -->
    <animegenre>Military</animegenre>
    <animegenre>Super Power</animegenre>
    
    <!-- Themes -->
    <theme>Survival</theme>
    <theme>Post-Apocalyptic</theme>
    <theme>Gore</theme>
    
    <!-- Demographics -->
    <demographic>Shounen</demographic>  <!-- Shounen, Shoujo, Seinen, Josei -->
</anime>
```

### Content Ratings

```xml
<anime>
    <!-- Age ratings -->
    <rating system="MPAA">
        <value>TV-MA</value>
        <reason>Violence and gore</reason>
    </rating>
    
    <!-- Anime-specific ratings -->
    <contentrating>
        <violence>High</violence>
        <profanity>Mild</profanity>
        <nudity>None</nudity>
        <sexual>None</sexual>
    </contentrating>
    
    <!-- MAL rating -->
    <score provider="MAL">8.54</score>
    <scoredby>2500000</scoredby>
</anime>
```

### Tags and Themes

```xml
<anime>
    <!-- Setting tags -->
    <tag>Historical</tag>
    <tag>Medieval</tag>
    <tag>Europe</tag>
    
    <!-- Content tags -->
    <tag>Gore</tag>
    <tag>Survival</tag>
    <tag>Tragedy</tag>
    
    <!-- Style tags -->
    <tag>Dark Fantasy</tag>
    <tag>Plot Twists</tag>
    <tag>Character Development</tag>
</anime>
```

## Related Media

### Anime Relations

```xml
<anime>
    <relations>
        <relation type="Sequel">
            <title>Attack on Titan Season 2</title>
            <malid>25777</malid>
        </relation>
        <relation type="Prequel">
            <title>Attack on Titan: Junior High</title>
            <malid>31374</malid>
        </relation>
        <relation type="Side Story">
            <title>Attack on Titan: No Regrets</title>
            <malid>25781</malid>
        </relation>
        <relation type="Alternative">
            <title>Attack on Titan: Crimson Bow and Arrow</title>
            <malid>23775</malid>
        </relation>
    </relations>
</anime>
```

### Music Information

```xml
<anime>
    <music>
        <opening number="1">
            <title>Guren no Yumiya</title>
            <artist>Linked Horizon</artist>
            <episodes>1-13</episodes>
        </opening>
        <opening number="2">
            <title>Jiyuu no Tsubasa</title>
            <artist>Linked Horizon</artist>
            <episodes>14-25</episodes>
        </opening>
        
        <ending number="1">
            <title>Utsukushiki Zankoku na Sekai</title>
            <artist>Yoko Hikasa</artist>
            <episodes>1-13</episodes>
        </ending>
    </music>
</anime>
```

## Examples

### Complete TV Anime Series

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <anime>
            <title>Death Note</title>
            <originaltitle>デスノート</originaltitle>
            <titlejp>Death Note</titlejp>
            <titleeng>Death Note</titleeng>
            
            <type>TV</type>
            <episodes>37</episodes>
            <episodelength>23</episodelength>
            <status>Finished Airing</status>
            
            <aired>
                <from>2006-10-04</from>
                <to>2007-06-27</to>
            </aired>
            
            <season>Fall 2006</season>
            <year>2006</year>
            
            <source>Manga</source>
            <adaptation>Full</adaptation>
            
            <synopsis>Light Yagami is a genius high school student who discovers a mysterious notebook...</synopsis>
            
            <genre>Psychological</genre>
            <genre>Supernatural</genre>
            <genre>Thriller</genre>
            
            <animegenre>Shounen</animegenre>
            <demographic>Shounen</demographic>
            
            <theme>Mind Games</theme>
            <theme>Police</theme>
            <theme>Serial Killers</theme>
            
            <studios>
                <studio primary="true">
                    <name>Madhouse</name>
                    <role>Animation Production</role>
                </studio>
            </studios>
            
            <producers>
                <producer>VAP</producer>
                <producer>Konami</producer>
                <producer>Shueisha</producer>
                <producer>Nippon Television Network</producer>
            </producers>
            
            <licensors>
                <licensor region="NA">Viz Media</licensor>
            </licensors>
            
            <score provider="MAL">8.62</score>
            <scoredby>3200000</scoredby>
            <ranked>75</ranked>
            <popularity>1</popularity>
            
            <rating system="MPAA">
                <value>TV-14</value>
            </rating>
            
            <anidbid>4563</anidbid>
            <malid>1535</malid>
            <tvdbid>79481</tvdbid>
            
            <characters>
                <character>
                    <name>Light Yagami</name>
                    <namejp>夜神月</namejp>
                    <role>Main</role>
                </character>
                <character>
                    <name>L Lawliet</name>
                    <namejp>エル・ローライト</namejp>
                    <role>Main</role>
                </character>
            </characters>
            
            <voiceactors>
                <voiceactor>
                    <character>Light Yagami</character>
                    <actor>Mamoru Miyano</actor>
                    <actorjp>宮野真守</actorjp>
                    <language>Japanese</language>
                </voiceactor>
                <voiceactor>
                    <character>L Lawliet</character>
                    <actor>Kappei Yamaguchi</actor>
                    <actorjp>山口勝平</actorjp>
                    <language>Japanese</language>
                </voiceactor>
            </voiceactors>
            
            <music>
                <opening number="1">
                    <title>The WORLD</title>
                    <artist>Nightmare</artist>
                    <episodes>1-19</episodes>
                </opening>
                <opening number="2">
                    <title>What's up, people?!</title>
                    <artist>Maximum the Hormone</artist>
                    <episodes>20-37</episodes>
                </opening>
            </music>
        </anime>
    </media>
</root>
```

### Anime Movie

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <anime>
            <title>Your Name</title>
            <originaltitle>君の名は。</originaltitle>
            <titlejp>Kimi no Na wa.</titlejp>
            <titleeng>Your Name.</titleeng>
            
            <type>Movie</type>
            <runtime>106</runtime>
            <status>Finished Airing</status>
            
            <aired>2016-08-26</aired>
            <year>2016</year>
            
            <source>Original</source>
            
            <synopsis>Two teenagers share a profound, magical connection upon discovering they are swapping bodies...</synopsis>
            
            <genre>Romance</genre>
            <genre>Supernatural</genre>
            <genre>Drama</genre>
            
            <theme>Time Travel</theme>
            <theme>Body Swapping</theme>
            <theme>Natural Disasters</theme>
            
            <studios>
                <studio primary="true">
                    <name>CoMix Wave Films</name>
                </studio>
            </studios>
            
            <director>Makoto Shinkai</director>
            <originalcreator>Makoto Shinkai</originalcreator>
            
            <score provider="MAL">8.83</score>
            <scoredby>2000000</scoredby>
            
            <malid>32281</malid>
            <anidbid>11829</anidbid>
            
            <boxoffice currency="USD">358000000</boxoffice>
            <budget currency="JPY">750000000</budget>
        </anime>
    </media>
</root>
```

### OVA Series

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <anime>
            <title>Hellsing Ultimate</title>
            <originaltitle>ヘルシング アルティメット</originaltitle>
            <titlejp>Hellsing Ultimate</titlejp>
            
            <type>OVA</type>
            <episodes>10</episodes>
            <episodelength>50</episodelength>
            <status>Finished Airing</status>
            
            <aired>
                <from>2006-02-10</from>
                <to>2012-12-26</to>
            </aired>
            
            <source>Manga</source>
            <adaptation>Full</adaptation>
            
            <genre>Action</genre>
            <genre>Horror</genre>
            <genre>Supernatural</genre>
            
            <animegenre>Seinen</animegenre>
            <demographic>Seinen</demographic>
            
            <theme>Vampires</theme>
            <theme>Gore</theme>
            <theme>Military</theme>
            
            <contentrating>
                <violence>Extreme</violence>
                <profanity>High</profanity>
                <nudity>Moderate</nudity>
            </contentrating>
            
            <rating system="MPAA">
                <value>TV-MA</value>
                <reason>Graphic violence and gore</reason>
            </rating>
            
            <studios>
                <studio primary="true">
                    <name>Madhouse</name>
                    <episodes>1-4</episodes>
                </studio>
                <studio primary="true">
                    <name>Graphinica</name>
                    <episodes>5-7</episodes>
                </studio>
                <studio primary="true">
                    <name>Kelmadick</name>
                    <episodes>8-10</episodes>
                </studio>
            </studios>
            
            <malid>777</malid>
            <anidbid>3296</anidbid>
        </anime>
    </media>
</root>
```

## Troubleshooting

### Common Issues

1. **Title Confusion**
   - Use the most recognized English title
   - Always include original Japanese
   - Add romaji for searchability

2. **Episode Numbering**
   - Always include absolute numbers
   - Handle recap episodes properly
   - Mark specials appropriately

3. **Season Organization**
   - Understand cour system (12-13 episodes)
   - Handle split-cour series
   - Track continuous vs separate seasons

### Best Practices

1. **File Organization**
   ```
   Anime/
   ├── Attack on Titan/
   │   ├── tvshow.nfo
   │   ├── Season 1/
   │   │   ├── S01E01.mkv
   │   │   ├── S01E01.nfo
   │   ├── Season 2/
   │   └── OVAs/
   │       ├── OVA1.mkv
   │       └── OVA1.nfo
   ```

2. **Metadata Sources**
   - Use MyAnimeList for comprehensive data
   - AniDB for technical details
   - Include multiple database IDs

3. **Language Handling**
   - Prefer subtitled version metadata
   - Note dub availability
   - Include voice actor information

4. **Special Content**
   - Separate OVAs from main series
   - Document movie compilations
   - Track alternate versions

## Related Topics

- [TV Shows Guide](tvshows.md)
- [Movies Guide](movies.md)
- [Artwork Specifications](artwork.md)
- [Internationalization](../advanced/i18n.md)