from src.agents.base_agent import AnthropicAgent, GuardrailViolation
from src.config import AppConfig, ExecutionConfig, ModelConfig, Settings, SkillGuardrail


def make_agent() -> AnthropicAgent:
    settings = Settings.model_construct(
        anthropic_api_key="test",
        anthropic_api_url="https://api.anthropic.com/v1/messages",
    )
    app_config = AppConfig(
        model=ModelConfig(name="test-model", max_tokens=100, api_version="2023-06-01"),
        execution=ExecutionConfig(
            request_timeout_seconds=1,
            max_retries=0,
            retry_backoff_seconds=0,
        ),
    )
    return AnthropicAgent(
        settings=settings,
        app_config=app_config,
        guardrail=SkillGuardrail(max_input_chars=5, max_execution_seconds=1),
        system_prompt="test",
        name="test_agent",
    )


def test_rejects_oversized_input():
    agent = make_agent()
    try:
        agent.run("123456")
    except GuardrailViolation as exc:
        assert "exceeds limit" in str(exc)
    else:
        raise AssertionError("Expected GuardrailViolation")
