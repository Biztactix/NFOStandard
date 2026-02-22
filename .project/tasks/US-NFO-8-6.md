---
assignee: claude
created: '2026-02-22'
id: US-NFO-8-6
points: 3
status: done
story_id: US-NFO-8
title: Write content type reference sections for all 9 types
updated: '2026-02-22'
---

Fill in the 9 content type reference sections in SPECIFICATION.md. Each section should contain:

- Schema file location
- A field table with columns: Element | Type | Required | Cardinality | Description
- Any type-specific notes (e.g. tvshow altOrder attributes, music album sub-structure)

Content types to document (use the post-rename, post-enhancement schema state):
1. **movieType** — movie.xsd
2. **tvshowType** — tvshow.xsd (include altOrder, namedSeason inline types)
3. **animeType** — anime.xsd (note isAdult boolean)
4. **adultType** — adult.xsd
5. **videoType** — video.xsd
6. **musicType** — music.xsd (include albumType inline structure)
7. **musicVideoType** — musicvideo.xsd
8. **audiobookType** — audiobook.xsd
9. **podcastType** — podcast.xsd

For each field table, list every element with its XML type (xs:string, xs:date, ratingType, personType, etc.), whether it's required, its maxOccurs, and a short description of semantics.

File: SPECIFICATION.md (append to existing structure from task 1)
Depends on: US-NFO-8 task 1, all EPIC-NFO-1 and EPIC-NFO-2 stories