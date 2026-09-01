"""Validated application and runtime configuration."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, HttpUrl, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Secrets and deployment-specific settings supplied by the runtime."""

    model_config = SettingsConfigDict(
        env_file=None,
        case_sensitive=True,
        extra="ignore",
    )

    anthropic_api_key: str = Field(
        ...,
        validation_alias="ANTHROPIC_API_KEY",
        min_length=1,
    )
    anthropic_api_url: HttpUrl = Field(
        "https://api.anthropic.com/v1/messages",
        validation_alias="ANTHROPIC_API_URL",
    )


class ModelConfig(BaseModel):
    name: str = Field(min_length=1)
    max_tokens: int = Field(gt=0, le=8192)
    api_version: str = Field(min_length=1)


class ExecutionConfig(BaseModel):
    request_timeout_seconds: float = Field(gt=0, le=300)
    max_retries: int = Field(ge=0, le=10)
    retry_backoff_seconds: float = Field(ge=0, le=30)


class AppConfig(BaseModel):
    model: ModelConfig
    execution: ExecutionConfig


class SkillGuardrail(BaseModel):
    max_input_chars: int = Field(gt=0)
    max_execution_seconds: float = Field(gt=0, le=600)


class PipelineGuardrail(BaseModel):
    max_execution_seconds: float = Field(gt=0, le=1800)


class GuardrailsConfig(BaseModel):
    requirements_extractor: SkillGuardrail
    techspec_generator: SkillGuardrail
    pipeline: PipelineGuardrail


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Configuration root must be a mapping: {path}")
    return data


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_app_config() -> AppConfig:
    return AppConfig.model_validate(_load_yaml(PROJECT_ROOT / "config" / "settings.yaml"))


@lru_cache(maxsize=1)
def get_guardrails() -> GuardrailsConfig:
    return GuardrailsConfig.model_validate(_load_yaml(PROJECT_ROOT / "config" / "guardrails.yaml"))


def format_validation_error(exc: ValidationError) -> str:
    fields = sorted({".".join(str(part) for part in err["loc"]) for err in exc.errors()})
    return f"Invalid or missing configuration: {', '.join(fields)}"
