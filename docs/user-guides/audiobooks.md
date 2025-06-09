# Audiobook Metadata Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Book Information](#book-information)
- [Narrator Details](#narrator-details)
- [Chapter Organization](#chapter-organization)
- [Series Management](#series-management)
- [Publisher Information](#publisher-information)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

NFOStandard provides comprehensive support for audiobook metadata, including book information, narration details, chapter structure, and series organization. This guide covers both single audiobooks and multi-part series.

## Quick Start

### Minimal Audiobook NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <audiobook>
            <title>The Hobbit</title>
            <author>J.R.R. Tolkien</author>
            <narrator>Rob Inglis</narrator>
            <year>2012</year>
        </audiobook>
    </media>
</root>
```

## Book Information

### Core Book Elements

```xml
<audiobook>
    <!-- Required -->
    <title>Project Hail Mary</title>
    
    <!-- Essential -->
    <author>Andy Weir</author>
    <narrator>Ray Porter</narrator>
    <year>2021</year>  <!-- Audiobook release year -->
    <originalpublicationyear>2021</originalpublicationyear>  <!-- Book publication -->
    
    <!-- Book details -->
    <subtitle>A Novel</subtitle>
    <description>A lone astronaut must save humanity from extinction...</description>
    <summary>Ryland Grace wakes up on a spaceship with no memory...</summary>
    
    <!-- Classification -->
    <genre>Science Fiction</genre>
    <genre>Thriller</genre>
    <tag>Space</tag>
    <tag>Amnesia</tag>
    <tag>First Contact</tag>
</audiobook>
```

### Book Identifiers

```xml
<audiobook>
    <isbn>9780593135204</isbn>  <!-- ISBN-13 -->
    <isbn10>0593135202</isbn10>  <!-- ISBN-10 -->
    <asin>B08FHBV4ZX</asin>  <!-- Amazon Standard Identification Number -->
    <audibleasin>B08GB58KD5</audibleasin>  <!-- Audible-specific ASIN -->
    <goodreadsid>54493401</goodreadsid>
    <librarythingid>123456</librarythingid>
</audiobook>
```

### Ratings and Reviews

```xml
<audiobook>
    <rating name="goodreads" max="5">
        <value>4.52</value>
        <votes>500000</votes>
    </rating>
    
    <rating name="audible" max="5">
        <value>4.8</value>
        <votes>150000</votes>
    </rating>
    
    <userrating>5.0</userrating>
    
    <review source="AudioFile Magazine">
        Ray Porter's narration brings Andy Weir's latest science fiction adventure to life...
    </review>
</audiobook>
```

### Language and Edition

```xml
<audiobook>
    <language>en</language>
    <originallanguage>en</originallanguage>
    
    <edition>Unabridged</edition>  <!-- Unabridged, Abridged -->
    <editioninfo>Audible Studios Edition</editioninfo>
    
    <!-- For translated works -->
    <translator>Carol Brown Janeway</translator>
</audiobook>
```

## Narrator Details

### Single Narrator

```xml
<audiobook>
    <narrator>
        <name>Ray Porter</name>
        <role>Narrator</role>
        <bio>Ray Porter is an award-winning audiobook narrator...</bio>
        <audiblenarratorid>B0034NF7LQ</audiblenarratorid>
    </narrator>
</audiobook>
```

### Multiple Narrators

```xml
<audiobook>
    <narrator>
        <name>Kate Reading</name>
        <role>Narrator - Female Characters</role>
        <order>1</order>
    </narrator>
    <narrator>
        <name>Michael Kramer</name>
        <role>Narrator - Male Characters</role>
        <order>2</order>
    </narrator>
</audiobook>
```

### Full Cast Production

```xml
<audiobook>
    <productiontype>Full Cast</productiontype>
    
    <cast>
        <narrator>
            <name>James Marsters</name>
            <role>Harry Dresden</role>
            <character>Harry Dresden</character>
        </narrator>
        <narrator>
            <name>Kate Mulgrew</name>
            <role>Karrin Murphy</role>
            <character>Karrin Murphy</character>
        </narrator>
    </cast>
</audiobook>
```

## Chapter Organization

### Chapter Information

```xml
<audiobook>
    <chapters>
        <chapter number="1">
            <title>Chapter 1: The Beginning</title>
            <starttime>00:00:00</starttime>
            <endtime>00:45:32</endtime>
            <duration>2732</duration>  <!-- seconds -->
        </chapter>
        <chapter number="2">
            <title>Chapter 2: Discovery</title>
            <starttime>00:45:32</starttime>
            <endtime>01:23:14</endtime>
            <duration>2262</duration>
        </chapter>
    </chapters>
    
    <totalchapters>25</totalchapters>
</audiobook>
```

### Part/Disc Structure

```xml
<audiobook>
    <parts>
        <part number="1">
            <title>Part One: Earth</title>
            <chapters>1-8</chapters>
            <duration>14400</duration>  <!-- 4 hours -->
        </part>
        <part number="2">
            <title>Part Two: Space</title>
            <chapters>9-16</chapters>
            <duration>14400</duration>
        </part>
    </parts>
    
    <totalparts>3</totalparts>
</audiobook>
```

## Series Management

### Book Series Information

```xml
<audiobook>
    <series>
        <name>The Dresden Files</name>
        <number>1</number>  <!-- Book number in series -->
        <total>17</total>  <!-- Total books in series -->
    </series>
    
    <!-- Alternative series format -->
    <seriestitle>The Dresden Files</seriestitle>
    <seriesnumber>1</seriesnumber>
    <seriesyear>2000</seriesyear>  <!-- Series start year -->
</audiobook>
```

### Multiple Series

```xml
<audiobook>
    <!-- Primary series -->
    <series primary="true">
        <name>The Stormlight Archive</name>
        <number>1</number>
    </series>
    
    <!-- Universe/meta-series -->
    <series>
        <name>The Cosmere</name>
        <number>3</number>
        <type>universe</type>
    </series>
</audiobook>
```

## Publisher Information

### Publishing Details

```xml
<audiobook>
    <publisher>
        <name>Random House Audio</name>
        <imprint>Books on Tape</imprint>
    </publisher>
    
    <originalpublisher>Ballantine Books</originalpublisher>
    <publisheddate>2021-05-04</publisheddate>
    
    <copyright>© 2021 by Andy Weir</copyright>
    <copyrightYear>2021</copyrightYear>
</audiobook>
```

### Technical Details

```xml
<audiobook>
    <duration>28920</duration>  <!-- Total seconds -->
    <formattedduration>8:02:00</formattedduration>  <!-- HH:MM:SS -->
    
    <fileinfo>
        <codec>AAC</codec>
        <bitrate>128</bitrate>  <!-- kbps -->
        <samplerate>44100</samplerate>
        <channels>2</channels>
        <format>M4B</format>  <!-- M4B, MP3, etc. -->
    </fileinfo>
    
    <filesize>458752000</filesize>  <!-- bytes -->
</audiobook>
```

### Production Credits

```xml
<audiobook>
    <producer>John Doe</producer>
    <director>Jane Smith</director>
    <recordingstudio>Deyan Audio</recordingstudio>
    <recordingdate>2021-03-15</recordingdate>
    
    <soundeditor>Bob Johnson</soundeditor>
    <musiccomposer>Sarah Williams</musiccomposer>
</audiobook>
```

## Awards and Recognition

```xml
<audiobook>
    <awards>
        <award>
            <name>Audie Award - Science Fiction</name>
            <year>2022</year>
            <won>true</won>
        </award>
        <award>
            <name>AudioFile Earphones Award</name>
            <year>2021</year>
            <won>true</won>
        </award>
    </awards>
</audiobook>
```

## Artwork

```xml
<audiobook>
    <!-- Cover art -->
    <cover>
        <url>https://covers.audible.com/cover.jpg</url>
        <width>500</width>
        <height>500</height>
    </cover>
    
    <!-- Alternative covers -->
    <cover>
        <url>https://covers.audible.com/cover-uk.jpg</url>
        <region>UK</region>
    </cover>
    
    <!-- Author photo -->
    <authorimage>
        <url>https://images.author.com/andy-weir.jpg</url>
    </authorimage>
    
    <!-- Narrator photo -->
    <narratorimage>
        <url>https://images.narrator.com/ray-porter.jpg</url>
    </narratorimage>
</audiobook>
```

## Examples

### Complete Single Audiobook

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <audiobook>
            <title>Dune</title>
            <subtitle>Book One in the Dune Chronicles</subtitle>
            <author>Frank Herbert</author>
            
            <narrator>
                <name>Simon Vance</name>
                <role>Narrator</role>
            </narrator>
            <narrator>
                <name>Scott Brick</name>
                <role>Narrator</role>
            </narrator>
            
            <year>2007</year>
            <originalpublicationyear>1965</originalpublicationyear>
            
            <publisher>
                <name>Macmillan Audio</name>
            </publisher>
            
            <description>Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides...</description>
            
            <genre>Science Fiction</genre>
            <genre>Epic</genre>
            <tag>Space Opera</tag>
            <tag>Politics</tag>
            <tag>Ecology</tag>
            
            <series>
                <name>Dune Chronicles</name>
                <number>1</number>
                <total>6</total>
            </series>
            
            <language>en</language>
            <edition>Unabridged</edition>
            
            <duration>77267</duration>
            <formattedduration>21:27:47</formattedduration>
            
            <isbn>9781427201409</isbn>
            <asin>B000PKZZ4S</asin>
            <goodreadsid>234225</goodreadsid>
            
            <rating name="goodreads" max="5">
                <value>4.25</value>
                <votes>1000000</votes>
            </rating>
            
            <rating name="audible" max="5">
                <value>4.7</value>
                <votes>50000</votes>
            </rating>
            
            <cover>
                <url>https://covers.audible.com/dune-cover.jpg</url>
            </cover>
            
            <chapters>
                <totalchapters>48</totalchapters>
            </chapters>
            
            <fileinfo>
                <codec>AAC</codec>
                <bitrate>64</bitrate>
                <format>M4B</format>
            </fileinfo>
        </audiobook>
    </media>
</root>
```

### Series Audiobook with Full Cast

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <audiobook>
            <title>The Eye of the World</title>
            <subtitle>Book One of The Wheel of Time</subtitle>
            <author>Robert Jordan</author>
            
            <narrator>
                <name>Kate Reading</name>
                <role>Narrator - Female POV</role>
                <order>1</order>
            </narrator>
            <narrator>
                <name>Michael Kramer</name>
                <role>Narrator - Male POV</role>
                <order>2</order>
            </narrator>
            
            <year>2004</year>
            <originalpublicationyear>1990</originalpublicationyear>
            
            <series primary="true">
                <name>The Wheel of Time</name>
                <number>1</number>
                <total>14</total>
            </series>
            
            <publisher>
                <name>Tor Audio</name>
                <imprint>Macmillan Audio</imprint>
            </publisher>
            
            <description>The Wheel of Time turns and Ages come and pass...</description>
            
            <genre>Fantasy</genre>
            <genre>Epic Fantasy</genre>
            <tag>Magic</tag>
            <tag>Prophecy</tag>
            <tag>Quest</tag>
            
            <language>en</language>
            <edition>Unabridged</edition>
            
            <duration>108000</duration>
            <formattedduration>30:00:00</formattedduration>
            
            <isbn>9781593976569</isbn>
            <audibleasin>B002U3CCYM</audibleasin>
            
            <parts>
                <part number="1">
                    <title>Part One: Earlier</title>
                    <chapters>1-20</chapters>
                </part>
                <part number="2">
                    <title>Part Two: Later</title>
                    <chapters>21-53</chapters>
                </part>
            </parts>
            
            <awards>
                <award>
                    <name>AudioFile Earphones Award</name>
                    <year>2004</year>
                    <won>true</won>
                </award>
            </awards>
            
            <fileinfo>
                <codec>MP3</codec>
                <bitrate>64</bitrate>
                <format>MP3</format>
            </fileinfo>
        </audiobook>
    </media>
</root>
```

### Non-Fiction Audiobook

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <audiobook>
            <title>Sapiens</title>
            <subtitle>A Brief History of Humankind</subtitle>
            <author>Yuval Noah Harari</author>
            
            <narrator>
                <name>Derek Perkins</name>
                <role>Narrator</role>
            </narrator>
            
            <year>2015</year>
            <originalpublicationyear>2011</originalpublicationyear>
            
            <publisher>
                <name>HarperAudio</name>
            </publisher>
            
            <description>From a renowned historian comes a groundbreaking narrative of humanity's creation and evolution...</description>
            
            <genre>Non-Fiction</genre>
            <genre>History</genre>
            <genre>Science</genre>
            <tag>Anthropology</tag>
            <tag>Evolution</tag>
            <tag>Philosophy</tag>
            
            <language>en</language>
            <originallanguage>he</originallanguage>
            <translator>Yuval Noah Harari</translator>
            <edition>Unabridged</edition>
            
            <duration>54180</duration>
            <formattedduration>15:03:00</formattedduration>
            
            <isbn>9780062316097</isbn>
            <asin>B00VXJQ88K</asin>
            
            <rating name="goodreads" max="5">
                <value>4.40</value>
                <votes>800000</votes>
            </rating>
            
            <chapters>
                <totalchapters>20</totalchapters>
            </chapters>
            
            <fileinfo>
                <codec>AAC</codec>
                <bitrate>128</bitrate>
                <format>M4B</format>
            </fileinfo>
        </audiobook>
    </media>
</root>
```

## Troubleshooting

### Common Issues

1. **Series Organization**
   - Use consistent series names
   - Include series number for proper ordering
   - Handle standalone books vs series entries

2. **Narrator Attribution**
   - Distinguish between single and multiple narrators
   - Note full cast productions
   - Include character assignments when relevant

3. **Duration Handling**
   - Store duration in seconds for consistency
   - Provide formatted duration for display
   - Account for multi-part audiobooks

### Best Practices

1. **File Organization**
   ```
   Audiobooks/
   ├── Author - Series/
   │   ├── Book 01 - Title/
   │   │   ├── Book.m4b
   │   │   ├── audiobook.nfo
   │   │   └── cover.jpg
   │   └── Book 02 - Title/
   │       ├── Book.m4b
   │       └── audiobook.nfo
   ```

2. **Metadata Sources**
   - Use Audible for comprehensive data
   - Include Goodreads for ratings
   - Add ISBN for library systems

3. **Edition Information**
   - Always specify if abridged
   - Note special editions
   - Include narrator changes between editions

4. **Chapter Markers**
   - Include chapter times when available
   - Use consistent time format
   - Consider part divisions for long books

## Related Topics

- [Music Guide](music.md)
- [Podcasts Guide](podcasts.md)
- [Artwork Specifications](artwork.md)
- [Migration from Other Formats](../migration/)