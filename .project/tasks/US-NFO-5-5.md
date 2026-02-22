---
assignee: claude
created: '2026-02-22'
id: US-NFO-5-5
points: 2
status: done
story_id: US-NFO-5
title: Add missing elements and fix cardinality in video.xsd
updated: '2026-02-22'
---

Enhance videoType in video.xsd with missing elements and fix maxOccurs constraints.

New elements to add (all optional, minOccurs="0"):
- `genre` (xs:string, maxOccurs="unbounded")
- `language` (xs:string, maxOccurs="unbounded")
- `duration` (xs:integer, maxOccurs="1")
- `banner` (subMediaType, maxOccurs="unbounded")
- `fanart` (subMediaType, maxOccurs="unbounded")

Cardinality fixes (maxOccurs="1" → "unbounded"):
- `rating` (ratingType) — allow multiple rating sources
- `uniqueId` (uniqueidType) — allow multiple external IDs
- `contentRating` (contentRatingType) — allow multiple country ratings
- `producer` (personType) — allow multiple producers

Rename for consistency:
- `thumbnail` → `thumb` (all other schemas use `thumb`)

Place `genre` and `language` near `keyword`/`tag`. Place `duration` near existing fields. Place `banner`/`fanart` near `thumb`. Follow element ordering from movie.xsd.

File: Schemas/video.xsd