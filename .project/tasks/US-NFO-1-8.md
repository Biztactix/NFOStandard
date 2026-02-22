---
assignee: null
created: '2026-02-22'
id: US-NFO-1-8
points: 2
status: done
story_id: US-NFO-1
title: Rename adult.xsd and video.xsd identifiers
updated: '2026-02-22'
---

Standardize primary identifiers and fix casing in adult.xsd and video.xsd.

adult.xsd:
- `name` → `title` (match all other schemas)
- `VideoURL` → `videoUrl` (fix PascalCase to camelCase)
- `TrailerURL` → `trailerUrl` (fix PascalCase to camelCase)

video.xsd:
- `name` → `title` (match all other schemas)

Files: Schemas/adult.xsd, Schemas/video.xsd