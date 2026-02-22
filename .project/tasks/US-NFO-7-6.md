---
assignee: claude
created: '2026-02-22'
id: US-NFO-7-6
points: 2
status: done
story_id: US-NFO-7
title: Create example XMLs for tvshow, anime, and video
updated: '2026-02-22'
---

Create 3 new example XML files with realistic data for the video-centric content types.

ExampleTVShow.xml:
- Use a well-known TV series (e.g. a specific episode). Include title, showTitle, season, episode, plot, outline, rating, actors, director, writer, genre, tags, premiered, studio, contentRating, uniqueId, thumb, fanart, banner.
- Include the new fields added in US-NFO-4 (runtime, language, country, productionCompany, etc.)

ExampleAnime.xml:
- Use a well-known anime series/episode. Include title, releaseDate, productionCompany, genre, language, season, episode, duration, director, voiceActor, description, outline, rating, uniqueId, contentRating, banner, thumb, fanart.
- Use boolean for isAdult (per US-NFO-6).

ExampleVideo.xml:
- Use a home video or general video scenario. Include title (post-rename from name), filmingDate, producer, people, genre, language, duration, description, rating, uniqueId, thumb, banner, fanart.

All files must use post-rename camelCase element names and the standard root/media wrapper.

Files: ExampleTVShow.xml, ExampleAnime.xml, ExampleVideo.xml
Depends on: US-NFO-1, US-NFO-4, US-NFO-5, US-NFO-6