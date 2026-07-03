"""Resolve default spec and skill roots.

The CLI works two ways. Inside a checkout (or any project that keeps its own
`specs/cli` and `skills/agent` folders) the current directory wins, so you can
edit specs and see the change immediately. Installed via pipx from anywhere
else, the defaults bundled into the package take over.
"""

from importlib import resources
from pathlib import Path

CWD_SPEC_ROOT = Path("specs/cli")
CWD_SKILL_ROOT = Path("skills/agent")


def _has_markdown(root: Path) -> bool:
    return root.is_dir() and any(root.rglob("*.md"))


def _bundled_root(*parts: str) -> Path:
    base = resources.files("agent_cli") / "_bundled"
    for part in parts:
        base = base / part
    return Path(str(base))


def default_spec_root() -> Path:
    if _has_markdown(CWD_SPEC_ROOT):
        return CWD_SPEC_ROOT
    bundled = _bundled_root("specs", "cli")
    if _has_markdown(bundled):
        return bundled
    return CWD_SPEC_ROOT


def default_skill_root() -> Path:
    if _has_markdown(CWD_SKILL_ROOT):
        return CWD_SKILL_ROOT
    bundled = _bundled_root("skills", "agent")
    if _has_markdown(bundled):
        return bundled
    return CWD_SKILL_ROOT
