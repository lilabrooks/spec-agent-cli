---
id: ADR-0010
title: Validate OKF docs with a repo-local stdlib script
type: adr
status: accepted
date: 2026-07-05
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, okf, validation]
related: [ADR-0004, ADR-0005]
---

# ADR-0010: Validate OKF Docs with a Repo-Local Stdlib Script

## Context

The repository now uses an OKF-style docs bundle under `docs/` plus buildable spec and skill documents under repo-root `specs/` and `skills/`. Those files are easy to drift: a new document can miss `owner`, `deciders`, `type`, `okf_version`, or a local link target while the package tests still pass.

The runtime Markdown loader deliberately stays tiny per ADR-0005. It parses flat metadata as strings for agent context and should not grow a YAML dependency just to police repository documentation.

## Decision

Add `scripts/check-okf-docs.py`, a repo-local, standard-library validation script. It runs as part of `make check`, `make check-all`, and the code-quality workflow.

The script validates repository documentation rather than runtime behavior:

- required OKF bundle files exist: `docs/index.md`, `docs/log.md`, `docs/specs/index.md`, and `docs/adr/index.md`
- `docs/index.md` declares `okf_version`
- tracked Markdown frontmatter under `docs/`, `specs/`, and `skills/` has a non-empty `owner`
- `deciders` is a non-empty list
- tracked Markdown files under `docs/` with frontmatter have a non-empty `type`
- local Markdown links under `docs/`, `specs/`, and `skills/` resolve inside the repo

The validator implements only the metadata subset this repo uses: scalar fields, inline lists, and simple block lists. It does not replace the runtime Markdown parser in `agent_cli.core.markdown`.

## Consequences

Documentation drift fails the same everyday quality command as lint, type-checking, and tests.

The package keeps zero runtime dependencies because OKF validation lives in a repo script, not application code.

The validator is intentionally conservative. If the docs start using richer YAML, this ADR should be superseded before adding a full YAML parser or external dependency.
