"""Pipeline-level execution budget enforcement."""
from __future__ import annotations

import time


class PipelineBudgetExceeded(TimeoutError):
    pass


class PipelineWatchdog:
    def __init__(self, max_execution_seconds: float) -> None:
        self.max_execution_seconds = max_execution_seconds
        self.started = time.monotonic()

    def check(self) -> None:
        elapsed = time.monotonic() - self.started
        if elapsed >= self.max_execution_seconds:
            raise PipelineBudgetExceeded(
                f"Pipeline execution budget exceeded ({self.max_execution_seconds}s)"
            )
