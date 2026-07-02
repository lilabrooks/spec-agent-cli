from dataclasses import dataclass

from agent_cli.core.messages import Message
from agent_cli.core.models import CompletionRequest
from agent_cli.core.ports import LanguageModel


@dataclass(frozen=True, slots=True)
class AgentResult:
    agent_name: str
    text: str


@dataclass(slots=True)
class Agent:
    name: str
    system_prompt: str
    model: LanguageModel

    def run(self, prompt: str) -> AgentResult:
        request = CompletionRequest(
            messages=(
                Message(role="system", content=self.system_prompt),
                Message(role="user", content=prompt),
            )
        )
        response = self.model.complete(request)
        return AgentResult(agent_name=self.name, text=response.text)
