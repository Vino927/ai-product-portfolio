"""Orchestrates requirements extraction -> technical specification generation."""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any

from orchestration.watchdog import PipelineWatchdog
from src.agents.requirements_extractor.agent import RequirementsExtractorAgent
from src.agents.techspec_generator.agent import TechSpecGeneratorAgent
from src.config import AppConfig, GuardrailsConfig, Settings


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(content, encoding="utf-8")
    os.replace(temp_path, path)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    _atomic_write(path, json.dumps(data, indent=2, sort_keys=True))


def run_pipeline(
    *,
    input_path: Path,
    output_dir: Path,
    log_root: Path,
    settings: Settings,
    app_config: AppConfig,
    guardrails: GuardrailsConfig,
) -> dict[str, Any]:
    run_id = uuid.uuid4().hex
    run_dir = log_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    started_wall = time.time()
    started_mono = time.monotonic()
    watchdog = PipelineWatchdog(guardrails.pipeline.max_execution_seconds)

    pipeline_log: dict[str, Any] = {
        "run_id": run_id,
        "status": "started",
        "input_file": str(input_path),
        "output_dir": str(output_dir),
        "started_at_epoch": started_wall,
        "model": app_config.model.name,
    }

    try:
        if not input_path.is_file():
            raise FileNotFoundError(f"Input transcript not found: {input_path}")

        transcript = input_path.read_text(encoding="utf-8")
        watchdog.check()

        requirements_agent = RequirementsExtractorAgent(settings, app_config, guardrails)
        req_started = time.monotonic()
        req_result = requirements_agent.extract(transcript)
        _atomic_write(output_dir / "brd.md", req_result.text)
        _write_json(
            run_dir / "extract_reqs.log.json",
            {
                "run_id": run_id,
                "agent": "requirements_extractor",
                "status": "success",
                "duration_seconds": round(time.monotonic() - req_started, 3),
                "usage": req_result.usage,
            },
        )

        watchdog.check()
        techspec_agent = TechSpecGeneratorAgent(settings, app_config, guardrails)
        spec_started = time.monotonic()
        spec_result = techspec_agent.generate(req_result.text)
        _atomic_write(output_dir / "techspec.md", spec_result.text)
        _write_json(
            run_dir / "generate_techspec.log.json",
            {
                "run_id": run_id,
                "agent": "techspec_generator",
                "status": "success",
                "duration_seconds": round(time.monotonic() - spec_started, 3),
                "usage": spec_result.usage,
            },
        )

        pipeline_log["status"] = "success"
        pipeline_log["artifacts"] = {
            "brd": str(output_dir / "brd.md"),
            "techspec": str(output_dir / "techspec.md"),
        }
        pipeline_log["usage"] = {
            "input_tokens": req_result.usage["input_tokens"] + spec_result.usage["input_tokens"],
            "output_tokens": req_result.usage["output_tokens"] + spec_result.usage["output_tokens"],
        }
        return pipeline_log
    except Exception as exc:
        pipeline_log["status"] = "failed"
        pipeline_log["error_type"] = type(exc).__name__
        pipeline_log["error"] = str(exc)
        raise
    finally:
        pipeline_log["duration_seconds"] = round(time.monotonic() - started_mono, 3)
        _write_json(run_dir / "pipeline.log.json", pipeline_log)
