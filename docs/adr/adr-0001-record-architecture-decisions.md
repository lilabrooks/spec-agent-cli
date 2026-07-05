---
id: ADR-0001
title: Record architecture decisions as ADRs
type: adr
status: accepted
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [process, documentation]
related: []
---

# ADR-0001: Record Architecture Decisions as ADRs

## Context

The project's design rationale lived in `docs/architecture.md`, the README, and commit messages. That captures the current shape well but not *why* it is shaped that way, or what was traded away. As the codebase grows past a starter scaffold, decisions made early (stdlib-only, Markdown parsing by hand, plain-text file contracts) will look questionable without their context attached.

## Decision

Keep one Markdown file per significant architectural decision under `docs/adr/`, numbered sequentially. Every file starts with a YAML frontmatter block carrying `id`, `title`, `type: adr`, `status` (`proposed` | `accepted` | `deprecated` | `superseded`), `date`, `owner`, `deciders`, `tags`, and `related`, followed by Context, Decision, and Consequences sections. A superseding ADR gets a new number; the old one changes status rather than being rewritten.

## Consequences

- Rationale survives independently of the people who made the call; ADR-0002 through ADR-0009 backfill the decisions already embodied in the code.
- The frontmatter is machine-readable, so future tooling (including this project's own Markdown loader) can index the records.
- Slight upkeep cost: a decision that changes needs a new record, not a silent edit.
