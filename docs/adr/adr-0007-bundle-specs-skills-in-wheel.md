---
id: ADR-0007
title: Bundle default specs/skills into the wheel, working directory wins
type: adr
status: accepted
date: 2026-07-04
deciders: [Lila Brooks]
tags: [packaging, resources, pipx]
related: [ADR-0004, ADR-0005]
---

# ADR-0007: Bundle Default Specs/Skills into the Wheel, Working Directory Wins

## Context

Before 0.2.0, spec and skill commands resolved `specs/cli` and `skills/agent` relative to the working directory only. Installed via pipx and run from anywhere else, `agent spec list` found nothing and `agent build` could not even attach its own file-output contract — the package's core inputs were not shipped with the package.

## Decision

Ship the repo's `specs/` and `skills/` trees inside the wheel (hatchling `force-include` → `agent_cli/_bundled/`), and resolve the active root in `resources.py` with a two-step rule: a working-directory `specs/cli`/`skills/agent` containing at least one `.md` file takes precedence; otherwise the bundled copy is used. An empty local folder does not shadow the bundle, and if neither location has Markdown the cwd path is returned so listings degrade to "No specs found" instead of crashing.

## Consequences

- `agent spec`, `agent skill`, and `build`'s automatic contract attachment work from any directory after `pip`/`pipx` install.
- A checkout still sees its own files immediately — editing a spec needs no reinstall — and any downstream project can override the defaults by creating the same folder layout.
- Editable installs get no `_bundled/` copy (no wheel is built), so slug resolution outside the checkout silently degrades; documented in the README rather than worked around in code.
- The wheel carries content that is not importable Python, and the bundled copy snapshots the trees at build time — stale until the next release.
