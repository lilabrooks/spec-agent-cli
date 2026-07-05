---
okf_version: "0.1"
title: Documentation index
type: index
status: current
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, index]
---

# Documentation

Bundle root for the `agent` CLI documentation. Changes to this bundle are recorded in [log.md](log.md), newest first.

## Bundle contents

| Location | Contents |
| --- | --- |
| [specs/](specs/index.md) | Component specifications: how the shipped code behaves |
| [adr/](adr/index.md) | Architecture decision records: why the codebase is shaped this way |

## Supporting material

| Location | Contents |
| --- | --- |
| [contributing.md](contributing.md) | How to extend the codebase and the quality bar for changes |
| [guides/](guides/) | Step-by-step how-tos |
| [notes/](notes/) | Working notes and research records |
| [assets/](assets/) | Images used by the README and docs |

## Guides

- [pipx-artifact-guide.md](guides/pipx-artifact-guide.md): install from GitHub, build an installable artifact, test both paths with pipx.
- [my-cli-generator-test.md](guides/my-cli-generator-test.md): test the `my-cli` generated CLI fixture end to end.

## Notes

- [skill-research.md](notes/skill-research.md): sources checked when the project skills were written.

## The two specs folders

`docs/specs/` (here) documents shipped behavior. The repo-root [specs/](../specs/) folder is buildable input: planned CLI feature specs that `agent spec check` validates and `agent build` executes against.
