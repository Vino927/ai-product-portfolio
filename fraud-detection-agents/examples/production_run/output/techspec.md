# Technical Specification

## 1. Architecture Overview

The solution is organized as a set of loosely coupled capabilities connected through stable, versioned interfaces.

### Core Components

1. **Transaction Intake** — receives payment transactions and makes them available to the scoring path.
2. **Feature/Data Assembly** — combines transaction attributes, customer profile/history, and available third-party signals into the scoring context.
3. **Risk Scoring Service** — evaluates the assembled context using detection rules and deployed machine-learning models and returns a risk score in real time.
4. **Rules Management Service** — allows authorized fraud-operations users to create, modify, simulate, test, and activate rules.
5. **Model Lifecycle Service** — provides the data-science workflow for training, validation, deployment, and monitoring of supervised and unsupervised models.
6. **Alerting and Routing Service** — creates alerts when configured risk thresholds are exceeded and assigns them using severity and investigator workload.
7. **Case Management Service** — supports investigator review, investigation, disposition, and resolution of alerts.
8. **External Data Ingestion** — accepts device-fingerprinting, IP-reputation, external-score, and other approved third-party signals through batch and real-time ingestion paths.
9. **Audit Service** — records security-sensitive, configuration, model, rule, and investigation activity required for operational traceability and compliance.

No specific cloud provider, database, programming language, message broker, or ML framework is mandated by the BRD.

## 2. Data Flow

### Real-Time Transaction Path

1. A transaction enters the Transaction Intake component.
2. Feature/Data Assembly retrieves or receives relevant transaction attributes, customer profile/history, and available real-time third-party signals.
3. The Risk Scoring Service evaluates applicable rules and deployed detection models.
4. A risk score is returned for immediate downstream consumption.
5. If the score exceeds the configured threshold, the Alerting and Routing Service creates an alert.
6. The alert is assigned using severity and current investigator workload.
7. The investigator works the alert through the Case Management Service and records the disposition.
8. Relevant actions and configuration changes are recorded in the audit trail.

### Batch Data Path

1. External Data Ingestion receives supported third-party datasets in batch mode.
2. Data is validated and associated with the appropriate internal customer or transaction context.
3. Prepared data becomes available to scoring, model-development, and monitoring workflows as applicable.

### Rules Lifecycle

`Draft -> Simulate/Test -> Review/Approval -> Active -> Replaced/Retired`

The BRD requires simulation and testing before production activation. Approval ownership remains an open item.

### Model Lifecycle

`Train -> Validate -> Deploy -> Monitor -> Replace/Roll Back`

The BRD requires lifecycle support but does not define model approval criteria or rollback policy.

## 3. Key Interfaces / APIs

The following interfaces are logical contracts; transport and implementation technology remain open.

### Transaction Scoring

- `POST /v1/risk-scores`
  - Input: transaction attributes, customer identifier/context, and available external signals.
  - Output: risk score and sufficient evaluation metadata for downstream action and auditability.
  - Requirement mapping: FR1–FR3, FR13–FR15.

### Rules Management

- `POST /v1/rules`
- `PUT /v1/rules/{rule_id}`
- `POST /v1/rules/{rule_id}/simulate`
- `POST /v1/rules/{rule_id}/activate`
  - Requirement mapping: FR4–FR6.

### Model Lifecycle

- `POST /v1/models/validation-runs`
- `POST /v1/models/{model_id}/deployments`
- `GET /v1/models/{model_id}/monitoring`
  - Requirement mapping: FR7–FR9.

### Alerts and Cases

- `GET /v1/alerts`
- `POST /v1/alerts/{alert_id}/assignments`
- `GET /v1/cases/{case_id}`
- `PATCH /v1/cases/{case_id}`
  - Requirement mapping: FR10–FR12.

### Third-Party Data

- `POST /v1/external-signals`
- Batch ingestion contract for approved external datasets.
  - Requirement mapping: FR13–FR15.

All externally consumed interfaces should be versioned to support NFR8 and reduce disruption as components evolve.

## 4. Non-Functional Design

### NFR1 — Throughput

- Design the scoring path for the stated peak load of approximately **10,000 transactions per second**.
- Establish performance tests that exercise peak load and expected growth scenarios before production release.
- Keep synchronous scoring-path dependencies bounded so downstream integration does not create uncontrolled latency.

### NFR2 — Scalability

- Keep scoring components independently scalable.
- Avoid designs that require platform-wide redeployment when additional scoring capacity is added.
- Validate capacity using production-like load tests and explicit headroom assumptions.

### NFR3 — Availability

- Remove single points of failure from the transaction-scoring path.
- Isolate failures in non-critical capabilities so they do not unnecessarily stop risk scoring.
- Define health checks, dependency monitoring, and recovery procedures.
- Final numerical availability SLO/SLA remains open.

### NFR4 — Security

- Encrypt sensitive data in transit and at rest.
- Require strong authentication for operational, investigator, rules-management, and model-management interfaces.
- Limit privileged actions to authorized roles.
- Keep secrets outside source control and runtime logs.

### NFR5 — Auditability

Audit records should capture, at minimum, the actor or service identity, timestamp, action, affected resource, and result for:

- rule creation, modification, simulation, and activation;
- model validation and deployment activity;
- alert assignment and case disposition;
- security-sensitive administrative actions.

### NFR6 — Compliance

- Maintain technical controls and evidence needed to support applicable PCI, GDPR, and CCPA obligations identified by the business.
- Treat exact retention, deletion, residency, consent, and access-control requirements as compliance-design inputs that must be confirmed before implementation.

### NFR7 — Modularity

- Separate transaction intake, scoring, rules, model lifecycle, external-data ingestion, alerting, and case management into clear functional boundaries.
- Prevent implementation details of one component from becoming required knowledge for unrelated components.

### NFR8 — Interface Stability

- Use explicit, versioned contracts for component integrations.
- Apply backward-compatible evolution where possible.
- Validate contract changes before rollout to dependent consumers.

## 5. Open Items Carried from BRD

1. Confirm production capacity assumptions and infrastructure-sizing methodology beyond the stated 10,000 transactions/second peak.
2. Define measurable data-quality and consistency controls for internal and third-party ingestion pipelines.
3. Assign ownership and approval authority for fraud risk thresholds.
4. Define alert assignment, escalation, reassignment, and workload-balancing policy.
5. Define model-governance approval criteria, deployment controls, rollback policy, and ownership.
6. Establish the numerical availability SLO/SLA for the real-time scoring path.
7. Confirm detailed PCI, GDPR, and CCPA control requirements, including retention and deletion obligations, with the appropriate compliance stakeholders.
