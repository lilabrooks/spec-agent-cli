# AI agent CLI

[![Tests](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/tests.yml)
[![Code quality](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/code-quality.yml/badge.svg)](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/code-quality.yml)
[![Coverage](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/coverage.yml/badge.svg)](https://github.com/lilabrooks/spec-agent-cli/actions/workflows/coverage.yml)
![Spec-driven](https://img.shields.io/badge/spec--driven-Markdown-blue)
![Agent-ready](https://img.shields.io/badge/agent--ready-yes-green)
![Model-agnostic](https://img.shields.io/badge/model--agnostic-yes-purple)
![pipx installable](https://img.shields.io/badge/pipx-installable-blue)

A Python 3.12+ starter structure for building a CLI around AI agents without tying the app to one vendor, API, or model family.

## Layout

```text
.
├── src/agent_cli/
│   ├── cli.py              # Command surface
│   ├── agents/             # Agent behavior and orchestration
│   ├── config/             # Settings and environment loading
│   ├── core/               # Vendor-neutral contracts, shared types, Markdown parsing
│   ├── providers/          # Model/provider adapters
│   ├── skills/             # Markdown skill loading and validation
│   ├── specs/              # Markdown spec loading and validation
│   └── runtime/            # Composition root for wiring objects together
├── skills/
│   ├── agent/              # Agent working style skills
│   └── templates/          # Reusable skill templates
├── specs/
│   ├── cli/                # CLI specs the agent can work from
│   └── templates/          # Reusable spec templates
├── tests/                  # Fast unit tests
├── docs/                   # Design notes and operational docs
└── pyproject.toml          # Packaging, tools, and CLI entry point
```

## Quick start

Install as a CLI with pip:

```bash
python -m pip install .
agent run "Write a release note for version 0.1.0"
```

Install as an isolated CLI with pipx:

```bash
pipx install .
agent run "Write a release note for version 0.1.0"
```

Install directly from GitHub with pipx:

```bash
pipx install "git+https://github.com/lilabrooks/spec-agent-cli.git"
agent providers
my-cli --basic
```

Install for local development:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
agent run "Write a release note for version 0.1.0"
agent spec check
agent spec show example
agent skill check
agent skill list
pytest
ruff check .
ruff format --check .
mypy
```

The default provider is `echo`, so the CLI runs locally without credentials. The runtime path uses only the Python standard library. Add real model vendors under `src/agent_cli/providers/` by implementing `LanguageModel`.

## Naming

This repo has two kinds of names:

- Distribution package: `ai-agent-cli`
- Installed commands: `agent` and `my-cli`

Build artifacts use the distribution package name. That is why `python -m build` creates files like:

```text
ai_agent_cli-0.1.0.tar.gz
ai_agent_cli-0.1.0-py3-none-any.whl
```

The generated fixture app is still installed and run as:

```bash
my-cli --basic
my-cli --detailed
```

See [docs/pipx-artifact-guide.md](docs/pipx-artifact-guide.md) for GitHub, wheel, and local pipx install flows.

## Quality standard

Use pytest for all tests. Prefer function tests with fixtures such as `tmp_path`, `capsys`, and `monkeypatch`.

Use Ruff for linting and formatting:

```bash
ruff check .
ruff format .
```

Use mypy in strict mode for type checking:

```bash
mypy
```

Runtime code should stay dependency-free unless a spec requires a dependency. Development tools belong in the `dev` optional dependency group.

## Spec workflow

Put CLI build specs in `specs/cli/` using `specs/templates/cli-spec.md`.

Each spec should include:

- `Purpose`
- `Commands`
- `Inputs`
- `Outputs`
- `Behavior`
- `Acceptance tests`

The CLI can validate specs and attach one to an agent run:

```bash
agent spec check specs/cli/example.md
agent run --spec example "Implement this CLI feature"
```

The repo includes a concrete generated-CLI fixture:

```bash
my-cli --basic
my-cli --detailed
```

See [docs/my-cli-generator-test.md](docs/my-cli-generator-test.md) for the full step-by-step test flow.

## Skill workflow

Agent skills live in `skills/agent/`. They describe how the agent should work while implementing a CLI spec.

Included skills, adapted from `multica-ai/andrej-karpathy-skills`:

- `think-before-coding`
- `focused-implementation`
- `goal-driven-execution`

Python and CLI quality skills:

- `python-code-quality`
- `stdlib-cli-ux`
- `cli-test-coverage`
- `python-packaging-cli`

Use one or more skills with a spec:

```bash
agent skill check
agent run --spec example --skill goal-driven-execution --skill stdlib-cli-ux "Implement this feature"
```

## Design

The project keeps provider details behind one small protocol:

```python
class LanguageModel(Protocol):
    def complete(self, request: CompletionRequest) -> CompletionResponse:
        ...
```

Agents receive a `LanguageModel` instance instead of constructing clients directly. That keeps the CLI, agent logic, tests, and future provider adapters loosely coupled.

Markdown parsing is shared through `agent_cli.core.markdown`, while specs and skills keep their own validation rules. That gives both document types the same frontmatter, title, section, list, and path-resolution behavior without mixing their responsibilities.
