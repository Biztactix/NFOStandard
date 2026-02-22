#!/usr/bin/env python3
"""
Test: GitHub Actions workflow runs on push and PR.

Verifies acceptance criterion for US-NFO-9:
  "GitHub Actions workflow runs on push and PR"

Checks that a GitHub Actions workflow YAML exists under
.github/workflows/ and is configured with push and
pull_request triggers.
"""

import glob
import os

import pytest
import yaml

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
WORKFLOWS_DIR = os.path.join(REPO_ROOT, ".github", "workflows")


def find_workflow_files():
    """Find all YAML workflow files in .github/workflows/."""
    patterns = [
        os.path.join(WORKFLOWS_DIR, "*.yml"),
        os.path.join(WORKFLOWS_DIR, "*.yaml"),
    ]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))
    return sorted(files)


def load_workflow(path):
    """Load and parse a workflow YAML file."""
    with open(path) as f:
        return yaml.safe_load(f)


def test_workflow_files_exist():
    """At least one GitHub Actions workflow file must exist."""
    files = find_workflow_files()
    assert len(files) > 0, (
        f"No workflow files found in {WORKFLOWS_DIR}. "
        "Expected at least one .yml or .yaml file."
    )


def test_workflow_triggers_push_and_pr():
    """At least one workflow must trigger on both push and pull_request."""
    files = find_workflow_files()
    if not files:
        pytest.skip("No workflow files found")

    has_push = False
    has_pr = False

    for wf_path in files:
        doc = load_workflow(wf_path)
        if not isinstance(doc, dict):
            continue
        triggers = doc.get(True) or doc.get("on") or {}
        if isinstance(triggers, list):
            if "push" in triggers:
                has_push = True
            if "pull_request" in triggers:
                has_pr = True
        elif isinstance(triggers, dict):
            if "push" in triggers:
                has_push = True
            if "pull_request" in triggers:
                has_pr = True

    assert has_push, (
        "No workflow triggers on 'push'. "
        "At least one workflow in .github/workflows/ must include 'push' in its 'on' triggers."
    )
    assert has_pr, (
        "No workflow triggers on 'pull_request'. "
        "At least one workflow in .github/workflows/ must include 'pull_request' in its 'on' triggers."
    )
