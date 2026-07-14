---
id: ADR-0011
title: Install provider SDKs in code-quality CI
type: adr
status: accepted
date: 2026-07-14
owner: Lila Brooks
deciders: [Lila Brooks]
description: Install optional provider SDKs in code-quality CI so strict mypy checks SDK-facing types.
tags: [dependencies, ci, mypy, providers]
related: [ADR-0004, SPEC-003, SPEC-008]
supersedes: ADR-0004 (CI dependency-free consequence only)
---

# ADR-0011: Install Provider SDKs in Code-Quality CI

## Context

ADR-0004 keeps the shipped package free of runtime dependencies and makes the Anthropic and
OpenAI SDKs optional extras. It also expected CI to remain free of those SDKs and configured mypy
to ignore missing top-level provider imports.

The provider adapters now use SDK type modules under `TYPE_CHECKING`, including
`openai.types.chat` and `anthropic.types`. The code-quality workflow installs only `.[dev]`, so
strict mypy fails on every supported Python version before it can check the SDK-facing request
shapes. Runtime tests still pass because the imports are deferred.

## Decision

The code-quality workflow installs `.[dev,anthropic,openai]` before running ruff, mypy, and the OKF
docs check. This supersedes ADR-0004 only where it says CI remains free of provider SDKs. The
package's `[project] dependencies` stays empty, provider SDKs remain optional install extras, and
runtime imports remain deferred inside each adapter.

## Alternatives considered

- Expand mypy's missing-import override to `anthropic.*` and `openai.*`. This would make CI green
  without checking the SDK type modules used by the adapters.
- Replace SDK types with local structural types. This would duplicate vendor contracts and could
  drift when the SDKs change.
- Remove the SDK type annotations. This would weaken strict checking at the provider boundary that
  most benefits from concrete request types.

## Consequences

- Code-quality CI can resolve and check the provider SDK types on Python 3.12, 3.13, and 3.14.
- CI installs more packages and depends on the provider packages being resolvable from PyPI.
- Normal and pipx installs remain dependency-free unless a provider extra is selected.
- Changes to provider extras in `pyproject.toml` must remain compatible with the CI install and the
  scanner mirror in `requirements.txt`.

## Rollback / revisit trigger

Revisit this decision if provider SDK resolution makes CI unreliable, if an SDK drops a supported
Python version, or if stable local structural types can check the same boundary without duplicating
vendor contracts. Rollback means restoring the `.[dev]` CI install and adding an explicit,
documented mypy strategy for every optional SDK submodule.
