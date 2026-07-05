---
id: SPEC-003
title: Provider adapters
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
components:
  - src/agent_cli/providers/registry.py
  - src/agent_cli/providers/echo.py
  - src/agent_cli/providers/anthropic.py
  - src/agent_cli/providers/openai.py
tags: [providers, adapters, anthropic, openai]
related: [SPEC-002, SPEC-004]
---

# Provider Adapters

## Purpose

Keep every model vendor behind the one-method `LanguageModel` port so the CLI, agent, and tests never depend on a vendor SDK. The registry is the single source of truth for which adapters exist.

## Registry

`providers/registry.py` maps provider name → factory `Callable[[str | None], LanguageModel]`, where the argument is the optional model override:

- `available_providers()` returns the sorted names; the `agent providers` command prints exactly this list.
- `create_provider(name, model=...)` looks up the factory and raises `ValueError` with the full supported list on an unknown name — the same message the CLI surfaces with a `Try 'agent providers'` hint.

Adding a vendor means one adapter module plus one registry entry; the factory, error message, and `providers` command all pick it up from there.

## Adapters

- **echo** — credential-free and offline. Returns `Echo provider received: <last user message>` and reports `model="echo"`. Ignores the system prompt and any model override (the registry factory discards it). Used for development, demos, and tests.
- **anthropic** — Claude Messages API. Default model `claude-opus-4-8`, `max_tokens` 1024. Joins all `system` messages into the API's `system` parameter, forwards `user`/`assistant` messages, concatenates `text` content blocks into the reply, and maps usage to `input_tokens`/`output_tokens`.
- **openai** — Chat Completions API. Default model `gpt-4o-mini`, `max_tokens` 1024. Forwards `system`/`user`/`assistant` messages as-is, takes the first choice's content (empty string if `None`), and maps `prompt_tokens`/`completion_tokens` to the same normalized usage keys.

## Behavior and constraints

- The `anthropic` and `openai` SDK imports happen inside `complete()`, not at module import time, so the registry can import every adapter unconditionally and the CLI works with neither extra installed. Credentials (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) are read by the SDKs themselves, never by this package.
- Both real adapters accept the model via constructor; the `AGENT_CLI_MODEL` override reaches them through `Settings` → `build_model` → registry factory.
- Usage keys are normalized across vendors so callers never see vendor-specific field names.

## Acceptance tests

`tests/test_anthropic_provider.py` and `tests/test_openai_provider.py` fake the SDK modules to verify request mapping, response mapping, and default-vs-override model selection without network access; `tests/test_factory.py` covers registry dispatch and the unknown-provider error.
