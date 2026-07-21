---
type: Goal
title: Project goal
description: The goal, success criteria, and milestone backlog Claude Code iterates toward in this repo.
tags: [goal, milestones]
timestamp: 2026-07-14T00:00:00Z
owner: Lila Brooks
deciders: [Lila Brooks]
---

<!-- Drafted from docs/specs/spec-000-project-objective.md during the
     2026-07-14 kit adoption. SPEC-000 remains the authoritative statement;
     keep the two consistent. -->

# Goal

Kind: utility

Problem: `claude-okf-repo-kit` needs a real Python CLI project to dogfood its workflows and a proven chassis for a kit-based template.

Solution: Use the `agent` CLI as a working dogfood project for enhancing [claude-okf-repo-kit](https://github.com/lilabrooks/claude-okf-repo-kit), while proving the chassis for a new template based on that kit, focused specifically on creating Python CLI apps.

# Target state

The `agent` command surface (`run`, `build`, `spec`, `skill`, `providers`) works end to end: Markdown spec and skill loading, validation, and rendering into agent context; provider adapters for Anthropic, OpenAI, and the local echo stub behind the one-method `LanguageModel` protocol; single-shot prompt → reply → optional safe file-write flows; installable via pip/pipx with default specs and skills shipped inside the wheel. See [spec-000-project-objective.md](specs/spec-000-project-objective.md) for the full core promises.

# Success criteria

On a clean machine with only Python 3.12+:

- `pipx install` from the repo followed by `agent providers` and `agent run "hello"` succeeds with no credentials or network.
- `agent build --spec <any-path>.md --apply --out-dir <dir>` with a real provider writes the generated files under `<dir>` and refuses to overwrite existing ones without `--force`.
- `make check` passes: lint, strict type-check, tests with the 70% branch-coverage floor, and OKF docs validation.

# Non-goals

Per SPEC-000: no conversation state, no streaming/tool-use/structured-output APIs, no plugin discovery, no config files or `.env` loading, no agentic loop, not a hosted service or IDE integration.

# Constraints

- Governing docs: [docs/specs/](specs/index.md) (SPEC-000–008) and [docs/adr/](adr/index.md) (ADR-0001–0012); source-to-doc mapping in `docs/okf-map.yml`.
- Zero runtime dependencies (ADR-0004); vendor SDKs are opt-in extras.
- Python 3.12–3.14; mypy strict, ruff, pytest coverage floor per SPEC-008.

# Milestones

Ordered backlog; selection, check-off, and goal-met mechanics per
`CLAUDE.md` § Goal iteration.

The backlog is empty as of the 2026-07-14 kit adoption: the repo is at its
SPEC-000 target state and the success criteria pass. Candidate next milestones
are proposed to the owner per the process above, not added here unilaterally.
