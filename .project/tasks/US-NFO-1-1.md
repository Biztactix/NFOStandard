---
assignee: claude
created: '2026-02-22'
id: US-NFO-1-1
points: 2
status: done
story_id: US-NFO-1
title: 'Test: All element names use consistent camelCase convention'
updated: '2026-02-22'
---

## Verification Results

**Test result: FAIL** — 26 element names across 5 schema files do not follow camelCase convention.

### Violations by file:

**movie.xsd (12):** `originaltitle`, `sorttitle`, `alternatetitle`, `userrating`, `contentrating`, `uniqueid`, `setname`, `setoverview`, `productioncompany`, `releasedate`, `subtitlelanguage`, `parentalguide`

**tvshow.xsd (6):** `originaltitle`, `showtitle`, `sorttitle`, `contentrating`, `uniqueid`, `namedseason`

**adult.xsd (2):** `VideoURL`, `TrailerURL` (PascalCase instead of camelCase)

**music.xsd (2):** `uniqueid` in albumType, `uniqueid` in inline album element

**library.xsd (4):** `appID`, `uniqueid`, `libraryid`, `librarysubid`

### Passing schemas:
common.xsd, anime.xsd, video.xsd, musicvideo.xsd, podcast.xsd, audiobook.xsd, person.xsd

Implementation tasks US-NFO-1-6, US-NFO-1-7, US-NFO-1-8 need to complete to resolve these violations. Note: music.xsd and library.xsd violations are not covered by existing implementation tasks.