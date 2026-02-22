---
assignee: claude
created: '2026-02-22'
id: US-NFO-3-5
points: 2
status: done
story_id: US-NFO-3
title: Relax required fields in music.xsd and musicvideo.xsd
updated: '2026-02-22'
---

Change minOccurs from "1" to "0" for all non-title fields in music.xsd and musicvideo.xsd.

music.xsd changes (6 fields to relax):
- `artist` (xs:string, line 13): minOccurs="1" → "0"
- `releaseDate` (line 23): minOccurs="1" → "0"
- `productionCompany` (line 36): minOccurs="1" → "0"
- `producer` (line 37): minOccurs="1" → "0"
- `writer` (line 38): minOccurs="1" → "0"
- `artist` (personType, line 39): minOccurs="1" → "0"

Also in albumType (inline):
- `artist` (line 13): minOccurs="1" → "0" (keep title and position required within album sub-type)

musicvideo.xsd changes (5 fields to relax):
- `releaseDate` (line 13): minOccurs="1" → "0"
- `productionCompany` (line 14): minOccurs="1" → "0"
- `producer` (line 15): minOccurs="1" → "0"
- `writer` (line 16): minOccurs="1" → "0"
- `artist` (line 17): minOccurs="1" → "0"

Files: Schemas/music.xsd, Schemas/musicvideo.xsd