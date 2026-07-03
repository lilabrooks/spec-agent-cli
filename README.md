# Spec Agent CLI

[![Tests](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/tests.yml)
[![Code quality](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/code-quality.yml/badge.svg)](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/code-quality.yml)
[![Coverage](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/coverage.yml/badge.svg)](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/coverage.yml)
![Spec-driven](https://img.shields.io/badge/spec--driven-Markdown-blue)
![Agent-ready](https://img.shields.io/badge/agent--ready-yes-green)
![Model-agnostic](https://img.shields.io/badge/model--agnostic-yes-purple)
![pipx installable](https://img.shields.io/badge/pipx-installable-blue)

A Python 3.12+ starter project for building spec-driven CLI generators. It combines Markdown CLI specs, reusable agent skills, strict Python quality checks, and pluggable model providers without tying the application to one vendor, API, or model family.

## What This Project Provides

- A packaged Python CLI named `agent` for running spec-aware agent workflows.
- A Markdown spec system under `specs/cli/` for describing CLIs before implementation.
- Reusable agent skills under `skills/agent/` for implementation style, testing, packaging, and CLI UX.
- A provider abstraction so model integrations can be swapped without changing command logic.
- A generated fixture command named `my-cli` that proves the generator structure can produce an installable CLI.
- Pytest, Ruff, mypy, coverage, packaging, and pipx-ready project configuration.

The default provider is `echo`, so the project runs locally without credentials or network access.

## Flow

![Spec Agent CLI flow](docs/assets/spec-agent-cli-flow.svg)

## Quick Start

Install the CLI locally with pip:

```bash
python -m pip install .
agent providers
agent run "Write a release note for version 0.1.0"
```

Install it as an isolated command with pipx:

```bash
pipx install .
agent providers
agent run "Write a release note for version 0.1.0"
```

Install directly from GitHub with pipx:

```bash
pipx install "git+https://github.com/lilabrooks/spec-agent-cli.git"
agent providers
my-cli --basic
```

The default specs and skills ship inside the package, so `agent spec` and `agent skill` work from any directory after install. For a complete pipx and artifact guide, see [docs/pipx-artifact-guide.md](docs/pipx-artifact-guide.md).

## Configuration

Two environment variables adjust runtime behavior. They are read directly from the process environment; there is no `.env` auto-loading.

- `AGENT_CLI_PROVIDER` sets the provider adapter (default `echo`). The `--provider` flag overrides it.
- `AGENT_CLI_SYSTEM_PROMPT` sets the system prompt passed to the agent (default `You are a concise, practical assistant.`). The bundled `echo` provider ignores it; real provider adapters will use it.

Export them before running, for example `AGENT_CLI_PROVIDER=echo agent providers`.

## Development Setup

Built and developed on Python 3.14.6. The project supports 3.12+, and CI runs against 3.12, 3.13, and 3.14. Use any interpreter in that range (`python3.14` shown here):

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run lint, type-check, and tests on the active interpreter with a single command:

```bash
make check
```

The underlying tools can also be run individually:

```bash
pytest
ruff check .
ruff format --check .
mypy
```

To run the full check across every supported Python version the way CI does, use `make check-all` (needs [uv](https://docs.astral.sh/uv/), which fetches the interpreters on demand). Save it for reproducing a version-specific failure that CI flags.

Run the CLI locally:

```bash
agent providers
agent spec check
agent skill check
```

## Spec Workflow

Write CLI requirements as Markdown specs in `specs/cli/`. Use `specs/templates/cli-spec.md` as the starting point.

Each spec should include:

- `Purpose`
- `Commands`
- `Inputs`
- `Outputs`
- `Behavior`
- `Acceptance tests`

The installed package ships with default specs. A `specs/cli` folder in your current directory takes precedence, so a checkout or your own project can override them.

Validate specs:

```bash
agent spec check
agent spec check my-cli-details
```

Attach a spec to an agent run:

```bash
agent run --spec my-cli-details "Implement this CLI feature"
```

## Skill Workflow

Agent skills live in `skills/agent/`. They describe how the agent should work while implementing a CLI spec.

Included skills adapted from `multica-ai/andrej-karpathy-skills`:

- `think-before-coding`
- `focused-implementation`
- `goal-driven-execution`

Python and CLI quality skills:

- `python-code-quality`
- `stdlib-cli-ux`
- `cli-test-coverage`
- `python-packaging-cli`

As with specs, default skills ship inside the package, and a `skills/agent` folder in your current directory takes precedence.

Skills are opt-in by default. Attach selected skills with a spec:

```bash
agent run --spec my-cli-details --skill goal-driven-execution --skill stdlib-cli-ux "Implement this feature"
```

Attach every available skill:

```bash
agent run --spec my-cli-details --all-skills "Implement this feature"
```

## Generated CLI Fixture

The repo includes a small generated CLI fixture named `my-cli`. It prints non-sensitive host machine details and exists as a test case for the generator structure.

```bash
my-cli --basic
my-cli --detailed
```

The fixture spec is [specs/cli/my-cli-details.md](specs/cli/my-cli-details.md). The step-by-step test guide is [docs/my-cli-generator-test.md](docs/my-cli-generator-test.md).

## Project Layout

```text
.
├── src/agent_cli/
│   ├── cli.py              # Main `agent` command surface
│   ├── agents/             # Agent behavior and orchestration
│   ├── commands/           # Generated or fixture CLI command modules
│   ├── config/             # Settings and environment loading
│   ├── core/               # Vendor-neutral contracts, shared types, Markdown parsing
│   ├── providers/          # Model/provider adapters
│   ├── runtime/            # Composition root for wiring objects together
│   ├── skills/             # Markdown skill loading and validation
│   └── specs/              # Markdown spec loading and validation
├── skills/
│   ├── agent/              # Agent working-style skills
│   └── templates/          # Reusable skill templates
├── specs/
│   ├── cli/                # CLI specs the agent can work from
│   └── templates/          # Reusable spec templates
├── tests/                  # Fast unit tests
├── docs/                   # Architecture, pipx, and fixture guides
└── pyproject.toml          # Packaging, tools, and CLI entry points
```

## Provider Design

The project keeps provider details behind one small protocol:

```python
class LanguageModel(Protocol):
    def complete(self, request: CompletionRequest) -> CompletionResponse:
        ...
```

Agents receive a `LanguageModel` instance instead of constructing provider clients directly. That keeps the CLI, agent logic, tests, and future provider adapters loosely coupled.

To add a real vendor, implement `LanguageModel` under `src/agent_cli/providers/` and register it in `src/agent_cli/providers/registry.py`. The factory, the unknown-provider error, and the `providers` command all read from that registry.

## Naming and Artifacts

This repository has two important names:

- Distribution package: `ai-agent-cli`
- Installed commands: `agent` and `my-cli`

Build artifacts use the distribution package name normalized for Python packaging. That is why `python -m build` creates files like:

```text
ai_agent_cli-0.1.0.tar.gz
ai_agent_cli-0.1.0-py3-none-any.whl
```

That is expected. The installed commands remain:

```bash
agent providers
my-cli --basic
```

## Quality Standard

Use pytest for behavior tests. Prefer function-level tests with fixtures such as `tmp_path`, `capsys`, and `monkeypatch`.

Ruff handles linting and formatting, and mypy runs in strict mode. Run them together with `make check`, or individually as shown in [Development Setup](#development-setup).

Runtime code should stay dependency-free unless a spec requires a dependency. Development-only tools belong in the `dev` optional dependency group.

## Additional Docs

- [docs/architecture.md](docs/architecture.md)
- [docs/pipx-artifact-guide.md](docs/pipx-artifact-guide.md)
- [docs/my-cli-generator-test.md](docs/my-cli-generator-test.md)
- [docs/skill-research.md](docs/skill-research.md)
- [skills/README.md](skills/README.md)
- [specs/README.md](specs/README.md)
```
