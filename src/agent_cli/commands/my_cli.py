import argparse
import platform
import socket
import sys
from dataclasses import dataclass

# my-cli fixture: this module exists to test the CLI generator repo with a
# concrete generated app. For an actual project, this file and the matching
# `my-cli` entry in pyproject.toml can be commented out or removed.


@dataclass(frozen=True, slots=True)
class MachineSnapshot:
    hostname: str
    system: str
    machine: str
    release: str
    version: str
    platform_name: str
    processor: str
    python_version: str


def collect_machine_snapshot() -> MachineSnapshot:
    return MachineSnapshot(
        hostname=socket.gethostname(),
        system=platform.system(),
        machine=platform.machine(),
        release=platform.release(),
        version=platform.version(),
        platform_name=platform.platform(),
        processor=platform.processor() or "unknown",
        python_version=sys.version.split()[0],
    )


def render_machine_details(snapshot: MachineSnapshot, detailed: bool) -> str:
    details = [
        ("hostname", snapshot.hostname),
        ("system", snapshot.system),
        ("machine", snapshot.machine),
    ]

    if detailed:
        details.extend(
            [
                ("release", snapshot.release),
                ("version", snapshot.version),
                ("platform", snapshot.platform_name),
                ("processor", snapshot.processor),
                ("python_version", snapshot.python_version),
            ]
        )

    return "\n".join(f"{key}: {value}" for key, value in details)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="my-cli",
        description="Print non-sensitive host machine details.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        allow_abbrev=False,
    )
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--basic", action="store_true", help="Print hostname, system, and machine.")
    modes.add_argument(
        "--detailed",
        action="store_true",
        help="Print hostname, OS/runtime, and Python details.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    sys.stdout.write(
        f"{render_machine_details(collect_machine_snapshot(), detailed=args.detailed)}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
