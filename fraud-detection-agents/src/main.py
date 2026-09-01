"""Command-line entry point for the agentic document-generation pipeline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pydantic import ValidationError

from orchestration.pipeline import run_pipeline
from src.config import (
    PROJECT_ROOT,
    format_validation_error,
    get_app_config,
    get_guardrails,
    get_settings,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a meeting transcript into a BRD and technical specification."
    )
    parser.add_argument("input_path", type=Path, help="Path to the source transcript")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "io" / "outputs",
        help="Directory for generated brd.md and techspec.md",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=PROJECT_ROOT / "logs" / "runs",
        help="Directory for per-run structured logs",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        settings = get_settings()
        app_config = get_app_config()
        guardrails = get_guardrails()
    except (ValidationError, FileNotFoundError, ValueError) as exc:
        message = format_validation_error(exc) if isinstance(exc, ValidationError) else str(exc)
        print(f"Startup configuration error: {message}", file=sys.stderr)
        return 2

    try:
        result = run_pipeline(
            input_path=args.input_path,
            output_dir=args.output_dir,
            log_root=args.log_dir,
            settings=settings,
            app_config=app_config,
            guardrails=guardrails,
        )
    except Exception as exc:
        print(f"Pipeline failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(f"Run {result['run_id']} completed successfully.")
    print(f"BRD: {result['artifacts']['brd']}")
    print(f"Tech spec: {result['artifacts']['techspec']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
