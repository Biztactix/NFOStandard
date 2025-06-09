# Artwork Specifications Guide

## Table of Contents
- [Overview](#overview)
- [Image Types](#image-types)
- [Resolution Guidelines](#resolution-guidelines)
- [File Formats](#file-formats)
- [Aspect Ratios](#aspect-ratios)
- [Storage Methods](#storage-methods)
- [Multiple Artwork](#multiple-artwork)
- [Language-Specific Artwork](#language-specific-artwork)
- [Best Practices](#best-practices)
- [Examples](#examples)

## Overview

NFOStandard supports comprehensive artwork metadata for all media types. This guide covers image specifications, storage methods, and best practices for managing artwork in your media library.

## Image Types

### Universal Image Types

| Type | Description | Common Use | Typical Aspect Ratio |
|------|-------------|------------|---------------------|
| `poster` | Vertical poster image | Movies, TV shows, anime | 2:3 (0.667) |
| `fanart` | Background/backdrop image | All media types | 16:9 (1.778) |
| `banner` | Horizontal banner | TV shows, anime | 5.4:1 (5.4) |
| `thumb` | Thumbnail image | Episodes, music | 16:9 or 1:1 |
| `clearlogo` | Transparent logo | Movies, TV shows | Variable |
| `clearart` | Transparent character art | Movies, TV shows | Variable |
| `landscape` | Landscape orientation | Movies, TV shows | 16:9 (1.778) |
| `discart` | Disc/CD artwork | Movies, music | 1:1 (1.0) |

### Media-Specific Image Types

#### Movies
```xml
<movie>
    <poster>...</poster>          <!-- Main movie poster -->
    <fanart>...</fanart>          <!-- Background/backdrop -->
    <banner>...</banner>          <!-- Horizontal banner -->
    <clearlogo>...</clearlogo>    <!-- Movie logo -->
    <clearart>...</clearart>      <!-- Character art -->
    <discart>...</discart>        <!-- Blu-ray/DVD art -->
    <keyart>...</keyart>          <!-- Alternative poster -->
</movie>
```

#### TV Shows
```xml
<tvshow>
    <poster>...</poster>          <!-- Series poster -->
    <seasonposter>...</seasonposter> <!-- Season-specific poster -->
    <fanart>...</fanart>          <!-- Series backdrop -->
    <banner>...</banner>          <!-- Series banner -->
    <characterart>...</characterart> <!-- Character artwork -->
    <clearlogo>...</clearlogo>    <!-- Show logo -->
</tvshow>
```

#### Music
```xml
<album>
    <cover>...</cover>            <!-- Album cover (front) -->
    <back>...</back>              <!-- Album back cover -->
    <spine>...</spine>            <!-- Album spine -->
    <inlay>...</inlay>            <!-- CD inlay -->
    <booklet>...</booklet>        <!-- Digital booklet -->
    <artistthumb>...</artistthumb> <!-- Artist photo -->
</album>
```

## Resolution Guidelines

### Recommended Minimum Resolutions

| Image Type | Minimum | Recommended | Maximum |
|------------|---------|-------------|---------|
| Poster | 500×750 | 1000×1500 | 2000×3000 |
| Fanart/Backdrop | 1280×720 | 1920×1080 | 3840×2160 |
| Banner | 758×140 | 1000×185 | 2000×370 |
| Thumb | 400×225 | 800×450 | 1920×1080 |
| Square Thumb | 400×400 | 800×800 | 1500×1500 |
| Clearlogo | 400×155 | 800×310 | 1600×620 |
| Album Cover | 600×600 | 1500×1500 | 3000×3000 |

### Quality Standards

```xml
<poster>
    <url>https://image.tmdb.org/t/p/original/poster.jpg</url>
    <width>2000</width>
    <height>3000</height>
    <quality>high</quality>  <!-- low, medium, high, original -->
    <filesize>2457600</filesize>  <!-- bytes -->
</poster>
```

## File Formats

### Supported Formats

| Format | Extension | Best For | Transparency |
|--------|-----------|----------|--------------|
| JPEG | .jpg, .jpeg | Photos, complex images | No |
| PNG | .png | Logos, simple graphics | Yes |
| WebP | .webp | Modern web images | Yes |
| GIF | .gif | Animated images | Limited |

### Format Guidelines

```xml
<artwork>
    <poster>
        <url>poster.jpg</url>
        <format>jpeg</format>
        <colorspace>sRGB</colorspace>
        <bitdepth>8</bitdepth>
        <compression>85</compression>  <!-- JPEG quality -->
    </poster>
    
    <clearlogo>
        <url>logo.png</url>
        <format>png</format>
        <transparency>true</transparency>
        <bitdepth>24</bitdepth>  <!-- 24-bit with alpha -->
    </clearlogo>
</artwork>
```

## Aspect Ratios

### Common Aspect Ratios

```xml
<artwork>
    <!-- Movie Poster (2:3) -->
    <poster>
        <url>poster.jpg</url>
        <width>1000</width>
        <height>1500</height>
        <aspectratio>0.667</aspectratio>
    </poster>
    
    <!-- Widescreen Backdrop (16:9) -->
    <fanart>
        <url>backdrop.jpg</url>
        <width>1920</width>
        <height>1080</height>
        <aspectratio>1.778</aspectratio>
    </fanart>
    
    <!-- Ultra-wide Banner (5.4:1) -->
    <banner>
        <url>banner.jpg</url>
        <width>1000</width>
        <height>185</height>
        <aspectratio>5.405</aspectratio>
    </banner>
    
    <!-- Square Album Art (1:1) -->
    <cover>
        <url>album.jpg</url>
        <width>1500</width>
        <height>1500</height>
        <aspectratio>1.0</aspectratio>
    </cover>
</artwork>
```

### Aspect Ratio Handling

```xml
<poster>
    <url>poster.jpg</url>
    <aspectratio>0.667</aspectratio>
    <orientation>portrait</orientation>  <!-- portrait, landscape, square -->
    <crop>false</crop>  <!-- Image should not be cropped -->
    <stretch>false</stretch>  <!-- Image should not be stretched -->
</poster>
```

## Storage Methods

### Remote URLs

```xml
<poster>
    <url>https://image.tmdb.org/t/p/original/qJ6ndFR0tQCXX1aJmBFkH8Pg0Zu.jpg</url>
    <provider>tmdb</provider>
    <language>en</language>
    <rating>9.2</rating>  <!-- User rating of image -->
    <votes>150</votes>
</poster>
```

### Local Files

```xml
<poster>
    <url>file:///media/movies/The Matrix/poster.jpg</url>
    <local>true</local>
    <relativepath>poster.jpg</relativepath>
    <checksum>d8e8fca2dc0f896fd7cb4cb0031ba249</checksum>  <!-- MD5 -->
</poster>
```

### Embedded Images

```xml
<poster>
    <embedded>true</embedded>
    <data encoding="base64">
        /9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJ...
    </data>
    <format>jpeg</format>
    <size>45678</size>
</poster>
```

## Multiple Artwork

### Multiple Images of Same Type

```xml
<movie>
    <!-- Primary poster -->
    <poster primary="true">
        <url>https://image.tmdb.org/t/p/original/poster1.jpg</url>
        <language>en</language>
        <season>all</season>
    </poster>
    
    <!-- Alternative posters -->
    <poster>
        <url>https://image.tmdb.org/t/p/original/poster2.jpg</url>
        <language>en</language>
        <type>theatrical</type>
    </poster>
    
    <poster>
        <url>https://image.tmdb.org/t/p/original/poster3.jpg</url>
        <language>en</language>
        <type>teaser</type>
    </poster>
</movie>
```

### Season-Specific Artwork

```xml
<tvshow>
    <!-- All seasons poster -->
    <poster season="all">
        <url>series-poster.jpg</url>
    </poster>
    
    <!-- Season 1 poster -->
    <poster season="1">
        <url>season1-poster.jpg</url>
    </poster>
    
    <!-- Season 2 poster -->
    <poster season="2">
        <url>season2-poster.jpg</url>
    </poster>
</tvshow>
```

## Language-Specific Artwork

### Localized Posters

```xml
<movie>
    <!-- English poster -->
    <poster>
        <url>poster-en.jpg</url>
        <language>en</language>
        <region>US</region>
    </poster>
    
    <!-- Japanese poster -->
    <poster>
        <url>poster-ja.jpg</url>
        <language>ja</language>
        <region>JP</region>
    </poster>
    
    <!-- French poster -->
    <poster>
        <url>poster-fr.jpg</url>
        <language>fr</language>
        <region>FR</region>
    </poster>
</movie>
```

### Text-Free Artwork

```xml
<poster>
    <url>poster-textless.jpg</url>
    <language>none</language>
    <textless>true</textless>
    <type>textless</type>
</poster>
```

## Best Practices

### Image Selection Criteria

1. **Resolution Priority**
   ```xml
   <poster>
       <url>poster-4k.jpg</url>
       <width>2000</width>
       <height>3000</height>
       <priority>1</priority>  <!-- Higher number = higher priority -->
       <source>theatrical</source>
   </poster>
   ```

2. **Source Quality**
   ```xml
   <artwork>
       <source>official</source>  <!-- official, fan-made, scan -->
       <quality>pristine</quality>  <!-- pristine, high, medium, low -->
       <upscaled>false</upscaled>
   </artwork>
   ```

3. **Completeness**
   ```xml
   <movie>
       <artworkcomplete>true</artworkcomplete>
       <artworktypes>
           <has>poster</has>
           <has>fanart</has>
           <has>clearlogo</has>
           <missing>banner</missing>
       </artworktypes>
   </movie>
   ```

### File Organization

```
Movie Title (Year)/
├── movie.nfo
├── poster.jpg          # Primary poster
├── fanart.jpg          # Primary backdrop
├── banner.jpg          # Banner image
├── clearlogo.png       # Transparent logo
├── disc.png            # Disc art
└── extrafanart/        # Additional backdrops
    ├── fanart1.jpg
    ├── fanart2.jpg
    └── fanart3.jpg
```

### Naming Conventions

| Type | Default Filename | Alternative Names |
|------|-----------------|-------------------|
| Poster | poster.jpg | folder.jpg, cover.jpg |
| Fanart | fanart.jpg | backdrop.jpg, background.jpg |
| Banner | banner.jpg | | 
| Logo | clearlogo.png | logo.png |
| Disc | disc.png | discart.png |
| Season Poster | season01-poster.jpg | season-specials-poster.jpg |

## Examples

### Complete Movie Artwork

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <movie>
            <title>Inception</title>
            
            <!-- Primary poster -->
            <poster primary="true">
                <url>https://image.tmdb.org/t/p/original/9gk7adHYeDvHkCSEqAvQNLnFqN.jpg</url>
                <width>2000</width>
                <height>3000</height>
                <language>en</language>
                <aspectratio>0.667</aspectratio>
                <rating>9.5</rating>
                <votes>234</votes>
            </poster>
            
            <!-- Alternative posters -->
            <poster>
                <url>https://image.tmdb.org/t/p/original/alt-poster.jpg</url>
                <language>en</language>
                <type>theatrical</type>
            </poster>
            
            <!-- Fanart/Backdrops -->
            <fanart>
                <url>https://image.tmdb.org/t/p/original/s3TBrRGB1iav7gFOCVXITyLhu.jpg</url>
                <width>1920</width>
                <height>1080</height>
                <aspectratio>1.778</aspectratio>
            </fanart>
            
            <fanart>
                <url>https://image.tmdb.org/t/p/original/backdrop2.jpg</url>
                <width>3840</width>
                <height>2160</height>
            </fanart>
            
            <!-- Clear logo -->
            <clearlogo>
                <url>https://fanart.tv/fanart/movies/27205/hdmovielogo/inception.png</url>
                <language>en</language>
                <transparency>true</transparency>
            </clearlogo>
            
            <!-- Banner -->
            <banner>
                <url>https://fanart.tv/fanart/movies/27205/moviebanner/inception.jpg</url>
                <width>1000</width>
                <height>185</height>
            </banner>
            
            <!-- Disc art -->
            <discart>
                <url>https://fanart.tv/fanart/movies/27205/moviedisc/inception.png</url>
                <type>bluray</type>
                <transparency>true</transparency>
            </discart>
        </movie>
    </media>
</root>
```

### TV Show Season Artwork

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <tvshow>
            <title>Breaking Bad</title>
            
            <!-- Series poster -->
            <poster season="all" primary="true">
                <url>https://artworks.thetvdb.com/banners/posters/81189-10.jpg</url>
                <language>en</language>
                <rating>9.8</rating>
                <width>680</width>
                <height>1000</height>
            </poster>
            
            <!-- Season posters -->
            <poster season="1">
                <url>https://artworks.thetvdb.com/banners/seasons/81189-1-7.jpg</url>
            </poster>
            
            <poster season="2">
                <url>https://artworks.thetvdb.com/banners/seasons/81189-2-7.jpg</url>
            </poster>
            
            <!-- Series fanart -->
            <fanart>
                <url>https://artworks.thetvdb.com/banners/fanart/original/81189-21.jpg</url>
                <resolution>1920x1080</resolution>
                <colors>dark</colors>
            </fanart>
            
            <!-- Series banner -->
            <banner type="graphical">
                <url>https://artworks.thetvdb.com/banners/graphical/81189-g19.jpg</url>
                <width>758</width>
                <height>140</height>
            </banner>
            
            <!-- Clear logo -->
            <clearlogo>
                <url>https://fanart.tv/fanart/tv/81189/hdtvlogo/breaking-bad.png</url>
                <language>en</language>
            </clearlogo>
            
            <!-- Character art -->
            <characterart>
                <url>https://fanart.tv/fanart/tv/81189/characterart/walter-white.png</url>
                <character>Walter White</character>
            </characterart>
        </tvshow>
    </media>
</root>
```

### Music Album Artwork

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="NFOStandard" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
    <media>
        <album>
            <title>The Dark Side of the Moon</title>
            <artist>Pink Floyd</artist>
            
            <!-- Album cover -->
            <cover type="front" primary="true">
                <url>https://coverartarchive.org/release/f33esf4-3e4f/3458934589.jpg</url>
                <width>1500</width>
                <height>1500</height>
                <format>jpeg</format>
                <approved>true</approved>
            </cover>
            
            <!-- Back cover -->
            <cover type="back">
                <url>https://coverartarchive.org/release/f33esf4-3e4f/3458934590.jpg</url>
                <width>1500</width>
                <height>1500</height>
            </cover>
            
            <!-- CD art -->
            <cover type="medium">
                <url>cd-art.jpg</url>
                <description>CD surface art</description>
            </cover>
            
            <!-- Booklet pages -->
            <booklet>
                <page number="1">
                    <url>booklet-page1.jpg</url>
                </page>
                <page number="2">
                    <url>booklet-page2.jpg</url>
                </page>
            </booklet>
            
            <!-- Artist image -->
            <artistimage>
                <url>https://fanart.tv/fanart/music/artist/pink-floyd.jpg</url>
                <type>band</type>
            </artistimage>
        </album>
    </media>
</root>
```

## Troubleshooting

### Common Issues

1. **Image Display Problems**
   - Verify URL accessibility
   - Check image format compatibility
   - Ensure proper aspect ratios

2. **Resolution Issues**
   - Use highest quality sources
   - Avoid upscaled images
   - Maintain proper dimensions

3. **Missing Artwork**
   - Check multiple sources
   - Verify language settings
   - Use fallback images

### Validation

```xml
<poster>
    <url>poster.jpg</url>
    <validated>true</validated>
    <validationdate>2024-01-09</validationdate>
    <accessible>true</accessible>
    <lastchecked>2024-01-09T12:00:00Z</lastchecked>
</poster>
```

## Related Topics

- [Movies Guide](movies.md)
- [TV Shows Guide](tvshows.md)
- [Music Guide](music.md)
- [File Organization](../advanced/file-organization.md)