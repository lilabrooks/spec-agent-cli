import pytest

from agent_cli.cli import main


def test_providers_command_writes_available_providers(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["providers"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "echo\n"
    assert captured.err == ""


def test_run_command_writes_agent_result(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["run", "hello"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "default-agent: Echo provider received: hello\n"
    assert captured.err == ""


def test_host_basic_command_writes_core_fields(capsys: pytest.CaptureFixture[str]) -> None:
    # Host fixture test: remove with the host command for an actual project.
    exit_code = main(["host", "--basic"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "hostname: " in captured.out
    assert "system: " in captured.out
    assert "machine: " in captured.out
    assert "python_version: " not in captured.out
    assert captured.err == ""


def test_host_detailed_command_writes_runtime_fields(capsys: pytest.CaptureFixture[str]) -> None:
    # Host fixture test: remove with the host command for an actual project.
    exit_code = main(["host", "--detailed"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "hostname: " in captured.out
    assert "platform: " in captured.out
    assert "python_version: " in captured.out
    assert captured.err == ""


def test_host_command_requires_one_detail_mode(capsys: pytest.CaptureFixture[str]) -> None:
    # Host fixture test: remove with the host command for an actual project.
    with pytest.raises(SystemExit) as error:
        main(["host"])

    captured = capsys.readouterr()
    assert error.value.code == 2
    assert captured.out == ""
    assert "one of the arguments --basic --detailed is required" in captured.err


def test_missing_spec_exits_with_clean_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["run", "--spec", "missing", "hello"])

    captured = capsys.readouterr()
    assert error.value.code == 1
    assert captured.out == ""
    assert captured.err == "error: Spec 'missing' was not found under specs/cli.\n"
