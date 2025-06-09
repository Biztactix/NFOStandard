# Music Metadata Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Album Structure](#album-structure)
- [Track Information](#track-information)
- [Artist Management](#artist-management)
- [Multi-Disc Albums](#multi-disc-albums)
- [Compilations and Various Artists](#compilations-and-various-artists)
- [Music Videos](#music-videos)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Overview

NFOStandard supports comprehensive music metadata for albums, tracks, and artists. This guide covers organizing music collections with rich metadata including album art, credits, and technical information.

## Quick Start

### Minimal Album NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <album>
            <title>The Dark Side of the Moon</title>
            <artist>Pink Floyd</artist>
            <year>1973</year>
        </album>
    </media>
</root>
```

### Minimal Track NFO

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <track>
            <title>Time</title>
            <artist>Pink Floyd</artist>
            <album>The Dark Side of the Moon</album>
            <tracknumber>4</tracknumber>
        </track>
    </media>
</root>
```

## Album Structure

### Core Album Elements

```xml
<album>
    <!-- Required -->
    <title>Abbey Road</title>
    <artist>The Beatles</artist>
    
    <!-- Essential -->
    <albumartist>The Beatles</albumartist>  <!-- For consistency -->
    <year>1969</year>
    <releasedate>1969-09-26</releasedate>
    <label>Apple Records</label>
    <type>studio</type>  <!-- studio, live, compilation, single -->
    
    <!-- Description -->
    <review>The Beatles' eleventh studio album, featuring the famous medley...</review>
    <theme>Rock, Pop, Progressive</theme>
    <mood>Nostalgic, Energetic, Melancholic</mood>
</album>
```

### Album Ratings

```xml
<album>
    <rating name="allmusic" max="5">
        <value>5.0</value>
    </rating>
    
    <rating name="pitchfork" max="10">
        <value>10.0</value>
    </rating>
    
    <rating name="rollingstone" max="5">
        <value>5.0</value>
    </rating>
    
    <userrating>4.5</userrating>
</album>
```

### Album Details

```xml
<album>
    <genre>Rock</genre>
    <genre>Pop Rock</genre>
    <genre>Progressive Rock</genre>
    
    <style>British Rock</style>
    <style>Psychedelic</style>
    
    <compilation>false</compilation>
    <releasestatus>Official</releasestatus>  <!-- Official, Promotion, Bootleg -->
    <releasetype>Album</releasetype>  <!-- Album, Single, EP -->
</album>
```

### Album Identifiers

```xml
<album>
    <musicbrainzalbumid>82819605-3d63-3e94-9998-4053b3435f8a</musicbrainzalbumid>
    <musicbrainzreleasegroupid>82819605-3d63-3e94-9998-4053b3435f8a</musicbrainzreleasegroupid>
    <spotifyid>0ETFjACtuP2ADo6LFhL6HN</spotifyid>
    <discogsid>4547297</discogsid>
</album>
```

## Track Information

### Core Track Elements

```xml
<track>
    <!-- Required -->
    <title>Come Together</title>
    <artist>The Beatles</artist>
    <album>Abbey Road</album>
    <tracknumber>1</tracknumber>
    
    <!-- Essential -->
    <duration>259</duration>  <!-- In seconds -->
    <year>1969</year>
    
    <!-- Disc information for multi-disc -->
    <discnumber>1</discnumber>
    <totaldiscs>1</totaldiscs>
    <totaltracks>17</totaltracks>
</track>
```

### Track Credits

```xml
<track>
    <composer>John Lennon</composer>
    <composer>Paul McCartney</composer>
    
    <lyricist>John Lennon</lyricist>
    <lyricist>Paul McCartney</lyricist>
    
    <producer>George Martin</producer>
    
    <performer name="John Lennon" instrument="Vocals, Rhythm Guitar"/>
    <performer name="Paul McCartney" instrument="Bass, Backing Vocals"/>
    <performer name="George Harrison" instrument="Lead Guitar"/>
    <performer name="Ringo Starr" instrument="Drums"/>
</track>
```

### Track Technical Details

```xml
<track>
    <bitrate>320</bitrate>  <!-- kbps -->
    <samplerate>44100</samplerate>  <!-- Hz -->
    <channels>2</channels>  <!-- Stereo -->
    <bitdepth>16</bitdepth>
    <codec>MP3</codec>
    <encoder>LAME 3.99</encoder>
    
    <replaygain_track_gain>-9.45 dB</replaygain_track_gain>
    <replaygain_track_peak>0.988525</replaygain_track_peak>
</track>
```

### Track Identifiers

```xml
<track>
    <musicbrainztrackid>ff95a0b8-4599-491e-859e-bdc5d98e6f96</musicbrainztrackid>
    <musicbrainzartistid>b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d</musicbrainzartistid>
    <spotifytrackid>2EqlS6tkEnglzr7tkKAAYD</spotifytrackid>
    <isrc>GBAYE0601648</isrc>  <!-- International Standard Recording Code -->
</track>
```

## Artist Management

### Artist Information

```xml
<artist>
    <name>The Beatles</name>
    <sortname>Beatles, The</sortname>
    <disambiguation>UK rock band</disambiguation>
    
    <formed>1960</formed>
    <disbanded>1970</disbanded>
    
    <born>Liverpool, England</born>  <!-- For bands: where formed -->
    <biography>The Beatles were an English rock band formed in Liverpool in 1960...</biography>
    
    <genre>Rock</genre>
    <genre>Pop</genre>
    <genre>Psychedelic Rock</genre>
    
    <mood>Energetic</mood>
    <mood>Romantic</mood>
    
    <instruments>Guitar</instruments>
    <instruments>Bass</instruments>
    <instruments>Drums</instruments>
    <instruments>Keyboards</instruments>
</artist>
```

### Artist Identifiers

```xml
<artist>
    <musicbrainzartistid>b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d</musicbrainzartistid>
    <spotifyartistid>3WrFJ7ztbogyGnTHbHJFl2</spotifyartistid>
    <discogsartistid>82730</discogsartistid>
</artist>
```

### Band Members

```xml
<artist>
    <members>
        <member>
            <name>John Lennon</name>
            <instruments>Vocals, Guitar, Keyboards</instruments>
            <period>1960-1970</period>
        </member>
        <member>
            <name>Paul McCartney</name>
            <instruments>Vocals, Bass, Guitar, Keyboards</instruments>
            <period>1960-1970</period>
        </member>
        <member>
            <name>George Harrison</name>
            <instruments>Guitar, Vocals</instruments>
            <period>1960-1970</period>
        </member>
        <member>
            <name>Ringo Starr</name>
            <instruments>Drums, Vocals</instruments>
            <period>1962-1970</period>
        </member>
    </members>
</artist>
```

## Multi-Disc Albums

### Multi-Disc Album Structure

```xml
<album>
    <title>The White Album</title>
    <artist>The Beatles</artist>
    <year>1968</year>
    
    <totaldiscs>2</totaldiscs>
    <totaltracks>30</totaltracks>
    
    <discs>
        <disc number="1">
            <title>Disc 1</title>  <!-- Optional disc subtitle -->
            <tracks>17</tracks>
        </disc>
        <disc number="2">
            <title>Disc 2</title>
            <tracks>13</tracks>
        </disc>
    </discs>
</album>
```

### Track on Multi-Disc

```xml
<track>
    <title>While My Guitar Gently Weeps</title>
    <artist>The Beatles</artist>
    <album>The White Album</album>
    <tracknumber>7</tracknumber>
    <discnumber>1</discnumber>
    <totaldiscs>2</totaldiscs>
</track>
```

## Compilations and Various Artists

### Compilation Album

```xml
<album>
    <title>Now That's What I Call Music! 100</title>
    <albumartist>Various Artists</albumartist>
    <compilation>true</compilation>
    <year>2018</year>
    
    <type>compilation</type>
    <releasetype>Album</releasetype>
</album>
```

### Track on Compilation

```xml
<track>
    <title>Shape of You</title>
    <artist>Ed Sheeran</artist>
    <albumartist>Various Artists</albumartist>
    <album>Now That's What I Call Music! 100</album>
    <tracknumber>1</tracknumber>
    <compilation>true</compilation>
    
    <!-- Original album info -->
    <originalalbum>÷ (Divide)</originalalbum>
    <originaldate>2017-01-06</originaldate>
</track>
```

## Music Videos

### Music Video NFO

```xml
<musicvideo>
    <title>Bohemian Rhapsody</title>
    <artist>Queen</artist>
    <album>A Night at the Opera</album>
    <year>1975</year>
    
    <director>Bruce Gowers</director>
    <studio>BBC</studio>
    
    <plot>The promotional video for Queen's "Bohemian Rhapsody"...</plot>
    
    <runtime>6</runtime>  <!-- minutes -->
    <premiered>1975-11-10</premiered>
    
    <genre>Rock</genre>
    <genre>Progressive Rock</genre>
    
    <fileinfo>
        <streamdetails>
            <video>
                <codec>h264</codec>
                <width>1920</width>
                <height>1080</height>
            </video>
            <audio>
                <codec>aac</codec>
                <channels>2</channels>
            </audio>
        </streamdetails>
    </fileinfo>
</musicvideo>
```

## Album Artwork

```xml
<album>
    <!-- Album cover -->
    <thumb>
        <url>https://coverartarchive.org/release/album-cover.jpg</url>
        <type>front</type>
        <size>1000x1000</size>
    </thumb>
    
    <!-- Back cover -->
    <thumb>
        <url>https://coverartarchive.org/release/album-back.jpg</url>
        <type>back</type>
    </thumb>
    
    <!-- CD art -->
    <thumb>
        <url>https://coverartarchive.org/release/cd.jpg</url>
        <type>disc</type>
    </thumb>
    
    <!-- Artist image -->
    <fanart>
        <url>https://fanart.tv/artist-backdrop.jpg</url>
    </fanart>
</album>
```

## Examples

### Complete Studio Album

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <album>
            <title>OK Computer</title>
            <artist>Radiohead</artist>
            <albumartist>Radiohead</albumartist>
            
            <year>1997</year>
            <releasedate>1997-05-21</releasedate>
            
            <type>studio</type>
            <releasestatus>Official</releasestatus>
            <releasetype>Album</releasetype>
            
            <label>Parlophone</label>
            <label>Capitol Records</label>
            
            <genre>Alternative Rock</genre>
            <genre>Art Rock</genre>
            <genre>Electronic</genre>
            
            <style>British Rock</style>
            <style>Experimental</style>
            
            <mood>Dark</mood>
            <mood>Atmospheric</mood>
            <mood>Futuristic</mood>
            
            <review>OK Computer is the third studio album by Radiohead, widely considered one of the greatest albums of all time...</review>
            
            <rating name="allmusic" max="5">
                <value>5.0</value>
            </rating>
            <rating name="pitchfork" max="10">
                <value>10.0</value>
            </rating>
            
            <compilation>false</compilation>
            <totaltracks>12</totaltracks>
            
            <musicbrainzalbumid>9a57b25f-228f-35f6-8203-3351dd7a3f90</musicbrainzalbumid>
            <spotifyid>7dxKtc08dYeRVEelmXFkal</spotifyid>
            
            <thumb>
                <url>https://coverartarchive.org/release/ok-computer-cover.jpg</url>
                <type>front</type>
            </thumb>
            <fanart>
                <url>https://fanart.tv/radiohead-backdrop.jpg</url>
            </fanart>
        </album>
    </media>
</root>
```

### Complete Track

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <track>
            <title>Paranoid Android</title>
            <artist>Radiohead</artist>
            <albumartist>Radiohead</albumartist>
            <album>OK Computer</album>
            
            <tracknumber>2</tracknumber>
            <totaltracks>12</totaltracks>
            <discnumber>1</discnumber>
            <totaldiscs>1</totaldiscs>
            
            <duration>387</duration>
            <year>1997</year>
            
            <composer>Thom Yorke</composer>
            <composer>Jonny Greenwood</composer>
            <composer>Ed O'Brien</composer>
            <composer>Colin Greenwood</composer>
            <composer>Philip Selway</composer>
            
            <producer>Nigel Godrich</producer>
            <producer>Radiohead</producer>
            
            <genre>Alternative Rock</genre>
            <genre>Progressive Rock</genre>
            
            <performer name="Thom Yorke" instrument="Vocals, Guitar"/>
            <performer name="Jonny Greenwood" instrument="Guitar, Keyboards"/>
            <performer name="Ed O'Brien" instrument="Guitar, Backing Vocals"/>
            <performer name="Colin Greenwood" instrument="Bass"/>
            <performer name="Philip Selway" instrument="Drums"/>
            
            <bitrate>320</bitrate>
            <samplerate>44100</samplerate>
            <channels>2</channels>
            <codec>MP3</codec>
            
            <musicbrainztrackid>8f2be627-0414-4f85-9b99-de3b8fd86bd6</musicbrainztrackid>
            <spotifytrackid>6LgJvl0Xdtc7ytCyVdslFA</spotifytrackid>
            <isrc>GBPKN9700005</isrc>
            
            <rating>5.0</rating>
            <playcount>127</playcount>
            <lastplayed>2024-01-08</lastplayed>
        </track>
    </media>
</root>
```

### Live Album

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <album>
            <title>Live at Wembley '86</title>
            <artist>Queen</artist>
            <albumartist>Queen</albumartist>
            
            <year>1992</year>
            <originaldate>1986-07-12</originaldate>  <!-- Concert date -->
            
            <type>live</type>
            <releasestatus>Official</releasestatus>
            
            <venue>Wembley Stadium</venue>
            <location>London, England</location>
            
            <review>Capturing Queen at the height of their powers during the Magic Tour...</review>
            
            <totaldiscs>2</totaldiscs>
            <totaltracks>28</totaltracks>
        </album>
    </media>
</root>
```

## Troubleshooting

### Common Issues

1. **Album Artist vs Track Artist**
   - Use `albumartist` for consistency
   - Especially important for compilations
   - Helps with proper library organization

2. **Track Numbering**
   - Always include track numbers
   - Use disc numbers for multi-disc
   - Include total tracks for completeness

3. **Music Identifiers**
   - MusicBrainz IDs are most reliable
   - Include multiple IDs when available
   - ISRC for official releases

### Best Practices

1. **File Organization**
   ```
   Music/
   ├── Artist/
   │   ├── Album/
   │   │   ├── 01 - Track.mp3
   │   │   ├── 01 - Track.nfo
   │   │   ├── album.nfo
   │   │   └── cover.jpg
   ```

2. **Metadata Consistency**
   - Match artist names exactly
   - Use consistent date formats
   - Include original release dates

3. **Compilation Handling**
   - Set compilation flag
   - Use "Various Artists" as album artist
   - Preserve original artist info

4. **Classical Music**
   - Use composer field prominently
   - Include conductor and orchestra
   - Consider work and movement tags

## Related Topics

- [Music Videos Guide](musicvideo.md)
- [Audiobooks Guide](audiobooks.md)
- [Artwork Specifications](artwork.md)
- [Migration from Other Formats](../migration/)