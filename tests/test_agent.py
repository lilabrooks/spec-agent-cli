from agent_cli.agents.base import Agent
from agent_cli.providers.echo import EchoLanguageModel


def test_agent_runs_prompt_through_model() -> None:
    agent = Agent(
        name="test-agent",
        system_prompt="You are terse.",
        model=EchoLanguageModel(),
    )

    result = agent.run("hello")

    assert result.agent_name == "test-agent"
    assert result.text == "Echo provider received: hello"
