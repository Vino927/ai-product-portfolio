from src.agents.base_agent import load_prompt
from src.agents.techspec_generator.agent import PROMPT_PATH


def test_techspec_prompt_is_external_and_nonempty():
    assert PROMPT_PATH.name == "prompt.md"
    assert "Technical Specification" in load_prompt(PROMPT_PATH)
