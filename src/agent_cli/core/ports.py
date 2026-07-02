from typing import Protocol

from agent_cli.core.models import CompletionRequest, CompletionResponse


class LanguageModel(Protocol):
    """Minimal interface every provider adapter must implement."""

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Return a text completion for the given request."""
