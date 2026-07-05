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

### 4. Quality gates

- ruff lint and format checks pass with the configured rule set.
- mypy passes in `strict` mode over the package.
- pytest passes with branch coverage ≥ 70% (`fail_under = 70`).
- CI runs the same gates on Python 3.12, 3.13, and 3.14; `make check-all` reproduces that matrix locally.

**Enforced by** `make check` locally and the GitHub Actions workflows on every push.

## Advisory (not hard-enforced)

- A git tag `v<x.y.z>` should exist for each CHANGELOG release heading once published.
- Snyk dashboard findings should be reproduced locally with `make snyk-open-source` for dependency/license findings or `make snyk-code` for SAST findings. These targets require an installed, authenticated Snyk CLI and may need `SNYK_ORG=<org-slug-or-id>` to match the dashboard project, so they stay outside `make check`. The Open Source target should pass the repo virtualenv through Snyk's Python `--command` option when `.venv/bin/python` exists.
- `requirements.txt` must mirror the optional provider SDKs and development tools declared in `pyproject.toml` whenever those package sets change. It exists for scanner visibility, not as the package install contract (ADR-0004).

## Acceptance tests

`tests/test_repo_health.py` — six tests: package/pyproject agreement, CHANGELOG agreement, docs references, doc frontmatter versions, spec validation, skill validation.

`scripts/check-okf-docs.py` — validates OKF-style frontmatter, required docs bundle files, and local Markdown links. All checks must pass for `make check` to succeed.
