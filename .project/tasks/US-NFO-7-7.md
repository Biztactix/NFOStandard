---
assignee: claude
created: '2026-02-22'
id: US-NFO-7-7
points: 2
status: done
story_id: US-NFO-7
title: Create example XMLs for music, musicvideo, audiobook, and adult
updated: '2026-02-22'
---

Create 4 new example XML files with realistic data for the remaining content types.

ExampleMusic.xml:
- Use a well-known song/track. Include title, releaseDate, album (with title, position, artist, cover), productionCompany, producer, writer, artist, genre, duration, language, description, rating, uniqueId, contentRating, cover, serviceLinks.

ExampleMusicVideo.xml:
- Use a well-known music video. Include title, releaseDate, productionCompany, producer, writer, artist, genre, duration, language, description, rating, uniqueId, contentRating, cover, serviceLinks.

ExampleAudiobook.xml:
- Use a well-known audiobook. Include title, releaseDate, productionCompany, isbn, duration, language, genre, writer, voiceActor, description, rating, uniqueId, contentRating, cover.

ExampleAdult.xml:
- Use generic/fictional data. Include title (post-rename from name), releaseDate, productionCompany, siteName, videoUrl, trailerUrl, duration, director, performer, genre, language, description, rating, uniqueId, contentRating, thumb, banner, fanart.

All files must use post-rename camelCase element names and the standard root/media wrapper.

Files: ExampleMusic.xml, ExampleMusicVideo.xml, ExampleAudiobook.xml, ExampleAdult.xml
Depends on: US-NFO-1, US-NFO-2, US-NFO-3, US-NFO-6