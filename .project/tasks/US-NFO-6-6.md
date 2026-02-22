---
assignee: claude
created: '2026-02-22'
id: US-NFO-6-6
points: 2
status: done
story_id: US-NFO-6
title: Enhance adult.xsd with genre, language, images, and contentRating
updated: '2026-02-22'
---

Enhance adultType in adult.xsd with missing elements and fix naming.

New elements to add (all optional, minOccurs="0"):
- `genre` (xs:string, maxOccurs="unbounded")
- `language` (xs:string, maxOccurs="unbounded")
- `contentRating` (contentRatingType, maxOccurs="unbounded") — currently absent from this schema
- `banner` (subMediaType, maxOccurs="unbounded")
- `fanart` (subMediaType, maxOccurs="unbounded")
- `outline` (xs:string, maxOccurs="1") — short description to complement existing `description`

Rename for consistency:
- `thumbnail` → `thumb` (all other schemas use `thumb`)

Place `genre`/`language` near existing `keyword`/`tag`. Place `banner`/`fanart` near `thumb`. Place `contentRating` near `rating`/`uniqueId`.

File: Schemas/adult.xsd