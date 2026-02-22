# NFO Standard Specification

Version 1.0 | Namespace: `NFOStandard`

This document is the formal specification for the NFO Standard XML schema. It describes every element, type, and attribute defined across all schema files so that developers can implement the standard without reading raw XSD.

## Table of Contents

- [Introduction](#introduction)
- [Document Structure](#document-structure)
- [Shared Types](#shared-types)
  - [ratingType](#ratingtype)
  - [uniqueidType](#uniqueidtype)
  - [contentRatingType](#contentratingtype)
  - [serviceLinksType](#servicelinkstype)
  - [subMediaType](#submediatype)
  - [personType](#persontype)
- [Content Types](#content-types)
  - [Movie](#movie)
  - [TV Show](#tv-show)
  - [Anime](#anime)
  - [Adult](#adult)
  - [Video](#video)
  - [Music](#music)
  - [Music Video](#music-video)
  - [Audiobook](#audiobook)
  - [Podcast](#podcast)
- [Library Metadata](#library-metadata)
  - [metadataType](#metadatatype)
  - [statsType](#statstype)
- [Usage Guidelines](#usage-guidelines)
- [Migration Notes](#migration-notes)

---

## Introduction

**NFO Standard** is an open, unified standard for `.nfo` metadata files used across media management applications. Rather than each application inventing its own metadata format, NFO Standard provides a comprehensive XSD-based schema that covers the vast majority of use cases with built-in extensibility for the rest.

### Versioning

This specification describes **Version 1.0** of the NFO Standard. The schema follows a single-version model — all schema files share the same version number and are released together.

### Namespace

All NFO Standard elements live under the `NFOStandard` namespace. Every conforming document must declare this namespace on the root element:

```xml
xmlns="NFOStandard"
```

### Schema Location

The canonical schema is published at:

```
https://xsd.nfostandard.com/main.xsd
```

The master schema (`main.xsd`) includes all type-specific schemas via `xs:include`. Individual schema files are available under `https://xsd.nfostandard.com/Schemas/`.

### License

NFO Standard is released under [The Unlicense](https://unlicense.org/) (public domain). There are no restrictions on use, modification, or distribution.

---

## Document Structure

Every NFO Standard document has the following root structure:

```xml
<root xmlns="NFOStandard"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="NFOStandard https://xsd.nfostandard.com/main.xsd">
  <media>
    <!-- Exactly one content type element here -->
  </media>
  <library>...</library>   <!-- optional, repeatable -->
  <stats>...</stats>       <!-- optional, repeatable -->
</root>
```

The `<media>` element contains exactly one of the nine content type elements: `movie`, `tvshow`, `adult`, `anime`, `video`, `music`, `audiobook`, `podcast`, or `musicvideo`.

The optional `<library>` and `<stats>` elements carry application-specific metadata and user watch statistics.

---

## Shared Types

These types are defined in `common.xsd` and `person.xsd` and are reused across all content types.

### ratingType

Represents a rating from an external source (e.g. IMDb, TMDb).

Defined in: `common.xsd`

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `value` | decimal | Yes | — | The rating value |
| `votes` | integer | No | — | Number of votes |
| `name` | string | Yes | — | Rating source name (e.g. "imdb") |
| `max` | integer | No | 10 | Maximum possible rating value |
| `default` | boolean | No | — | Whether this is the default/primary rating |

### uniqueidType

An identifier from an external database.

Defined in: `common.xsd`

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | Yes | Source database (e.g. "imdb", "tmdb") |
| `default` | boolean | No | Whether this is the primary identifier |

Text content: the ID string value (e.g. "tt1375666").

### contentRatingType

An age/content rating from a classification board.

Defined in: `common.xsd`

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | Yes | Country code (e.g. "USA") |
| `board` | string | Yes | Classification board (e.g. "MPAA") |
| `rating` | string | Yes | Rating value (e.g. "PG-13") |
| `image` | string | Yes | Image filename for the rating badge |

### serviceLinksType

A link to a streaming or distribution service.

Defined in: `common.xsd`

| Child Element | Type | Occurs | Description |
|---------------|------|--------|-------------|
| `service` | string | 1 | Service name (e.g. "Spotify") |
| `url` | string | 1 | URL to the content on that service |

### subMediaType

Represents a media asset such as a thumbnail, banner, or fanart image.

Defined in: `common.xsd`

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `type` | string | No | Asset subtype (e.g. "poster", "thumbnail", "background") |
| `aspect` | string | No | Aspect ratio |
| `season` | integer | No | Associated season number |
| `preview` | string | No | Preview image URL |
| `width` | integer | No | Image width in pixels |
| `height` | integer | No | Image height in pixels |
| `url` | string | No | URL to the image |
| `extUrl` | string | No | External/alternate URL |

Text content: optional path or identifier string.

### personType

Represents a person associated with the content (actor, director, etc.).

Defined in: `person.xsd`

| Child Element | Type | Min | Max | Description |
|---------------|------|-----|-----|-------------|
| `name` | string | 1 | 1 | Full name of the person |
| `role` | string | 0 | 1 | Role or character played |
| `order` | integer | 0 | 1 | Display/credit order |
| `thumb` | string | 0 | 1 | Thumbnail image path or URL |
| `bio` | string | 0 | 1 | Short biography |
| `url` | string | 0 | unbounded | Profile or reference URLs |
| `gender` | string | 0 | 1 | Gender |
| `tag` | string | 0 | unbounded | Descriptive tags |

---

## Content Types

### Movie

Schema type: `movieType` | Defined in: `movie.xsd` | Element: `<movie>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Primary title |
| `originalTitle` | string | 0 | 1 | Title in original language |
| `sortTitle` | string | 0 | 1 | Title used for sorting |
| `alternateTitle` | string | 0 | unbounded | Alternate/localized titles |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `userRating` | decimal | 0 | 1 | User's personal rating |
| `outline` | string | 0 | 1 | Short synopsis |
| `plot` | string | 0 | 1 | Full plot description |
| `tagline` | string | 0 | 1 | Marketing tagline |
| `runtime` | integer | 0 | 1 | Runtime in minutes |
| `banner` | subMediaType | 0 | unbounded | Banner images |
| `thumb` | subMediaType | 0 | unbounded | Thumbnail images |
| `fanart` | subMediaType | 0 | unbounded | Fan art / background images |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `genre` | string | 0 | unbounded | Genre classifications |
| `tag` | string | 0 | unbounded | User or system tags |
| `setName` | string | 0 | 1 | Name of the movie collection/set |
| `setOverview` | string | 0 | 1 | Description of the collection/set |
| `country` | string | 0 | unbounded | Production countries |
| `productionCompany` | string | 0 | unbounded | Production companies |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `releaseDate` | date | 0 | unbounded | Release dates |
| `award` | string | 0 | unbounded | Awards received |
| `subtitleLanguage` | string | 0 | unbounded | Available subtitle languages |
| `soundtrack` | string | 0 | 1 | Soundtrack reference |
| `parentalGuide` | string | 0 | 1 | Parental guidance notes |
| `actor` | personType | 0 | unbounded | Cast members |
| `director` | personType | 0 | unbounded | Directors |
| `writer` | personType | 0 | unbounded | Writers/screenwriters |
| `composer` | personType | 0 | unbounded | Music composers |
| `producers` | personType | 0 | unbounded | Producers |
| `collection` | string | 0 | 1 | Collection identifier |

### TV Show

Schema type: `tvshowType` | Defined in: `tvshow.xsd` | Element: `<tvshow>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Episode or show title |
| `originalTitle` | string | 0 | 1 | Title in original language |
| `showTitle` | string | 0 | 1 | Parent show title |
| `sortTitle` | string | 0 | 1 | Title used for sorting |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `userRating` | decimal | 0 | 1 | User's personal rating |
| `season` | integer | 0 | 1 | Season number |
| `episode` | integer | 0 | 1 | Episode number |
| `altOrder` | (inline complex) | 0 | unbounded | Alternate ordering (see below) |
| `outline` | string | 0 | 1 | Short synopsis |
| `plot` | string | 0 | 1 | Full plot description |
| `tagline` | string | 0 | 1 | Marketing tagline |
| `runtime` | integer | 0 | 1 | Runtime in minutes |
| `language` | string | 0 | unbounded | Audio languages |
| `banner` | subMediaType | 0 | unbounded | Banner images |
| `thumb` | subMediaType | 0 | unbounded | Thumbnail images |
| `fanart` | subMediaType | 0 | unbounded | Fan art / background images |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `genre` | string | 0 | unbounded | Genre classifications |
| `tag` | string | 0 | unbounded | User or system tags |
| `country` | string | 0 | unbounded | Production countries |
| `productionCompany` | string | 0 | unbounded | Production companies |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `releaseDate` | date | 0 | unbounded | Release dates |
| `award` | string | 0 | unbounded | Awards received |
| `subtitleLanguage` | string | 0 | unbounded | Available subtitle languages |
| `parentalGuide` | string | 0 | 1 | Parental guidance notes |
| `premiered` | date | 0 | 1 | Premiere date |
| `year` | gYear | 0 | 1 | Year of release |
| `status` | string | 0 | 1 | Show status (e.g. "Continuing", "Ended") |
| `studio` | string | 0 | unbounded | Studios |
| `trailer` | string | 0 | 1 | Trailer URL |
| `actor` | personType | 0 | unbounded | Cast members |
| `director` | personType | 0 | unbounded | Directors |
| `writer` | personType | 0 | unbounded | Writers |
| `composer` | personType | 0 | unbounded | Music composers |
| `producers` | personType | 0 | unbounded | Producers |
| `namedSeason` | (inline complex) | 0 | unbounded | Named season mapping (see below) |

**altOrder attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `altSeason` | integer | No | Alternate season number |
| `altEpisode` | integer | No | Alternate episode number |
| `name` | string | No | Name of the alternate ordering scheme |

Text content: optional description.

**namedSeason attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `number` | integer | Yes | Season number |

Text content: the season name.

### Anime

Schema type: `animeType` | Defined in: `anime.xsd` | Element: `<anime>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Primary title |
| `releaseDate` | date | 0 | 1 | Release date |
| `productionCompany` | string | 0 | 1 | Production studio |
| `genre` | string | 0 | unbounded | Genre classifications |
| `language` | string | 0 | unbounded | Audio languages |
| `season` | integer | 0 | 1 | Season number |
| `episode` | integer | 0 | 1 | Episode number |
| `duration` | integer | 0 | 1 | Duration in minutes |
| `isAdult` | boolean | 0 | 1 | Whether the content is adult-rated |
| `director` | personType | 0 | unbounded | Directors |
| `voiceActor` | personType | 0 | unbounded | Original voice actors |
| `translationVoice` | personType | 0 | unbounded | Dubbed/translation voice actors |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `tag` | string | 0 | unbounded | Tags |
| `outline` | string | 0 | 1 | Short synopsis |
| `tagline` | string | 0 | 1 | Marketing tagline |
| `description` | string | 0 | 1 | Full description |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `userRating` | decimal | 0 | 1 | User's personal rating |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `country` | string | 0 | unbounded | Production countries |
| `subtitleLanguage` | string | 0 | unbounded | Available subtitle languages |
| `soundtrack` | string | 0 | 1 | Soundtrack reference |
| `banner` | subMediaType | 0 | unbounded | Banner images |
| `thumb` | subMediaType | 0 | unbounded | Thumbnail images |
| `fanart` | subMediaType | 0 | unbounded | Fan art / background images |
| `links` | string | 0 | unbounded | Related links |

### Adult

Schema type: `adultType` | Defined in: `adult.xsd` | Element: `<adult>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Primary title |
| `releaseDate` | date | 0 | 1 | Release date |
| `productionCompany` | string | 0 | 1 | Production company/studio |
| `siteName` | string | 0 | 1 | Website name |
| `VideoURL` | string | 0 | 1 | Direct video URL |
| `TrailerURL` | string | 0 | 1 | Trailer URL |
| `duration` | integer | 0 | 1 | Duration in minutes |
| `director` | personType | 0 | unbounded | Directors |
| `performer` | personType | 0 | unbounded | Performers |
| `genre` | string | 0 | unbounded | Genre classifications |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `tag` | string | 0 | unbounded | Tags |
| `language` | string | 0 | unbounded | Audio languages |
| `link` | string | 0 | unbounded | Related links |
| `outline` | string | 0 | 1 | Short synopsis |
| `description` | string | 0 | 1 | Full description |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `banner` | subMediaType | 0 | unbounded | Banner images |
| `thumb` | subMediaType | 0 | unbounded | Thumbnail images |
| `fanart` | subMediaType | 0 | unbounded | Fan art / background images |

### Video

Schema type: `videoType` | Defined in: `video.xsd` | Element: `<video>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Primary title |
| `filmingDate` | date | 0 | 1 | Date the video was filmed |
| `producer` | personType | 0 | unbounded | Producers |
| `collectionName` | string | 0 | 1 | Collection or series name |
| `people` | personType | 0 | unbounded | People featured in the video |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `genre` | string | 0 | unbounded | Genre classifications |
| `language` | string | 0 | unbounded | Audio languages |
| `tag` | string | 0 | unbounded | Tags |
| `duration` | integer | 0 | 1 | Duration in minutes |
| `description` | string | 0 | 1 | Full description |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `thumb` | subMediaType | 0 | unbounded | Thumbnail images |
| `banner` | subMediaType | 0 | unbounded | Banner images |
| `fanart` | subMediaType | 0 | unbounded | Fan art / background images |

### Music

Schema type: `musicType` | Defined in: `music.xsd` | Element: `<music>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Track title |
| `releaseDate` | date | 0 | 1 | Release date |
| `album` | (inline complex) | 0 | unbounded | Album associations (see below) |
| `productionCompany` | string | 0 | 1 | Record label or production company |
| `producer` | personType | 0 | unbounded | Producers |
| `writer` | personType | 0 | unbounded | Songwriters |
| `artist` | personType | 0 | unbounded | Performing artists |
| `genre` | string | 0 | unbounded | Genre classifications |
| `duration` | integer | 0 | 1 | Duration in seconds |
| `language` | string | 0 | 1 | Language |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `tag` | string | 0 | unbounded | Tags |
| `description` | string | 0 | 1 | Track description |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `cover` | subMediaType | 0 | unbounded | Cover art images |
| `serviceLinks` | serviceLinksType | 0 | unbounded | Streaming service links |

**album child elements (inline):**

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Album title |
| `position` | integer | 1 | 1 | Track number within the album |
| `artist` | string | 1 | 1 | Album artist |
| `uniqueid` | string | 0 | 1 | Album identifier |
| `url` | string | 0 | 1 | Album URL |
| `cover` | subMediaType | 0 | unbounded | Album cover art |

Note: `music.xsd` also defines a standalone `albumType` with elements: `title` (required), `artist`, `uniqueid`, `url`, and `cover`.

### Music Video

Schema type: `musicVideoType` | Defined in: `musicvideo.xsd` | Element: `<musicvideo>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Video title |
| `releaseDate` | date | 0 | 1 | Release date |
| `productionCompany` | string | 0 | 1 | Production company |
| `producer` | personType | 0 | unbounded | Producers |
| `writer` | personType | 0 | unbounded | Songwriters |
| `artist` | personType | 0 | unbounded | Performing artists |
| `genre` | string | 0 | unbounded | Genre classifications |
| `duration` | integer | 0 | 1 | Duration in seconds |
| `language` | string | 0 | 1 | Language |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `tag` | string | 0 | unbounded | Tags |
| `description` | string | 0 | 1 | Video description |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `cover` | subMediaType | 0 | unbounded | Cover art images |
| `serviceLinks` | serviceLinksType | 0 | unbounded | Streaming service links |

### Audiobook

Schema type: `audiobookType` | Defined in: `audiobook.xsd` | Element: `<audiobook>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Book title |
| `releaseDate` | date | 0 | 1 | Release date |
| `productionCompany` | string | 0 | 1 | Publisher or production company |
| `isbn` | string | 0 | 1 | ISBN identifier |
| `duration` | integer | 0 | 1 | Duration in minutes |
| `language` | string | 0 | 1 | Language |
| `genre` | string | 0 | 1 | Genre |
| `writer` | personType | 0 | unbounded | Authors |
| `voiceActor` | personType | 0 | unbounded | Narrators |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `tag` | string | 0 | unbounded | Tags |
| `description` | string | 0 | 1 | Book description |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `cover` | subMediaType | 0 | unbounded | Cover art images |

### Podcast

Schema type: `podcastType` | Defined in: `podcast.xsd` | Element: `<podcast>`

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `title` | string | 1 | 1 | Episode or show title |
| `releaseDate` | date | 0 | 1 | Release date |
| `productionCompany` | string | 0 | 1 | Production company or network |
| `host` | personType | 0 | unbounded | Hosts |
| `guest` | personType | 0 | unbounded | Guests |
| `duration` | integer | 0 | 1 | Duration in minutes |
| `language` | string | 0 | 1 | Language |
| `genre` | string | 0 | unbounded | Genre classifications |
| `keyword` | string | 0 | unbounded | Searchable keywords |
| `tag` | string | 0 | unbounded | Tags |
| `description` | string | 0 | 1 | Episode description |
| `rating` | ratingType | 0 | unbounded | External ratings |
| `uniqueId` | uniqueidType | 0 | unbounded | External database identifiers |
| `contentRating` | contentRatingType | 0 | unbounded | Age/content ratings |
| `cover` | subMediaType | 0 | unbounded | Cover art images |
| `serviceLinks` | serviceLinksType | 0 | unbounded | Streaming service links |

---

## Library Metadata

These types are defined in `library.xsd` and carry application-level tracking data that is separate from the media content itself.

### metadataType

Used by the `<library>` element. Stores application and library management fields.

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `appID` | string | 1 | 1 | Identifier for the application that created/manages this entry |
| `uniqueid` | string | 0 | 1 | Unique identifier within the library |
| `libraryid` | string | 0 | 1 | Library-level identifier |
| `librarysubid` | string | 0 | 1 | Sub-identifier within the library |
| `dateAdded` | dateTime | 0 | 1 | When the item was added to the library |
| `dateUpdated` | dateTime | 0 | 1 | When the item was last updated |
| `lastMetadataScan` | dateTime | 0 | 1 | Last metadata scan timestamp |
| `lastChapterSearch` | dateTime | 0 | 1 | Last chapter search timestamp |
| `lastIntroSearch` | dateTime | 0 | 1 | Last intro detection timestamp |
| `thumbnails` | subMediaType | 0 | unbounded | Thumbnail images |
| `fanart` | subMediaType | 0 | unbounded | Fan art images |
| `banner` | subMediaType | 0 | unbounded | Banner images |
| `internalLink` | string | 0 | 1 | Internal application link |
| `externalLink` | string | 0 | 1 | External link (e.g. web URL) |
| `tags` | string | 0 | unbounded | Library tags |
| `liked` | int | 0 | 1 | Liked status (numeric) |
| `duration` | long | 0 | unbounded | Duration values |
| `collection` | (inline complex) | 0 | 1 | Collection association (see below) |

**collection attributes:**

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Collection name |
| `id` | string | No | Collection identifier |
| `description` | string | No | Collection description |

### statsType

Used by the `<stats>` element. Stores per-user watch/listen statistics.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `userId` | string | Yes | User identifier |

| Element | Type | Min | Max | Description |
|---------|------|-----|-----|-------------|
| `watchCount` | integer | 0 | 1 | Number of times watched/listened |
| `liked` | boolean | 0 | 1 | Whether the user liked the content |
| `userRating` | decimal | 0 | 1 | User's personal rating |
| `watched` | boolean | 0 | 1 | Whether the user has watched/listened |
| `progress` | decimal | 0 | 1 | Playback progress (0.0 to 1.0) |

---

## Usage Guidelines

### General Principles

1. **One file per media item.** Each `.nfo` file describes a single media item. The `<media>` element contains exactly one content type child.

2. **Only `title` is required.** Every content type requires only a `title` element. All other fields are optional. Populate as many fields as your data source provides.

3. **Use the correct content type.** Choose the most specific content type that fits your media. Use `video` as a catch-all for general video content that does not fit other categories.

4. **Namespace is mandatory.** Always declare `xmlns="NFOStandard"` on the root element and reference the schema location for validation.

### Identifiers

- Use `uniqueId` elements to link to external databases (IMDb, TMDb, TVDB, etc.).
- Mark exactly one `uniqueId` with `default="true"` to indicate the primary identifier.
- The `type` attribute should use lowercase short names: `imdb`, `tmdb`, `tvdb`, etc.

### Ratings

- Each `rating` element represents a score from a single source.
- Mark one rating as `default="true"` for the preferred display rating.
- Set `max` only when it differs from the default of 10.

### Media Assets

- Use `thumb`, `banner`, and `fanart` for image assets. Some content types use `cover` instead (music, audiobook, podcast, music video).
- Always populate `width`, `height`, and `url` attributes when available.
- The `type` attribute should describe the purpose: `poster`, `thumbnail`, `background`, etc.

### People

- Use the appropriate element name for the role: `actor`, `director`, `writer`, `host`, `guest`, `performer`, `voiceActor`, etc.
- The `name` child element is required. All other person fields are optional.
- Use the `order` element for cast members to define credit order.

### Library and Stats Sections

- The `<library>` element is intended for media management applications to store their own tracking data. The `appID` field is required and should uniquely identify the application.
- The `<stats>` element stores per-user statistics. The `userId` attribute is required. Multiple `<stats>` elements can appear for different users.
- These sections are optional and should be preserved but not modified by applications that do not own them.

### Dates

- Use ISO 8601 format: `YYYY-MM-DD` for `date` fields and `YYYY-MM-DDTHH:MM:SS` for `dateTime` fields.
- The `releaseDate` element may repeat when a title has multiple release dates (theatrical, digital, etc.).

### Extensibility

The standard is designed to cover the majority of use cases. If you need fields beyond what the standard provides:
- Open an issue or pull request at the NFO Standard repository to propose additions.
- Do not add non-standard elements inside the `NFOStandard` namespace, as they will fail schema validation.

---

## Migration Notes

This section documents breaking changes introduced in Version 1.0 of the NFO Standard. If you are migrating from an earlier draft or pre-standard NFO format, review the following changes.

### Element Name Standardization (camelCase)

Several element names in `movie.xsd` and `tvshow.xsd` were renamed from flat lowercase to camelCase for consistency across the standard:

| Schema | Old Name | New Name |
|--------|----------|----------|
| movie.xsd | `originaltitle` | `originalTitle` |
| movie.xsd | `sorttitle` | `sortTitle` |
| movie.xsd | `alternatetitle` | `alternateTitle` |
| movie.xsd | `userrating` | `userRating` |
| movie.xsd | `contentrating` | `contentRating` |
| movie.xsd | `uniqueid` | `uniqueId` |
| movie.xsd | `setname` | `setName` |
| movie.xsd | `setoverview` | `setOverview` |
| movie.xsd | `productioncompany` | `productionCompany` |
| movie.xsd | `releasedate` | `releaseDate` |
| movie.xsd | `subtitlelanguage` | `subtitleLanguage` |
| movie.xsd | `parentalguide` | `parentalGuide` |
| tvshow.xsd | `originaltitle` | `originalTitle` |
| tvshow.xsd | `showtitle` | `showTitle` |
| tvshow.xsd | `sorttitle` | `sortTitle` |
| tvshow.xsd | `userrating` | `userRating` |
| tvshow.xsd | `contentrating` | `contentRating` |
| tvshow.xsd | `uniqueid` | `uniqueId` |
| tvshow.xsd | `productioncompany` | `productionCompany` |
| tvshow.xsd | `releasedate` | `releaseDate` |
| tvshow.xsd | `subtitlelanguage` | `subtitleLanguage` |
| tvshow.xsd | `parentalguide` | `parentalGuide` |

### Identifier Standardization (`name` to `title`)

The `adult.xsd` and `video.xsd` schemas previously used `name` as the required identifier element. This has been renamed to `title` to be consistent with all other content types:

| Schema | Old Name | New Name |
|--------|----------|----------|
| adult.xsd | `name` | `title` |
| video.xsd | `name` | `title` |

### Type Corrections

| Schema | Element | Old Type | New Type | Notes |
|--------|---------|----------|----------|-------|
| anime.xsd | `isAdult` | `xs:integer` | `xs:boolean` | Was incorrectly typed as integer; now uses `true`/`false` |
