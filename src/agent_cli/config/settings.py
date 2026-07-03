from dataclasses import dataclass
from os import environ

DEFAULT_PROVIDER = "echo"
DEFAULT_SYSTEM_PROMPT = "You are a concise, practical assistant."


@dataclass(frozen=True, slots=True)
class Settings:
    provider: str = DEFAULT_PROVIDER
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    model: str | None = None

    @classmethod
    def from_env(cls, provider_override: str | None = None) -> "Settings":
        provider = provider_override or environ.get("AGENT_CLI_PROVIDER", DEFAULT_PROVIDER)
        system_prompt = environ.get("AGENT_CLI_SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)
        model = environ.get("AGENT_CLI_MODEL")
        return cls(provider=provider, system_prompt=system_prompt, model=model)
