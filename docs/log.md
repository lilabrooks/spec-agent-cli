---
title: Documentation log
type: log
status: current
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, log]
---

# Documentation log

Dated changes to the docs bundle, newest first.

## 2026-07-21

- Accepted ADR-0012 (dual-agent config parity) at the owner's direction. Status flipped to `accepted` in the frontmatter and body, index entry updated, and the ADR now binds future work: `.codex/hooks/` mirrors stay byte-identical to `.claude/hooks/` and the `okf-*` skill sets stay paired, enforced by `tests/test_repo_health.py` under SPEC-008 invariant #7 (checks skip when the Codex stack is absent). No implementation change needed — the guard has been in the gate since 2026-07-14 per the propose-then-implement policy. Constraint ranges in `CLAUDE.md`, `AGENTS.md`, and `docs/GOAL.md` corrected to "ADR-0001–0012 (all accepted)" (they had drifted at 0010/0011). `bash scripts/okf pending` is now empty. Verified: `make check`.

- Upgraded claude-okf-repo-kit 0.3.7 → 0.3.8. The 0.3.8 release is this repo's own upgrade friction harvested back into the kit (its four updater review aids came from our 0.3.0→0.3.7 pass), and this run live-verified them here: the declared `.codex/hooks` mirrors were synced mechanically (reported "already current" — no manual re-sync step this time), the populated map drew no `okf-map.2.yml` noise, skill pairing and template delta stayed quiet as expected, and the only candidate (`CLAUDE.2.md`, the rendered template with no new kit content since the 0.3.7 merge) was reviewed and deleted. Refreshed skills (`okf-kit-upgrade`, `okf-second-agent`) carried over to `.agents/skills/` per the ADR-0012 pairing rule, with the `okf-kit-upgrade` `.codex/hooks.json` substitution re-applied. No spec or ADR change warranted: skill refreshes and the restamp are kit-managed maintenance under ADR-0012's existing parity contract. Verified: `make check` (68 tests), `bash scripts/okf check-stale` clean after this entry.

- Upgraded claude-okf-repo-kit 0.3.0 → 0.3.7 via `update-existing-repo` (backup under `.okf-kit-backups/20260721T212444Z/`). Refreshed in place by provenance: `scripts/okf`, `.claude/hooks/check-okf-version.sh` (now reports unresolved kit candidates, empty maps, and undeclared hook mirrors), `.claude/skills/okf-kit-upgrade` and `okf-adopt`; new `.claude/skills/okf-second-agent` skill installed; `kit_version` restamped in `docs/index.md`. Candidate review: merged the new kit paragraphs from `CLAUDE.2.md` into the live `CLAUDE.md` (expanded skills list, second-agent port rules, unresolved-candidate policy, `.env.example` loader-statement rule) while keeping all owner-filled content, and adopted the `mirrors:` block from `okf-map.2.yml` into the live map — `docs/okf-map.yml` now declares `mirrors: [.codex/hooks]` (kit ADR 0021) so future upgrades sync the hook mirrors mechanically; both candidates then deleted. Codex stack re-paired per ADR-0012: `.codex/hooks/check-okf-version.sh` re-synced byte-identical, `.agents/skills/okf-adopt` and `okf-second-agent` copied verbatim, `okf-kit-upgrade` re-adapted with its `.codex/hooks.json` substitution. Brought `AGENTS.md` up to the kit's new port conventions from the `okf-second-agent` skill: `@` imports replaced with explicit session-start reads (Codex never resolved them), env-file denial stated honestly as policy-only for Codex, self-describing port paragraph added, plus the same new kit paragraphs as `CLAUDE.md`. Updated proposed ADR-0012 with a dated note: its root-cause finding shipped as kit ADR 0021, the repo-side parity checks stay as belt-and-suspenders. Verified: `make check` (68 tests), `bash scripts/okf check-stale` clean, JSON/`bash -n` syntax checks on both stacks.

## 2026-07-14

- Consolidated the README purpose into its opening paragraph and removed the repeated `Project Objective` section. Presentation only; SPEC-000 remains current.
- Documented the repository's sole objective: dogfood `claude-okf-repo-kit` and provide the proven chassis for a kit-based template focused on Python CLI apps. Updated `README.md`, SPEC-000, `docs/GOAL.md`, and `AGENTS.md`; no shipped CLI behavior changed.
- Proposed ADR-0012 and added a repo-health guard for parity between the two agent stacks. The Codex stack (`AGENTS.md`, `.codex/hooks/`, `.agents/skills/`) mirrors the Claude stack, but nothing enforced that the shared lifecycle hooks stay identical or that the `okf-*` skills stay paired — SPEC-008 invariant #7 checked each side in isolation only. `tests/test_repo_health.py` now asserts `.claude/hooks/*.sh` are byte-identical to their `.codex/hooks/` mirrors and that the `okf-*` skill set matches across `.claude/skills/` and `.agents/skills/`; both checks skip when the Codex stack is absent, since Codex is optional (a Claude-only checkout stays green). Skill *contents* are deliberately not compared — the `CLAUDE.md`⇄`AGENTS.md` / `.claude`⇄`.codex` substitutions are intended. Updated SPEC-008 invariant #7 with the parity clause, mapped ADR-0012 in `docs/okf-map.yml`. ADR-0012 is `status: proposed` — the dual-stack decision was Codex's to introduce; the ADR records the invariant and names the root-cause finding to carry back to the kit (its updater does not sync second-agent mirrors). Verified: `make check`.
- Added Codex-native repository guidance, OKF workflow skills, and portable lifecycle hooks under
  `AGENTS.md`, `.agents/`, and `.codex/`; added matching OKF mappings and local-settings ignores.
  This mirrors the existing Claude workflow without changing the shipped CLI.
