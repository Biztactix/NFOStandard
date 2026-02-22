---
acceptance_criteria:
- serviceLinksType defined in common.xsd and used by music/musicvideo/podcast
- tvshow thumb and fanart use subMediaType from common.xsd (with any needed attribute
  additions)
- No inline complex types duplicated across schemas
created: '2026-02-22'
epic_id: EPIC-NFO-1
id: US-NFO-2
points: 3
priority: must
status: done
tags: []
title: Extract shared inline types to common.xsd
updated: '2026-02-22'
---

As a schema maintainer, I want shared types defined once in common.xsd so that changes propagate consistently.

Currently `serviceLinks` is defined as an identical inline complexType in music.xsd, musicvideo.xsd, and podcast.xsd. The tvshow.xsd defines custom inline types for `thumb` and `fanart` instead of using `subMediaType` from common.xsd. These should all use shared types.