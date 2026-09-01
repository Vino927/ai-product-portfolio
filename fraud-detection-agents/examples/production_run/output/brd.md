# Business Requirements Document

## Business Goals

- Reduce fraud losses by **25% over the next 12 months**.
- Improve fraud-investigation accuracy and efficiency by reducing time spent on false positives.
- Minimize unnecessary friction for legitimate customers while strengthening fraud detection.

## Functional Requirements

### Transaction Risk Scoring

- **FR1 — Real-time scoring:** The system must assign a fraud risk score to each incoming payment transaction in real time.
- **FR2 — Scoring inputs:** Risk scoring must be able to use transaction attributes, customer profile information, and customer history.
- **FR3 — Score availability:** Risk scores must be made available immediately for downstream systems to consume and act on.

### Rules Management

- **FR4 — Business-managed rules:** Fraud operations users must be able to define and modify detection rules without engineering support for routine changes.
- **FR5 — Complex rule conditions:** Rules must support combinations of multiple attributes.
- **FR6 — Pre-production rule testing:** Users must be able to simulate and test rule changes before they are activated in production.

### Machine-Learning Detection

- **FR7 — Supervised detection:** The platform must support supervised models for fraud classification using known fraud labels.
- **FR8 — Unsupervised detection:** The platform must support unsupervised anomaly detection to identify unusual or previously unseen patterns.
- **FR9 — Model lifecycle:** The data-science team must have an interface or portal supporting model training, validation, deployment, and monitoring.

### Alerts and Investigations

- **FR10 — Alert generation:** Transactions that exceed the configured risk threshold must generate an investigation alert.
- **FR11 — Intelligent alert routing:** Alerts must be routed to investigators using factors including severity and current team workload.
- **FR12 — Case management:** Investigators must have a case-management interface for investigating and resolving alerts.

### External Data

- **FR13 — Third-party signals:** The system must support external fraud signals such as device fingerprinting, IP reputation, and external scores.
- **FR14 — Multi-mode ingestion:** Third-party data must be ingestible in both batch and real-time modes.
- **FR15 — Data integration:** External signals must be combined with internal customer and transaction data for detection and scoring.

## Non-Functional Requirements

- **NFR1 — Throughput:** The platform must support peak transaction volumes of approximately **10,000 transactions per second**.
- **NFR2 — Scalability:** The architecture must support scaling capacity as transaction volume grows without requiring major application redesign.
- **NFR3 — Availability:** Fraud-scoring services must be designed for high availability because scoring is part of the transaction path.
- **NFR4 — Security:** Sensitive financial and customer data must be protected with strong encryption and authentication controls.
- **NFR5 — Auditability:** Security-sensitive and operational actions must produce a detailed audit trail.
- **NFR6 — Compliance:** The solution must support applicable obligations discussed in the meeting, including **PCI, GDPR, and CCPA**.
- **NFR7 — Modularity:** Components should be modular and loosely coupled so individual capabilities can be replaced or evolved without major platform-wide changes.
- **NFR8 — Interface stability:** Component interactions should use well-defined interfaces that can evolve without disrupting dependent services.

## Questions & Risks

- **Infrastructure sizing:** Final production capacity and infrastructure sizing need to be validated against expected traffic and growth assumptions.
- **Data consistency and quality:** Reliable scoring depends on consistent, clean, and correctly prepared data across ingestion pipelines.
- **Risk-threshold ownership:** The meeting establishes threshold-based alerting but does not define who owns threshold configuration or approval.
- **Alert-routing policy:** Severity and investigator workload are identified as routing factors, but the exact assignment algorithm and escalation rules remain open.
- **Model governance:** Training, validation, deployment, and monitoring are required, but approval criteria, rollback rules, and model-governance ownership are not yet defined.
- **Availability target:** High availability is required, but a numerical SLO/SLA was not finalized in the meeting.
