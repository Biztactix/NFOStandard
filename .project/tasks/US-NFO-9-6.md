---
assignee: claude
created: '2026-02-22'
id: US-NFO-9-6
points: 2
status: done
story_id: US-NFO-9
title: Create GitHub Actions workflow and add README validation instructions
updated: '2026-02-22'
---

Create a CI workflow and document local validation usage.

**.github/workflows/validate.yml** — GitHub Actions workflow:
- Trigger: push to main, pull requests to main
- Runner: ubuntu-latest
- Steps:
  1. Checkout repository
  2. Install libxml2-utils (`sudo apt-get install -y libxml2-utils`)
  3. Make validate.sh executable
  4. Run `./validate.sh`
- Name: "Validate Schemas"

**README.md update** — Add a "Validation" section (before Contributing):
- Prerequisites: `libxml2-utils` (install command for Ubuntu/macOS)
- How to run: `./validate.sh`
- What it checks: XSD well-formedness + example XML schema validation
- Note about CI running automatically on PRs

Files: .github/workflows/validate.yml, README.md
Depends on: US-NFO-9 task 1 (validate.sh must exist)