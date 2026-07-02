from agent_cli.config.settings import Settings


def test_settings_allow_provider_override() -> None:
    settings = Settings.from_env(provider_override="echo")

    assert settings.provider == "echo"
