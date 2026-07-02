from pathlib import Path

from agent_cli.core.markdown import list_markdown, load_markdown, resolve_markdown
from agent_cli.skills.document import REQUIRED_SECTIONS, SkillDocument, SkillValidationResult


def load_skill(path: Path) -> SkillDocument:
    document = load_markdown(path)
    return SkillDocument(
        path=document.path,
        title=document.title,
        raw=document.raw,
        body=document.body,
        metadata=document.metadata,
        sections=document.sections,
    )


def list_skills(root: Path) -> list[Path]:
    return list_markdown(root)


def resolve_skill(target: str, root: Path) -> Path:
    return resolve_markdown(target, root, "skill")


def validate_skill(skill: SkillDocument) -> SkillValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not skill.raw.strip():
        errors.append("file is empty")

    if not skill.title.strip():
        errors.append("missing title")

    for section in REQUIRED_SECTIONS:
        if section not in skill.sections:
            errors.append(f"missing required section: {section}")
        elif not skill.sections[section].strip():
            warnings.append(f"section is empty: {section}")

    if "source" not in skill.metadata:
        warnings.append("metadata should include source")

    return SkillValidationResult(
        path=skill.path,
        title=skill.title,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )
