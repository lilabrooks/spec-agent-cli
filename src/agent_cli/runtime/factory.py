from agent_cli.agents.base import Agent
from agent_cli.config.settings import Settings
from agent_cli.core.ports import LanguageModel
from agent_cli.providers.echo import EchoLanguageModel


def build_model(settings: Settings) -> LanguageModel:
    match settings.provider:
        case "echo":
            return EchoLanguageModel()
        case unknown:
            supported = "echo"
            msg = f"Unknown provider {unknown!r}. Supported providers: {supported}."
            raise ValueError(msg)


def build_agent(settings: Settings) -> Agent:
    return Agent(
        name="default-agent",
        system_prompt=settings.system_prompt,
        model=build_model(settings),
    )
