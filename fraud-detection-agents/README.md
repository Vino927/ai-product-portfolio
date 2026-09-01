# Fraud Detection Agents

A production-style agentic AI portfolio project demonstrating a bounded two-agent workflow:

`meeting transcript -> requirements agent -> BRD -> architecture agent -> technical specification`

The project focuses on orchestration, configuration validation, guardrails, failure handling, observability, and separation of prompts from code. The agents are domain-agnostic; a fraud-detection transcript can be used as the portfolio scenario.

## Architecture

```text
src/main.py
  -> validated runtime secrets (src/config.py)
  -> validated application config (config/settings.yaml)
  -> validated guardrails (config/guardrails.yaml)
  -> orchestration/pipeline.py
       -> RequirementsExtractorAgent
       -> TechSpecGeneratorAgent
  -> io/outputs/{brd.md,techspec.md}
  -> logs/runs/<run_id>/*.log.json
```

### Configuration boundary

- Runtime environment: secrets and deployment-specific values only (`ANTHROPIC_API_KEY`, optional API URL override).
- `config/settings.yaml`: non-secret model and execution behavior.
- `config/guardrails.yaml`: per-agent and pipeline resource limits.
- Prompt files: version-controlled next to each agent, not embedded in Python.

The application intentionally does **not** load `.env` files. `.env.example` documents variables for local setup; export them into the process environment before running.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export ANTHROPIC_API_KEY="your-key"
```

## Run the full pipeline

```bash
fraud-agents io/inputs/transcript.txt
```

Optional output locations:

```bash
python -m src.main io/inputs/transcript.txt \
  --output-dir io/outputs \
  --log-dir logs/runs
```

## Outputs

- `io/outputs/brd.md`
- `io/outputs/techspec.md`
- `logs/runs/<run_id>/extract_reqs.log.json`
- `logs/runs/<run_id>/generate_techspec.log.json`
- `logs/runs/<run_id>/pipeline.log.json`

Logs contain status, duration, model token usage, and failure metadata. API keys and prompt/input contents are not logged.

## Representative production run

A sanitized end-to-end run is committed under [`examples/production_run`](examples/production_run/README.md). It shows the transcript input, generated BRD, generated technical specification, and structured per-agent/pipeline logs without exposing secrets or raw provider payloads.

## Failure behavior

- Invalid startup configuration: exit code `2`.
- Pipeline/provider/guardrail failure: exit code `1`.
- Successful run: exit code `0`.
- Provider retries are bounded and only applied to transient failures (429, 5xx, network errors, timeouts).
- Inputs and execution time are bounded by `config/guardrails.yaml`.
- Generated artifacts and JSON logs use atomic file replacement.

See `runbooks/failure_scenarios.md` for operational scenarios.

## Test

Tests do not call the Anthropic API.

```bash
pytest -q
```

## Repository layout

```text
fraud-detection-agents/
├── README.md
├── requirements.txt
├── .env.example
├── config/
│   ├── settings.yaml
│   └── guardrails.yaml
├── src/
│   ├── main.py
│   ├── config.py
│   └── agents/
│       ├── base_agent.py
│       ├── requirements_extractor/
│       │   ├── agent.py
│       │   └── prompt.md
│       └── techspec_generator/
│           ├── agent.py
│           └── prompt.md
├── orchestration/
│   ├── pipeline.py
│   └── watchdog.py
├── io/
│   ├── inputs/
│   └── outputs/
├── logs/runs/
├── tests/
└── runbooks/
    └── failure_scenarios.md
```
