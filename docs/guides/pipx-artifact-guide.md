---
title: pipx artifact guide
type: guide
status: current
date: 2026-07-04
owner: Lila Brooks
deciders: [Lila Brooks]
tags: [documentation, guide, pipx, packaging]
---

# pipx artifact guide

This guide shows how to install from GitHub, create an installable artifact, and test both paths with pipx.

## 1. Install directly from GitHub

Use this when someone wants to install the CLI without cloning the repo.

```bash
pipx install "git+https://github.com/lilabrooks/spec-agent-cli.git"
```

Test the installed commands:

```bash
agent providers
my-cli --basic
```

Install from a specific branch:

```bash
pipx install "git+https://github.com/lilabrooks/spec-agent-cli.git@main"
```

Install from a tag after you create one:

```bash
pipx install "git+https://github.com/lilabrooks/spec-agent-cli.git@v0.3.0"
```

Upgrade later:

```bash
pipx upgrade ai-agent-cli
```

Uninstall:

```bash
pipx uninstall ai-agent-cli
```

## 2. Enter the project for local artifact builds

```bash
cd "/Users/lilabrooks/Documents/Python CLI"
source .venv/bin/activate
```

## 3. Run quality checks

```bash
pytest
ruff check .
ruff format --check .
mypy
```

Fix any failures before building.

## 4. Install the build tools

If you did not install the development extra, install the build frontend and backend:

```bash
python -m pip install build hatchling
```

## 5. Build the artifacts

```bash
python -m build
```

Expected output files:

```text
dist/ai_agent_cli-0.3.0.tar.gz
dist/ai_agent_cli-0.3.0-py3-none-any.whl
```

The artifact names use the distribution package name, `ai-agent-cli`, normalized to `ai_agent_cli`. The installed commands are still `agent` and `my-cli`.

## 6. Install the wheel with pipx

```bash
pipx install dist/ai_agent_cli-0.3.0-py3-none-any.whl
```

If `ai-agent-cli` is already installed with pipx, reinstall it:

```bash
pipx reinstall ai-agent-cli
```

For local development, install the project in editable mode:

```bash
pipx install -e .
```

## 7. Test the installed commands

```bash
agent providers
agent spec check my-cli-details
my-cli --basic
my-cli --detailed
```

Expected `my-cli --basic` shape:

```text
hostname: ...
system: ...
machine: ...
```

## 8. Move the artifact

The portable file to share is the wheel:

```text
dist/ai_agent_cli-0.3.0-py3-none-any.whl
```

On another machine with Python and pipx installed:

```bash
pipx install /path/to/ai_agent_cli-0.3.0-py3-none-any.whl
my-cli --basic
```

## 9. Uninstall

```bash
pipx uninstall ai-agent-cli
```
