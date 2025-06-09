# NFO Standard Field Mappings

This document provides comprehensive field mappings between NFO Standard and popular media databases, metadata providers, and media management systems.

## Table of Contents

- [Movie Fields](#movie-fields)
- [TV Show Fields](#tv-show-fields)
- [Music Fields](#music-fields)
- [Common Fields](#common-fields)
- [Rating Systems](#rating-systems)
- [Content Ratings](#content-ratings)
- [Unique Identifiers](#unique-identifiers)
- [Image Types](#image-types)

## Movie Fields

### Core Movie Metadata

| NFO Standard | TMDB | IMDB | OMDB | Kodi | Plex | Emby/Jellyfin |
|--------------|------|------|------|------|------|---------------|
| title | title | primaryTitle | Title | title | title | title |
| originaltitle | original_title | originalTitle | - | originaltitle | originalTitle | originaltitle |
| sorttitle | - | - | - | sorttitle | titleSort | sorttitle |
| year | release_date (year) | startYear | Year | year | year | year |
| runtime | runtime | runtimeMinutes | Runtime | runtime | duration/60000 | runtime |
| plot | overview | plot | Plot | plot | summary | plot |
| outline | - | plotOutline | - | outline | - | outline |
| tagline | tagline | - | - | tagline | tagline | tagline |
| genre | genres[].name | genres | Genre | genre | genres[].tag | genre |
| country | production_countries[].name | country | Country | country | countries[].tag | country |
| productioncompany | production_companies[].name | companies | Production | studio | studio | studio |
| releasedate | release_date | releaseDate | Released | releasedate | originallyAvailableAt | releasedate |

### People

| NFO Standard | TMDB | IMDB | Kodi | Plex | Emby/Jellyfin |
|--------------|------|------|------|------|---------------|
| actor.name | cast[].name | principals[].name | actor.name | actors[].tag | actor.name |
| actor.role | cast[].character | principals[].characters | actor.role | actors[].role | actor.role |
| actor.order | cast[].order | principals[].ordering | actor.order | (index) | actor.sortorder |
| director.name | crew[job=Director].name | directors[].name | director | directors[].tag | director |
| writer.name | crew[job=Writer].name | writers[].name | credits | writers[].tag | writer |
| producer.name | crew[job=Producer].name | producers[].name | - | producers[].tag | - |

### Collections

| NFO Standard | TMDB | Kodi | Plex | Emby/Jellyfin |
|--------------|------|------|------|---------------|
| setname | belongs_to_collection.name | set | collections[].tag | set.name |
| setoverview | belongs_to_collection.overview | - | - | set.overview |
| setorder | - | - | - | collectionnumber |

## TV Show Fields

### Show Level

| NFO Standard | TMDB | TVDB | Kodi | Plex | Emby/Jellyfin |
|--------------|------|------|------|------|---------------|
| title | name | seriesName | title | title | title/SeriesName |
| originaltitle | original_name | originalName | originaltitle | originalTitle | originaltitle |
| year | first_air_date (year) | firstAired (year) | year | year | year |
| plot | overview | overview | plot | summary | plot |
| premiered | first_air_date | firstAired | premiered | originallyAvailableAt | premiered |
| status | status | status | status | - | status/Status |
| studio | networks[].name | network | studio | studio/network | studio/Network |
| season | number_of_seasons | - | - | childCount | - |
| episode | number_of_episodes | - | - | leafCount | - |
| genre | genres[].name | genre | genre | genres[].tag | genre |
| contentrating | content_ratings[].rating | rating | mpaa | contentRating | contentrating |

### Episode Level

| NFO Standard | TMDB | TVDB | Kodi | Plex | Emby/Jellyfin |
|--------------|------|------|------|------|---------------|
| title | name | episodeName | title | title | title/EpisodeName |
| season | season_number | airedSeason | season | seasonNumber | season/SeasonNumber |
| episode | episode_number | airedEpisodeNumber | episode | episodeNumber | episode/EpisodeNumber |
| aired | air_date | firstAired | aired | originallyAvailableAt | aired/FirstAired |
| plot | overview | overview | plot | summary | plot |
| runtime | runtime | runtime | runtime | duration/60000 | runtime |

## Music Fields

### Album Level

| NFO Standard | MusicBrainz | Last.fm | Plex | Emby/Jellyfin |
|--------------|-------------|---------|------|---------------|
| title | title | name | title | title |
| artist | artist-credit[].name | artist | parentTitle | artist |
| albumartist | artist-credit[].name | - | parentTitle | albumartist |
| year | date (year) | - | year | year |
| genre | tags[].name | tags[].name | genres[].tag | genre |
| label | label[].name | - | - | label |
| releasedate | date | - | originallyAvailableAt | releasedate |

### Track Level

| NFO Standard | MusicBrainz | Plex | Emby/Jellyfin |
|--------------|-------------|------|---------------|
| position | position | index | tracknumber |
| title | title | title | title |
| duration | length/1000 | duration/1000 | runtime |
| artist | artist-credit[].name | originalTitle | artist |

## Common Fields

### Ratings

| NFO Standard | Description | Range | Example |
|--------------|-------------|-------|---------|
| rating[@name="imdb"] | IMDB rating | 0-10 | 8.5 |
| rating[@name="tmdb"] | TMDB rating | 0-10 | 8.2 |
| rating[@name="tvdb"] | TVDB rating | 0-10 | 8.7 |
| rating[@name="metacritic"] | Metacritic score | 0-100 | 74 |
| rating[@name="rottentomatoes"] | RT Tomatometer | 0-100 | 92 |
| rating[@name="audience"] | Audience score | 0-10 | 8.9 |
| userrating | Personal rating | 0-10 | 9.0 |

## Rating Systems

### Source Mappings

| Provider | NFO rating[@name] | Scale | Notes |
|----------|------------------|-------|-------|
| IMDB | imdb | 0-10 | Most common default |
| TMDB | tmdb | 0-10 | The Movie Database |
| TVDB | tvdb | 0-10 | For TV shows |
| Metacritic | metacritic | 0-100 | Critical aggregate |
| Rotten Tomatoes | rottentomatoes | 0-100 | Tomatometer |
| MyAnimeList | myanimelist | 0-10 | For anime |
| AniDB | anidb | 0-10 | For anime |

## Content Ratings

### Movie Ratings

| Country | Board | Ratings | NFO Example |
|---------|-------|---------|-------------|
| USA | MPAA | G, PG, PG-13, R, NC-17 | `<contentrating country="USA" board="MPAA" rating="PG-13"/>` |
| UK | BBFC | U, PG, 12, 12A, 15, 18, R18 | `<contentrating country="UK" board="BBFC" rating="15"/>` |
| Germany | FSK | 0, 6, 12, 16, 18 | `<contentrating country="Germany" board="FSK" rating="12"/>` |
| France | CNC | U, 10, 12, 16, 18 | `<contentrating country="France" board="CNC" rating="12"/>` |
| Japan | Eirin | G, PG12, R15+, R18+ | `<contentrating country="Japan" board="Eirin" rating="PG12"/>` |

### TV Ratings

| Country | Board | Ratings | NFO Example |
|---------|-------|---------|-------------|
| USA | TV | TV-Y, TV-Y7, TV-G, TV-PG, TV-14, TV-MA | `<contentrating country="USA" board="TV" rating="TV-14"/>` |
| UK | - | U, PG, 12, 15, 18 | `<contentrating country="UK" rating="15"/>` |
| Australia | ACB | C, P, G, PG, M, MA15+, R18+ | `<contentrating country="Australia" board="ACB" rating="M"/>` |

## Unique Identifiers

### Movie IDs

| Type | Format | Example | Source |
|------|--------|---------|--------|
| imdb | tt + 7-8 digits | tt0111161 | IMDB |
| tmdb | numeric | 278 | The Movie Database |
| omdb | tt + digits | tt0111161 | Open Movie Database |

### TV Show IDs

| Type | Format | Example | Source |
|------|--------|---------|--------|
| imdb | tt + digits | tt0903747 | IMDB |
| tvdb | numeric | 81189 | TheTVDB |
| tmdb | numeric | 1396 | The Movie Database |
| tvrage | numeric | 18164 | TVRage (deprecated) |

### Music IDs

| Type | Format | Example | Source |
|------|--------|---------|--------|
| musicbrainz | UUID | 7e84f845-ac16-41fe-9ff8-df12eb32af55 | MusicBrainz |
| spotify | alphanumeric | 2noRn2Aes5aoNVsU6iWThc | Spotify |
| lastfm | URL slug | The+Beatles | Last.fm |

## Image Types

### Standard Image Mappings

| NFO Standard | TMDB | TVDB | Plex | Emby | Typical Use |
|--------------|------|------|------|------|-------------|
| thumb[@type="poster"] | poster_path | poster | thumb | Primary | Main poster |
| fanart[@type="background"] | backdrop_path | fanart | art | Backdrop | Background art |
| banner[@type="banner"] | - | banner | banner | Banner | Wide banner |
| thumb[@type="landscape"] | backdrop_path | - | - | Landscape | 16:9 thumb |
| banner[@type="logo"] | logos[] | - | - | Logo | Clear logo |
| thumb[@type="clearart"] | - | clearart | - | - | Character art |

### Image Dimensions

| Type | Aspect Ratio | Common Sizes | Notes |
|------|--------------|--------------|-------|
| poster | 2:3 | 1000×1500, 680×1000 | Movie/TV posters |
| fanart | 16:9 | 1920×1080, 3840×2160 | Backgrounds |
| banner | ~5.4:1 | 1000×185, 758×140 | Wide banners |
| landscape | 16:9 | 1920×1080, 1280×720 | Thumbnails |
| square | 1:1 | 1000×1000, 500×500 | Music albums |

## Provider-Specific Mappings

### TMDB API to NFO

```json
// TMDB API Response
{
  "adult": false,
  "backdrop_path": "/path.jpg",
  "belongs_to_collection": {
    "id": 1241,
    "name": "Harry Potter Collection"
  },
  "budget": 125000000,
  "genres": [{"id": 12, "name": "Adventure"}],
  "id": 671
}
```

Maps to:
```xml
<movie>
  <adult>false</adult>
  <fanart type="background" url="https://image.tmdb.org/t/p/original/path.jpg"/>
  <setname>Harry Potter Collection</setname>
  <budget>125000000</budget>
  <genre>Adventure</genre>
  <uniqueid type="tmdb">671</uniqueid>
</movie>
```

### TVDB API to NFO

```json
// TVDB API Response
{
  "id": 81189,
  "seriesName": "Breaking Bad",
  "status": "Ended",
  "firstAired": "2008-01-20",
  "network": "AMC",
  "runtime": "45",
  "genre": ["Crime", "Drama", "Thriller"],
  "overview": "Breaking Bad follows..."
}
```

Maps to:
```xml
<tvshow>
  <uniqueid type="tvdb">81189</uniqueid>
  <title>Breaking Bad</title>
  <status>Ended</status>
  <premiered>2008-01-20</premiered>
  <studio>AMC</studio>
  <runtime>45</runtime>
  <genre>Crime</genre>
  <genre>Drama</genre>
  <genre>Thriller</genre>
  <plot>Breaking Bad follows...</plot>
</tvshow>
```

## Best Practices

1. **Default Ratings**: Always mark one rating as default (usually IMDB)
2. **ID Priority**: IMDB > TMDB > TVDB for cross-referencing
3. **Date Formats**: Use ISO 8601 (YYYY-MM-DD)
4. **Image URLs**: Use highest quality available
5. **Genre Consistency**: Use standard genre names across media types
6. **Multiple Values**: Use separate elements for multiple values (genres, actors, etc.)