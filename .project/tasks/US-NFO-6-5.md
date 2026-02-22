---
assignee: claude
created: '2026-02-22'
id: US-NFO-6-5
points: 2
status: done
story_id: US-NFO-6
title: Enhance anime.xsd with outline, fix isAdult type, add extras
updated: '2026-02-22'
---

Enhance animeType in anime.xsd with missing elements and fix the isAdult data type.

Type fix:
- `isAdult`: change type from xs:integer to xs:boolean

New elements to add (all optional, minOccurs="0"):
- `outline` (xs:string, maxOccurs="1") — short description to complement existing `description` (long-form). Place before `description`.
- `tagline` (xs:string, maxOccurs="1")
- `userRating` (xs:decimal, maxOccurs="1") — place after `rating`
- `country` (xs:string, maxOccurs="unbounded")
- `subtitleLanguage` (xs:string, maxOccurs="unbounded")
- `soundtrack` (xs:string, maxOccurs="1")

File: Schemas/anime.xsd