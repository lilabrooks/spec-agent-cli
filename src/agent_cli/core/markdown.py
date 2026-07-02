from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MarkdownDocument:
    path: Path
    title: str
    raw: str
    body: str
    metadata: dict[str, str] = field(default_factory=dict)
    sections: dict[str, str] = field(default_factory=dict)

    @property
    def slug(self) -> str:
        return self.path.stem


def load_markdown(path: Path) -> MarkdownDocument:
    raw = path.read_text(encoding="utf-8")
    body, metadata = split_metadata(raw)
    title = extract_title(body) or path.stem.replace("-", " ").title()
    return MarkdownDocument(
        path=path,
        title=title,
        raw=raw,
        body=body,
        metadata=metadata,
        sections=extract_sections(body),
    )


def list_markdown(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def resolve_markdown(target: str, root: Path, kind: str) -> Path:
    candidate = Path(target)
    if candidate.exists():
        return candidate

    rooted_candidate = root / target
    if rooted_candidate.exists():
        return rooted_candidate

    if not target.endswith(".md"):
        markdown_candidate = root / f"{target}.md"
        if markdown_candidate.exists():
            return markdown_candidate

    matches = [path for path in list_markdown(root) if path.stem == target]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        choices = ", ".join(str(path) for path in matches)
        msg = f"{kind.title()} name {target!r} is ambiguous. Matches: {choices}"
        raise FileNotFoundError(msg)

    msg = f"{kind.title()} {target!r} was not found under {root}."
    raise FileNotFoundError(msg)


def split_metadata(raw: str) -> tuple[str, dict[str, str]]:
    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        return raw, {}

    metadata: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body = "\n".join(lines[index + 1 :])
            return body, metadata
        if ":" in line:
            key, value = line.split(":", maxsplit=1)
            metadata[key.strip()] = value.strip()

    return raw, {}


def extract_title(raw: str) -> str | None:
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return None


def extract_sections(raw: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped.removeprefix("## ").strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)

    return {name: "\n".join(lines).strip() for name, lines in sections.items()}
