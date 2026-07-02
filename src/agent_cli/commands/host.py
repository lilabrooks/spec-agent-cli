import platform
import socket
import sys
from dataclasses import dataclass

# Host fixture: this module exists to test the CLI generator repo with a
# concrete generated command. For an actual project, this file and the
# matching wiring in cli.py can be commented out or removed.


@dataclass(frozen=True, slots=True)
class HostSnapshot:
    hostname: str
    system: str
    machine: str
    release: str
    version: str
    platform_name: str
    processor: str
    python_version: str


def collect_host_snapshot() -> HostSnapshot:
    return HostSnapshot(
        hostname=socket.gethostname(),
        system=platform.system(),
        machine=platform.machine(),
        release=platform.release(),
        version=platform.version(),
        platform_name=platform.platform(),
        processor=platform.processor() or "unknown",
        python_version=sys.version.split()[0],
    )


def render_host_details(snapshot: HostSnapshot, detailed: bool) -> str:
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
