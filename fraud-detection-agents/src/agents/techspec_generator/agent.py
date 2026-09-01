"""Technical-specification generation agent."""
from pathlib import Path

from src.agents.base_agent import AnthropicAgent, AgentResult, load_prompt
from src.config import AppConfig, GuardrailsConfig, Settings

PROMPT_PATH = Path(__file__).with_name("prompt.md")


class TechSpecGeneratorAgent(AnthropicAgent):
    def __init__(self, settings: Settings, app_config: AppConfig, guardrails: GuardrailsConfig):
        super().__init__(
            settings=settings,
            app_config=app_config,
            guardrail=guardrails.techspec_generator,
            system_prompt=load_prompt(PROMPT_PATH),
            name="techspec_generator",
        )

    def generate(self, brd: str) -> AgentResult:
        return self.run(brd)
