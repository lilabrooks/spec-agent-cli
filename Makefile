# Local quality checks. Mirrors the GitHub Actions workflows.
#
#   make check       Run lint, type-check, and tests on the active interpreter
#                    (whatever your .venv has). This is the everyday command.
#   make check-all   Run the same checks across every supported Python version.
#                    Uses uv to fetch interpreters on demand; CI already does
#                    this on push, so reach for it mainly to reproduce a
#                    version-specific failure locally.
#
# Individual targets (lint, typecheck, test, coverage) are available too.

PYTHON ?= python
VERSIONS ?= 3.12 3.13 3.14

.PHONY: check lint format typecheck test coverage check-all

check: lint typecheck test

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .

typecheck:
	mypy

test:
	pytest

coverage:
	coverage run -m pytest
	coverage report

check-all:
	@command -v uv >/dev/null 2>&1 || { \
		echo "check-all needs uv (https://docs.astral.sh/uv/). Install it, or run 'make check' per interpreter."; \
		exit 1; \
	}
	@for v in $(VERSIONS); do \
		echo "=== Python $$v ==="; \
		uv run --python $$v --extra dev -- ruff check . && \
		uv run --python $$v --extra dev -- ruff format --check . && \
		uv run --python $$v --extra dev -- mypy && \
		uv run --python $$v --extra dev -- pytest || exit 1; \
	done
	@echo "All versions passed."
