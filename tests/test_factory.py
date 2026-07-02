import pytest

from agent_cli.config.settings import Settings
from agent_cli.runtime.factory import build_model


def test_unknown_provider_fails_with_supported_provider_names() -> None:
    with pytest.raises(ValueError, match="Supported providers: echo"):
        build_model(Settings(provider="missing"))
