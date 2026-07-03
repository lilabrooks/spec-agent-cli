# pipx artifact guide

This guide shows how to create an installable artifact and test it with pipx.

## 1. Enter the project

```bash
cd "/Users/lilabrooks/Documents/Python CLI"
source .venv/bin/activate
```

## 2. Run quality checks

```bash
pytest
ruff check .
ruff format --check .
mypy
```

Fix any failures before building.

## 3. Install the build tool

If `build` is not installed in the virtualenv:

```bash
python -m pip install build
```

## 4. Build the artifacts

```bash
python -m build
```

Expected output files:

```text
dist/ai_agent_cli-0.1.0.tar.gz
dist/ai_agent_cli-0.1.0-py3-none-any.whl
```

The artifact names use the distribution package name, `ai-agent-cli`, normalized to `ai_agent_cli`. The installed commands are still `agent` and `my-cli`.

## 5. Install the wheel with pipx

```bash
pipx install dist/ai_agent_cli-0.1.0-py3-none-any.whl
```

If `ai-agent-cli` is already installed with pipx, reinstall it:

```bash
pipx reinstall ai-agent-cli
```

For local development, install the project in editable mode:

```bash
pipx install -e .
```

## 6. Test the installed commands

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

## 7. Move the artifact

The portable file to share is the wheel:

```text
dist/ai_agent_cli-0.1.0-py3-none-any.whl
```

On another machine with Python and pipx installed:

```bash
pipx install /path/to/ai_agent_cli-0.1.0-py3-none-any.whl
my-cli --basic
```

## 8. Uninstall

```bash
pipx uninstall ai-agent-cli
```

