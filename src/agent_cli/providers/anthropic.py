from agent_cli.core.models import CompletionRequest, CompletionResponse

DEFAULT_MODEL = "claude-opus-4-8"
DEFAULT_MAX_TOKENS = 1024


class AnthropicLanguageModel:
    """Provider adapter backed by the Anthropic Claude API.

    Requires the `anthropic` package (`pip install ".[anthropic]"`). The
    import is deferred to `complete()` so the rest of the CLI keeps working
    without it installed.
    """

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS) -> None:
        self._model = model
        self._max_tokens = max_tokens

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        import anthropic  # noqa: PLC0415 (kept optional; see module docstring)

        client = anthropic.Anthropic()
        system = "\n\n".join(
            message.content for message in request.messages if message.role == "system"
        )
        messages = [
            {"role": message.role, "content": message.content}
            for message in request.messages
            if message.role in ("user", "assistant")
        ]

        kwargs: dict[str, object] = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system

        response = client.messages.create(**kwargs)
        text = "".join(block.text for block in response.content if block.type == "text")
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        return CompletionResponse(text=text, model=response.model, usage=usage)
