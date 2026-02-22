---
assignee: claude
created: '2026-02-22'
id: US-NFO-4-6
points: 1
status: done
story_id: US-NFO-4
title: Add production and localization elements to tvshow.xsd
updated: '2026-02-22'
---

Add missing production, localization, and media elements to tvshowType in tvshow.xsd.

New elements to add (all optional, minOccurs="0"):

Production elements:
- `runtime` (xs:integer, maxOccurs="1")
- `country` (xs:string, maxOccurs="unbounded")
- `productionCompany` (xs:string, maxOccurs="unbounded")
- `releaseDate` (xs:date, maxOccurs="unbounded")
- `award` (xs:string, maxOccurs="unbounded")

Localization elements:
- `language` (xs:string, maxOccurs="unbounded")
- `subtitleLanguage` (xs:string, maxOccurs="unbounded")
- `parentalGuide` (xs:string, maxOccurs="1")

Media elements:
- `banner` (subMediaType, maxOccurs="unbounded") — tvshow already has thumb/fanart but no banner

Place production elements in a logical group. Place `banner` near existing `thumb`/`fanart`. Follow the element ordering convention from movie.xsd.

File: Schemas/tvshow.xsd