---
id: ADR-0002
title: Thin hexagonal architecture with inward-only imports
type: adr
status: accepted
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [architecture, layering]
related: [ADR-0003]
---

# ADR-0002: Thin Hexagonal Architecture with Inward-Only Imports

## Context

The CLI must stay useful across model vendors that change quickly, and its logic (spec parsing, prompt assembly, file writing) should be testable without a terminal, network, or API key. A flat script would couple argparse, vendor SDKs, and file I/O together; a full ports-and-adapters framework would be overkill for ~1,000 lines of code.

## Decision

Use a thin hexagonal layout with a single import rule — imports flow inward only:

- `core/` holds contracts and shared types (`Message`, `CompletionRequest/Response`, `LanguageModel`, Markdown parsing, `fileset`) and imports nothing from the outer rings.
- `agents/`, `specs/`, `skills/` build on core.
- `providers/` are adapters that import core contracts; core never imports a provider.
- `cli.py` is the only module touching argparse and stdout/stderr; `config/settings.py` is the only module reading the environment.
- `runtime/factory.py` is the composition root where concrete implementations are wired together.

## Consequences

- Every layer below `cli.py` is plain functions and frozen dataclasses, tested directly without subprocesses or mocking frameworks.
- Swapping or adding a vendor cannot ripple into agent or CLI code (see ADR-0003).
- The rule is enforced by convention and review, not tooling — an import-linter contract would make it mechanical if the project grows.
- Small indirection cost: trivial features touch two or three files (parser wiring in `cli.py`, logic in an inner module) instead of one.
