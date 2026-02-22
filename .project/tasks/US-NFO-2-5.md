---
assignee: claude
created: '2026-02-22'
id: US-NFO-2-5
points: 2
status: done
story_id: US-NFO-2
title: Enhance subMediaType and refactor tvshow inline thumb/fanart
updated: '2026-02-22'
---

Add missing attributes to subMediaType in common.xsd so that tvshow.xsd can use it instead of defining inline complex types for thumb and fanart.

Attributes to add to subMediaType:
- `aspect` (xs:string, optional) — used by tvshow thumb for aspect ratio
- `season` (xs:integer, optional) — used by tvshow thumb for season-specific art
- `preview` (xs:string, optional) — used by tvshow thumb and fanart for preview URLs

After enhancement, subMediaType will have: type, width, height, url, extUrl, aspect, season, preview.

Then in tvshow.xsd:
- Replace inline thumb complexType (lines 32-43) with: `<xs:element name="thumb" type="subMediaType" minOccurs="0" maxOccurs="unbounded"/>`
- Replace inline fanart complexType (lines 44-52) with: `<xs:element name="fanart" type="subMediaType" minOccurs="0" maxOccurs="unbounded"/>`

Files: Schemas/common.xsd, Schemas/tvshow.xsd