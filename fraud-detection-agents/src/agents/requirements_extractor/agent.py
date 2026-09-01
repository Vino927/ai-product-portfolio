"""Requirements-extraction agent."""
from pathlib import Path

from src.agents.base_agent import AnthropicAgent, AgentResult, load_prompt
from src.config import AppConfig, GuardrailsConfig, Settings

PROMPT_PATH = Path(__file__).with_name("prompt.md")


class RequirementsExtractorAgent(AnthropicAgent):
    def __init__(self, settings: Settings, app_config: AppConfig, guardrails: GuardrailsConfig):
        super().__init__(
            settings=settings,
            app_config=app_config,
            guardrail=guardrails.requirements_extractor,
            system_prompt=load_prompt(PROMPT_PATH),
            name="requirements_extractor",
        )

    def extract(self, transcript: str) -> AgentResult:
        return self.run(transcript)
