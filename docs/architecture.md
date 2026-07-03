# Architecture

This project uses a thin hexagonal shape:

- `cli.py` owns terminal input and output.
- `agents/` owns task behavior.
- `core/` owns contracts and shared Markdown parsing.
- `providers/` owns model-specific adapters.
- `skills/` owns Markdown skill loading and validation.
- `specs/` owns Markdown spec loading and validation.
- `runtime/` wires concrete implementations together.

Keep imports flowing inward. Provider modules can import core contracts, but core modules should never import a provider.

The Markdown parser lives in `core/markdown.py`. Specs and skills wrap that parser with their own document objects and validation rules, which keeps parsing consistent while preserving separate responsibilities.

## Adding a provider

1. Create a module under `src/agent_cli/providers/`.
2. Implement `LanguageModel`.
3. Register it in `providers/registry.py`. The factory, the unknown-provider error, and the `providers` command all read from that registry.
4. Add focused tests for request mapping, response mapping, and error handling.

Provider configuration should stay in `config/settings.py` or in provider-owned config types. Avoid reading environment variables deep inside agent code.

## Quality standard

Tests use pytest. New tests should be function-based and use fixtures such as `tmp_path`, `capsys`, and `monkeypatch` instead of `unittest` classes.

Ruff owns linting, import sorting, and formatting. The configured rule set favors modern Python, simple returns, pathlib, no stray print debugging, and no unused arguments or imports.

mypy runs in strict mode against the package. Public functions should have typed signatures, and the package includes `py.typed` so type checkers can inspect it after installation.

## Spec-driven CLI building

CLI feature specs live in `specs/cli/`. The Python package reads those Markdown files through `agent_cli.specs`, validates required sections, and can attach the full spec as agent context.

Required sections:

- `Purpose`
- `Commands`
- `Inputs`
- `Outputs`
- `Behavior`
- `Acceptance tests`

This keeps the handoff clear: humans write specs, agents receive normalized context, and Python code handles loading, validation, and provider-neutral execution.

## Agent skills

Agent skills live in `skills/agent/`. They are Markdown files that shape how the agent works while implementing a spec.

The initial set is adapted from `multica-ai/andrej-karpathy-skills`:

- Think before coding: surface assumptions and ask when requirements are unclear.
- Focused implementation: avoid speculative abstractions and keep diffs focused.
- Goal-driven execution: define checks, run them, and report the result.

The CLI can validate skills and attach them to a run:

```bash
agent skill check
agent run --spec example --skill goal-driven-execution "Implement this feature"
```

## Building files from a spec

`agent run` prints the model's text reply and stops there — it never touches the filesystem. `agent build` is the command that turns a reply into real files:

- `core/fileset.py` defines the parsing/writing contract: `parse_generated_files` extracts `FILE: <path>` markers and their following fenced code block into `GeneratedFile` records, `resolve_target_path` rejects absolute paths and `..` traversal, and `write_generated_files` writes to disk, refusing to overwrite existing files unless `force=True`.
- `skills/agent/file-output-contract.md` documents that exact reply format. `cli.build()` always attaches it (independent of `--skill`/`--all-skills`), so the model is told how to reply in a parseable way regardless of what other skills are selected.
- `cli.handle_build_command()` wires the two together: no `FILE:` blocks means it just prints the raw reply with a stderr warning; blocks found and no `--apply` means it prints the write plan only; `--apply` performs the write, and requires `--force` to overwrite existing files.

This keeps the same inward-facing import rule as the rest of the project: `core/fileset.py` has no dependency on `cli.py`, providers, or skills — it only knows about plain text and paths.

### `--spec` accepts any path, so `build` validates it first

`resolve_spec`/`resolve_markdown` check whether the given string is an existing path before trying it as a slug under the spec root, so `--spec` on both `run` and `build` already accepts a spec file anywhere on disk, not just one under `specs/cli/`. That is convenient but means `agent build` can be pointed at a spec that was never checked — spending a real model call on a spec missing required sections wastes it. `cli._validate_spec_or_raise()` runs the same `validate_spec()` used by `agent spec check` before `build()` constructs the agent or calls the model: by default it only prints the errors to stderr and continues (a spec doesn't have to be complete to give useful context); with `--strict` it raises `SpecValidationError`, which `handle_build_command()` catches and reports with a pointer to `agent spec check <spec>`, before any provider is built or API call made.
