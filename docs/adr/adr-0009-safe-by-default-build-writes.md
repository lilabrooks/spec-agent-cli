---
id: ADR-0009
title: "Safe-by-default build writes: plan first, no silent overwrite, no path escape"
type: adr
status: accepted
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [build, safety, file-output]
related: [ADR-0006]
---

# ADR-0009: Safe-by-Default Build Writes

## Context

`agent build` writes model-generated content to the user's disk. The paths come from the model's reply, not from the user, so the write step has to assume the reply may be wrong, hostile, or half-compliant: paths could point outside the target directory, collide with existing work, or arrive when the user only wanted to inspect the output.

## Decision

Three stacked safeguards in `core/fileset.py` and `handle_build_command()`:

1. **Plan before write.** Without `--apply`, `build` only prints the resolved target list; nothing touches disk. Applying is a separate, explicit re-run.
2. **No silent overwrite.** `write_generated_files` checks every target before writing any; if one exists and `--force` was not given, it raises `FileExistsError` naming them all and the batch writes nothing — never a partial apply.
3. **No path escape.** `resolve_target_path` rejects empty paths, absolute paths, and any `..` component, so generated files land under `--out-dir` unconditionally.

Related soft-fail choices: a reply with no `FILE:` blocks prints the raw text with a stderr warning (exit 0), and `--spec` validation problems warn by default, failing fast only under `--strict` — before any model call is spent.

## Consequences

- The worst a misbehaving reply can do by default is print text; destructive outcomes require the user to have typed both `--apply` and `--force`.
- All-or-nothing overwrite checking avoids the hardest failure to recover from — a half-applied file set.
- The check-then-write sequence is not atomic against concurrent writers, and `--force` has no per-file granularity; both accepted for a single-user CLI.
- Slightly more ceremony on the happy path (two invocations to actually write), which matches the project's preview-first UX stance.
