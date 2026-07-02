import argparse
import sys
from pathlib import Path

from agent_cli.config.settings import Settings
from agent_cli.runtime.factory import build_agent
from agent_cli.skills.loader import list_skills, load_skill, resolve_skill, validate_skill
from agent_cli.specs.loader import list_specs, load_spec, resolve_spec, validate_spec

DEFAULT_SPEC_ROOT = Path("specs/cli")
DEFAULT_SKILL_ROOT = Path("skills/agent")


def run(
    prompt: str,
    provider: str | None = None,
    spec: str | None = None,
    skills: list[str] | None = None,
) -> str:
    settings = Settings.from_env(provider_override=provider)
    agent = build_agent(settings)
    context_blocks: list[str] = []
    if spec is not None:
        spec_path = resolve_spec(spec, DEFAULT_SPEC_ROOT)
        context_blocks.append(load_spec(spec_path).to_agent_context())
    for skill in skills or []:
        skill_path = resolve_skill(skill, DEFAULT_SKILL_ROOT)
        context_blocks.append(load_skill(skill_path).to_agent_context())
    agent_prompt = "\n\n".join([*context_blocks, f"Task:\n{prompt}"]) if context_blocks else prompt
    result = agent.run(agent_prompt)
    return f"{result.agent_name}: {result.text}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Run vendor-neutral AI agent workflows.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    parser.suggest_on_error = True  # type: ignore[attr-defined]
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run one prompt through the configured agent.")
    run_parser.add_argument("prompt", help="Task or question for the agent.")
    run_parser.add_argument("--provider", "-p", help="Provider adapter to use.")
    run_parser.add_argument("--spec", help="Markdown CLI spec to attach to the agent prompt.")
    run_parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Markdown agent skill to attach. Repeat for multiple skills.",
    )

    spec_parser = subparsers.add_parser("spec", help="Work with Markdown CLI specs.")
    spec_subparsers = spec_parser.add_subparsers(dest="spec_command", required=True)

    spec_list_parser = spec_subparsers.add_parser("list", help="List available CLI specs.")
    spec_list_parser.add_argument(
        "--root", default=str(DEFAULT_SPEC_ROOT), help="Spec root folder."
    )

    spec_show_parser = spec_subparsers.add_parser(
        "show",
        help="Print the agent-ready context for a spec.",
    )
    spec_show_parser.add_argument("spec", help="Spec path or slug.")
    spec_show_parser.add_argument(
        "--root", default=str(DEFAULT_SPEC_ROOT), help="Spec root folder."
    )

    spec_check_parser = spec_subparsers.add_parser("check", help="Validate one spec or all specs.")
    spec_check_parser.add_argument("spec", nargs="?", help="Spec path or slug.")
    spec_check_parser.add_argument(
        "--root", default=str(DEFAULT_SPEC_ROOT), help="Spec root folder."
    )

    skill_parser = subparsers.add_parser("skill", help="Work with Markdown agent skills.")
    skill_subparsers = skill_parser.add_subparsers(dest="skill_command", required=True)

    skill_list_parser = skill_subparsers.add_parser("list", help="List available agent skills.")
    skill_list_parser.add_argument(
        "--root", default=str(DEFAULT_SKILL_ROOT), help="Skill root folder."
    )

    skill_show_parser = skill_subparsers.add_parser(
        "show",
        help="Print the agent-ready context for a skill.",
    )
    skill_show_parser.add_argument("skill", help="Skill path or slug.")
    skill_show_parser.add_argument(
        "--root", default=str(DEFAULT_SKILL_ROOT), help="Skill root folder."
    )

    skill_check_parser = skill_subparsers.add_parser(
        "check",
        help="Validate one skill or all skills.",
    )
    skill_check_parser.add_argument("skill", nargs="?", help="Skill path or slug.")
    skill_check_parser.add_argument(
        "--root", default=str(DEFAULT_SKILL_ROOT), help="Skill root folder."
    )

    subparsers.add_parser("providers", help="Show installed provider adapters.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            write_stdout_line(
                run(prompt=args.prompt, provider=args.provider, spec=args.spec, skills=args.skill)
            )
            return 0

        if args.command == "spec":
            return handle_spec_command(args)

        if args.command == "skill":
            return handle_skill_command(args)

        if args.command == "providers":
            write_stdout_line("echo")
            return 0
    except (FileNotFoundError, ValueError) as error:
        parser.exit(1, f"error: {error}\n")

    parser.error(f"Unknown command {args.command!r}")
    return 2


def write_stdout_line(value: object) -> None:
    sys.stdout.write(f"{value}\n")


def handle_spec_command(args: argparse.Namespace) -> int:
    root = Path(args.root)

    if args.spec_command == "list":
        paths = list_specs(root)
        if not paths:
            write_stdout_line(f"No specs found under {root}.")
            return 0
        for path in paths:
            write_stdout_line(path)
        return 0

    if args.spec_command == "show":
        path = resolve_spec(args.spec, root)
        write_stdout_line(load_spec(path).to_agent_context())
        return 0

    if args.spec_command == "check":
        paths = [resolve_spec(args.spec, root)] if args.spec else list_specs(root)
        if not paths:
            write_stdout_line(f"No specs found under {root}.")
            return 1

        results = [validate_spec(load_spec(path)) for path in paths]
        for result in results:
            write_stdout_line(result.format())
        return 0 if all(result.ok for result in results) else 1

    raise ValueError(f"Unknown spec command {args.spec_command!r}")


def handle_skill_command(args: argparse.Namespace) -> int:
    root = Path(args.root)

    if args.skill_command == "list":
        paths = list_skills(root)
        if not paths:
            write_stdout_line(f"No skills found under {root}.")
            return 0
        for path in paths:
            write_stdout_line(path)
        return 0

    if args.skill_command == "show":
        path = resolve_skill(args.skill, root)
        write_stdout_line(load_skill(path).to_agent_context())
        return 0

    if args.skill_command == "check":
        paths = [resolve_skill(args.skill, root)] if args.skill else list_skills(root)
        if not paths:
            write_stdout_line(f"No skills found under {root}.")
            return 1

        results = [validate_skill(load_skill(path)) for path in paths]
        for result in results:
            write_stdout_line(result.format())
        return 0 if all(result.ok for result in results) else 1

    raise ValueError(f"Unknown skill command {args.skill_command!r}")


if __name__ == "__main__":
    raise SystemExit(main())
