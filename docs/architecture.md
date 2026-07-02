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
3. Register it in `runtime/factory.py`.
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
