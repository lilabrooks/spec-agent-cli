"""Repository health invariants (docs/specs/spec-008-repository-health.md).

These tests guard repo-level consistency rather than package behavior: the
declared version must agree everywhere it appears, and the bundled specs and
skills must pass their own validators.
"""

import re
import tomllib
from pathlib import Path

import agent_cli
from agent_cli.skills.loader import list_skills, load_skill, validate_skill
from agent_cli.specs.loader import list_specs, load_spec, validate_spec

REPO_ROOT = Path(__file__).resolve().parent.parent

ARTIFACT_VERSION = re.compile(r"ai_agent_cli-(\d+\.\d+\.\d+)")
TAG_VERSION = re.compile(r"@v(\d+\.\d+\.\d+)")


def declared_version() -> str:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = data["project"]["version"]
    assert isinstance(version, str)
    return version


def test_package_version_matches_pyproject() -> None:
    assert agent_cli.__version__ == declared_version()


def test_changelog_latest_entry_matches_pyproject() -> None:
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## \[(\d+\.\d+\.\d+)\]", changelog, flags=re.MULTILINE)
    assert match is not None, "CHANGELOG.md has no '## [x.y.z]' release heading"
    assert match.group(1) == declared_version(), (
        f"CHANGELOG.md latest entry is {match.group(1)}, pyproject.toml says {declared_version()}"
    )


def test_docs_reference_current_version() -> None:
    version = declared_version()
    docs = [REPO_ROOT / "README.md", *sorted((REPO_ROOT / "docs").glob("*.md"))]
    stale: list[str] = []
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for pattern in (ARTIFACT_VERSION, TAG_VERSION):
            stale.extend(
                f"{doc.relative_to(REPO_ROOT)}: {found}"
                for found in pattern.findall(text)
                if found != version
            )
    assert not stale, f"stale version references (expected {version}): {stale}"


def test_doc_frontmatter_version_matches_pyproject() -> None:
    version = declared_version()
    frontmatter_version = re.compile(r"^version:\s*(\S+)\s*$", flags=re.MULTILINE)
    stale: list[str] = []
    for doc in sorted((REPO_ROOT / "docs").rglob("*.md")):
        text = doc.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        frontmatter = text.split("\n---", maxsplit=1)[0]
        stale.extend(
            f"{doc.relative_to(REPO_ROOT)}: {found}"
            for found in frontmatter_version.findall(frontmatter)
            if found != version
        )
    assert not stale, f"stale frontmatter versions (expected {version}): {stale}"


def test_bundled_specs_pass_validation() -> None:
    root = REPO_ROOT / "specs" / "cli"
    paths = list_specs(root)
    assert paths, f"no specs found under {root}"
    failures = [
        result.format()
        for result in (validate_spec(load_spec(path)) for path in paths)
        if not result.ok
    ]
    assert not failures, "\n".join(failures)


def test_bundled_skills_pass_validation() -> None:
    root = REPO_ROOT / "skills" / "agent"
    paths = list_skills(root)
    assert paths, f"no skills found under {root}"
    failures = [
        result.format()
        for result in (validate_skill(load_skill(path)) for path in paths)
        if not result.ok
    ]
    assert not failures, "\n".join(failures)
