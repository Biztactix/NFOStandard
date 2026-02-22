---
acceptance_criteria:
- anime.xsd includes plot and outline distinction
- anime.xsd isAdult changed from integer to boolean
- adult.xsd includes genre and language elements
- adult.xsd includes banner and fanart image elements
created: '2026-02-22'
epic_id: EPIC-NFO-2
id: US-NFO-6
points: 3
priority: should
status: done
tags: []
title: Enhance anime.xsd and adult.xsd with missing fields
updated: '2026-02-22'
---

As a metadata consumer, I want anime and adult schemas to have comparable depth to other schemas.

Anime is missing: outline/plot distinction, tagline, userrating, country, subtitle languages, soundtrack.
Adult is missing: genre, language, contentRating, banner/fanart images (only has thumbnail).

Also: anime uses `isAdult` as xs:integer — should be xs:boolean.