import pytest

from agent_cli.config.settings import Settings
from agent_cli.providers.registry import available_providers, create_provider
from agent_cli.runtime.factory import build_model


def test_unknown_provider_fails_with_supported_provider_names() -> None:
    with pytest.raises(ValueError, match="Supported providers: echo"):
        build_model(Settings(provider="missing"))


def test_registry_lists_available_providers() -> None:
    assert available_providers() == ["echo"]


def test_create_provider_returns_working_adapter() -> None:
    model = create_provider("echo")

    assert model.__class__.__name__ == "EchoLanguageModel"
