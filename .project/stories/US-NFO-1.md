---
acceptance_criteria:
- All element names use consistent camelCase convention
- movie.xsd elements renamed to match other schemas
- adult.xsd and video.xsd primary identifier standardized
- ExampleMovie.xml updated to match renamed elements
- README example updated to match renamed elements
created: '2026-02-22'
epic_id: EPIC-NFO-1
id: US-NFO-1
points: 5
priority: must
status: done
tags: []
title: Standardize element naming to camelCase across all schemas
updated: '2026-02-22'
---

As a schema consumer, I want consistent element naming so that I don't have to handle different casing conventions per content type.

Currently movie.xsd uses lowercase (`releasedate`, `uniqueid`, `contentrating`, `productioncompany`) while all other schemas use camelCase (`releaseDate`, `uniqueId`, `contentRating`, `productionCompany`). Movie is the outlier — standardize it to match the others.

Also standardize the primary identifier: adult.xsd and video.xsd use `name` while all others use `title`. Pick one convention.