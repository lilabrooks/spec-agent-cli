---
id: SPEC-007
title: Resource resolution
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
components:
  - src/agent_cli/resources.py
  - pyproject.toml
tags: [packaging, resources, pipx]
related: [SPEC-005]
---

# Resource Resolution

## Purpose

Make `agent spec`/`agent skill` work from any directory after a `pip`/`pipx` install, while a checkout (or any project with its own spec/skill folders) still sees its local files first.

## Behavior

`resources.py` resolves the default roots used everywhere a `--root`/`--spec`/`--skill` value is not an explicit existing path:

1. If `specs/cli` (respectively `skills/agent`) exists under the current working directory **and contains at least one `.md` file**, it wins. An empty local folder does not shadow the bundled defaults.
2. Otherwise the copy bundled inside the installed package at `agent_cli/_bundled/specs/cli` (respectively `_bundled/skills/agent`) is used.
3. If neither has Markdown (e.g. an editable install run outside the checkout), the cwd-relative path is returned anyway and downstream listing yields "No specs/skills found" rather than a crash.

The bundling itself is a hatchling `force-include` in `pyproject.toml` that copies the repo's `specs/` and `skills/` trees into the wheel under `agent_cli/_bundled/`.

## Constraints

- Editable installs (`pip install -e`) never build a wheel, so `_bundled/` does not exist; slug resolution and `agent build`'s automatic `file-output-contract` attachment then only work when the current directory is inside the checkout. This is documented in the README's Development Setup note.
- Explicit file paths bypass root resolution entirely — `resolve_markdown` checks the literal path before consulting any root (SPEC-005).

## Acceptance tests

`tests/test_resources.py` covers cwd precedence, the bundled fallback, and the empty-local-folder case.
