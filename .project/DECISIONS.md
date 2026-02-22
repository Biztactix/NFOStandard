# Architectural Decisions

## ADR-001: Required vs Optional Field Policy

**Status:** Accepted
**Date:** 2026-02-22
**Story:** US-NFO-3 — Standardize required vs optional field patterns

### Context

NFOStandard defines XSD schemas for multiple content types (movie, TV show, anime, music, etc.). Prior to this decision, each schema independently chose which fields to mark as required (`minOccurs="1"`), leading to significant inconsistencies:

| Schema | Required Fields | Count |
|--------|----------------|-------|
| movie.xsd | title | 1 |
| tvshow.xsd | title | 1 |
| adult.xsd | title, releaseDate | 2 |
| anime.xsd | title, releaseDate, productionCompany | 3 |
| video.xsd | title, filmingDate, producer | 3 |
| audiobook.xsd | title, releaseDate, productionCompany, writer | 4 |
| podcast.xsd | title, releaseDate, productionCompany, host | 4 |
| music.xsd | title, releaseDate, productionCompany, producer, writer, artist | 6 |
| musicvideo.xsd | title, releaseDate, productionCompany, producer, writer, artist | 6 |

This inconsistency makes it harder for consumers to predict what metadata is mandatory and raises the barrier for producers to create valid NFO files.

### Decision

**Baseline policy: `title` is always required; everything else is optional unless there is a strong semantic reason.**

Specifically:

1. **Universal required field:** Every content type schema MUST require `title` (or its equivalent, e.g., `name`). A piece of media without a title is not meaningfully identifiable.

2. **Maximum required fields:** No schema should require more than **2–3 fields**. If a schema currently exceeds this, the extra required fields must be relaxed to optional.

3. **Exception criteria:** A field may be required beyond `title` only if:
   - The content type is meaningless or unidentifiable without it (strong semantic coupling)
   - There is broad consensus among consumers that the field is always available
   - Example: a podcast episode arguably needs a `host`, but in practice this metadata is often missing from feeds, so it should be optional

4. **Default to optional:** When in doubt, make it optional. Consumers should handle missing fields gracefully. Producers should be encouraged (via documentation and examples) to populate fields, but not forced by the schema.

### Consequences

- **Schemas to update:** music.xsd, musicvideo.xsd, anime.xsd, adult.xsd, video.xsd, audiobook.xsd, podcast.xsd all need required fields relaxed
- **movie.xsd and tvshow.xsd** already comply (only `title` required)
- **Backward compatibility:** Relaxing required fields is backward-compatible — existing valid documents remain valid
- **Documentation:** Examples and README should encourage populating key fields even though they are optional
