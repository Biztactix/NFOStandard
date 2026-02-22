---
acceptance_criteria:
- Validation script exists that checks all XSD files compile
- Validation script validates all example XMLs against schemas
- GitHub Actions workflow runs on push and PR
- README includes local validation instructions
created: '2026-02-22'
epic_id: EPIC-NFO-4
id: US-NFO-9
points: 5
priority: should
status: done
tags: []
title: Add XML schema validation script and GitHub Actions CI
updated: '2026-02-22'
---

As a contributor, I want automated validation so that schema changes are tested before merge.

Should include:
1. A validation script that compiles all XSD files and validates example XMLs against them
2. A GitHub Actions workflow that runs validation on push/PR
3. Local validation instructions in README or CONTRIBUTING.md