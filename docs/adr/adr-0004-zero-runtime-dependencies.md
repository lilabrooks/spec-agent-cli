---
id: ADR-0004
title: Zero runtime dependencies; provider SDKs as optional extras with deferred imports
type: adr
status: accepted
date: 2026-07-04
deciders: [Lila Brooks]
tags: [dependencies, packaging]
related: [ADR-0003, ADR-0005]
---

# ADR-0004: Zero Runtime Dependencies; Provider SDKs as Optional Extras with Deferred Imports

## Context

A scaffold that people install via pipx and fork for their own tools should be cheap to install, quick to audit, and free of dependency churn. But the two real provider adapters need vendor SDKs, and pulling both `anthropic` and `openai` into every install would contradict the vendor-neutral premise.

## Decision

- `[project] dependencies` stays empty: the runtime is stdlib-only (argparse, dataclasses, pathlib, importlib.resources). Development tooling lives in the `dev` extra.
- Vendor SDKs are opt-in extras: `pip install ".[anthropic]"` or `".[openai]"`.
- Adapter modules import their SDK **inside `complete()`**, not at module top, so `providers/registry.py` can import every adapter unconditionally and `agent providers`, `run --provider echo`, and all tests work with neither SDK installed. mypy overrides mark both modules `ignore_missing_imports`.
- API keys are never read by this package; each SDK picks up its own `*_API_KEY` from the environment when instantiated.

## Consequences

- Out of the box the CLI runs with no network, no credentials, and nothing to `pip`-resolve; the echo provider exercises the full pipeline.
- A missing SDK only surfaces when that provider is actually invoked — the failure is late but precisely scoped to the user's choice.
- Runtime code must stay within stdlib capabilities unless a spec justifies a dependency (this is written into the project's quality standard), which drove the hand-rolled Markdown parsing in ADR-0005.
- Provider tests fake the SDK modules rather than importing them, keeping CI dependency-free too.
