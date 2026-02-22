---
assignee: claude
created: '2026-02-22'
id: US-NFO-3-4
points: 1
status: done
story_id: US-NFO-3
title: Document required/optional field policy in DECISIONS.md
updated: '2026-02-22'
---

Create the first architectural decision record documenting the required vs optional field policy.

Policy:
- Only `title` is required (minOccurs="1") at the content-type level across all media schemas
- All other fields are optional (minOccurs="0")
- Exception: `library.appID` stays required since it's an application identifier, not media metadata
- Exception: Within inline sub-types (e.g. serviceLinks service/url, personType name), required fields are allowed since they define structural integrity of the sub-type itself

Rationale: Lowering the required-field barrier makes the standard more adoptable for partial metadata use cases while still ensuring every entry has an identifier.

File: .project/DECISIONS.md (create via pm_update_doc)