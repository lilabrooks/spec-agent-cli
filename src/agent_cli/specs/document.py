from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_SECTIONS = (
    "Purpose",
    "Commands",
    "Inputs",
    "Outputs",
    "Behavior",
    "Acceptance tests",
)


@dataclass(frozen=True, slots=True)
class SpecDocument:
    path: Path
    title: str
    raw: str
    body: str
    metadata: dict[str, str] = field(default_factory=dict)
    sections: dict[str, str] = field(default_factory=dict)

    @property
    def slug(self) -> str:
        return self.path.stem

    def to_agent_context(self) -> str:
        metadata = "\n".join(f"- {key}: {value}" for key, value in sorted(self.metadata.items()))
        metadata_block = metadata or "- none"
        return (
            f"# CLI spec: {self.title}\n\n"
            f"Path: {self.path}\n\n"
            f"Metadata:\n{metadata_block}\n\n"
            "Use this Markdown spec as the source of truth for the CLI behavior.\n\n"
            f"{self.body.strip()}\n"
        )


@dataclass(frozen=True, slots=True)
class SpecValidationResult:
    path: Path
    title: str
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors

    def format(self) -> str:
        status = "ok" if self.ok else "failed"
        lines = [f"{self.path}: {status}"]
        lines.extend(f"  Error: {error}" for error in self.errors)
        lines.extend(f"  Warning: {warning}" for warning in self.warnings)
        return "\n".join(lines)
