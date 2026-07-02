# Host CLI generator test

This guide shows how to test the host-machine CLI fixture in this repo.

## 1. Enter the project

```bash
cd "/Users/lilabrooks/Documents/Python CLI"
source .venv/bin/activate
```

## 2. Validate the host CLI spec

```bash
agent spec check host-machine-details
```

Expected result:

```text
specs/cli/host-machine-details.md: ok
```

## 3. Run the implemented host command

Basic mode:

```bash
agent host --basic
```

Expected shape:

```text
hostname: ...
system: ...
machine: ...
```

Detailed mode:

```bash
agent host --detailed
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
agent run --spec host-machine-details \
  --skill goal-driven-execution \
  --skill focused-implementation \
  --skill stdlib-cli-ux \
  --skill cli-test-coverage \
  "Implement this CLI feature"
```

The default provider is `echo`, so this command proves that the Markdown spec and skills are loaded into the agent prompt. It does not call a real AI model yet.

## 5. Run quality checks

```bash
pytest
ruff check .
ruff format --check .
mypy
```

All checks should pass before committing changes.

