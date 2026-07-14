"""Repository health invariants (docs/specs/spec-008-repository-health.md).

These tests guard repo-level consistency rather than package behavior: the
declared version must agree everywhere it appears, and the bundled specs and
skills must pass their own validators.
"""

import filecmp
import re
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest

import agent_cli
from agent_cli.skills.loader import list_skills, load_skill, validate_skill
from agent_cli.specs.loader import list_specs, load_spec, validate_spec

REPO_ROOT = Path(__file__).resolve().parent.parent

ARTIFACT_VERSION = re.compile(r"ai_agent_cli-(\d+\.\d+\.\d+)")
TAG_VERSION = re.compile(r"@v(\d+\.\d+\.\d+)")
PINNED_REQUIREMENT = re.compile(r"^[A-Za-z0-9_.-]+(?:\[[A-Za-z0-9_,.-]+\])?==")


def declared_version() -> str:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = data["project"]["version"]
    assert isinstance(version, str)
    return version


def project_metadata() -> dict[str, object]:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]
    assert isinstance(project, dict)
    return project


def scanner_requirements() -> list[str]:
    return [
        line.strip()
        for line in (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


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
    docs = [REPO_ROOT / "README.md", *sorted((REPO_ROOT / "docs").rglob("*.md"))]
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


def test_scanner_requirements_mirror_optional_dependencies() -> None:
    optional_dependencies = project_metadata()["optional-dependencies"]
    assert isinstance(optional_dependencies, dict)
    expected = sorted(
        dependency for dependencies in optional_dependencies.values() for dependency in dependencies
    )
    actual = sorted(scanner_requirements())
    missing = sorted(set(expected) - set(actual))
    assert not missing, f"requirements.txt is missing optional dependencies: {missing}"


def test_scanner_requirements_avoid_exact_pins() -> None:
    pinned = [line for line in scanner_requirements() if PINNED_REQUIREMENT.match(line)]
    assert not pinned, f"requirements.txt should use lower bounds, not exact pins: {pinned}"


def test_no_tracked_files_match_gitignore() -> None:
    """No committed file should match a .gitignore pattern.

    Guards against build/test artifacts (e.g. the .coverage database) being
    re-committed after they've been ignored. Skipped when run outside a git
    checkout, such as against an installed wheel.
    """
    if shutil.which("git") is None or not (REPO_ROOT / ".git").exists():
        pytest.skip("not a git checkout")
    result = subprocess.run(
        ["git", "ls-files", "-i", "-c", "--exclude-standard"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    tracked_but_ignored = result.stdout.split()
    assert not tracked_but_ignored, (
        f"tracked files match .gitignore (untrack with 'git rm --cached'): {tracked_but_ignored}"
    )


def test_codex_hooks_match_claude_hooks() -> None:
    """The Codex hook mirror must stay byte-identical to the Claude hooks.

    The lifecycle hooks enforce the same OKF guardrails regardless of which
    agent runs, so a hook present in both `.claude/hooks/` and `.codex/hooks/`
    must match byte for byte (ADR-0012, SPEC-008 invariant #7). The Codex stack
    is optional: when `.codex/hooks/` is absent the check no-ops, keeping a
    Claude-only checkout green.
    """
    claude_hooks = REPO_ROOT / ".claude" / "hooks"
    codex_hooks = REPO_ROOT / ".codex" / "hooks"
    if not codex_hooks.is_dir():
        pytest.skip("no Codex hook mirror in this repo")
    mismatched: list[str] = []
    for claude_hook in sorted(claude_hooks.glob("*.sh")):
        codex_hook = codex_hooks / claude_hook.name
        if codex_hook.is_file() and not filecmp.cmp(claude_hook, codex_hook, shallow=False):
            mismatched.append(claude_hook.name)
    assert not mismatched, (
        "Codex hooks have drifted from the Claude source of truth "
        f"(re-sync from .claude/hooks/): {mismatched}"
    )


def test_codex_skills_pair_with_claude_skills() -> None:
    """Every `okf-*` skill must exist in both agent stacks when both are present.

    The playbooks and skills are deliberately adapted per agent, so their
    contents differ; the *set* of skills must stay paired so a capability added
    to one stack is not silently missing from the other (ADR-0012, SPEC-008
    invariant #7). The Codex stack is optional: when `.agents/skills/` is absent
    the check no-ops.
    """
    claude_skills = REPO_ROOT / ".claude" / "skills"
    codex_skills = REPO_ROOT / ".agents" / "skills"
    if not codex_skills.is_dir():
        pytest.skip("no Codex skill mirror in this repo")
    claude_names = {p.name for p in claude_skills.glob("okf-*") if p.is_dir()}
    codex_names = {p.name for p in codex_skills.glob("okf-*") if p.is_dir()}
    assert claude_names == codex_names, (
        "okf-* skills are not paired across the two agent stacks "
        f"(only in .claude: {sorted(claude_names - codex_names)}; "
        f"only in .agents: {sorted(codex_names - claude_names)})"
    )


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
