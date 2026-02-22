---
acceptance_criteria:
- tvshow.xsd includes director/writer/composer person elements
- tvshow.xsd includes runtime and language elements
- tvshow.xsd includes outline for short descriptions
- tvshow.xsd includes country and productionCompany
created: '2026-02-22'
epic_id: EPIC-NFO-2
id: US-NFO-4
points: 3
priority: must
status: done
tags: []
title: Enhance tvshow.xsd with missing standard fields
updated: '2026-02-22'
---

As a TV show metadata consumer, I want the TV show schema to include all standard fields so that I can represent complete episode/series metadata.

Currently missing: director, writer, runtime/duration, language, outline (short description), country, productionCompany. Also missing: userrating, releasedate, award, subtitlelanguage. The tvshow schema should be on par with movie for completeness.