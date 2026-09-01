import pytest
from pydantic import ValidationError

from src.config import Settings


def test_settings_requires_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        Settings()


def test_settings_reads_runtime_environment(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    settings = Settings()
    assert settings.anthropic_api_key == "test-key"
