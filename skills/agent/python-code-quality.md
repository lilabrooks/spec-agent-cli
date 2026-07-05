---
source: https://docs.astral.sh/ruff/; https://mypy.readthedocs.io/en/stable/command_line.html
owner: Lila Brooks
deciders: [Lila Brooks]
---
# Python code quality

## Purpose
Guide the agent toward clean, typed, lint-friendly Python when implementing CLI features.

## When to use
Use this for any Python source change, especially new modules, parser code, providers, validators, file IO, or tests.

## Rules
- Write Python 3.12+ code using modern standard-library types such as `list[str]`, `dict[str, str]`, and `Path`.
- Keep public function signatures typed.
- Prefer small functions with clear return values over shared mutable state.
- Keep side effects at the command boundary; parsing, validation, and business logic should be callable from tests.
- Use `pathlib.Path` for filesystem paths.
- Avoid broad `except Exception` blocks unless the CLI converts a known failure into a clear user-facing message.
- Keep code passing Ruff lint and format checks.
- Keep imports sorted and unused imports removed.
- Keep strict mypy checks passing.
- Do not add runtime dependencies unless the spec requires them.

## Verification
- Run the unit tests.
- Run `python -m compileall -q src tests`.
- Run `ruff check .`, `ruff format --check .`, and `mypy`.
- Any skipped check must be named with the reason.
