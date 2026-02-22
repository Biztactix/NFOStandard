---
acceptance_criteria:
- Documented policy for required vs optional fields
- All schemas follow the agreed policy
- No schema requires more than 2-3 fields
created: '2026-02-22'
epic_id: EPIC-NFO-1
id: US-NFO-3
points: 3
priority: should
status: done
tags: []
title: Standardize required vs optional field patterns
updated: '2026-02-22'
---

As a schema consumer, I want predictable required/optional patterns so I know what to expect across content types.

Current inconsistencies:
- movie: only `title` required
- anime: `title`, `releaseDate`, `productionCompany` required
- music: `title`, `releaseDate`, `productionCompany`, `producer`, `writer`, `artist` required (6 fields!)
- video: `name`, `filmingDate`, `producer` required

Propose a consistent baseline: `title` always required, everything else optional unless there's a strong semantic reason.