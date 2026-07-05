---
id: SPEC-006
title: Build and file output
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
components:
  - src/agent_cli/core/fileset.py
  - src/agent_cli/cli.py
  - skills/agent/file-output-contract.md
tags: [build, file-output, safety]
related: [SPEC-001, SPEC-005]
---

# Build and File Output

## Purpose

`agent run` only prints text; `agent build` turns a model reply into files on disk. This spec covers the reply contract, the parser, and the safety rules around writing.

## The `FILE:` contract

The model is told (via the `file-output-contract` skill, which `build()` always attaches regardless of `--skill`/`--all-skills`) to emit each file as:

````text
FILE: relative/path/to/file.py
```
full file contents
```
````

`parse_generated_files` scans the reply line by line: a stripped line starting with `FILE:` names a path; blank lines may follow; the next line must open a fenced code block, whose contents up to the closing bare ``` fence become the file. A marker with no fence after it is treated as prose and skipped, as is a marker with an empty path. Parsing never fails — a reply with no valid blocks just yields an empty list.

## Pipeline (`build()` + `handle_build_command()`)

1. If `--spec` is given, validate it first with the same rules as `agent spec check`. Errors warn on stderr and continue by default; `--strict` raises `SpecValidationError` before any provider is constructed or model call made.
2. Run the same spec/skill-aware prompt as `run`, with the file-output contract appended as the final context block.
3. Parse the reply. No `FILE:` blocks → print the raw reply, warn on stderr, exit 0.
4. Resolve each parsed path against `--out-dir` (default `.`). `resolve_target_path` rejects empty paths, absolute paths, and any `..` component with `ValueError` → exit 1.
5. Without `--apply`, print the plan (`Plan: N file(s) under <dir>:` plus each target) and stop — nothing is written.
6. With `--apply`, `write_generated_files` first checks every target; if any exists and `--force` was not given, it raises `FileExistsError` listing them and writes nothing at all. Otherwise it creates parent directories and writes each file with a trailing newline.

## Invariants

- `core/fileset.py` knows only text and paths — no imports from `cli.py`, providers, or skills (same inward-import rule as the rest of core).
- The overwrite check is all-or-nothing: a batch never partially applies because one target already existed.
- Generated files can never escape `--out-dir` via absolute paths or traversal.

## Acceptance tests

`tests/test_fileset.py` covers parsing edge cases, unsafe paths, and overwrite refusal; `tests/test_cli_build.py` covers plan/apply/force/strict and the no-blocks warning end to end.
