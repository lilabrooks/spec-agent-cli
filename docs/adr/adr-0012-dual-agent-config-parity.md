---
id: ADR-0012
title: Guard parity between the Claude and Codex agent stacks
type: adr
status: proposed
date: 2026-07-14
owner: Lila Brooks
deciders: [Lila Brooks]
description: Run an optional Codex agent stack mirroring the Claude one, with hooks kept byte-identical and guidance adapted, enforced by a repo-health check.
tags: [agent-config, codex, repo-health, ci]
related: [SPEC-008, ADR-0010]
---

# ADR-0012: Guard Parity Between the Claude and Codex Agent Stacks

## Status

Proposed (authored per the decision policy; awaiting owner review)

## Context

The repository now carries two agent toolchains side by side. The Claude stack
(`CLAUDE.md`, `.claude/hooks/`, `.claude/skills/okf-*`) was installed by the
claude-okf-repo-kit adoption. A parallel Codex stack (`AGENTS.md`,
`.codex/hooks/`, `.agents/skills/okf-*`) was added later and merged via PR #5.

The two stacks are not independent. The lifecycle hooks
(`check-docs-sync.sh`, `check-okf-version.sh`) are meant to enforce the same
OKF guardrails regardless of which agent runs, so they must stay byte-identical
across `.claude/hooks/` and `.codex/hooks/`. The playbook and workflow skills
are deliberately *not* identical: each is adapted to its agent
(`CLAUDE.md` ⇄ `AGENTS.md`, `.claude` ⇄ `.codex` path substitutions), but the
*set* of skills must stay paired so a capability added to one stack is not
silently missing from the other.

Nothing enforces either invariant today. SPEC-008 invariant #7 verifies the
Codex config in isolation (its JSON parses, its shell scripts have valid
syntax) but never checks the two stacks against each other. The kit's own
`okf-kit-upgrade` skill states the byte-identical hook rule in prose, but it is
enforced only by an agent remembering to read that skill mid-upgrade. The kit
updater does not know about second-agent mirrors, so a hook edit on the Claude
side leaves the Codex mirror stale with no signal until a Codex session behaves
differently.

The Codex stack is optional. A fork or a clean adoption may run the Claude
stack alone, and the guard must not punish that.

## Decision

Treat the Codex stack as an optional mirror of the Claude stack, and record the
two invariants as repo-health checks in `tests/test_repo_health.py` under
SPEC-008 invariant #7:

1. **Hooks are byte-identical when both exist.** For each hook present in both
   `.claude/hooks/` and `.codex/hooks/`, the two files must be byte-for-byte
   equal.
2. **Skills are paired when both stacks exist.** When `.agents/skills/` is
   present, the set of `okf-*` skill directories under `.claude/skills/` and
   `.agents/skills/` must match. Contents are not compared — the per-agent
   substitutions are intended.

Both checks are conditional on the Codex stack being present. With no
`.codex/hooks/` or no `.agents/skills/`, the checks pass without assertion, so a
Claude-only repository stays green.

The Claude stack is the source of truth: when the two diverge, the fix is to
re-sync the Codex mirror from `.claude/`, not the reverse.

## Alternatives considered

- **Prose rule only (status quo).** The `okf-kit-upgrade` skill already
  documents the byte-identical rule. It is silently violable and depends on an
  agent reading the skill during an upgrade — exactly the failure mode a
  mechanical check exists to remove.
- **Assert the skills are byte-identical too.** Rejected: the substitutions
  (`CLAUDE.md` → `AGENTS.md`, `.claude` → `.codex`) are correct and required, so
  byte-equality would fail on healthy config.
- **Assert skill differences are only the known substitutions.** Rejected as
  brittle: it hard-codes the substitution set and breaks whenever a skill gains
  legitimately agent-specific wording. Presence-parity catches the likely
  failure (a skill added to one stack, forgotten in the other) without false
  alarms.
- **Make the Codex stack mandatory.** Rejected: it is optional tooling; a
  Claude-only fork must remain valid.

## Consequences

- `make check` fails when the hooks drift or a skill is added to one stack and
  not the other, so drift is caught on every push instead of at a future Codex
  session.
- Editing a shared hook now means updating both copies in the same change; the
  test names the mismatch.
- A Claude-only repository is unaffected: the checks no-op when the Codex stack
  is absent.
- SPEC-008 invariant #7 gains a cross-stack parity clause and its verifying
  test.
- This does not fix the root cause — the kit updater still does not sync
  second-agent mirrors. That remains a finding to carry back to
  claude-okf-repo-kit (ship this parity test with the kit, or teach the updater
  to sync mirrors).

## Rollback / revisit trigger

Revisit if the Codex stack is removed (drop the checks and invariant clause), if
the kit gains native multi-agent install that keeps mirrors in sync (the check
becomes redundant with the kit's own guarantee), or if a future arrangement
needs the hooks to diverge intentionally (replace byte-equality with a
documented per-stack contract). Rollback means removing the two assertions and
the invariant #7 parity clause.
