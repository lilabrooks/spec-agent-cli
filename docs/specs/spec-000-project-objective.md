---
id: SPEC-000
title: Project objective and scope
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
components:
  - README.md
  - pyproject.toml
tags: [objective, scope, non-goals]
related: [SPEC-001, SPEC-002, SPEC-003, SPEC-004, SPEC-005, SPEC-006, SPEC-007]
---

# Project Objective and Scope

## Objective

Dogfood [claude-okf-repo-kit](https://github.com/lilabrooks/claude-okf-repo-kit) through a working Python CLI project, and provide the proven chassis for a new template based on that kit, focused specifically on creating Python CLI apps. The `agent` CLI is the current chassis: humans write specs, agents receive normalized context shaped by reusable skills, and the Python code handles loading, validation, and provider-neutral execution.

## Target user

The kit maintainer and template author. They use this repo to exercise the kit and shape a Python CLI template from a working project.

## Core promises

These are the properties the project treats as contractual. Breaking any of them is a design change, not a refactor:

1. **Vendor-neutral.** Application code depends only on the one-method `LanguageModel` protocol; vendors are adapters behind a registry, swappable per invocation with `--provider` or `AGENT_CLI_PROVIDER` (SPEC-002, SPEC-003).
2. **Works offline and credential-free out of the box.** The default `echo` provider exercises the full pipeline with no network, no API key, and nothing beyond the standard library installed (SPEC-003, SPEC-004).
3. **Zero runtime dependencies.** `[project] dependencies` stays empty; vendor SDKs are opt-in extras whose imports are deferred until that provider actually runs (ADR-0004).
4. **Specs are plain Markdown, usable from anywhere on disk.** `--spec` accepts any path, not just `specs/cli/` slugs, and validation warns before a real model call is spent — failing fast only under `--strict` (SPEC-005, SPEC-006).
5. **Safe writes.** `agent build` previews its plan by default, never overwrites without `--force`, and never lets generated paths escape `--out-dir` (SPEC-006, ADR-0009).
6. **Installable as a real tool.** `pip`/`pipx` installs work from any directory because the default specs and skills ship inside the wheel (SPEC-007).
7. **Strict quality floor.** mypy `strict`, the configured ruff rule set, pytest with a 70% branch-coverage floor, CI across Python 3.12–3.14.

## Scope

- The `agent` command surface: `run`, `build`, `spec`, `skill`, `providers` (SPEC-001).
- Markdown spec and skill loading, validation, and rendering into agent context (SPEC-005).
- Provider adapters for Anthropic, OpenAI, and the local echo stub (SPEC-003).
- Single-shot prompt → reply → optional file-write flows; the `my-cli` fixture as an end-to-end proof of the generation pattern.

## Non-goals

- **No conversation state.** The agent is stateless per invocation; there is no history, memory, or multi-turn session.
- **No streaming, tool use, or structured-output APIs.** The provider contract is one blocking text completion (ADR-0003); file generation rides on the plain-text `FILE:` contract instead (ADR-0006).
- **No plugin discovery.** New providers are added by editing the registry in a fork, not via entry points.
- **No config files or `.env` loading.** Environment variables and flags only (ADR-0008).
- **No agentic loop.** `build` makes exactly one model call; it does not iterate, self-correct, run generated tests, or retry.
- **Not a hosted service or IDE integration.** It is a local CLI, full stop.

## Acceptance criteria

The objective is met when, on a clean machine with only Python 3.12+:

- `pipx install` from the repo followed by `agent providers` and `agent run "hello"` succeeds with no credentials or network.
- Pointing `agent build --spec <any-path>.md --apply --out-dir <dir>` at a valid spec, with a real provider configured, writes the generated files under `<dir>` and refuses to overwrite existing ones without `--force`.
- `make check` passes: lint, strict type-check, and tests with the coverage floor.
