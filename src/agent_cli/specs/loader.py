from pathlib import Path

from agent_cli.core.markdown import list_markdown, load_markdown, resolve_markdown
from agent_cli.specs.document import REQUIRED_SECTIONS, SpecDocument, SpecValidationResult


def load_spec(path: Path) -> SpecDocument:
    document = load_markdown(path)
    return SpecDocument(
        path=document.path,
        title=document.title,
        raw=document.raw,
        body=document.body,
        metadata=document.metadata,
        sections=document.sections,
    )


def list_specs(root: Path) -> list[Path]:
    return list_markdown(root)


def resolve_spec(target: str, root: Path) -> Path:
    return resolve_markdown(target, root, "spec")


def validate_spec(spec: SpecDocument) -> SpecValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not spec.raw.strip():
        errors.append("file is empty")

    if not spec.title.strip():
        errors.append("missing title")

    for section in REQUIRED_SECTIONS:
        if section not in spec.sections:
            errors.append(f"missing required section: {section}")
        elif not spec.sections[section].strip():
            warnings.append(f"section is empty: {section}")

    if "status" not in spec.metadata:
        warnings.append("metadata should include status")

    return SpecValidationResult(
        path=spec.path,
        title=spec.title,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )
