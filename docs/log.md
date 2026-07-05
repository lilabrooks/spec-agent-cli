---
title: Documentation log
type: log
status: current
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, log]
---

# Documentation log

Dated changes to the docs bundle, newest first.

## 2026-07-05

- Documented the root `requirements.txt` as a Snyk-friendly scan manifest that mirrors optional and development dependencies from `pyproject.toml`, including the decision record in ADR-0004.
- Added a static README OKF docs validated badge that links to the quality standard section.
- Added OKF docs validation to `make check`, `make check-all`, and the code-quality workflow, and recorded the decision in ADR-0010.

## 2026-07-04

- Adopted the bundle layout: `index.md` at the bundle root and in `specs/` and `adr/`, plus this `log.md`.
- Moved the pipx artifact guide and the my-cli generator test guide into `guides/`.
- Moved `skill-research.md` into `notes/`.
- Replaced `architecture.md` with `contributing.md`. Component behavior moved to `specs/`, decision rationale to `adr/`.
- Added component specifications SPEC-000 through SPEC-008 with an index.
- Added architecture decision records ADR-0001 through ADR-0009 with an index.

## 2026-07-02

- Updated the spec-agent CLI flow diagram in `assets/`.
- Added the pipx artifact guide and the my-cli generator test guide.
- Added `architecture.md` in the initial commit.
