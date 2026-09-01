
# Fraud Detection Multi-Agent Pipeline - Requirements and Technical Specification 

A multi-agent workflow that turns business meeting notes into structured business requirements and a technical specification.

The project uses two specialized Claude agents with structured handoffs, configurable guardrails, retry and timeout handling, validated configuration, and per-run logging.

## How It Works

```text
Business Meeting Notes
         │
         ▼
┌──────────────────────────┐
│ Requirements Extractor   │
│                          │
│ Extracts requirements,   │
│ constraints, assumptions │
│ and acceptance criteria  │
└────────────┬─────────────┘
             │
             │ Structured handoff
             ▼
┌──────────────────────────┐
│ Tech Spec Generator      │
│                          │
│ Converts requirements    │
│ into an implementation   │
│ specification            │
└────────────┬─────────────┘
             │
             ▼
      Technical Specification
```

The project focuses on orchestration, configuration validation, guardrails, failure handling, observability, and separation of prompts from code. The agents are domain-agnostic; a fraud-detection transcript can be used as the portfolio scenario.

## Agents
### Requirements Extractor
Reads meeting notes and converts unstructured business discussion into a structured BRD containing requirements, constraints, assumptions, and acceptance criteria.
### Tech Spec Generator
Consumes the BRD produced by the first agent and generates a technical specification covering implementation considerations, interfaces, data flow, and operational requirements.

## Guardrails
- Operational limits are defined separately from agent code in config/guardrails.yaml.
- Controls include:
- Execution time limits
- Input-size limits
- Retry limits
- Agent-level resource limits
- Pipeline-level budgets

### Configuration
```
Environment Variables
└── API credentials

config/settings.yaml
└── Non-secret application settings

config/guardrails.yaml
└── Agent and pipeline limits
```
The application intentionally does **not** load `.env` files. `.env.example` documents variables for local setup; export them into the process environment before running.

## Observability
Each execution receives a run ID.

logs/runs/{run_id}/
├── extract_reqs.log.json
├── generate_techspec.log.json
└── pipeline.log.json

The logs capture execution status, timing, model usage, and pipeline-level information so activity from the two agents can be correlated.
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
