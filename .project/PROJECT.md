# NFOStandard

## Overview
NFOStandard is an open, unified standard for `.nfo` metadata files used across media applications. It eliminates the need for each application to invent its own format by providing a comprehensive XSD-based schema covering 95% of use cases, with built-in extensibility for fringe cases.

## Tech Stack
- **Schema Language**: XSD (XML Schema Definition)
- **Data Format**: XML
- **Hosting**: GitHub Pages (xsd.nfostandard.com)
- **License**: The Unlicense (public domain)

## Project Structure
```
main.xsd                 # Master schema — includes/imports type-specific schemas
Schemas/
  common.xsd             # Shared custom types (ratings, images, dates, etc.)
  person.xsd             # Person-related types (actors, directors, writers)
  library.xsd            # Library software integration elements
  movie.xsd              # Movie metadata schema
  tvshow.xsd             # TV show metadata schema
  anime.xsd              # Anime metadata schema
  adult.xsd              # Adult video metadata schema
  music.xsd              # Music metadata schema
  musicvideo.xsd         # Music video metadata schema
  audiobook.xsd          # Audiobook metadata schema
  podcast.xsd            # Podcast metadata schema
  video.xsd              # General video metadata schema
ExampleMovie.xml         # Sample movie NFO file
SamplePodcast.xml        # Sample podcast NFO file
```

## Key Concepts
- **Modular schemas**: Each content type has its own XSD, with `common.xsd` and `person.xsd` providing shared types
- **Namespace**: `NFOStandard` — all elements live under this namespace
- **Schema location**: Published at `https://xsd.nfostandard.com/main.xsd`
- **Extensibility**: Custom types and extension points built into the schema

## Contribution Model
Open-source, community-driven. Pull requests reviewed by maintainer.
