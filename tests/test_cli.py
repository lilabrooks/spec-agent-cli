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


def test_run_command_can_attach_all_skills(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["run", "--spec", "my-cli-details", "--all-skills", "build it"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "# Agent skill: CLI test coverage" in captured.out
    assert "# Agent skill: Focused implementation" in captured.out
    assert "# Agent skill: Goal-driven execution" in captured.out
    assert "# Agent skill: Python code quality" in captured.out
    assert "# Agent skill: Python packaging for CLIs" in captured.out
    assert "# Agent skill: Standard-library CLI UX" in captured.out
    assert "# Agent skill: Think before coding" in captured.out
    assert captured.err == ""


def test_run_command_rejects_all_skills_with_specific_skill(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as error:
        main(["run", "--all-skills", "--skill", "focused-implementation", "build it"])

    captured = capsys.readouterr()
    assert error.value.code == 2
    assert captured.out == ""
    assert "Error:" in captured.err
    assert "not allowed with argument" in captured.err
    assert "Try 'agent run --help' for available options." in captured.err


def test_missing_command_explains_available_help(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main([])

    captured = capsys.readouterr()
    assert error.value.code == 2
    assert captured.out == ""
    assert "Error: the following arguments are required: command" in captured.err
    assert "Try 'agent --help' for available options." in captured.err


def test_missing_spec_exits_with_clean_error(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["run", "--spec", "missing", "hello"])

    captured = capsys.readouterr()
    assert error.value.code == 1
    assert captured.out == ""
    assert captured.err == (
        "Error: Spec 'missing' was not found under specs/cli.\n"
        "Try 'agent spec list' or 'agent skill list' to see available files.\n"
    )


def test_unknown_provider_exits_with_clear_next_step(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["run", "--provider", "missing", "hello"])

    captured = capsys.readouterr()
    assert error.value.code == 1
    assert captured.out == ""
    assert captured.err == (
        "Error: Unknown provider 'missing'. Supported providers: echo.\n"
        "Try 'agent providers' to see available providers.\n"
    )
