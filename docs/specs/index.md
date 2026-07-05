---
title: Component specification index
type: index
status: current
date: 2026-07-04
owner: Lila Brooks
tags: [documentation, specs]
---

# Component Specifications

These specs describe the architecture and behavior of the `agent` CLI as it exists today. They document the shipped code. The source of truth for planned CLI features remains the repo-root `specs/cli/` folder that `agent spec check` validates.

Each file starts with a YAML frontmatter block (`id`, `title`, `type`, `status`, `version`, `date`, `owner`, `components`, `tags`, `related`).

| ID | Spec | Covers |
| --- | --- | --- |
| SPEC-000 | [Project objective and scope](spec-000-project-objective.md) | Mission, target user, core promises, non-goals |
| SPEC-001 | [CLI command surface](spec-001-cli-command-surface.md) | `agent` argparse tree, exit codes, output streams |
| SPEC-002 | [Agent core](spec-002-agent-core.md) | `Agent`, messages, completion models, `LanguageModel` port |
| SPEC-003 | [Provider adapters](spec-003-provider-adapters.md) | Registry plus `echo`, `anthropic`, `openai` adapters |
| SPEC-004 | [Configuration](spec-004-configuration.md) | `Settings`, environment variables, precedence rules |
| SPEC-005 | [Markdown document system](spec-005-markdown-document-system.md) | Parser, spec/skill documents, validation |
| SPEC-006 | [Build and file output](spec-006-build-file-output.md) | `agent build`, `FILE:` contract, safe writes |
| SPEC-007 | [Resource resolution](spec-007-resource-resolution.md) | Working-directory vs. bundled spec/skill roots |
| SPEC-008 | [Repository health invariants](spec-008-repository-health.md) | Version consistency, document validity, quality gates |

Architecture decisions behind these components are recorded separately in [docs/adr/](../adr/index.md).
