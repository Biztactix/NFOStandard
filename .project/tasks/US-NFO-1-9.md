---
assignee: null
created: '2026-02-22'
id: US-NFO-1-9
points: 1
status: done
story_id: US-NFO-1
title: Update ExampleMovie.xml to match camelCase renames
updated: '2026-02-22'
---

Update all element names in ExampleMovie.xml to match the camelCase renames applied to movie.xsd.

Elements to rename in the XML:
- `<originaltitle>` → `<originalTitle>`
- `<sorttitle>` → `<sortTitle>`
- `<alternatetitle>` → `<alternateTitle>`
- `<userrating>` → `<userRating>`
- `<contentrating>` → `<contentRating>`
- `<uniqueid>` → `<uniqueId>`
- `<setname>` → `<setName>`
- `<setoverview>` → `<setOverview>`
- `<productioncompany>` → `<productionCompany>`
- `<releasedate>` → `<releaseDate>`
- `<subtitlelanguage>` → `<subtitleLanguage>`
- `<parentalguide>` → `<parentalGuide>`

Both opening and closing tags must be renamed.

File: ExampleMovie.xml