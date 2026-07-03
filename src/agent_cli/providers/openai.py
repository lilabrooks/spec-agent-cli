from agent_cli.core.models import CompletionRequest, CompletionResponse

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_MAX_TOKENS = 1024


class OpenAILanguageModel:
    """Provider adapter backed by the OpenAI Chat Completions API.

    Requires the `openai` package (`pip install ".[openai]"`). The import is
    deferred to `complete()` so the rest of the CLI keeps working without it
    installed.
    """

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = DEFAULT_MAX_TOKENS) -> None:
        self._model = model
        self._max_tokens = max_tokens

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        import openai  # noqa: PLC0415 (kept optional; see module docstring)

        client = openai.OpenAI()
        messages = [
            {"role": message.role, "content": message.content}
            for message in request.messages
            if message.role in ("system", "user", "assistant")
        ]

        response = client.chat.completions.create(
            model=self._model,
            max_tokens=self._max_tokens,
            messages=messages,
        )
        text = response.choices[0].message.content or ""
        usage = {}
        if response.usage is not None:
            usage = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
            }
        return CompletionResponse(text=text, model=response.model, usage=usage)
