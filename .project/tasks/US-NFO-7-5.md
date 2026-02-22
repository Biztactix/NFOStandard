---
assignee: claude
created: '2026-02-22'
id: US-NFO-7-5
points: 1
status: done
story_id: US-NFO-7
title: Rewrite SamplePodcast.xml with realistic data
updated: '2026-02-22'
---

Replace the current SamplePodcast.xml which uses placeholder "string" values and negative duration (-4020) with a realistic podcast example.

Use a well-known podcast as the basis (e.g. a tech or science podcast). Include:
- Realistic title, releaseDate, productionCompany
- Named hosts with real-looking bios and URLs
- Named guests
- Realistic duration, language, genre, keywords, tags
- Proper rating values
- Real-looking uniqueId entries (e.g. Apple Podcasts ID, Spotify ID)
- Realistic contentRating
- Cover image URL
- serviceLinks (Spotify, Apple Podcasts, etc.)

Use post-rename element names (camelCase from US-NFO-1). Follow the same root/media/podcast structure as current file.

File: SamplePodcast.xml
Depends on: US-NFO-1 (naming), US-NFO-3 (required fields)