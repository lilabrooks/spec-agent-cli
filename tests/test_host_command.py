from agent_cli.commands.host import HostSnapshot, render_host_details

SNAPSHOT = HostSnapshot(
    hostname="workstation",
    system="Darwin",
    machine="arm64",
    release="25.0.0",
    version="Darwin Kernel Version",
    platform_name="macOS-26.0-arm64-arm-64bit",
    processor="arm",
    python_version="3.14.6",
)


def test_basic_host_details_include_core_fields_only() -> None:
    # Host fixture test: remove with the host command for an actual project.
    output = render_host_details(SNAPSHOT, detailed=False)

    assert output == "\n".join(
        [
            "hostname: workstation",
            "system: Darwin",
            "machine: arm64",
        ]
    )


def test_detailed_host_details_include_runtime_fields() -> None:
    # Host fixture test: remove with the host command for an actual project.
    output = render_host_details(SNAPSHOT, detailed=True)

    assert "hostname: workstation" in output
    assert "release: 25.0.0" in output
    assert "version: Darwin Kernel Version" in output
    assert "platform: macOS-26.0-arm64-arm-64bit" in output
    assert "processor: arm" in output
    assert "python_version: 3.14.6" in output
