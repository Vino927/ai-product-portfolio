"""Shared Anthropic client, retry behavior, prompt loading, and guardrail checks."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.config import AppConfig, Settings, SkillGuardrail


class AgentError(RuntimeError):
    """Base exception for expected agent failures."""


class GuardrailViolation(AgentError):
    """Raised when an agent exceeds a configured safety/resource limit."""


class ProviderError(AgentError):
    """Raised when the model provider request fails or is malformed."""


@dataclass(frozen=True)
class AgentResult:
    text: str
    usage: dict[str, int]


def load_prompt(path: Path) -> str:
    prompt = path.read_text(encoding="utf-8").strip()
    if not prompt:
        raise AgentError(f"Prompt file is empty: {path}")
    return prompt


class AnthropicAgent:
    def __init__(
        self,
        *,
        settings: Settings,
        app_config: AppConfig,
        guardrail: SkillGuardrail,
        system_prompt: str,
        name: str,
    ) -> None:
        self.settings = settings
        self.app_config = app_config
        self.guardrail = guardrail
        self.system_prompt = system_prompt
        self.name = name

    def run(self, user_content: str) -> AgentResult:
        if not user_content.strip():
            raise GuardrailViolation(f"{self.name}: input is empty")
        if len(user_content) > self.guardrail.max_input_chars:
            raise GuardrailViolation(
                f"{self.name}: input length {len(user_content)} exceeds "
                f"limit {self.guardrail.max_input_chars}"
            )

        started = time.monotonic()
        attempts = self.app_config.execution.max_retries + 1
        last_error: Exception | None = None

        for attempt in range(1, attempts + 1):
            self._check_deadline(started)
            try:
                return self._request(user_content)
            except (HTTPError, URLError, TimeoutError, ProviderError) as exc:
                last_error = exc
                if attempt >= attempts or not self._retryable(exc):
                    break
                delay = self.app_config.execution.retry_backoff_seconds * (2 ** (attempt - 1))
                remaining = self.guardrail.max_execution_seconds - (time.monotonic() - started)
                if delay >= remaining:
                    break
                time.sleep(delay)

        raise ProviderError(f"{self.name}: provider request failed after {attempts} attempt(s): {last_error}")

    def _check_deadline(self, started: float) -> None:
        if time.monotonic() - started >= self.guardrail.max_execution_seconds:
            raise GuardrailViolation(f"{self.name}: execution budget exceeded")

    @staticmethod
    def _retryable(exc: Exception) -> bool:
        if isinstance(exc, HTTPError):
            return exc.code == 429 or 500 <= exc.code < 600
        return isinstance(exc, (URLError, TimeoutError))

    def _request(self, user_content: str) -> AgentResult:
        payload = json.dumps(
            {
                "model": self.app_config.model.name,
                "max_tokens": self.app_config.model.max_tokens,
                "system": self.system_prompt,
                "messages": [{"role": "user", "content": user_content}],
            }
        ).encode("utf-8")

        request = Request(
            str(self.settings.anthropic_api_url),
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.settings.anthropic_api_key,
                "anthropic-version": self.app_config.model.api_version,
                "User-Agent": "fraud-detection-agents/1.0",
            },
            method="POST",
        )

        timeout = min(
            self.app_config.execution.request_timeout_seconds,
            self.guardrail.max_execution_seconds,
        )
        with urlopen(request, timeout=timeout) as response:
            data: dict[str, Any] = json.loads(response.read().decode("utf-8"))

        text = "".join(
            block.get("text", "")
            for block in data.get("content", [])
            if block.get("type") == "text"
        ).strip()
        if not text:
            raise ProviderError(f"{self.name}: provider returned no text content")

        raw_usage = data.get("usage", {})
        usage = {
            "input_tokens": int(raw_usage.get("input_tokens", 0)),
            "output_tokens": int(raw_usage.get("output_tokens", 0)),
        }
        return AgentResult(text=text, usage=usage)
