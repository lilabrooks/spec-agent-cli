---
id: ADR-0006
title: "Plain-text FILE: block contract for file generation"
type: adr
status: accepted
date: 2026-07-04
deciders: [Lila Brooks]
tags: [build, file-output, agent-contract]
related: [ADR-0003, ADR-0005, ADR-0009]
---

# ADR-0006: Plain-Text `FILE:` Block Contract for File Generation

## Context

`agent build` needs machine-readable file output from a model reply. The obvious alternatives — vendor tool-calling/structured-output APIs, or asking for a JSON document of paths and contents — either break vendor neutrality (each vendor's structured-output surface differs, and the `LanguageModel` protocol is deliberately one plain-text method, ADR-0003) or get mangled easily (code inside JSON strings needs escaping models often fumble).

## Decision

The contract is plain text in the reply itself: each generated file is a `FILE: <relative path>` line followed by one fenced code block containing the complete file contents. The instruction lives in a normal skill document (`skills/agent/file-output-contract.md`) that `build()` always appends to the context, independent of `--skill`/`--all-skills` — so the contract is versioned, reviewable, and overridable like any other skill. `core/fileset.py::parse_generated_files` is the counterpart parser; it is lenient (markers without a following fence are prose; a reply with no blocks parses to an empty list and warns rather than fails).

## Consequences

- Works identically on every provider, including `echo`, because it only requires text out.
- Code arrives inside ordinary fences — no escaping layer, and the raw reply is human-readable as a review artifact.
- The parser has known blind spots: files whose own content contains a bare ``` line (nested fences) will be truncated, and there is no checksum or count to detect a half-followed contract. Mitigated by plan-preview before writing (ADR-0009).
- Prompt-level contracts depend on model compliance; a model that ignores the skill produces a warning and no files, never a crash or partial write.
