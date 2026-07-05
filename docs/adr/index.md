---
title: Architecture decision record index
type: index
status: current
date: 2026-07-04
owner: Lila Brooks
tags: [documentation, adr]
---

# Architecture Decision Records

Decisions that shaped this codebase, recorded after the fact from the shipped code, the architecture notes now in [contributing.md](../contributing.md), and the git history. Each ADR starts with a YAML frontmatter block (`id`, `title`, `type`, `status`, `date`, `deciders`, `tags`, `related`) and follows the Context / Decision / Consequences shape described in ADR-0001.

| ID | Decision | Status |
| --- | --- | --- |
| [ADR-0001](adr-0001-record-architecture-decisions.md) | Record architecture decisions as ADRs | accepted |
| [ADR-0002](adr-0002-hexagonal-architecture.md) | Thin hexagonal architecture with inward-only imports | accepted |
| [ADR-0003](adr-0003-language-model-protocol-and-registry.md) | Vendor-neutral `LanguageModel` protocol with a central provider registry | accepted |
| [ADR-0004](adr-0004-zero-runtime-dependencies.md) | Zero runtime dependencies; provider SDKs as optional extras with deferred imports | accepted |
| [ADR-0005](adr-0005-markdown-with-minimal-parser.md) | Markdown specs/skills with a minimal hand-rolled parser | accepted |
| [ADR-0006](adr-0006-file-block-output-contract.md) | Plain-text `FILE:` block contract for file generation | accepted |
| [ADR-0007](adr-0007-bundle-specs-skills-in-wheel.md) | Bundle default specs/skills into the wheel, working directory wins | accepted |
| [ADR-0008](adr-0008-env-var-configuration.md) | Environment-variable-only configuration, no `.env` auto-loading | accepted |
| [ADR-0009](adr-0009-safe-by-default-build-writes.md) | Safe-by-default build writes: plan first, no silent overwrite, no path escape | accepted |

The component-level behavior these decisions produce is specified in [docs/specs/](../specs/index.md).
