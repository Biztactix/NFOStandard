---
assignee: claude
created: '2026-02-22'
id: US-NFO-8-5
points: 2
status: done
story_id: US-NFO-8
title: 'Write spec foundation: intro, shared types, usage guidelines'
updated: '2026-02-22'
---

Create SPECIFICATION.md with the document skeleton, shared types reference, usage guidelines, and migration notes.

Sections to write:

1. **Introduction** — What NFOStandard is, versioning, namespace (`NFOStandard`)
2. **Document Structure** — The root/media/[type] XML structure, how to reference the schema via xsi:schemaLocation
3. **Shared Types Reference** — Detailed table for each type in common.xsd, person.xsd, library.xsd:
   - `ratingType` — attributes: value, votes, name, max, default
   - `uniqueidType` — content + attributes: type, default
   - `contentRatingType` — content + attributes: country, board, rating, image
   - `subMediaType` — content + attributes: type, width, height, url, extUrl, aspect, season, preview
   - `serviceLinkType` — elements: service, url
   - `personType` — elements: name, role, order, thumb, bio, url, gender, tag
   - `metadataType` (library) — elements reference
   - `statsType` — elements + userId attribute
4. **Usage Guidelines** — How to create a valid NFO file, how to extend, partial metadata patterns
5. **Migration Notes** — Breaking changes from camelCase renames (movie, tvshow), identifier standardization (adult/video name→title), type fixes (anime isAdult integer→boolean)

Leave placeholder sections for the 9 content types (to be filled in task 2).

File: SPECIFICATION.md (project root)
Depends on: US-NFO-1, US-NFO-2 (finalized shared types)