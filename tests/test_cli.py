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


def test_missing_spec_exits_with_clean_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["run", "--spec", "missing", "hello"])

    captured = capsys.readouterr()
    assert error.value.code == 1
    assert captured.out == ""
    assert captured.err == "error: Spec 'missing' was not found under specs/cli.\n"