- Accepted ADR-0011 at the owner's direction and installed the optional Anthropic and OpenAI SDK
  extras in code-quality CI so strict mypy can resolve provider type modules. This supersedes only
  ADR-0004's CI dependency-free consequence; its zero shipped-runtime-dependency decision remains.
- Added SPEC-008 invariant #5 "No committed build artifacts" and its guard in `tests/test_repo_health.py` (`test_no_tracked_files_match_gitignore`): fails if `git ls-files -i -c --exclude-standard` reports any tracked-but-ignored file, so a re-committed `.coverage` (or similar) is caught in CI. Skips outside a git checkout. Renumbered the former invariant #5 to #6.
- Added `.github/dependabot.yml` covering the `github-actions` ecosystem only (weekly), to keep workflow action pins (`actions/checkout`, `actions/setup-python`) current. Not decision-shaped: no new runtime dependency (ADR-0004 stands), and the `pip` ecosystem is intentionally excluded — Snyk already covers dependency vulnerabilities and the optional extras use `>=` lower bounds.
- Fixed mypy strict errors in `src/agent_cli/providers/openai.py` and `src/agent_cli/providers/anthropic.py` caused by updated vendor SDK type stubs: OpenAI messages are now built per-role as `list[ChatCompletionMessageParam]`, and the Anthropic `Messages.create` call uses explicit keyword arguments (two call shapes) instead of an untyped `dict[str, object]` expansion. Typing only — no behavior, contract, or spec change, so SPEC-003 and ADR-0003 stand as written; type-only imports sit under `TYPE_CHECKING`, preserving SPEC-003's deferred-SDK-import rule.
- Adopted claude-okf-repo-kit 0.3.0 via its `update-existing-repo` updater: installed `CLAUDE.md`, `.claude/` settings/hooks/skills, `scripts/okf`, `docs/okf-map.yml`, and `docs/GOAL.md`; stamped `kit_version` into `docs/index.md`; appended kit `.gitignore` entries. Existing docs, naming (`spec-NNN-*` / `adr-NNNN-*` prefixes), and indexes left untouched — the kit's brownfield tolerance (its ADRs 0018/0019) follows them in place.
- Populated `docs/okf-map.yml` mappings from each spec's `components:` frontmatter plus the ADRs governing each area; no `layout:` block needed since the repo already uses the default tree.
- Drafted `docs/GOAL.md` from SPEC-000 (objective, target state, acceptance criteria, non-goals) with an empty milestone backlog, pending owner review; filled the `CLAUDE.md` template brackets (master objective, `make check` verification commands).
- Trimmed the `GOAL.md` milestone-mechanics boilerplate to a pointer at `CLAUDE.md` § Goal iteration, which both preload at session start; keeping the rules in one place.
- Adoption inventory: all knowledge already lives in `docs/specs/` and `docs/adr/`; `guides/` and `notes/` are supporting material, and the repo-root `specs/` and `skills/` folders are buildable product input (bundled in the wheel), not governance docs — nothing was moved or reclassified.

- Updated local Make targets to use `.venv/bin` quality tools when the repo virtualenv exists and to report missing coverage tooling clearly.
- Added repo-health coverage that keeps `requirements.txt` synchronized with optional dependencies and prevents exact scanner pins.
- Added `anyio>=4.4.0`, `h11>=0.16.0`, `idna>=3.15`, and `zipp>=3.19.1` lower-bound constraints for the `openai` extra and Snyk scan manifest to address SNYK-PYTHON-ANYIO-7361842, SNYK-PYTHON-H11-10293728, SNYK-PYTHON-IDNA-16769942, and SNYK-PYTHON-ZIPP-7430899.
- Added local Snyk Make targets and documented how to reproduce dashboard findings before fixing them, including Python resolver options and the advisory repo-health expectation in SPEC-008.
- Documented the root `requirements.txt` as a Snyk-friendly scan manifest that mirrors optional and development dependencies from `pyproject.toml`, including the decision record in ADR-0004.
- Added a static README OKF docs validated badge that links to the quality standard section.
- Added OKF docs validation to `make check`, `make check-all`, and the code-quality workflow, and recorded the decision in ADR-0010.

## 2026-07-04

- Adopted the bundle layout: `index.md` at the bundle root and in `specs/` and `adr/`, plus this `log.md`.
- Moved the pipx artifact guide and the my-cli generator test guide into `guides/`.
- Moved `skill-research.md` into `notes/`.
- Replaced `architecture.md` with `contributing.md`. Component behavior moved to `specs/`, decision rationale to `adr/`.
- Added component specifications SPEC-000 through SPEC-008 with an index.
- Added architecture decision records ADR-0001 through ADR-0009 with an index.

## 2026-07-02

- Updated the spec-agent CLI flow diagram in `assets/`.
- Added the pipx artifact guide and the my-cli generator test guide.
- Added `architecture.md` in the initial commit.
