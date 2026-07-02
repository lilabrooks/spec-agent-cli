from pathlib import Path

import pytest

from agent_cli.specs.loader import load_spec, resolve_spec, validate_spec

VALID_SPEC = """---
status: draft
owner: product
---
# Example CLI

## Purpose
Create an example command.

## Commands
- `example run`

## Inputs
- `name`

## Outputs
Greeting text.

## Behavior
Print a greeting.

## Acceptance tests
- Given `name` is `Lila`, output includes `Lila`.
"""


def test_load_spec_extracts_metadata_title_and_sections(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text(VALID_SPEC, encoding="utf-8")

    spec = load_spec(path)

    assert spec.title == "Example CLI"
    assert spec.metadata["status"] == "draft"
    assert "Commands" in spec.sections
    assert "---" not in spec.to_agent_context()


def test_validate_spec_accepts_required_sections(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text(VALID_SPEC, encoding="utf-8")

    result = validate_spec(load_spec(path))

    assert result.ok


def test_resolve_spec_finds_specs_by_slug(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text(VALID_SPEC, encoding="utf-8")

    assert resolve_spec("example", tmp_path) == path


def test_resolve_spec_reports_missing_specs_cleanly(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Spec 'missing' was not found"):
        resolve_spec("missing", tmp_path)
