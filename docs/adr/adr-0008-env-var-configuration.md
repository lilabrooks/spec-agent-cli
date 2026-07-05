---
id: ADR-0008
title: Environment-variable-only configuration, no .env auto-loading
type: adr
status: accepted
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [configuration, environment]
related: [ADR-0002, ADR-0004]
---

# ADR-0008: Environment-Variable-Only Configuration, No `.env` Auto-Loading

## Context

The CLI needs a handful of runtime knobs (provider, model, system prompt) and the vendor SDKs need API keys. Config files, `.env` auto-loading, or a settings command would each add state whose origin is hard to see; an early `.env.example` in the repo implied auto-loading the project never performed, and was actively misleading.

## Decision

Configuration is read from the process environment only, in exactly one place (`Settings.from_env`): `AGENT_CLI_PROVIDER`, `AGENT_CLI_MODEL`, `AGENT_CLI_SYSTEM_PROMPT`, each with a sensible default (`echo`, adapter default, generic assistant prompt). Precedence for the provider is flag → env var → default; model and system prompt are env-only. There is no `.env` loading — `.env.example` was removed in 0.2.0 and the variables documented in the README instead. API keys stay entirely outside the package: the SDKs read their own `*_API_KEY` at call time.

## Consequences

- What the process sees is what runs; per-command prefixing (`AGENT_CLI_PROVIDER=echo agent run ...`) and shell exports both work with no hidden file lookup order.
- Frozen `Settings` keeps environment reads out of agent and provider code (ruff/mypy make regressions visible), and tests configure everything through `monkeypatch`.
- Users of `.env` workflows must bring their own loader (direnv, dotenv-cli); the README says so explicitly.
- A documented sharp edge remains: `AGENT_CLI_MODEL` with the provider left at `echo` is a silent no-op. Accepted as the cost of not validating configuration combinations.
