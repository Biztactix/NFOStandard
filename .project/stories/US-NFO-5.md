---
acceptance_criteria:
- video.xsd includes genre and language elements
- video.xsd includes duration element
- video.xsd supports multiple ratings and uniqueIds
- video.xsd includes banner and fanart image elements
created: '2026-02-22'
epic_id: EPIC-NFO-2
id: US-NFO-5
points: 2
priority: should
status: done
tags: []
title: Enhance video.xsd with missing standard fields
updated: '2026-02-22'
---

As a general video metadata consumer, I want a more complete video schema. Currently video.xsd is the most sparse schema with only 13 elements. It's missing: genre, language, duration, tags reuse subMediaType for banner/fanart (only has thumbnail), rating allowing multiple sources, and service links.