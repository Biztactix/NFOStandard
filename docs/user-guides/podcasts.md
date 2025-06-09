# Podcast Metadata Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Podcast Show Structure](#podcast-show-structure)
- [Episode Metadata](#episode-metadata)
- [Host and Guest Information](#host-and-guest-information)
- [Categories and Tags](#categories-and-tags)
- [RSS Feed Integration](#rss-feed-integration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

NFOStandard provides comprehensive support for podcast metadata, covering both podcast shows (series) and individual episodes. This guide explains how to organize and document your podcast collection with rich metadata.

## Quick Start

### Minimal Podcast Show NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <podcast>
            <title>The Daily</title>
            <author>The New York Times</author>
            <description>This is what the news should sound like.</description>
            <language>en</language>
        </podcast>
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
            <title>Understanding Climate Change</title>
            <podcast>The Daily</podcast>
            <season>2024</season>
            <episode>45</episode>
            <duration>1800</duration>
        </episode>
    </media>
</root>
```

## Podcast Show Structure

### Core Podcast Elements

```xml
<podcast>
    <!-- Required -->
    <title>Serial</title>
    
    <!-- Essential -->
    <author>Sarah Koenig</author>
    <owner>Serial Productions</owner>
    <description>Serial is a podcast from the creators of This American Life...</description>
    <summary>One story told week by week</summary>
    
    <!-- Publishing info -->
    <publisher>Serial Productions</publisher>
    <copyright>© 2024 Serial Productions</copyright>
    <language>en</language>
    <country>US</country>
    
    <!-- Contact and links -->
    <email>info@serialpodcast.org</email>
    <website>https://serialpodcast.org</website>
    <feedurl>https://feeds.serialpodcast.org/serial</feedurl>
</podcast>
```

### Podcast Categories

```xml
<podcast>
    <!-- Primary category (iTunes/Apple Podcasts) -->
    <category>
        <primary>True Crime</primary>
        <secondary>Documentary</secondary>
    </category>
    
    <!-- Multiple categories -->
    <categories>
        <category>True Crime</category>
        <category>News</category>
        <category>Society &amp; Culture</category>
    </categories>
    
    <!-- Tags for discovery -->
    <tag>investigative</tag>
    <tag>journalism</tag>
    <tag>mystery</tag>
    <tag>long-form</tag>
</podcast>
```

### Show Details

```xml
<podcast>
    <!-- Schedule -->
    <frequency>weekly</frequency>  <!-- daily, weekly, biweekly, monthly -->
    <releaseday>Tuesday</releaseday>
    
    <!-- Status -->
    <status>active</status>  <!-- active, hiatus, completed -->
    <explicit>false</explicit>
    
    <!-- Type -->
    <type>episodic</type>  <!-- episodic, serial -->
    
    <!-- Subscription info -->
    <subscribers>5000000</subscribers>
    <rating>4.8</rating>
    <reviews>125000</reviews>
</podcast>
```

### Podcast Identifiers

```xml
<podcast>
    <podcastid type="apple">1437238896</podcastid>
    <podcastid type="spotify">4rOoJ6Egrf9aW7yXrsxWFg</podcastid>
    <podcastid type="google">KT89as983jfkjdf83</podcastid>
    <rssfeed>https://feeds.example.com/podcast</rssfeed>
    <guid>9b9b4e2a-9d5e-4d9a-8c3f-6e7f5a4b3c2a</guid>
</podcast>
```

## Episode Metadata

### Core Episode Elements

```xml
<episode>
    <!-- Required -->
    <title>The Alibi</title>
    <podcast>Serial</podcast>
    
    <!-- Episode numbering -->
    <season>1</season>
    <episode>1</episode>
    <globalepisode>1</globalepisode>  <!-- Across all seasons -->
    
    <!-- Essential details -->
    <description>It's Baltimore, 1999. Hae Min Lee, a popular high-school senior...</description>
    <duration>3240</duration>  <!-- seconds -->
    <publisheddate>2014-10-03T06:00:00Z</publisheddate>
    
    <!-- File info -->
    <enclosure>
        <url>https://dts.podtrac.com/redirect.mp3/serial.mp3</url>
        <type>audio/mpeg</type>
        <length>52428800</length>  <!-- bytes -->
    </enclosure>
</episode>
```

### Episode Details

```xml
<episode>
    <!-- Content warnings -->
    <explicit>false</explicit>
    <contentwarning>Discussion of violence</contentwarning>
    
    <!-- Episode type -->
    <episodetype>full</episodetype>  <!-- full, trailer, bonus -->
    
    <!-- Transcript -->
    <transcript>
        <url>https://serialpodcast.org/season-one/1/transcript</url>
        <type>text/html</type>
    </transcript>
    
    <!-- Chapters/segments -->
    <chapters>
        <chapter>
            <title>Introduction</title>
            <starttime>00:00:00</starttime>
            <endtime>00:02:30</endtime>
        </chapter>
        <chapter>
            <title>The Day</title>
            <starttime>00:02:30</starttime>
            <endtime>00:15:45</endtime>
        </chapter>
    </chapters>
</episode>
```

### Episode Links and References

```xml
<episode>
    <!-- Episode webpage -->
    <link>https://serialpodcast.org/season-one/1/the-alibi</link>
    
    <!-- Show notes -->
    <shownotes>
        <![CDATA[
        <p>It's Baltimore, 1999. Hae Min Lee, a popular high-school senior, disappears after school one day...</p>
        <h3>Links:</h3>
        <ul>
            <li><a href="https://example.com/court-documents">Court Documents</a></li>
            <li><a href="https://example.com/timeline">Case Timeline</a></li>
        </ul>
        ]]>
    </shownotes>
    
    <!-- Related links -->
    <links>
        <link type="documentation" url="https://example.com/evidence"/>
        <link type="discussion" url="https://reddit.com/r/serial"/>
    </links>
</episode>
```

## Host and Guest Information

### Podcast Hosts

```xml
<podcast>
    <hosts>
        <host>
            <name>Sarah Koenig</name>
            <role>Host</role>
            <bio>Sarah Koenig is a journalist and creator of Serial...</bio>
            <email>sarah@serialpodcast.org</email>
            <twitter>@sarahkoenig</twitter>
            <image>https://serialpodcast.org/sarah.jpg</image>
        </host>
        <host>
            <name>Julie Snyder</name>
            <role>Co-Creator</role>
            <bio>Julie Snyder is the co-creator of Serial...</bio>
        </host>
    </hosts>
</podcast>
```

### Episode Guests

```xml
<episode>
    <guests>
        <guest>
            <name>Asia McClain</name>
            <role>Witness</role>
            <description>Key alibi witness</description>
        </guest>
        <guest>
            <name>Rabia Chaudry</name>
            <role>Advocate</role>
            <bio>Attorney and family friend</bio>
            <twitter>@rabiasquared</twitter>
        </guest>
    </guests>
    
    <!-- For interview shows -->
    <interviewee>Dr. Jane Smith</interviewee>
    <interviewertitle>Climate Scientist</interviewertitle>
</episode>
```

## Categories and Tags

### Standard Podcast Categories

```xml
<podcast>
    <!-- Apple Podcasts categories -->
    <itunesCategory>
        <category>True Crime</category>
    </itunesCategory>
    
    <!-- Spotify categories -->
    <spotifyCategory>
        <category>True Crime</category>
        <category>Documentary</category>
    </spotifyCategory>
    
    <!-- General categories -->
    <genre>True Crime</genre>
    <genre>Investigative Journalism</genre>
    <subgenre>Murder Mystery</subgenre>
</podcast>
```

### Content Classification

```xml
<podcast>
    <!-- Content rating -->
    <rating>
        <scheme>iTunes</scheme>
        <value>explicit</value>  <!-- clean, explicit -->
    </rating>
    
    <!-- Audience -->
    <targetaudience>adult</targetaudience>
    <agerating>16+</agerating>
    
    <!-- Content type -->
    <format>narrative</format>  <!-- narrative, interview, panel, solo -->
    <style>investigative</style>
</podcast>
```

## RSS Feed Integration

### Feed Information

```xml
<podcast>
    <feed>
        <url>https://feeds.example.com/podcast.xml</url>
        <format>RSS 2.0</format>
        <updatefrequency>daily</updatefrequency>
        <lastupdate>2024-01-09T12:00:00Z</lastupdate>
    </feed>
    
    <!-- iTunes/Apple specific -->
    <itunes>
        <author>Serial Productions</author>
        <block>no</block>  <!-- Prevent iTunes listing -->
        <complete>no</complete>  <!-- Show is ongoing -->
        <newfeedurl>https://new.feed.url/podcast.xml</newfeedurl>
    </itunes>
</podcast>
```

### Feed Synchronization

```xml
<episode>
    <!-- RSS guid for synchronization -->
    <guid isPermaLink="false">serial-s01e01</guid>
    
    <!-- Alternate feeds -->
    <alternateenclosure>
        <url>https://example.com/episode-hd.mp3</url>
        <type>audio/mpeg</type>
        <bitrate>320</bitrate>
        <title>HD Audio</title>
    </alternateenclosure>
</episode>
```

## Artwork and Images

```xml
<podcast>
    <!-- Podcast cover art -->
    <image>
        <url>https://serialpodcast.org/cover.jpg</url>
        <width>3000</width>
        <height>3000</height>
        <type>cover</type>
    </image>
    
    <!-- Banner/header image -->
    <banner>
        <url>https://serialpodcast.org/banner.jpg</url>
        <width>1400</width>
        <height>400</height>
    </banner>
    
    <!-- Episode-specific artwork -->
    <episodeimage>
        <url>https://serialpodcast.org/s01e01.jpg</url>
        <width>1400</width>
        <height>1400</height>
    </episodeimage>
</podcast>
```

## Examples

### Complete Podcast Show

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <podcast>
            <title>This American Life</title>
            <author>Ira Glass</author>
            <owner>Chicago Public Media</owner>
            
            <description>This American Life is a weekly public radio program and podcast. Each week we choose a theme and put together different kinds of stories on that theme.</description>
            <summary>Stories on a theme, from Chicago Public Media</summary>
            
            <publisher>PRX</publisher>
            <copyright>© 2024 Chicago Public Media</copyright>
            
            <language>en</language>
            <country>US</country>
            
            <website>https://thisamericanlife.org</website>
            <email>web@thisamericanlife.org</email>
            <feedurl>https://www.thisamericanlife.org/podcast/rss.xml</feedurl>
            
            <frequency>weekly</frequency>
            <releaseday>Sunday</releaseday>
            <status>active</status>
            <explicit>false</explicit>
            <type>episodic</type>
            
            <category>
                <primary>Society &amp; Culture</primary>
                <secondary>Documentary</secondary>
            </category>
            
            <genre>Documentary</genre>
            <genre>Storytelling</genre>
            <genre>Journalism</genre>
            
            <hosts>
                <host>
                    <name>Ira Glass</name>
                    <role>Host and Executive Producer</role>
                    <bio>Ira Glass is the host and creator of This American Life...</bio>
                    <image>https://thisamericanlife.org/ira.jpg</image>
                </host>
            </hosts>
            
            <podcastid type="apple">201671138</podcastid>
            <podcastid type="spotify">2gozmRXcbPH4CwZe2Eg3YC</podcastid>
            
            <rating>4.7</rating>
            <reviews>50000</reviews>
            <subscribers>2500000</subscribers>
            
            <image>
                <url>https://thisamericanlife.org/cover.jpg</url>
                <width>3000</width>
                <height>3000</height>
            </image>
        </podcast>
    </media>
</root>
```

### Complete Episode

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <episode>
            <title>24 Hours at the Golden Apple</title>
            <podcast>This American Life</podcast>
            
            <season>2024</season>
            <episode>823</episode>
            <globalepisode>823</globalepisode>
            
            <description>We spend 24 hours at a rest stop in Chicago and talk to people who are just passing through.</description>
            
            <publisheddate>2024-01-07T21:00:00Z</publisheddate>
            <duration>3540</duration>
            
            <enclosure>
                <url>https://dts.podtrac.com/redirect.mp3/thisamericanlife.mp3</url>
                <type>audio/mpeg</type>
                <length>56640000</length>
            </enclosure>
            
            <link>https://thisamericanlife.org/823/24-hours-at-the-golden-apple</link>
            
            <chapters>
                <chapter>
                    <title>Prologue</title>
                    <starttime>00:00:00</starttime>
                    <endtime>00:04:30</endtime>
                </chapter>
                <chapter>
                    <title>Act One: Midnight to 6 AM</title>
                    <starttime>00:04:30</starttime>
                    <endtime>00:22:15</endtime>
                </chapter>
                <chapter>
                    <title>Act Two: Morning Rush</title>
                    <starttime>00:22:15</starttime>
                    <endtime>00:45:30</endtime>
                </chapter>
            </chapters>
            
            <transcript>
                <url>https://thisamericanlife.org/823/transcript</url>
                <type>text/html</type>
            </transcript>
            
            <credits>
                <producer>Nancy Updike</producer>
                <producer>Diane Cook</producer>
                <editor>Joel Lovell</editor>
            </credits>
            
            <guid isPermaLink="false">prx_96_4b5c6d7e-8f9a-4d3c-9e1f-2a3b4c5d6e7f</guid>
            
            <explicit>false</explicit>
            <episodetype>full</episodetype>
        </episode>
    </media>
</root>
```

### Interview Podcast Episode

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <episode>
            <title>Neil deGrasse Tyson on the Universe and Everything</title>
            <podcast>The Joe Rogan Experience</podcast>
            
            <episode>1904</episode>
            <globalepisode>1904</globalepisode>
            
            <description>Joe sits down with astrophysicist Neil deGrasse Tyson to discuss the universe, aliens, and the future of humanity.</description>
            
            <publisheddate>2023-11-22T12:00:00Z</publisheddate>
            <duration>10800</duration>  <!-- 3 hours -->
            
            <format>interview</format>
            <style>long-form</style>
            
            <hosts>
                <host>
                    <name>Joe Rogan</name>
                    <role>Host</role>
                </host>
            </hosts>
            
            <guests>
                <guest>
                    <name>Neil deGrasse Tyson</name>
                    <role>Guest</role>
                    <title>Astrophysicist</title>
                    <bio>Neil deGrasse Tyson is an American astrophysicist, author, and science communicator.</bio>
                    <twitter>@neiltyson</twitter>
                </guest>
            </guests>
            
            <topics>
                <topic>Astrophysics</topic>
                <topic>Space Exploration</topic>
                <topic>Aliens</topic>
                <topic>Philosophy</topic>
            </topics>
            
            <explicit>true</explicit>
            <contentwarning>Strong language</contentwarning>
            
            <video>
                <available>true</available>
                <url>https://youtube.com/watch?v=example</url>
            </video>
        </episode>
    </media>
</root>
```

## Troubleshooting

### Common Issues

1. **Episode Numbering**
   - Use consistent numbering schemes
   - Handle season transitions properly
   - Include global episode numbers for serialized shows

2. **Feed Synchronization**
   - Match GUIDs with RSS feed
   - Update metadata when feed changes
   - Handle feed redirects properly

3. **File Organization**
   - Maintain consistent folder structure
   - Include show name in episode files
   - Keep artwork with metadata files

### Best Practices

1. **Directory Structure**
   ```
   Podcasts/
   ├── This American Life/
   │   ├── podcast.nfo
   │   ├── cover.jpg
   │   ├── Season 2024/
   │   │   ├── TAL-823-24-Hours.mp3
   │   │   ├── TAL-823-24-Hours.nfo
   │   │   └── TAL-824-Next-Episode.mp3
   ```

2. **Metadata Sources**
   - Pull from RSS feeds when available
   - Use podcast APIs for additional data
   - Maintain consistency with official sources

3. **Episode Identification**
   - Include podcast name in episode metadata
   - Use GUIDs for unique identification
   - Track both seasonal and global numbering

4. **Content Classification**
   - Mark explicit content appropriately
   - Include content warnings
   - Specify episode types (full, trailer, bonus)

## Related Topics

- [TV Shows Guide](tvshows.md) (for video podcasts)
- [Audiobooks Guide](audiobooks.md)
- [Artwork Specifications](artwork.md)
- [RSS Feed Integration](../advanced/rss-integration.md)