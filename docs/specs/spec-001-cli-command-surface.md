---
id: SPEC-001
title: CLI command surface
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
components:
  - src/agent_cli/cli.py
  - src/agent_cli/core/parser.py
tags: [cli, argparse, ux]
related: [SPEC-004, SPEC-005, SPEC-006]
---

# CLI Command Surface

## Purpose

Define the terminal-facing contract of the `agent` command: its subcommands, flags, output streams, and exit codes. `cli.py` is the only module that touches `argparse`, stdout, or stderr; everything below it is plain functions and dataclasses.

## Commands

- `agent run <prompt> [--provider|-p NAME] [--spec SPEC] [--skill NAME ...| --all-skills]` — send one prompt through the configured agent and print the reply.
- `agent build <prompt> [--provider|-p NAME] [--spec SPEC] [--skill NAME ...| --all-skills] [--out-dir DIR] [--apply] [--force] [--strict]` — same prompt pipeline as `run`, plus `FILE:` block parsing and optional writes (see SPEC-006).
- `agent spec list|show|check [SPEC] [--root DIR]` — enumerate, print, or validate Markdown CLI specs.
- `agent skill list|show|check [SKILL] [--root DIR]` — same for agent skills.
- `agent providers` — print the registered provider names, one per line, sorted.

`--skill` and `--all-skills` are a mutually exclusive group on both `run` and `build`. Subcommands are required at both levels (`agent` alone and bare `agent spec`/`agent skill` are usage errors).

## Behavior

- `run` output is prefixed with the agent name: `default-agent: <reply text>`.
- `spec check`/`skill check` with no argument validate every document under the root; with an argument they validate just that one. Output is one `path: ok|failed` block per document with indented `Error:`/`Warning:` lines.
- All parsers are `FriendlyArgumentParser` (`core/parser.py`), which overrides `argparse.ArgumentParser.error` to print usage plus `Error: <message>` and a `Try '<prog> --help'` hint. Abbreviated flags are disabled (`allow_abbrev=False`).
- Domain errors are translated at the `main()` boundary: `FileNotFoundError` (unresolvable spec/skill) exits with a hint to run `agent spec list`/`agent skill list`; `ValueError` (unknown provider) exits with a hint to run `agent providers`.

## Outputs and exit codes

- Results go to stdout; warnings and errors go to stderr, via the `write_stdout_line`/`write_stderr_line` helpers (the only print sites in the package, keeping ruff's `T20` rule meaningful).
- Exit `0` on success, including a `build` whose reply contained no `FILE:` blocks (warned, not failed).
- Exit `1` on: unresolvable spec/skill, unknown provider, failed `spec check`/`skill check` (any document failed, or no documents found), `--strict` spec validation failure, unsafe generated path, or overwrite refusal.
- Exit `2` on argparse usage errors.

## Acceptance tests

Covered by `tests/test_cli.py` (run/providers/spec/skill flows, error hints, empty-skill warning) and `tests/test_cli_build.py` (build planning, apply, force, strict).
