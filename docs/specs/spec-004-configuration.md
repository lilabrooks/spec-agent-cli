---
id: SPEC-004
title: Configuration
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
components:
  - src/agent_cli/config/settings.py
tags: [configuration, environment]
related: [SPEC-002, SPEC-003]
---

# Configuration

## Purpose

Centralize every runtime knob in one frozen `Settings` dataclass, read from the process environment in exactly one place, so agent and provider code never touch `os.environ`.

## Inputs

Three environment variables, all optional:

| Variable | Effect | Default |
| --- | --- | --- |
| `AGENT_CLI_PROVIDER` | Which registered adapter answers prompts | `echo` |
| `AGENT_CLI_MODEL` | Model override passed to the active adapter | adapter's own default |
| `AGENT_CLI_SYSTEM_PROMPT` | System message sent ahead of the task | `You are a concise, practical assistant.` |

## Behavior

- `Settings.from_env(provider_override=...)` is the only environment read. Provider precedence is: `--provider` flag → `AGENT_CLI_PROVIDER` → `echo`.
- There is no `.env` auto-loading and no CLI flag for model or system prompt; whatever is in the process environment at invocation time wins (ADR-0008).
- `AGENT_CLI_MODEL` only takes effect on the provider actually selected. With the default `echo` provider it is a silent no-op, since echo has no underlying model.
- API keys are deliberately outside this module: the vendor SDKs read them from the environment themselves, and only once that vendor's adapter actually runs.

## Invariants

- `Settings` is immutable after construction; the CLI builds it once per command.
- No module outside `config/settings.py` reads `AGENT_CLI_*` variables.

## Acceptance tests

`tests/test_settings.py` covers defaults, environment values, and the flag-over-environment precedence using `monkeypatch`.
