# Failure Scenarios

## Missing or invalid runtime configuration
The application validates environment variables and YAML configuration before pipeline execution. It exits with code `2` for startup configuration errors.

## Provider timeout or transient failure
Each agent uses a bounded request timeout and exponential retry. HTTP 429, HTTP 5xx, network errors, and timeouts are retryable up to the configured limit.

## Oversized input
Each agent rejects input exceeding its `max_input_chars` guardrail before making a provider request.

## Pipeline execution budget exceeded
The pipeline watchdog checks the aggregate execution budget between agent stages and fails the run when the configured limit is reached.

## Partial run
Artifacts are written atomically. Each run receives a unique ID and structured JSON logs under `logs/runs/<run_id>/`. A failed pipeline records the exception type and message in `pipeline.log.json`.

## Secret handling
`ANTHROPIC_API_KEY` must be injected by the runtime. The application does not load `.env` files, and `.env` is gitignored.
