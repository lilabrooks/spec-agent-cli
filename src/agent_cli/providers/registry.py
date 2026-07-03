"""Single source of truth for provider adapters.

The factory, the unknown-provider error, and the `providers` command all read
from `_PROVIDERS`. Add a real vendor by importing its adapter and adding one
entry here.
"""

from collections.abc import Callable

from agent_cli.core.ports import LanguageModel
from agent_cli.providers.echo import EchoLanguageModel

_PROVIDERS: dict[str, Callable[[], LanguageModel]] = {
    "echo": EchoLanguageModel,
}


def available_providers() -> list[str]:
    return sorted(_PROVIDERS)


def create_provider(name: str) -> LanguageModel:
    try:
        factory = _PROVIDERS[name]
    except KeyError:
        supported = ", ".join(available_providers())
        msg = f"Unknown provider {name!r}. Supported providers: {supported}."
        raise ValueError(msg) from None
    return factory()
