from pathlib import Path

import pytest

from agent_cli.skills.loader import load_skill, resolve_skill, validate_skill

VALID_SKILL = """---
source: test
---
# Example skill

## Purpose
Guide the agent.

## When to use
Use for tests.

## Rules
- Keep it small.

## Verification
- Check the result.
"""


def test_load_skill_extracts_metadata_title_and_sections(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text(VALID_SKILL, encoding="utf-8")

    skill = load_skill(path)

    assert skill.title == "Example skill"
    assert skill.metadata["source"] == "test"
    assert "Rules" in skill.sections
    assert "---" not in skill.to_agent_context()


def test_validate_skill_accepts_required_sections(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text(VALID_SKILL, encoding="utf-8")

    result = validate_skill(load_skill(path))

    assert result.ok


def test_resolve_skill_finds_skills_by_slug(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text(VALID_SKILL, encoding="utf-8")

    assert resolve_skill("example", tmp_path) == path


def test_resolve_skill_reports_missing_skills_cleanly(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Skill 'missing' was not found"):
        resolve_skill("missing", tmp_path)
