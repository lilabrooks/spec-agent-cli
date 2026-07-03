# my-cli generator test

This guide shows how to test the `my-cli` generated CLI fixture in this repo.

## 1. Enter the project

```bash
cd "/Users/lilabrooks/Documents/Python CLI"
source .venv/bin/activate
```

## 2. Validate the my-cli spec

```bash
agent spec check my-cli-details
```

Expected result:

```text
specs/cli/my-cli-details.md: ok
```

If `agent` fails with `ModuleNotFoundError: No module named 'agent_cli'`, reinstall the project into the virtualenv:

```bash
python -m pip install -e ".[dev]"
```

On macOS, if the error persists, clear hidden flags on the virtualenv and retry:

```bash
chflags -R nohidden .venv
source .venv/bin/activate
agent spec check my-cli-details
```

## 3. Run the implemented my-cli app

Basic mode:

```bash
my-cli --basic
```

Expected shape:

```text
hostname: ...
system: ...
machine: ...
```

Detailed mode:

```bash
my-cli --detailed
```

Expected shape:

```text
hostname: ...
system: ...
machine: ...
release: ...
version: ...
platform: ...
processor: ...
python_version: ...
```

## 4. Test the spec-to-agent prompt path

```bash
agent run --spec my-cli-details \
  --skill goal-driven-execution \
  --skill focused-implementation \
  --skill stdlib-cli-ux \
  --skill cli-test-coverage \
  "Implement this CLI feature"
```

The default provider is `echo`, so this command proves that the Markdown spec and skills are loaded into the agent prompt. It does not call a real AI model yet.

To attach every available skill instead of selecting them one by one:

```bash
agent run --spec my-cli-details --all-skills "Implement this CLI feature"
```

## 5. Run quality checks

```bash
pytest
ruff check .
ruff format --check .
mypy
```

All checks should pass before committing changes.

## 6. Understand build artifact names

If you build the project:

```bash
python -m build
```

The files in `dist/` use the distribution package name, `ai-agent-cli`, normalized to `ai_agent_cli`:

```text
ai_agent_cli-0.1.0.tar.gz
ai_agent_cli-0.1.0-py3-none-any.whl
```

That is expected. The command installed from those artifacts is still:

```bash
my-cli --basic
my-cli --detailed
```

For the full artifact build and pipx install flow, see [pipx-artifact-guide.md](pipx-artifact-guide.md).
