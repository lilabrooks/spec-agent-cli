---
id: SPEC-005
title: Markdown document system
type: spec
status: current
version: 0.3.0
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
components:
  - src/agent_cli/core/markdown.py
  - src/agent_cli/specs/document.py
  - src/agent_cli/specs/loader.py
  - src/agent_cli/skills/document.py
  - src/agent_cli/skills/loader.py
tags: [markdown, specs, skills, validation]
related: [SPEC-001, SPEC-007]
---

# Markdown Document System

## Purpose

Turn plain Markdown files into normalized agent context. One shared parser lives in `core/markdown.py`; the `specs/` and `skills/` packages wrap it with their own document types and validation rules, so parsing stays consistent while the two document kinds keep separate required sections.

## Parsing (`core/markdown.py`)

- `split_metadata` reads an optional frontmatter block delimited by `---` lines at the top of the file. It parses flat `key: value` pairs only — values stay strings, nesting and YAML types are intentionally unsupported (ADR-0005). A block that never closes is treated as body text.
- `extract_title` takes the first `# ` heading; if none, the filename stem is title-cased.
- `extract_sections` maps each `## ` heading to its trimmed content, up to the next `## `.
- `list_markdown(root)` returns all `*.md` files under the root, sorted, or `[]` when the root does not exist.
- `resolve_markdown(target, root, kind)` resolution order: exact path as given → `root/target` → `root/target.md` (when the target lacks the suffix) → unique filename-stem match anywhere under the root. Ambiguous stems and misses raise `FileNotFoundError` with the candidate list or the searched root.

## Documents and agent context

`SpecDocument` and `SkillDocument` mirror `MarkdownDocument` (path, title, raw, body, metadata, sections; slug = filename stem). Each renders itself with `to_agent_context()`: a heading (`# CLI spec: <title>` / `# Agent skill: <title>`), the source path, a metadata bullet list (`- none` when empty), one instruction line, and the full body. This rendered string is what `agent run`/`build` join into the prompt and what `spec show`/`skill show` print.

## Validation

`validate_spec` / `validate_skill` return a result with `errors` (fail) and `warnings` (advice):

- Errors: empty file, missing title, missing required section. Specs require `Purpose`, `Commands`, `Inputs`, `Outputs`, `Behavior`, `Acceptance tests`; skills require `Purpose`, `When to use`, `Rules`, `Verification`.
- Warnings: a required section present but empty; missing `status` metadata (specs) or `source` metadata (skills).

`agent spec check` / `agent skill check` exit non-zero if any validated document has errors.

## Acceptance tests

`tests/test_specs.py` and `tests/test_skills.py` cover loading, slug resolution, context rendering, and each validation error and warning.
