---
assignee: null
created: '2026-02-22'
id: US-NFO-1-6
points: 3
status: done
story_id: US-NFO-1
title: Rename movie.xsd elements to camelCase
updated: '2026-02-22'
---

Rename 12 elements in movie.xsd from lowercase to camelCase to match the convention used in all other schemas.

Renames:
- `originaltitle` → `originalTitle`
- `sorttitle` → `sortTitle`
- `alternatetitle` → `alternateTitle`
- `userrating` → `userRating`
- `contentrating` → `contentRating`
- `uniqueid` → `uniqueId`
- `setname` → `setName`
- `setoverview` → `setOverview`
- `productioncompany` → `productionCompany`
- `releasedate` → `releaseDate`
- `subtitlelanguage` → `subtitleLanguage`
- `parentalguide` → `parentalGuide`

File: Schemas/movie.xsd