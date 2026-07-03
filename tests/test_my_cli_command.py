import pytest

from agent_cli.commands.my_cli import MachineSnapshot, main, render_machine_details

SNAPSHOT = MachineSnapshot(
    hostname="workstation",
    system="Darwin",
    machine="arm64",
    release="25.0.0",
    version="Darwin Kernel Version",
    platform_name="macOS-26.0-arm64-arm-64bit",
    processor="arm",
    python_version="3.14.6",
)


def test_basic_my_cli_details_include_core_fields_only() -> None:
    # my-cli fixture test: remove with the my-cli app for an actual project.
    output = render_machine_details(SNAPSHOT, detailed=False)

    assert output == "\n".join(
        [
            "hostname: workstation",
            "system: Darwin",
            "machine: arm64",
        ]
    )


def test_detailed_my_cli_details_include_runtime_fields() -> None:
    # my-cli fixture test: remove with the my-cli app for an actual project.
    output = render_machine_details(SNAPSHOT, detailed=True)

    assert "hostname: workstation" in output
    assert "release: 25.0.0" in output
    assert "version: Darwin Kernel Version" in output
    assert "platform: macOS-26.0-arm64-arm-64bit" in output
    assert "processor: arm" in output
    assert "python_version: 3.14.6" in output


def test_my_cli_basic_command_writes_core_fields(capsys: pytest.CaptureFixture[str]) -> None:
    # my-cli fixture test: remove with the my-cli app for an actual project.
    exit_code = main(["--basic"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "hostname: " in captured.out
    assert "system: " in captured.out
    assert "machine: " in captured.out
    assert "python_version: " not in captured.out
    assert captured.err == ""


def test_my_cli_detailed_command_writes_runtime_fields(capsys: pytest.CaptureFixture[str]) -> None:
    # my-cli fixture test: remove with the my-cli app for an actual project.
    exit_code = main(["--detailed"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "hostname: " in captured.out
    assert "platform: " in captured.out
    assert "python_version: " in captured.out
    assert captured.err == ""


def test_my_cli_requires_one_detail_mode(capsys: pytest.CaptureFixture[str]) -> None:
    # my-cli fixture test: remove with the my-cli app for an actual project.
    with pytest.raises(SystemExit) as error:
        main([])

    captured = capsys.readouterr()
    assert error.value.code == 2
    assert captured.out == ""
    assert "one of the arguments --basic --detailed is required" in captured.err
