---
id: SPEC-002
title: Agent core
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
components:
  - src/agent_cli/agents/base.py
  - src/agent_cli/core/messages.py
  - src/agent_cli/core/models.py
  - src/agent_cli/core/ports.py
  - src/agent_cli/runtime/factory.py
tags: [agent, hexagonal, protocol]
related: [SPEC-003, SPEC-004]
---

# Agent Core

## Purpose

Define the vendor-neutral center of the application: the message and completion types every provider speaks, the `LanguageModel` port they implement, the single `Agent` that uses it, and the composition root that wires them together.

## Types

All core types are frozen, slotted dataclasses:

- `Message(role, content)` — `role` is `Literal["system", "user", "assistant", "tool"]` (`core/messages.py`).
- `CompletionRequest(messages, metadata)` — an immutable tuple of messages plus a free-form `dict[str, str]` (`core/models.py`).
- `CompletionResponse(text, model, usage)` — reply text, the model that answered (optional), and token usage as `dict[str, int]`.
- `AgentResult(agent_name, text)` — what `Agent.run` returns to the CLI layer.

## Port

`LanguageModel` (`core/ports.py`) is a `typing.Protocol` with exactly one method:

```python
def complete(self, request: CompletionRequest) -> CompletionResponse: ...
```

Adapters satisfy it structurally — no registration, inheritance, or base class. Core modules never import a provider; providers import core (see ADR-0002).

## Behavior

`Agent` (`agents/base.py`) holds a `name`, a `system_prompt`, and a `LanguageModel`. `Agent.run(prompt)` builds a two-message request — the system prompt followed by the user prompt — calls `model.complete()`, and wraps the reply text in an `AgentResult`. It is stateless between calls and holds no conversation history.

`runtime/factory.py` is the composition root: `build_model(settings)` resolves the provider through the registry with the settings' model override, and `build_agent(settings)` constructs the single `Agent` named `default-agent` with the configured system prompt. Nothing outside `runtime/` and `cli.py` constructs providers.

## Invariants

- Core never imports providers, `cli.py`, or anything that reads the environment.
- Requests and responses are immutable once constructed.
- The `tool` role exists in the `Role` literal but no current adapter emits or forwards it; adapters filter to the roles their API supports.

## Acceptance tests

`tests/test_agent.py` verifies the request shape (system + user message) and result wrapping; `tests/test_factory.py` verifies settings-to-agent wiring and the unknown-provider error path.
