---
id: SPEC-008
title: Repository health invariants
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
components:
  - tests/test_repo_health.py
  - scripts/check-okf-docs.py
  - pyproject.toml
  - requirements.txt
  - CHANGELOG.md
  - Makefile
  - .github/workflows/code-quality.yml
  - AGENTS.md
  - .agents/skills
  - .codex/hooks.json
  - .codex/hooks
tags: [health, versioning, quality, ci, security]
related: [SPEC-000, SPEC-005, ADR-0004, ADR-0010]
---

# Repository Health Invariants

## Purpose

Define the repo-level consistency rules that must hold on every commit, independent of any feature's behavior — and where each one is enforced. The trigger for this spec was a real drift: a commit claimed a 0.3.0 bump while `pyproject.toml`, `__version__`, and the CHANGELOG all still said 0.2.0, and nothing failed.

## Invariants

### 1. One version, everywhere

`pyproject.toml` `[project] version` is the single source of truth. The following must always agree with it:

- `agent_cli.__version__` in `src/agent_cli/__init__.py`.
- The newest `## [x.y.z]` release heading in `CHANGELOG.md` (older headings are history and exempt).
- Every `ai_agent_cli-<x.y.z>` artifact name and `@v<x.y.z>` git-tag reference in `README.md` and `docs/**/*.md`.
- Every `version:` field in the YAML frontmatter of documents under `docs/` (the component specs in `docs/specs/`).

**Enforced by** `tests/test_repo_health.py` (version tests), which run in `make check` and CI. A version bump that misses any of these files now fails the suite instead of shipping silently.

### 2. Bundled documents stay valid

Every spec under `specs/cli/` and every skill under `skills/agent/` must pass its own validator (`validate_spec` / `validate_skill`) with zero errors — these files ship inside the wheel (SPEC-007) and are attached to real model calls, so a broken one is a runtime defect, not a docs problem.

**Enforced by** `tests/test_repo_health.py` (validation tests), equivalent to `agent spec check` and `agent skill check` exiting 0.

### 3. OKF docs stay navigable

The OKF-style documentation bundle must keep its structure and metadata intact:

- `docs/index.md`, `docs/log.md`, `docs/specs/index.md`, and `docs/adr/index.md` exist.
- `docs/index.md` declares `okf_version`.
- Every tracked Markdown frontmatter block under `docs/`, `specs/`, and `skills/` has a non-empty `owner` and a `deciders` list.
- Every tracked Markdown file under `docs/` with frontmatter has a non-empty `type`.
- Local Markdown links under `docs/`, `specs/`, and `skills/` point at files or directories inside the repo.

**Enforced by** `scripts/check-okf-docs.py`, which runs in `make check` and the code-quality workflow.

### 4. Scanner dependencies stay synchronized

`requirements.txt` exists for Snyk scanning and must remain a mirror of the optional dependency groups in `pyproject.toml`, including security lower-bound constraints. It should use lower bounds such as `h11>=0.16.0`, not exact pins such as `h11==0.16.0`, because this package is a reusable scaffold rather than a deployment lockfile.

**Enforced by** `tests/test_repo_health.py`, which fails if an optional dependency is missing from `requirements.txt` or if `requirements.txt` contains an exact pin.

### 5. No committed build artifacts

No tracked file may match a `.gitignore` pattern. This catches build and test artifacts — the `.coverage` database, caches, `dist/` output — that get committed once and then silently re-dirtied on every run. Untracking such a file (`git rm --cached`) and ignoring it is the fix.

**Enforced by** `tests/test_repo_health.py`, which fails if `git ls-files -i -c --exclude-standard` reports any tracked-but-ignored file. Skipped when run outside a git checkout (e.g. against an installed wheel).

### 6. Quality gates

- ruff lint and format checks pass with the configured rule set.
- mypy passes in `strict` mode over the package.
- Code-quality CI installs the optional Anthropic and OpenAI extras so mypy resolves the SDK type
  modules used at provider boundaries (ADR-0011); shipped runtime dependencies remain empty.
- pytest passes with branch coverage ≥ 70% (`fail_under = 70`).
- CI runs the same gates on Python 3.12, 3.13, and 3.14; `make check-all` reproduces that matrix locally.

**Enforced by** `make check` locally and the GitHub Actions workflows on every push.

### 7. Agent configuration stays portable

Repository guidance lives in `AGENTS.md`, Codex workflow skills live under `.agents/skills/`, and
Codex lifecycle hooks live under `.codex/`. Hook commands resolve scripts from the Git root rather
than a developer-specific absolute path. Personal Codex overrides remain ignored.

The Codex stack is an optional mirror of the Claude stack (`CLAUDE.md`, `.claude/hooks/`,
`.claude/skills/okf-*`), which is the source of truth. When the Codex stack is present, two parity
invariants hold (ADR-0012):

- **Hooks are byte-identical.** A lifecycle hook present in both `.claude/hooks/` and `.codex/hooks/`
  must match byte for byte, so both agents enforce the same guardrails.
- **Skills stay paired.** The set of `okf-*` skill directories under `.claude/skills/` and
  `.agents/skills/` must match. Contents are not compared — each skill is deliberately adapted to
  its agent (`CLAUDE.md` ⇄ `AGENTS.md`, `.claude` ⇄ `.codex` paths).

Both parity checks no-op when the Codex stack is absent, so a Claude-only checkout stays green.

**Verified by** JSON parsing of `.codex/hooks.json`, shell syntax checks for `.codex/hooks/*.sh`,
byte-comparison of the mirrored hooks, presence-parity of the `okf-*` skills across both stacks, and
the repository quality gate.

## Advisory (not hard-enforced)

- A git tag `v<x.y.z>` should exist for each CHANGELOG release heading once published.
- Snyk dashboard findings should be reproduced locally with `make snyk-open-source` for dependency/license findings or `make snyk-code` for SAST findings. These targets require an installed, authenticated Snyk CLI and may need `SNYK_ORG=<org-slug-or-id>` to match the dashboard project, so they stay outside `make check`. The Open Source target should pass the repo virtualenv through Snyk's Python `--command` option when `.venv/bin/python` exists.
- Snyk dashboard fixes should be added as lower-bound constraints in `pyproject.toml` and mirrored in `requirements.txt`, unless the project deliberately adopts a lockfile later.

## Acceptance tests

`tests/test_repo_health.py` — package/pyproject agreement, CHANGELOG agreement, docs references, doc frontmatter versions, Snyk scanner manifest synchronization, exact-pin prevention, no tracked files matching `.gitignore`, Claude/Codex hook byte-parity and `okf-*` skill pairing (skipped when the Codex stack is absent), spec validation, and skill validation.

`scripts/check-okf-docs.py` — validates OKF-style frontmatter, required docs bundle files, and local Markdown links. All checks must pass for `make check` to succeed.
