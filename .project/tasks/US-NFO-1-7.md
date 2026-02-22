---
assignee: claude
created: '2026-02-22'
id: US-NFO-1-7
points: 2
status: done
story_id: US-NFO-1
title: Rename tvshow.xsd elements to camelCase
updated: '2026-02-22'
---

Rename 7 elements and 2 attributes in tvshow.xsd from lowercase to camelCase.

Element renames:
- `originaltitle` → `originalTitle`
- `showtitle` → `showTitle`
- `sorttitle` → `sortTitle`
- `contentrating` → `contentRating`
- `uniqueid` → `uniqueId`
- `altorder` → `altOrder`
- `namedseason` → `namedSeason`

Attribute renames (on altOrder):
- `altseason` → `altSeason`
- `altepisode` → `altEpisode`

File: Schemas/tvshow.xsd