# Architecture

## Schema Architecture

NFOStandard uses a modular XSD architecture with a single entry point (`main.xsd`) that includes type-specific schemas.

### Schema Hierarchy
```
main.xsd
  ├── common.xsd          (shared types: ratings, images, content ratings, etc.)
  ├── person.xsd           (actor, director, writer, producer types)
  ├── library.xsd          (library software metadata)
  ├── movie.xsd            (movie-specific elements)
  ├── tvshow.xsd           (TV show-specific elements)
  ├── anime.xsd            (anime-specific elements)
  ├── adult.xsd            (adult content elements)
  ├── music.xsd            (music elements)
  ├── musicvideo.xsd       (music video elements)
  ├── audiobook.xsd        (audiobook elements)
  ├── podcast.xsd          (podcast elements)
  └── video.xsd            (general video elements)
```

### Design Principles
1. **Single namespace** (`NFOStandard`) — keeps validation simple
2. **Composition over inheritance** — content types compose shared types from `common.xsd` and `person.xsd`
3. **Schema-first** — the XSD is the source of truth; examples are derived from it
4. **Backward-compatible evolution** — new optional elements can be added without breaking existing consumers

### XML Document Structure
```xml
<root xmlns="NFOStandard">
  <media>
    <movie>...</movie>    <!-- or tvshow, anime, music, etc. -->
  </media>
</root>
```

### Publishing
Schemas are published via GitHub Pages at `xsd.nfostandard.com`, allowing consumers to reference them via `xsi:schemaLocation`.
