---
id: ADR-0005
title: Markdown specs/skills with a minimal hand-rolled parser
type: adr
status: accepted
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [markdown, parsing, specs, skills]
related: [ADR-0004, ADR-0006]
---

# ADR-0005: Markdown Specs/Skills with a Minimal Hand-Rolled Parser

## Context

Specs and skills are the human-authored inputs of the whole system. They need to be pleasant to write, reviewable in a diff, and renderable on GitHub — and the tool needs just enough structure from them: a title, named sections to validate, and a few metadata fields. A YAML library or Markdown AST parser would each add a runtime dependency (against ADR-0004) for far more capability than required.

## Decision

Specs and skills are plain Markdown files. One shared parser in `core/markdown.py` extracts exactly four things: an optional frontmatter block of flat `key: value` string pairs between `---` delimiters, the first `# ` heading as title (falling back to the filename), a map of `## ` sections to their content, and the raw body. Both document kinds wrap this parser with their own required-section lists and validation rules (`Purpose/Commands/Inputs/Outputs/Behavior/Acceptance tests` for specs; `Purpose/When to use/Rules/Verification` for skills). Validation distinguishes errors (missing section, missing title, empty file) from warnings (empty section, missing `status`/`source` metadata).

## Consequences

- Documents are the agent context, near-verbatim: `to_agent_context()` prepends a heading, path, and metadata list to the body, so what the human reviews is what the model reads.
- No dependency, and parsing behavior is small enough to hold in one file with full test coverage.
- Known limits accepted deliberately: frontmatter nesting/lists/types are unsupported (values stay strings), only `##`-level sections are recognized, and a `## ` line inside a fenced code block would be misread as a section boundary. If specs ever need richer metadata, adopting a real YAML parser becomes a new ADR.
- Consistency for free: any future document kind reuses the same parser and gets the same resolution rules (path → root-relative → slug).
