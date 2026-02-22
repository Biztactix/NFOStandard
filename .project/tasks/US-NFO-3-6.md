---
assignee: claude
created: '2026-02-22'
id: US-NFO-3-6
points: 1
status: done
story_id: US-NFO-3
title: Relax required fields in anime, adult, video, audiobook, and podcast schemas
updated: '2026-02-22'
---

Change minOccurs from "1" to "0" for all non-title fields in the remaining 5 schemas. This task depends on US-NFO-1 completing the name→title rename in adult.xsd and video.xsd.

anime.xsd (2 fields):
- `releaseDate` (line 13): minOccurs="1" → "0"
- `productionCompany` (line 14): minOccurs="1" → "0"

adult.xsd (1 field — after name→title rename):
- `releaseDate` (line 13): minOccurs="1" → "0"

video.xsd (2 fields — after name→title rename):
- `filmingDate` (line 13): minOccurs="1" → "0"
- `producer` (line 14): minOccurs="1" → "0"

audiobook.xsd (3 fields):
- `releaseDate` (line 13): minOccurs="1" → "0"
- `productionCompany` (line 14): minOccurs="1" → "0"
- `writer` (line 19): minOccurs="1" → "0"

podcast.xsd (3 fields):
- `releaseDate` (line 14): minOccurs="1" → "0"
- `productionCompany` (line 15): minOccurs="1" → "0"
- `host` (line 16): minOccurs="1" → "0"

Files: Schemas/anime.xsd, Schemas/adult.xsd, Schemas/video.xsd, Schemas/audiobook.xsd, Schemas/podcast.xsd