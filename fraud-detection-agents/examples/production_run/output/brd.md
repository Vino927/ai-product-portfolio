# Business Requirements Document --- Fraud Detection System

## 1. Business Objective

Reduce fraud losses by **25% within 12 months**, improve investigation
accuracy and efficiency, reduce false-positive work, and avoid adding
friction for legitimate customers.

## 2. Scope

-   Real-time transaction risk scoring using transaction attributes and
    customer profile/history.
-   Fraud rules managed by fraud operations.
-   Simulation/testing of rule changes before production.
-   Supervised fraud classification and unsupervised anomaly detection.
-   Model lifecycle management for training, validation, deployment, and
    monitoring.
-   Risk-based alert generation, investigator routing, and case
    management.
-   Batch and real-time ingestion of external signals such as device
    fingerprinting and IP reputation.

## 3. Functional Requirements

-   **FR-01:** Assign a risk score to each incoming payment in real
    time.
-   **FR-02:** Make risk scores immediately available to downstream
    systems.
-   **FR-03:** Allow fraud operations to create and modify detection
    rules without engineering involvement.
-   **FR-04:** Support rules combining multiple attributes.
-   **FR-05:** Allow rule simulation/testing before production
    activation.
-   **FR-06:** Support supervised classification and unsupervised
    anomaly detection.
-   **FR-07:** Provide model lifecycle capabilities for training,
    validation, deployment, and monitoring.
-   **FR-08:** Generate an alert when a transaction exceeds the
    applicable risk threshold.
-   **FR-09:** Route alerts using severity and team workload.
-   **FR-10:** Provide case-management capabilities for investigation
    and resolution.
-   **FR-11:** Ingest third-party fraud signals in batch and real time.
-   **FR-12:** Associate external signals with relevant internal data.

## 4. Non-Functional Requirements

-   **NFR-01 --- Scalability:** Support approximately **10,000
    transactions/second** at peak and scale as load grows.
-   **NFR-02 --- Availability:** Scale without downtime.
-   **NFR-03 --- Security:** Use strong encryption and authentication.
-   **NFR-04 --- Auditability:** Provide detailed auditability.
-   **NFR-05 --- Compliance:** Support applicable PCI, GDPR, and CCPA
    requirements.
-   **NFR-06 --- Modularity:** Use a modular, loosely coupled
    architecture.
-   **NFR-07 --- Interfaces:** Provide well-defined interfaces that can
    evolve safely.

## 5. Business Rules

-   Transactions exceeding the applicable risk threshold trigger an
    alert.
-   Alert routing considers severity and investigator/team workload.
-   Fraud operations can manage detection rules without routine
    engineering intervention.
-   Rule changes must be testable through simulation before production
    use.

## 6. Data Requirements

-   Transaction attributes.
-   Customer profile and historical data.
-   Known fraud labels for supervised learning.
-   Data suitable for anomaly detection.
-   Device fingerprinting and IP reputation signals.
-   Batch and real-time external feeds.
-   Clean, consistently prepared data across pipelines.

## 7. Dependencies

-   Internal transaction/customer data availability and quality.
-   Fraud labels for supervised model development.
-   Third-party fraud-data providers.
-   Downstream systems capable of consuming risk scores.
-   Infrastructure capable of supporting required transaction volume.
-   Investigation workflows for receiving and resolving alerts.

## 8. Risks

-   Infrastructure sizing remains unresolved.
-   Data consistency across pipelines may affect scoring and model
    quality.
-   Incorrectly prepared data may affect detection accuracy.
-   Insufficiently tested rule changes may adversely affect detection
    behavior.
-   External-data availability or quality may affect accuracy.

## 9. Open Questions

1.  What infrastructure sizing is required?
2.  What latency target defines "immediately" for scoring and downstream
    availability?
3.  What availability target/SLA is required?
4.  What authentication and authorization mechanisms are required?
5.  Which PCI requirements apply to the specific data flows?
6.  How will risk thresholds be defined and governed?
7.  Which third-party data providers will be used?
8.  What data-quality and consistency controls are required?
9.  What investigator workflow states and case-resolution outcomes are
    required?
