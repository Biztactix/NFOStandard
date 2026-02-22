---
assignee: claude
created: '2026-02-22'
id: US-NFO-4-5
points: 2
status: done
story_id: US-NFO-4
title: Add crew and descriptive elements to tvshow.xsd
updated: '2026-02-22'
---

Add missing person and descriptive elements to tvshowType in tvshow.xsd.

New elements to add (all optional, minOccurs="0"):

Person elements (using personType, maxOccurs="unbounded"):
- `director`
- `writer`
- `composer`
- `producers`

Descriptive elements:
- `outline` (xs:string, maxOccurs="1") — short description, complementing existing `plot`
- `userRating` (xs:decimal, maxOccurs="1")
- `keyword` (xs:string, maxOccurs="unbounded")

Place person elements after `actor` in the sequence. Place `outline` before `plot`. Place `userRating` after `rating`. Place `keyword` after `tag`.

File: Schemas/tvshow.xsd