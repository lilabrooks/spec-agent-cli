---
title: Contributing guide
type: guide
status: current
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, contributing]
---

# Contributing

How to extend this codebase and the quality bar for changes. For why the architecture looks this way, see [adr/](adr/index.md). For how each shipped component behaves, see [specs/](specs/index.md) in this folder.

## Architecture in one screen

The project uses a thin hexagonal shape ([ADR-0002](adr/adr-0002-hexagonal-architecture.md)):

- `cli.py` owns terminal input and output.
- `agents/` owns task behavior.
- `core/` owns contracts and shared Markdown parsing.
- `providers/` owns model-specific adapters.
- `skills/` owns Markdown skill loading and validation.
- `specs/` owns Markdown spec loading and validation.
- `runtime/` wires concrete implementations together.

Keep imports flowing inward. Provider modules can import core contracts, but core modules should never import a provider.

## Adding a provider

1. Create a module under `src/agent_cli/providers/`.
2. Implement `LanguageModel` ([SPEC-003](specs/spec-003-provider-adapters.md)).
3. Register it in `providers/registry.py`. The factory, the unknown-provider error, and the `providers` command all read from that registry.
4. Add focused tests for request mapping, response mapping, and error handling.

Provider configuration should stay in `config/settings.py` or in provider-owned config types. Avoid reading environment variables deep inside agent code.

## Quality standard

Tests use pytest. New tests should be function-based and use fixtures such as `tmp_path`, `capsys`, and `monkeypatch` instead of `unittest` classes.

Ruff owns linting, import sorting, and formatting. The configured rule set favors modern Python, simple returns, pathlib, no stray print debugging, and no unused arguments or imports.

mypy runs in strict mode against the package. Public functions should have typed signatures, and the package includes `py.typed` so type checkers can inspect it after installation.

Repo-level invariants (version consistency everywhere it appears, document validity, quality gates) are enforced by `tests/test_repo_health.py` and specified in [SPEC-008](specs/spec-008-repository-health.md).

`pyproject.toml` is the dependency source of truth. The root `requirements.txt` exists so GitHub-based dependency scanners such as Snyk can inspect the optional provider SDKs and development tools with a standard pip manifest. Keep it synchronized with `[project.optional-dependencies]`, but keep normal development installs on `pip install -e ".[dev]"`.

## Where behavior is specified

Details that used to live in this file are now specified per component:

- Markdown parsing, spec and skill documents, required sections: [SPEC-005](specs/spec-005-markdown-document-system.md)
- `agent build`, the `FILE:` contract, safe writes, `--strict` validation: [SPEC-006](specs/spec-006-build-file-output.md)
- Working with agent skills: [skills/README.md](../skills/README.md)
- Writing CLI feature specs: the repo-root [specs/README.md](../specs/README.md)
