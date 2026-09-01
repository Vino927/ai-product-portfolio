from pathlib import Path

import pytest

from src.agents.base_agent import GuardrailViolation, load_prompt
from src.agents.requirements_extractor.agent import PROMPT_PATH


def test_requirements_prompt_is_external_and_nonempty():
    assert PROMPT_PATH.name == "prompt.md"
    assert "Business Requirements Document" in load_prompt(PROMPT_PATH)


def test_load_prompt_rejects_empty_file(tmp_path: Path):
    path = tmp_path / "prompt.md"
    path.write_text("", encoding="utf-8")
    with pytest.raises(Exception):
        load_prompt(path)
