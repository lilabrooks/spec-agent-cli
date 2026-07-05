---
id: ADR-0003
title: Vendor-neutral LanguageModel protocol with a central provider registry
type: adr
status: accepted
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [providers, protocol, registry]
related: [ADR-0002, ADR-0004]
---

# ADR-0003: Vendor-Neutral `LanguageModel` Protocol with a Central Provider Registry

## Context

The project's core promise is model-agnosticism: Anthropic, OpenAI, or a local stub, swappable without touching application code. Early versions selected providers with a hardcoded `match` statement in the factory, which meant the factory, the unknown-provider error message, and the `providers` command each had their own idea of what existed and could drift apart.

## Decision

Two pieces:

1. **The port is a one-method `typing.Protocol`** — `LanguageModel.complete(CompletionRequest) -> CompletionResponse`. Adapters satisfy it structurally; there is no base class to inherit or interface to register. Requests and responses use the project's own frozen dataclasses, with usage keys normalized to `input_tokens`/`output_tokens` across vendors.
2. **`providers/registry.py` is the single source of truth**: a dict of name → factory taking the optional model override. `available_providers()`, `create_provider()`, and therefore the CLI's error message and the `providers` command all read the same dict. Adding a vendor is one adapter module plus one registry entry (replacing the `match` statement, 0.2.0).

## Consequences

- Agents, tests, and the CLI depend only on the protocol; the echo stub makes the whole pipeline runnable offline and credential-free.
- The provider list can never disagree with the error message or the `providers` output.
- A protocol this narrow cannot express streaming, tool use, or multi-turn state; extending it will be a deliberate contract change rather than a per-vendor leak.
- The registry is static (no entry-point plugin discovery); third-party providers require editing this repo, which is acceptable for a scaffold meant to be forked.
