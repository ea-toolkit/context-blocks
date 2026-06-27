# Context Blocks — Phase 1 Analysis Report

**Documents processed:** 28
**Total entities extracted:** 402
**Unresolved questions:** 215

---

## Current Domain Understanding

Clearview operates cloud-native microservices on Google Cloud Platform with dual processing tracks: medical claims flow Claims Gateway → HealthLogic Rules Engine → Payment Engine, while pharmacy claims process through legacy PharmaCore (2026 migration scheduled). All services coordinate via Confluent Kafka event streaming with PostgreSQL persistence managed through PgBouncer connection pooling. Eligibility Service acts as central API hub providing member verification, accumulator tracking, and benefit reservations across domains. Member Portal provides consumer-facing interface with separate BFF layer handling authentication, data aggregation, and API orchestration to backend services. A major migration is underway to replace HealthLogic Adjudicator with a custom Drools-based rules engine by Q2 2025.

### Key Relationships
- Event-driven architecture with 20+ Kafka event types enables real-time coordination, with accumulator events managing benefit tracking and reservation workflows across all claim processing systems
- Claims Gateway connection pool exhaustion during high-volume institutional claim batches cascades to timeout failures in Eligibility Service calls, demonstrating tight coupling between gateway performance and downstream services
- Payment Engine race conditions between void/reissue operations and nightly NACHA file generation can cause duplicate payments, requiring FOR UPDATE SKIP LOCKED implementation in batching queries
- Fraud Detection integration creates performance constraints on Claims Gateway processing, requiring circuit breaker patterns and denormalized provider profiles to meet 30-second professional claims SLA with additional 120ms fraud scoring overhead
- Rules Engine migration reveals tight coupling between clinical knowledge and technical implementation, with 4,200+ rules requiring parallel testing and clinical expert knowledge transfer before Rachel Dominguez's October contract end

### Open Questions
- What is the current process for clinical teams to request rule changes, and how will this change during the dual maintenance period between HealthLogic and Drools?
- How does PharmaCore integrate with Clearview systems for unified member eligibility and benefit verification across medical and pharmacy claims before the 2026 migration?
- What are the specific features used by the XGBoost fraud model for scoring, and how does it handle claims from new providers with no historical data?
- What is the fallback plan if parallel testing reveals significant issues with the new Drools engine during the Q1-Q2 2025 migration period?
- How will clinical knowledge be captured and transferred before Rachel Dominguez's contract ends in October, given her deep expertise in medical coding systems?

---

## Entities by Document

### architecture-overview.txt
*Comprehensive architecture overview of Clearview Health Plans' claims processing platform, detailing eight primary systems, their interactions, data flows, tech stacks, and infrastructure. Written by Claims Operations engineering lead in November 2025.*

- **Claims Submission API** (api) — REST API exposed by Claims Gateway for claim submission and status retrieval [confidence: 0.9]
- **Eligibility Check API** (api) — REST API exposed by Eligibility Service for member eligibility verification and accumulator queries [confidence: 0.9]
- **Payment API** (api) — REST API exposed by Payment Engine for payment history, remittance advice, and payment holds [confidence: 0.9]
- **GKE Production Cluster (prod-claims-01)** (platform) — Google Kubernetes Engine cluster hosting production claims processing workloads [confidence: 0.9]
- **GKE Non-Production Cluster (nonprod-claims-01)** (platform) — Google Kubernetes Engine cluster hosting development, staging, and QA environments [confidence: 0.9]
- **Cloud SQL PostgreSQL** (software-component) — Managed PostgreSQL 15 database service with high availability failover for claims data storage [confidence: 0.9]
- **Confluent Cloud Kafka** (software-component) — Managed Apache Kafka service for asynchronous message processing and system integration [confidence: 0.9]
- **HashiCorp Vault** (software-component) — Secrets management system for storing and accessing sensitive configuration data [confidence: 0.8]
- **Datadog** (software-component) — Monitoring and alerting platform for metrics, performance monitoring, and system observability [confidence: 0.9]
- **Splunk** (software-component) — Log aggregation and analysis platform for centralized logging across the claims processing systems [confidence: 0.9]
- **Elasticsearch** (software-component) — Search engine powering provider search functionality in the Member Portal [confidence: 0.9]
- **Vertex AI** (software-component) — Google Cloud machine learning platform used for fraud detection model training [confidence: 0.9]
- **Duplicate Detection Process** (process) — Process for identifying and preventing duplicate claim submissions using composite key matching [confidence: 0.9]
- **Claim Routing Process** (process) — Process that routes validated claims to appropriate downstream systems based on business rules [confidence: 0.9]
- **Retroactive Reprocessing** (process) — Automated process that re-adjudicates claims when member enrollment changes are backdated [confidence: 0.9]
- **Payment Cycle Processing** (process) — Nightly batch job process that generates provider payments and member reimbursements [confidence: 0.9]
- **Provider Re-credentialing Process** (process) — Required process to verify provider credentials every 3 years per NCQA standards [confidence: 0.8]
- **Claim Submitted Event** (business-event) — Event triggered when a provider submits a claim through any intake channel [confidence: 0.9]
- **Claim Adjudicated Event** (business-event) — Event emitted when Rules Engine completes adjudication with PAY, DENY, or PEND disposition [confidence: 0.9]
- **Enrollment Change Event** (business-event) — Event triggered when member enrollment data is modified, potentially with retroactive effective dates [confidence: 0.8]
- **Fraud Alert Event** (business-event) — Event generated when fraud detection identifies suspicious patterns requiring SIU investigation [confidence: 0.8]
- **Allowed Amount Calculation** (domain-logic) — Business rule that calculates the maximum payable amount based on provider contract fee schedules [confidence: 0.9]
- **Soft Reservation Logic** (domain-logic) — Business rule preventing over-application of benefit accumulators during concurrent claim processing [confidence: 0.9]
- **Payment Threshold Rules** (domain-logic) — Business rules governing minimum payment amounts and recoupment spreading for provider payments [confidence: 0.9]
- **Fraud Scoring Algorithm** (domain-logic) — ML-based algorithm that scores claims for fraud, waste, and abuse risk using multiple models [confidence: 0.9]
- **Authorization Validity Rules** (domain-logic) — Business rules defining how long prior authorizations remain valid for different service types [confidence: 0.9]
- **EDI 837 Professional** (data-model) — Electronic data interchange format for professional healthcare claims (CMS-1500 equivalent) [confidence: 0.9]
- **EDI 837 Institutional** (data-model) — Electronic data interchange format for institutional healthcare claims (UB-04 equivalent) [confidence: 0.9]
- **ERA 835** (data-model) — Electronic remittance advice format providing payment details to healthcare providers [confidence: 0.9]
- **EDI 270/271** (data-model) — Electronic data interchange format for eligibility inquiry requests and responses [confidence: 0.9]
- **Auth-Required Service Lists** (reference-data) — Lists of medical services that require prior authorization, maintained per benefit plan [confidence: 0.8]
- **TIN** (jargon-business) — Tax Identification Number used for provider payment batching and tax reporting [confidence: 0.9]
- **SIU** (jargon-business) — Special Investigation Unit responsible for investigating potential fraud, waste, and abuse cases [confidence: 0.9]
- **OON** (jargon-business) — Out-of-Network, referring to providers not contracted with the health plan [confidence: 0.9]
- **Member ID** (jargon-business) — Unique identifier for health plan members used across all systems for member identification [confidence: 0.9]
- **HealthLogic Adjudicator** (jargon-tech) — Vendor rules engine product currently running version 4.2, being replaced per ADR-2024-007 [confidence: 0.9]
- **ADR-2024-007** (decision) — Architecture decision record documenting the rationale for replacing HealthLogic Adjudicator [confidence: 0.8]
- **Marcus Reeves** (persona) — Claims Operations team lead responsible for claims processing systems [confidence: 0.9]
- **Priya Anand** (persona) — Claims Operations Engineering Lead and document author [confidence: 0.9]
- **Dana Okafor** (persona) — Member Services team lead responsible for eligibility and member portal systems [confidence: 0.9]
- **James Whitfield** (persona) — Provider Network team lead responsible for provider directory and credentialing [confidence: 0.9]

### original-architecture-2021.txt
*Historical documentation of Clearview Health Plans' 2021 claims processing architecture after migrating from the ClaimsPro monolith to microservices, including original system components, infrastructure setup, known issues, and team structure.*

- **ClaimsPro** (system) — Legacy .NET monolithic claims processing system replaced during 2020-2021 migration [confidence: 0.9]
- **ClaimsPro Inc.** (external-party) — Vendor company that developed and supported the legacy ClaimsPro monolithic system [confidence: 0.9]
- **ClaimsPro Migration Decision** (decision) — Decision to migrate from ClaimsPro monolith to microservices architecture in 2020-2021 [confidence: 0.9]
- **HealthLogic Selection Decision** (decision) — Decision to choose HealthLogic Adjudicator over alternatives for rules engine in 2019 [confidence: 0.9]
- **Samir Patel** (persona) — Former Principal Architect who led the ClaimsPro migration, left Clearview in Q2 2022 [confidence: 0.9]
- **Tom Nguyen** (persona) — Former Senior Engineer on Claims Platform team who left in Q1 2023 [confidence: 0.9]
- **Nina Petrovich** (persona) — Former Senior Engineer who led the Payment Engine rewrite, left in Q4 2022 [confidence: 0.9]
- **Claims Platform Team (2021)** (team) — Original unified team that executed the ClaimsPro migration before being split in late 2022 [confidence: 0.9]
- **RabbitMQ (2021)** (software-component) — Message broker used in original 2021 architecture, later replaced by Kafka in Q2 2022 [confidence: 0.9]
- **GKE Single Cluster (2021)** (platform) — Original single GKE cluster in us-central1 that hosted all services before prod/nonprod separation [confidence: 0.9]
- **Cloud SQL Single Instance (2021)** (software-component) — Original single Cloud SQL PostgreSQL instance without HA failover used in 2021 architecture [confidence: 0.9]
- **Jenkins (2021)** (software-component) — Original CI/CD tool used in 2021, later migrated to GitHub Actions in 2023 [confidence: 0.9]
- **CloudWatch + Grafana (2021)** (software-component) — Original monitoring setup using CloudWatch and custom Grafana dashboards, replaced by Datadog in Q3 2022 [confidence: 0.9]
- **Kubernetes Secrets (2021)** (software-component) — Original secret management using native Kubernetes secrets, later replaced by Vault in 2023 [confidence: 0.9]
- **Dual-Write** (jargon-business) — Migration strategy where data is written to both old and new systems simultaneously during transition [confidence: 0.9]
- **Void/Reissue Workflow** (process) — Payment correction process designed by Nina Petrovich during Payment Engine rewrite [confidence: 0.9]
- **Cascading Failures** (jargon-tech) — System failure pattern where one service failure triggers failures in dependent services [confidence: 0.9]
- **CLV-3904** (jargon-business) — Ticket or issue identifier for ongoing cascading failure problem [confidence: 0.8]

### claims-data-model-reference.txt
*Comprehensive data model reference for Clearview Health Plans claims platform, defining schemas and relationships for core entities including claims, members, providers, benefit plans, payments, fee schedules, authorizations, and accumulators across all platform services.*

- **Claim** (data-model) — The central data entity representing a healthcare service claim submitted for payment processing [confidence: 1.0]
- **Member** (data-model) — Data model representing health plan members and their enrollment information [confidence: 1.0]
- **Provider** (data-model) — Data model representing healthcare providers with credentials and network participation [confidence: 1.0]
- **Benefit Plan** (data-model) — Data model defining member benefit plan configurations and coverage parameters [confidence: 1.0]
- **Payment** (data-model) — Data model representing provider and member payments with void/reissue tracking [confidence: 1.0]
- **Fee Schedule** (data-model) — Data model defining contracted allowed amounts for procedure codes by provider contract [confidence: 1.0]
- **Authorization** (data-model) — Data model for prior authorization requests and approvals with validity tracking [confidence: 1.0]
- **Accumulator** (data-model) — Data model tracking member benefit utilization including deductibles and out-of-pocket maximums [confidence: 1.0]
- **Leo Chen** (persona) — Document author and data model maintainer for claims platform [confidence: 0.9]
- **CLV-4521** (jargon-business) — JIRA ticket tracking accumulator reservation cleanup workaround for Rules Engine crashes [confidence: 0.9]
- **Usual and Customary** (jargon-business) — Pricing methodology for out-of-network providers based on Medicare RBRVS data [confidence: 0.9]
- **RBRVS** (jargon-tech) — Resource-Based Relative Value Scale - Medicare's physician payment methodology [confidence: 1.0]
- **NCQA** (jargon-business) — National Committee for Quality Assurance - healthcare accreditation organization [confidence: 1.0]
- **CARC/RARC** (jargon-business) — Claim Adjustment Reason Code / Remittance Advice Remark Code - standard denial reason codes [confidence: 1.0]
- **Facility Flag** (jargon-business) — Indicator for different payment rates between facility and non-facility service locations [confidence: 0.9]
- **Place of Service Codes** (reference-data) — CMS standardized codes indicating where healthcare services were performed [confidence: 1.0]
- **Facility Type Codes** (reference-data) — Coded values identifying the type of healthcare facility where services were rendered [confidence: 1.0]
- **CPT Modifier Codes** (reference-data) — Two-character codes that provide additional information about procedures to affect payment [confidence: 1.0]
- **ICD-10-CM Codes** (reference-data) — International Classification of Diseases diagnosis codes used in US healthcare claims [confidence: 1.0]
- **Specialty Taxonomy Codes** (reference-data) — Healthcare provider specialty classification codes maintained by NUCC [confidence: 0.9]

### integration-patterns-guide.txt
*Comprehensive guide to integration patterns used across Clearview Health Plans claims platform, covering six patterns: synchronous request-response, event-driven Kafka messaging, batch processing, EDI transaction processing, data replication/denormalization, and external partner integration. Includes anti-patterns to avoid.*

- **Istio Service Mesh** (software-component) — Internal service mesh handling all synchronous inter-service communication with circuit breakers and timeouts [confidence: 0.9]
- **Resilience4j** (software-component) — Circuit breaker library implementing fault tolerance for service-to-service calls [confidence: 0.9]
- **Claim Submitted Event (Kafka)** (business-event) — Kafka event published when Claims Gateway receives and validates a new claim submission [confidence: 0.9]
- **Payment Completed Event** (business-event) — Kafka event published when Payment Engine completes a payment transaction [confidence: 0.9]
- **Enrollment Change Event** (business-event) — Kafka event published when member enrollment or eligibility status changes [confidence: 0.9]
- **Provider Status Changed Event** (business-event) — Kafka event published when provider information or network status changes in Provider Directory [confidence: 0.9]
- **Fraud Alert Generated Event** (business-event) — Kafka event published when Fraud Detection generates a fraud alert requiring investigation [confidence: 0.9]
- **Confluent Schema Registry** (software-component) — Schema registry managing Avro schemas for Kafka message evolution and compatibility [confidence: 0.9]
- **Institutional Claims Intake Batch** (process) — Scheduled batch job processing EDI 837I institutional claims files from clearinghouses [confidence: 0.9]
- **Fraud Model Retraining Batch** (process) — Monthly batch job retraining fraud detection ML models using historical claims and investigation outcomes [confidence: 0.9]
- **Dead Letter Topic (DLT)** (jargon-tech) — Kafka topic pattern for handling failed message processing using .dlt suffix convention [confidence: 0.9]
- **Exactly-Once Semantics** (jargon-tech) — Kafka delivery guarantee ensuring messages are processed exactly once, used for financial transactions [confidence: 0.9]
- **Consumer Groups** (jargon-tech) — Kafka consumer group naming pattern following team.service.purpose convention [confidence: 0.9]
- **EDI Transaction Processing** (process) — Standardized workflow for processing healthcare EDI transactions with clearinghouses and trading partners [confidence: 0.9]
- **Northeast Clearinghouse** (external-party) — Primary healthcare clearinghouse handling ~60% of Clearview's EDI transaction volume [confidence: 0.9]
- **MedConnect Exchange** (external-party) — Healthcare clearinghouse handling ~25% of Clearview's EDI transaction volume [confidence: 0.9]
- **DirectSubmit** (external-party) — Healthcare clearinghouse handling ~15% of Clearview's EDI volume, mostly smaller provider groups [confidence: 0.9]
- **Banking Partner** (external-party) — Financial institution processing EFT/ACH payments and providing settlement confirmations [confidence: 0.9]
- **NACHA Format** (data-model) — Standard file format for ACH/EFT payment transactions sent to banking partners [confidence: 0.9]
- **AS2 Protocol** (jargon-tech) — Applicability Statement 2 protocol for secure real-time EDI transmission [confidence: 0.8]
- **EDI 997/999** (data-model) — Functional acknowledgment transaction sets confirming receipt and processing of EDI documents [confidence: 0.9]
- **Nadia Volkov** (persona) — Claims Operations team member specializing in EDI and clearinghouse integrations [confidence: 0.9]
- **X12 Validator** (jargon-tech) — Tool for validating EDI document compliance with X12 standards before transmission [confidence: 0.8]
- **Data Replication Rules** (domain-logic) — Governance rules for implementing data replication and denormalization across services [confidence: 0.9]
- **Fraud Detection Sync Migration** (decision) — 2025 decision to move fraud detection integration from async Kafka to synchronous HTTP for real-time claim blocking [confidence: 0.9]
- **Manual Payment Approval Gate** (process) — Manual approval process requiring Claims Ops lead approval before releasing payment files to banking partner [confidence: 0.9]
- **2024 Connection Pool Incident** (jargon-business) — Production incident that led to implementing 2,000 claim batch size limits in institutional claims processing [confidence: 0.8]

### claims-processing-workflow.txt
*End-to-end claims processing workflow at Clearview Health Plans covering claim submission through EDI/API/OCR channels, validation, eligibility verification, fraud screening, pre-authorization checks, adjudication, payment processing, and exception flows including appeals and coordination of benefits.*

- **Claims Processing Workflow** (process) — Complete end-to-end workflow for processing health insurance claims from submission to payment [confidence: 0.9]
- **Professional Claims Processing** (process) — Real-time processing of 837P professional claims with 30-second SLA [confidence: 0.9]
- **Institutional Claims Batch Processing** (process) — Batch processing of 837I institutional claims in 4-hour windows [confidence: 0.9]
- **OCR Pipeline Processing** (process) — Paper claims processing through OCR with 94% accuracy and manual fallback [confidence: 0.8]
- **Duplicate Detection Logic** (domain-logic) — Composite key matching logic to identify duplicate claims within 90-day window [confidence: 0.9]
- **Eligibility Date of Service Rule** (domain-logic) — Business rule requiring eligibility verification against date of service, not submission date [confidence: 0.9]
- **Fraud Scoring Thresholds** (domain-logic) — Three-tier fraud scoring system with thresholds at 0.65 and 0.82 for different processing paths [confidence: 0.9]
- **SIU Review Process** (process) — Special Investigations Unit manual review process for high-risk fraud claims [confidence: 0.9]
- **Pre-Authorization Requirements** (domain-logic) — Service-specific authorization rules maintained per benefit plan and updated quarterly [confidence: 0.9]
- **Cost-Sharing Calculation Rules** (domain-logic) — Algorithm for calculating member cost-sharing based on allowed amounts, not billed amounts [confidence: 0.9]
- **Adjudication Disposition Rules** (domain-logic) — Logic determining PAY/DENY/PEND outcomes from rules engine evaluation [confidence: 0.9]
- **EOB Generation Process** (process) — Automated generation of Explanation of Benefits documents for all processed claims [confidence: 0.9]
- **Provider Payment Batching** (process) — Batching of provider payments by TIN per payment cycle with $5 minimum threshold [confidence: 0.9]
- **Member Reimbursement Process** (process) — Processing of member reimbursements for out-of-network claims within 10 business days [confidence: 0.8]
- **Recoupment Distribution Rules** (domain-logic) — Logic for spreading large recoupments exceeding 50% of payment across multiple cycles [confidence: 0.8]
- **Post-Payment Fraud Analysis** (process) — Analysis of flagged claims and provider patterns after payment to identify fraud schemes [confidence: 0.9]
- **Claims Appeals Process** (process) — Two-level appeals process for denied or underpaid claims with internal and external review [confidence: 0.9]
- **Retroactive Enrollment Reprocessing** (process) — Automatic reprocessing of claims when retroactive enrollment changes occur within 60-day window [confidence: 0.9]
- **Coordination of Benefits Logic** (domain-logic) — Business rules for determining payer order and calculating secondary payer responsibility [confidence: 0.8]
- **Provider Network Date of Service Rule** (domain-logic) — Rule applying provider network status as of service date, not processing date [confidence: 0.9]
- **Claims Adjudicator Queue** (jargon-business) — Work queue for manual review of pended claims by senior claims staff [confidence: 0.9]
- **Manual Data Entry Queue** (jargon-business) — Work queue for paper claims that failed OCR processing and require human data entry [confidence: 0.8]
- **Usual and Customary Rate** (jargon-business) — Pricing methodology for out-of-network providers based on regional market rates [confidence: 0.9]
- **Clearview Standard Schedules** (jargon-business) — Internal fee schedules maintained by actuarial team for services without contracted rates [confidence: 0.8]
- **Independent Review Organization** (jargon-business) — External organization providing binding Level 2 appeals review [confidence: 0.9]
- **Actuarial Team** (team) — Team responsible for maintaining Clearview standard fee schedules and risk analysis [confidence: 0.8]
- **Tariq Hassan** (persona) — Fraud Detection team member available for fraud model questions [confidence: 0.9]
- **Fraud Detection Team** (team) — Team responsible for fraud detection models and pattern analysis [confidence: 0.8]

### enrollment-workflow.txt
*A placeholder TODO document outlining the need for comprehensive documentation of member enrollment workflows, including new member enrollment, plan changes, qualifying life events, COBRA, retroactive changes, and EDI 834 processing. Created by Marcus Reeves and assigned to Dana Okafor for completion by Q4 2025.*

- **Member Enrollment Workflow** (process) — End-to-end process for enrolling members in health plans and managing enrollment changes [confidence: 0.9]
- **New Member Enrollment** (process) — Process for enrolling brand new members who are joining a health plan for the first time [confidence: 0.8]
- **Open Enrollment Process** (process) — Annual enrollment period process where existing members can change their health plan coverage [confidence: 0.8]
- **Qualifying Life Events Process** (process) — Process for handling mid-year enrollment changes triggered by qualifying life events [confidence: 0.8]
- **COBRA Enrollment Process** (process) — Process for enrolling members in COBRA continuation coverage after losing employer-sponsored coverage [confidence: 0.9]
- **EDI 834** (data-model) — Standard electronic data interchange format for health insurance enrollment and maintenance transactions [confidence: 0.9]
- **EDI 834 Processing** (process) — Technical process for parsing and processing EDI 834 enrollment files in the Eligibility Service [confidence: 0.8]

### pharmacy-claims.txt
*Placeholder documentation for pharmacy claims processing, which currently operates on the legacy PharmaCore system outside Clearview's main claims platform, with plans for migration in 2026.*

- **PharmaCore** (system) — Legacy system currently processing all pharmacy claims outside the main Clearview platform [confidence: 0.9]
- **Pharmacy Claims Migration (2026)** (process) — Planned migration of pharmacy claims processing from PharmaCore to the main Clearview platform [confidence: 0.8]

### provider-credentialing.txt
*A placeholder document for provider credentialing documentation that was never completed, mentioning NCQA compliance requirements and processes for handling expired credentials during claims adjudication.*


### claims-coding-standards.txt
*Technical coding standards and conventions for the Clearview Health Plans claims platform, covering language choices, API design, naming conventions, code review processes, configuration management, logging standards, HIPAA compliance requirements, and dependency management practices.*

- **Spring Boot** (jargon-tech) — Java application framework used for Claims Gateway, Payment Engine, and Provider Directory [confidence: 1.0]
- **Quarkus** (jargon-tech) — Java framework used specifically for Eligibility Service due to superior cold start performance [confidence: 1.0]
- **FastAPI** (jargon-tech) — Python web framework used for serving Fraud Detection service APIs [confidence: 1.0]
- **Gradle (Kotlin DSL)** (software-component) — Build tool standardized across Java services using Kotlin DSL syntax [confidence: 1.0]
- **Poetry** (software-component) — Python dependency management tool used for Fraud Detection service [confidence: 1.0]
- **Vite** (software-component) — Frontend build tooling used for Member Portal development [confidence: 1.0]
- **Node.js BFF** (software-component) — Backend For Frontend layer serving the Member Portal application [confidence: 0.9]
- **Claims Submission API v2** (api) — Current version of Claims Submission API with improved design over deprecated v1 [confidence: 0.8]
- **Eligibility API v2** (api) — Current version of Eligibility API following platform REST standards [confidence: 0.8]
- **API Versioning Lifecycle** (process) — Platform process for managing API version transitions and deprecation timelines [confidence: 0.9]
- **API Error Response Format** (domain-logic) — Standardized error response structure across all platform APIs [confidence: 1.0]
- **Code Review Process** (process) — Mandatory peer review process with coverage, security, and compatibility requirements [confidence: 1.0]
- **Flyway** (software-component) — Database migration tool used for Java services schema evolution [confidence: 1.0]
- **LaunchDarkly** (software-component) — Feature flag management service currently under consideration for removal [confidence: 0.9]
- **Configuration Precedence Rules** (domain-logic) — Hierarchical configuration override rules from environment variables to application defaults [confidence: 1.0]
- **Structured Logging Format** (domain-logic) — Mandatory JSON logging format with correlation ID and metadata requirements [confidence: 1.0]
- **PII Logging Restrictions** (domain-logic) — HIPAA compliance rules prohibiting Protected Health Information in logs [confidence: 1.0]
- **Splunk Indexes** (reference-data) — Service-specific Splunk log indexes with HIPAA-compliant partitioning [confidence: 1.0]
- **HIPAA Compliance Requirements** (domain-logic) — Comprehensive healthcare data protection requirements covering encryption, access control, and retention [confidence: 1.0]
- **Dependabot** (software-component) — Automated dependency update tool for security patch management [confidence: 1.0]
- **Clearview Hardened Base Images** (reference-data) — Security-hardened container base images stored in Google Artifact Registry [confidence: 1.0]
- **HealthLogic SDK** (jargon-tech) — Vendor software development kit for integrating with HealthLogic Rules Engine [confidence: 1.0]

### claims-ops-contacts-and-escalation.txt
*Claims Operations team contact directory with team roster, escalation procedures, vendor contacts, and communication channels*

- **Kenji Watanabe** (persona) — Senior Engineer joining Claims Operations team for Rules Engine migration [confidence: 0.9]
- **Rachel Dominguez** (persona) — Contractor from Apex Consulting serving as Rules Engine migration SME [confidence: 0.9]
- **Dr. Sarah Lin** (persona) — Clinical Review Lead responsible for pre-authorization clinical decisions and medical policy [confidence: 0.9]
- **Mei-Lin Torres** (persona) — UX Lead responsible for Member Portal redesign and provider portal design [confidence: 0.9]
- **Apex Consulting** (external-party) — Consulting firm providing contractor services for Rules Engine migration [confidence: 0.9]
- **Meridian Health Systems** (external-party) — Healthcare organization where Kenji Watanabe previously worked [confidence: 0.8]
- **HealthLogic Systems** (external-party) — Vendor providing the Rules Engine system that Clearview is planning to replace [confidence: 0.9]
- **First Alliance Banking** (external-party) — Banking partner providing EFT processing services for provider payments [confidence: 0.9]
- **Incident Escalation Process** (process) — Structured escalation workflow for handling system incidents by severity level [confidence: 0.9]
- **On-Call Handoff Process** (process) — Weekly process for transferring on-call responsibilities between engineers [confidence: 0.9]
- **PagerDuty** (software-component) — Incident management and on-call scheduling platform [confidence: 0.9]
- **Claims War Room Zoom** (software-component) — Dedicated Zoom room for Claims Operations incident response [confidence: 0.9]

### monitoring-alerting-runbook.txt
*Operations runbook for the Claims Platform monitoring and alerting setup, detailing critical alerts, escalation procedures, dashboards, and troubleshooting guidance for on-call engineers.*

- **Datadog** (software-component) — Observability platform providing metrics, APM tracing, and alerting for Claims Platform services [confidence: 1.0]
- **Splunk** (software-component) — Log aggregation and search platform for Claims Platform application logs [confidence: 1.0]
- **Claims Operations On-Call Rotation** (process) — Weekly on-call rotation schedule for Claims Operations team covering Monday 9AM to Monday 9AM ET [confidence: 1.0]
- **Alert Severity Classification** (domain-logic) — Three-tier severity classification system for Claims Platform alerts with defined response times [confidence: 1.0]
- **Connection Pool Utilization Thresholds** (domain-logic) — HikariCP connection pool monitoring with 90% utilization threshold triggering immediate alerts [confidence: 1.0]
- **Payment Cycle Timing Constraints** (domain-logic) — Critical timing requirements for Payment Engine batch processing to meet banking cutoff deadlines [confidence: 1.0]
- **Fraud Circuit Breaker Logic** (domain-logic) — Fraud Detection circuit breaker that defaults claims to 0.0 fraud score when service is degraded [confidence: 1.0]
- **Auto-Adjudication Rate Targets** (domain-logic) — Target 85% auto-adjudication rate with alerts when dropping below 75% threshold [confidence: 1.0]
- **HikariCP Pool Exhaustion Event** (business-event) — Critical system event when database connection pool utilization exceeds 90% threshold [confidence: 1.0]
- **Payment Batch Failure Event** (business-event) — Critical event when Payment Engine nightly batch job fails during payment cycle processing [confidence: 1.0]
- **HealthLogic SOAP Endpoint** (api) — SOAP web service endpoint used by Rules Engine to communicate with HealthLogic Adjudicator [confidence: 1.0]
- **CLV-3903** (jargon-business) — Incident identifier for the 2024-03-12 connection pool exhaustion incident [confidence: 1.0]
- **PgBouncer** (software-component) — PostgreSQL connection pooling proxy introduced in Q3 2024 migration [confidence: 0.9]

### meeting-notes-quarterly-ops-review-2025q3.txt
*Q3 2025 quarterly operations review for Claims Operations team covering metrics (81.3% auto-adjudication rate, 2.4M claims processed), team updates on rules engine migration, member portal redesign, capitation payment exploration, and infrastructure improvements including PgBouncer migration completion.*

- **Quarterly Operations Review** (process) — Quarterly meeting to review operational metrics and team updates across Claims Operations [confidence: 0.9]
- **Q3 2025 Performance Metrics** (domain-logic) — Operational performance targets and achievements for Claims Operations in Q3 2025 [confidence: 0.9]
- **Capitation** (jargon-business) — Per-member-per-month (PMPM) payment model for providers regardless of services rendered [confidence: 0.9]
- **Fee-for-Service** (jargon-business) — Payment model where providers are paid for each service or procedure performed [confidence: 0.9]
- **PMPM** (jargon-business) — Per-Member-Per-Month - pricing metric used in capitation payment models [confidence: 0.9]
- **Formulary** (jargon-business) — List of covered prescription drugs per health plan [confidence: 0.9]
- **DRG Grouper** (jargon-business) — System logic that assigns Diagnosis Related Group codes to institutional claims [confidence: 0.8]
- **Multi-Claim Bundling** (jargon-business) — Logic for grouping related claims together for coordinated adjudication and payment [confidence: 0.8]
- **XGBoost** (jargon-tech) — Machine learning framework used for Clearview's fraud detection models [confidence: 0.9]
- **Provider Referral Network Analysis** (domain-logic) — Fraud detection model feature to identify coordinated billing patterns between referring providers [confidence: 0.8]
- **Open Enrollment Preparation** (process) — Annual preparation process for member open enrollment period starting November 1 [confidence: 0.9]
- **Member Portal Redesign** (process) — November 2025 launch of redesigned Member Portal with improved claims status and benefit balance features [confidence: 0.9]
- **COB Auto-Detection Project** (process) — Project to automatically detect coordination of benefits scenarios, pushed to Q1 2026 [confidence: 0.8]
- **Provider Portal Design** (process) — Early design phase project for self-service provider credential updates portal [confidence: 0.8]
- **Pharmacy Claims Integration Scoping** (process) — Q4 2025 priority to scope feasibility of bringing pharmacy claims onto main processing pipeline [confidence: 0.8]
- **Kenji Watanabe** (persona) — Senior engineer joining Claims Operations November 1, 2025 to focus on rules engine migration [confidence: 0.9]
- **Rules Engine Connectivity Incident (August 15)** (business-event) — SEV-1 incident caused by VPN tunnel failure to HealthLogic data center affecting claims processing [confidence: 0.9]
- **MedConnect Encoding Issue** (business-event) — SEV-2 incident when MedConnect Exchange changed character sets in EDI 837I batches without notification [confidence: 0.8]
- **Accumulator Cleanup Job Failures** (business-event) — Two SEV-2 incidents in Q3 2025 when accumulator reservation cleanup job failed due to Cloud SQL maintenance conflicts [confidence: 0.8]
- **ERA 835 Settlement Confirmation** (domain-logic) — Payment reconciliation improvement where ERA 835 generation is delayed until settlement confirmation [confidence: 0.8]
- **SIU Investigation Targets** (domain-logic) — Performance target requiring 95% of fraud holds to be investigated within 10 business days [confidence: 0.9]

### eligibility-api-reference.txt
*API reference documentation for the Eligibility Check API v2.3, detailing endpoints for member eligibility verification, accumulator tracking, batch processing, authentication, and integration patterns used by internal systems.*

- **Eligibility API v2** (api) — RESTful API providing member eligibility verification, benefit accumulator tracking, and point-in-time eligibility lookups [confidence: 0.9]
- **Soft Reservation Created Event** (business-event) — Event flow when the Eligibility Service creates temporary benefit amount holds during claim adjudication [confidence: 0.8]
- **Soft Reservation Released Event** (business-event) — Event flow when temporary benefit reservations are released after claim finalization or denial [confidence: 0.8]
- **CLV-4890** (jargon-business) — JIRA ticket tracking batch endpoint partial results issue under heavy load [confidence: 0.9]
- **Eligibility Response** (data-model) — Data structure returned by eligibility endpoints containing member status, plan details, and optional accumulator/COB data [confidence: 0.9]
- **Batch Eligibility Request** (data-model) — Data structure for submitting bulk eligibility verification requests in JSON or EDI 270 format [confidence: 0.9]
- **Point-in-Time Eligibility Rules** (domain-logic) — Business rules governing historical eligibility lookups with 2-year retrospective limit and date validation [confidence: 0.9]
- **API Rate Limiting Rules** (domain-logic) — Rate limiting policies enforcing 500 req/sec for real-time endpoints and 10 req/min for batch processing [confidence: 0.9]
- **Accumulator Reservation Cleanup** (process) — Batch process running every 6 hours to expire orphaned soft reservations from crashed adjudication processes [confidence: 0.8]
- **WebSocket Eligibility Feed Development** (process) — Planned real-time WebSocket eligibility feed for Member Portal scheduled for Q1 2026 [confidence: 0.8]
- **Clearinghouse Partners** (external-party) — Healthcare clearinghouses submitting EDI 270/271 eligibility verification transactions via batch processing [confidence: 0.9]
- **IAM Service** (software-component) — Identity and Access Management service providing OAuth 2.0 token authentication for API access [confidence: 0.9]

### claims-gateway-api-v1-deprecated.txt
*Documentation for the deprecated Claims Submission API v1, covering its limitations, migration path to v2, remaining users, and decommission timeline. Details the technical issues that led to v2 development and provides endpoint specifications for reference.*

- **Claims Submission API v1** (api) — Deprecated REST API for claim submission built in 2020, scheduled for decommission June 2025 [confidence: 0.9]
- **March 2024 Claims Gateway Outage** (business-event) — System outage caused by unlimited batch sizes in Claims Submission API v1 [confidence: 0.9]
- **Claims API v1 Decommission** (process) — Planned process to retire Claims Submission API v1 by June 2025 [confidence: 0.9]
- **Unnamed Provider Group** (external-party) — Provider organization still using Claims Submission API v1 for direct REST submissions [confidence: 0.8]
- **Claims API v1 Status Model** (data-model) — Simplified claim status enumeration used in deprecated Claims Submission API v1 [confidence: 0.9]
- **Claims API v2 Status Model** (data-model) — Comprehensive claim status enumeration providing full lifecycle visibility in Claims Submission API v2 [confidence: 0.9]
- **Claims API v1 Validation Logic** (domain-logic) — Asynchronous validation approach in Claims Submission API v1 that accepts invalid claims [confidence: 0.9]
- **Claims API v2 Validation Logic** (domain-logic) — Synchronous validation in Claims Submission API v2 that rejects invalid claims immediately [confidence: 0.9]

### ocr-pipeline-extracted-spec.txt
*Technical specification for the OCR (Optical Character Recognition) pipeline that processes paper claims submitted via fax or mail, extracting structured data from scanned images and routing them through Claims Gateway for processing.*

- **OCR Pipeline** (system) — System that processes paper claims from fax/mail, extracting structured data via OCR and routing to Claims Gateway [confidence: 0.9]
- **OCR Extracted Claim Data Event** (business-event) — Event containing structured claim data extracted from paper forms via OCR processing [confidence: 0.9]
- **Manual Data Entry Process** (process) — Manual review and correction process for low-confidence OCR extractions before Claims Gateway submission [confidence: 0.9]
- **Google Document AI** (software-component) — Google Cloud OCR service used for extracting structured data from scanned claim forms [confidence: 0.9]
- **Manual Data Entry Tool** (software-component) — Legacy web application from ClaimsPro era used for manual claim data entry and OCR correction [confidence: 0.9]
- **CMS-1500 Form** (data-model) — Standardized paper form structure for professional healthcare claims with specific field mappings [confidence: 0.9]
- **UB-04 Form** (data-model) — Standardized paper form structure for institutional healthcare claims with complex field layouts [confidence: 0.9]
- **Google Cloud Platform** (platform) — Cloud infrastructure platform hosting OCR pipeline components and storage [confidence: 0.8]
- **Maria Chen** (persona) — Contract team lead supervising the manual data entry team for OCR claim processing [confidence: 0.9]
- **Valley Orthopedic Associates** (external-party) — Provider group that submits non-standard CMS-1500 forms causing OCR processing issues [confidence: 0.9]
- **CLV-5102** (jargon-business) — Incident identifier for archive retention policy mismatch between regulatory requirement and GCS configuration [confidence: 0.9]
- **Claims Archive Process** (process) — Process for storing and retaining original scanned claim images with regulatory compliance requirements [confidence: 0.9]
- **OCR Confidence Scoring Rules** (domain-logic) — Business rules for routing claims based on OCR extraction confidence levels and field accuracy [confidence: 0.9]
- **Seven Year Retention Rule** (domain-logic) — Regulatory compliance requirement for retaining original scanned claim images for seven years [confidence: 0.9]
- **TOB** (jargon-business) — Type of Bill code used in UB-04 institutional claim forms to classify the billing category [confidence: 0.9]

### deployment-guide.txt
*Deployment guide covering CI/CD pipeline, environment promotion, service-specific deployment procedures, database migrations, and Kubernetes resource configuration for Clearview's claims platform services.*

- **GitHub Actions CI/CD Pipeline** (process) — Six-stage continuous integration and deployment pipeline for all claims platform services [confidence: 0.9]
- **GitHub** (software-component) — Source code repository and CI/CD platform hosting clearview-health organization [confidence: 0.9]
- **Artifact Registry** (software-component) — Google Cloud container image registry for storing Docker images [confidence: 0.9]
- **Snyk** (software-component) — Dependency vulnerability scanning tool used in CI/CD pipeline [confidence: 0.8]
- **Trivy** (software-component) — Container image vulnerability scanner used in CI/CD pipeline [confidence: 0.8]
- **Environment Promotion Pipeline** (process) — Three-stage environment promotion process: dev → staging → production [confidence: 0.9]
- **Database Migration Process** (process) — Automated database schema change process using Flyway (Java) and Alembic (Python) [confidence: 0.9]
- **Alembic** (software-component) — Python database migration tool used by Fraud Detection service [confidence: 0.8]
- **Claims Gateway Deployment** (process) — Specific deployment procedure for Claims Gateway with connection pool monitoring [confidence: 0.9]
- **Rules Engine Deployment** (process) — Mandatory canary deployment process for Rules Engine with auto-adjudication rate monitoring [confidence: 0.9]
- **Payment Engine Deployment** (process) — High-risk deployment process for Payment Engine with strict timing constraints and banking coordination [confidence: 0.9]
- **Eligibility Service Deployment** (process) — Deployment process for Eligibility Service with open enrollment period restrictions [confidence: 0.8]
- **Fraud Detection Deployment** (process) — Dual deployment process for Fraud Detection covering both model updates and code changes [confidence: 0.9]
- **Google Cloud Storage** (software-component) — Cloud storage service used for ML model binaries and configuration files [confidence: 0.8]
- **Pre-Auth Service Deployment** (process) — Dual deployment process for Pre-Auth Service covering clinical criteria and code changes [confidence: 0.9]
- **Member Portal Deployment** (process) — Multi-component deployment process for Member Portal covering frontend, BFF, and feature flags [confidence: 0.8]
- **CDN** (software-component) — Content Delivery Network serving Member Portal React SPA frontend [confidence: 0.8]
- **Kubernetes Resource Defaults** (reference-data) — Standard resource allocation settings for claims platform Kubernetes deployments [confidence: 0.9]
- **Kubernetes Deployment Manifests** (data-model) — Service deployment configurations stored in clearview-infra repository [confidence: 0.9]
- **Clearview-Infra Repository** (software-component) — Centralized repository containing all Kubernetes deployment manifests for claims platform services [confidence: 0.8]
- **Claims-Ops Namespace** (platform) — Kubernetes namespace hosting core claims processing services [confidence: 0.9]
- **Member-Svc Namespace** (platform) — Kubernetes namespace hosting member-facing services [confidence: 0.9]
- **Provider-Net Namespace** (platform) — Kubernetes namespace hosting provider network services [confidence: 0.9]

### eligibility-monitoring-guide.txt
*Operational monitoring guide for the Eligibility Service covering key metrics, open enrollment scaling, accumulator management, enrollment data feeds, coordination of benefits (COB) handling, and escalation contacts.*

- **Eligibility Service Monitoring** (process) — Daily operational monitoring process for Eligibility Service metrics and health indicators [confidence: 0.9]
- **Open Enrollment Scaling Process** (process) — Preparation and scaling process for Eligibility Service during November-December open enrollment period [confidence: 0.9]
- **Accumulator Audit Job** (process) — Post-enrollment job that verifies accumulator resets were processed correctly for plan changes [confidence: 0.8]
- **Accumulator Types Logic** (domain-logic) — Business rules defining four accumulator types for tracking member deductible and out-of-pocket progress [confidence: 0.9]
- **Accumulator Reconciliation Job** (process) — Monthly batch job that corrects accumulator drift by recalculating from adjudicated claims [confidence: 0.9]
- **Accumulator Drift Event** (business-event) — Data inconsistency event where accumulator amounts drift from actual claim payment totals [confidence: 0.9]
- **Double Applied Deductible Event** (business-event) — Error condition where two claims incorrectly both apply toward deductible independently [confidence: 0.9]
- **Member Escalation Process** (process) — Process for handling member complaints and escalations related to eligibility and accumulator issues [confidence: 0.8]
- **Member Services Call Center Supervisor** (persona) — Supervisor role handling final escalations for member complaints and eligibility issues [confidence: 0.8]
- **Accumulator Reset Logic** (domain-logic) — Business rules for resetting accumulators to zero at plan year boundaries [confidence: 0.9]
- **Plan Year Boundary Event** (business-event) — Annual event marking transition from one plan year to the next, triggering accumulator resets [confidence: 0.9]
- **EDI 834 Batch Processing** (process) — Nightly batch process for processing group enrollment updates from benefits administration system [confidence: 0.9]
- **Benefits Administration System** (system) — External HR/Benefits system that provides primary enrollment data to Clearview [confidence: 0.9]
- **Enrollment API** (api) — Real-time API interface for individual enrollment changes from benefits administration system [confidence: 0.8]
- **Benefits Administration Team** (team) — HR/Benefits team responsible for managing enrollment data systems outside of engineering [confidence: 0.9]
- **COB Payer Order Rules** (domain-logic) — Business rules determining primary vs secondary payer order using birthday rule, active/retired rule, etc. [confidence: 0.9]
- **COB Data Model** (data-model) — Data structure storing coordination of benefits information within member records [confidence: 0.9]
- **COB Questionnaire** (process) — Member Portal questionnaire for collecting coordination of benefits information with ~40% completion rate [confidence: 0.9]
- **Annual COB Verification Letters** (process) — Annual mailed letters to verify coordination of benefits information for members with other coverage [confidence: 0.8]
- **COB Auto-Detection Project** (process) — Future system design project for automatically detecting coordination of benefits situations [confidence: 0.8]
- **Compliance Team** (team) — Team responsible for COB policy questions and regulatory compliance matters [confidence: 0.8]
- **Admin API** (api) — Administrative API interface for manual adjustments requiring Member Services lead approval [confidence: 0.8]
- **Bulk Enrollment Correction Event** (business-event) — Large-scale enrollment data correction resulting in high volume retroactive reprocessing triggers [confidence: 0.9]

### pre-auth-runbook.txt
*Operational runbook for Pre-Auth Service troubleshooting, covering common alerts, resolution steps, manual operations, database queries, and escalation contacts.*

- **Auth Request Processing Backlog** (business-event) — Alert triggered when pending authorization requests exceed threshold of 4 hours [confidence: 0.9]
- **Pre-Auth Backlog Resolution Process** (process) — Operational process for resolving Pre-Auth Service processing backlogs [confidence: 0.9]
- **Auto-Approval Rate Drop** (business-event) — Alert when Pre-Auth Service auto-approval rate falls below 50% target threshold [confidence: 0.9]
- **Auto-Approval Rate Investigation Process** (process) — Process to investigate and resolve drops in Pre-Auth Service auto-approval rates [confidence: 0.9]
- **Auth Expiration Warning** (business-event) — Informational alert for authorizations expiring within 7 days without associated claims [confidence: 0.9]
- **Auth Requests Table** (data-model) — Database table storing authorization requests with status and processing timestamps [confidence: 0.9]
- **Authorizations Table** (data-model) — Database table storing approved/denied authorization decisions with validity periods [confidence: 0.9]
- **Criteria Load History Table** (data-model) — Database table tracking versions and load times of clinical criteria files [confidence: 0.9]
- **Clinical Criteria Files** (reference-data) — GCS-stored configuration files defining clinical rules for authorization decisions [confidence: 0.9]
- **Manual Auth Override Process** (process) — Emergency process for manually approving authorizations with clinical lead approval [confidence: 0.9]
- **Stuck Auth Reprocessing** (process) — Manual operation to reset stuck authorization requests for reprocessing [confidence: 0.9]

### requirements-provider-portal-2023.txt
*Requirements document for a provider self-service portal to allow healthcare providers to manage their profile information, upload credentialing documents, view network status and payment history. Project was drafted in 2023 but deprioritized in favor of Rules Engine migration.*

- **Provider Self-Service Portal** (system) — Self-service web portal for healthcare providers to manage their information and interact with Clearview [confidence: 0.9]
- **Provider Office Manager** (persona) — Primary user persona for Provider Portal - handles administrative tasks at provider offices [confidence: 0.9]
- **Clearview Provider Relations Rep** (persona) — Internal user who reviews and approves provider-submitted changes through the portal [confidence: 0.9]
- **Credentialing Specialist** (persona) — Internal user who reviews credentialing document submissions and manages re-credentialing workflows [confidence: 0.9]
- **Provider Change Approval Workflow** (process) — Two-business-day approval process for provider demographic changes submitted through the portal [confidence: 0.8]
- **Credentialing Document Workflow** (process) — Process for providers to upload credentialing documents and specialists to review them [confidence: 0.9]
- **Provider Portal Backend-for-Frontend** (api) — Proposed BFF API to serve the Provider Portal frontend with provider-specific data aggregation [confidence: 0.8]
- **Credentialing Status Model** (data-model) — Data model representing provider credentialing status with defined status values [confidence: 0.8]
- **CAQH ProView Database** (reference-data) — Industry standard provider data exchange database mentioned for potential integration [confidence: 0.7]
- **Provider Data Update Restrictions** (domain-logic) — Business rules defining which provider data fields can be self-updated versus requiring manual review [confidence: 0.9]
- **Credential Expiration Alert Rules** (domain-logic) — Business rule requiring 90-day advance alerts for credential expiration per NCQA requirements [confidence: 0.9]
- **Provider Portal Deprioritization (2023)** (decision) — Decision to pause Provider Portal development in December 2023 in favor of Rules Engine migration [confidence: 0.9]

### design-session-accumulator-rework.txt
*Design session documenting the decision to rework the accumulator system using transactional reservations with SELECT FOR UPDATE to address concurrent processing issues, crash cleanup problems, and plan year boundary handling*

- **Accumulator Rework - Transactional Reservations Decision** (decision) — Decision to implement transactional accumulator reservations with SELECT FOR UPDATE to solve crash cleanup and concurrency issues [confidence: 1.0]
- **November 2024 Accumulator Plan Year Incident** (business-event) — Plan year boundary failure where accumulators weren't created for new plan year until batch job ran [confidence: 0.9]
- **Event-Sourced Accumulator Approach** (domain-logic) — Alternative approach storing accumulator events as immutable log with derived balance calculations [confidence: 0.9]
- **Distributed Lock Accumulator Approach** (domain-logic) — Alternative approach using Redis distributed locks with TTL to ensure accumulator update consistency [confidence: 0.9]
- **Open Enrollment Accumulator Pre-Creation** (process) — Process to pre-create next plan year accumulators during open enrollment to prevent plan year boundary issues [confidence: 0.9]
- **Accumulator Concurrent Claim Analysis** (domain-logic) — Analysis showing most members have at most 2 concurrent claims, validating low contention for row-level locking [confidence: 0.9]

### design-session-cob-handling.txt
*Design session for COB auto-detection system to identify members with unreported other coverage through claims data analysis and automated signals, reducing overpayment from incorrect payer order*

- **COB Auto-Detection Project** (process) — Project to automatically detect members with unreported other coverage through claims data analysis [confidence: 0.9]
- **COB Detection Signals** (domain-logic) — Five identified signals in claims data that indicate potential unreported other coverage [confidence: 0.9]
- **COB Verification Workflow** (process) — Five-step process for verifying and updating member COB information after auto-detection [confidence: 0.9]
- **HETS (Healthcare Eligibility Transaction System)** (system) — CMS system for Medicare beneficiary identifier lookups and eligibility verification [confidence: 0.8]
- **COB Overpayment Problem** (business-event) — Ongoing issue causing $4-6M annual overpayment due to stale COB data [confidence: 0.9]
- **COB Questionnaire** (process) — Portal-based questionnaire for members to self-report other insurance coverage [confidence: 0.9]
- **Annual COB Verification Letters** (process) — Annual physical mail campaign asking members to verify their other insurance coverage [confidence: 0.9]
- **Medicare Beneficiary Identifier (MBI)** (jargon-business) — Unique identifier used by CMS for Medicare beneficiaries [confidence: 0.9]
- **Recoupment Time Limits** (domain-logic) — Regulatory constraints on how far back payers can recover overpayments from providers [confidence: 0.8]
- **COB Batch Analysis** (process) — Weekly batch job analyzing claims data for COB detection signals [confidence: 0.9]

### design-session-payment-reconciliation.txt
*Design session documenting three major problems with Payment Engine reconciliation: timing mismatches between ERA 835 and EFT settlement, void/reissue tracking issues, and recoupment spreading logic problems. Team reached decisions on first two problems but deferred complex recoupment logic for follow-up.*

- **Payment Reconciliation Rework** (process) — Design initiative to fix three critical problems in Payment Engine reconciliation workflow [confidence: 0.9]
- **ERA 835 Timing Mismatch Problem** (business-event) — Reconciliation problem where ERA 835 remittance advice doesn't match actual EFT settlement amounts [confidence: 0.9]
- **Void/Reissue Tracking Problem** (business-event) — Payment linkage issue where voided and reissued payments lack proper relationship tracking [confidence: 0.9]
- **Recoupment Spreading Problem** (domain-logic) — Flawed logic for distributing large recoupments across payment cycles that doesn't coordinate multiple simultaneous recoupments [confidence: 0.8]
- **Payments Table Void Linkage Schema** (data-model) — Database schema changes to add void reason tracking and payment chain linkage to payments table [confidence: 0.9]
- **EFT Settlement Confirmation** (business-event) — Banking partner notification confirming actual Electronic Funds Transfer settlement completion [confidence: 0.8]

### 2024-claims-gateway-outage-postmortem.txt
*Post-mortem analysis of a SEV-1 Claims Gateway outage on March 12, 2024, caused by connection pool exhaustion when processing an abnormally large batch of institutional claims, including root cause analysis, timeline, impact, and action items.*

- **HikariCP** (software-component) — JDBC connection pool library used by Claims Gateway for PostgreSQL connections [confidence: 0.9]
- **claims-gw-prod-01** (software-component) — Production Cloud SQL PostgreSQL database instance for Claims Gateway [confidence: 0.9]
- **HikariCP Pool Exhaustion Event** (business-event) — Event that occurs when the Claims Gateway connection pool reaches its maximum capacity and can't serve new requests [confidence: 0.9]
- **Eligibility Service Timeout Cascade** (business-event) — Cascading failure event where Eligibility Service's connection pool fills up due to timeouts from Claims Gateway [confidence: 0.8]
- **Claims Gateway Incident Response** (process) — The operational process followed during the March 2024 Claims Gateway outage [confidence: 0.9]
- **Batch vs Real-time Connection Separation** (domain-logic) — Architectural pattern requiring separate connection pools for batch and real-time processing [confidence: 0.9]
- **Batch Size Admission Control** (domain-logic) — Business rule limiting the maximum number of claims that can be submitted in a single batch [confidence: 0.9]
- **CLV-3901** (jargon-business) — Action item to implement separate connection pools for batch and real-time processing [confidence: 1.0]
- **CLV-3902** (jargon-business) — Action item to add batch size limit to Claims Submission API [confidence: 1.0]
- **CLV-3905** (jargon-business) — Action item to improve error logging for connection pool exhaustion [confidence: 1.0]
- **CLV-3906** (jargon-business) — Action item to notify Northeast Clearinghouse about new batch size limits [confidence: 1.0]
- **Northeast Family Medicine Associates** (external-party) — Provider group that experienced real-time claim submission failures during the March 2024 outage [confidence: 0.9]
- **Connection Pool Utilization Alerting** (domain-logic) — Alert threshold rule triggering when database connection pool utilization exceeds 90% for 2 minutes [confidence: 0.9]

### postmortem-2022-eligibility-outage.txt
*Post-mortem analysis of a 4-hour Eligibility Service outage in September 2022 caused by a database migration that locked the members table, cascading to Claims Gateway and Rules Engine failures and creating an 18K claim backlog.*

- **September 2022 Eligibility Service Outage** (business-event) — Complete Eligibility Service outage lasting 3 hours 47 minutes due to database migration table lock [confidence: 1.0]
- **Members Table Index Migration** (process) — Database migration to add index on members table that caused September 2022 outage [confidence: 1.0]
- **Members Table** (data-model) — Database table storing member enrollment data with approximately 800K rows [confidence: 0.9]
- **Database Restart Decision (2022 Outage)** (decision) — Dana Okafor's decision to restart the Cloud SQL instance to resolve the table lock [confidence: 1.0]
- **PostgreSQL Migration Best Practices** (domain-logic) — Guidelines requiring concurrent index creation and DBA review for schema changes [confidence: 1.0]
- **Schema Change Review Process** (process) — DBA review requirement for all database schema changes established after 2022 outage [confidence: 1.0]
- **INC-2022-0094** (jargon-business) — Incident tracking identifier for the September 2022 Eligibility Service outage [confidence: 1.0]
- **SEV-1** (jargon-business) — Highest severity incident classification for complete service outages affecting business operations [confidence: 0.9]

### postmortem-2023-payment-file-corruption.txt
*Post-mortem analysis of a April 2023 payment file corruption incident where duplicate provider payments totaling $2.3M were sent due to race condition between void/reissue operations and nightly payment batching, requiring months of recoupment recovery.*

- **INC-2023-0031: Payment File Corruption Incident** (business-event) — SEV-1 incident where duplicate provider payments totaling $2.3M were processed due to race condition in payment batching logic [confidence: 0.9]
- **Payment Batching Query Logic** (domain-logic) — SQL query logic that selects pending payments for NACHA file generation, historically vulnerable to race conditions [confidence: 0.9]
- **Statewide Physicians Group** (external-party) — Provider group whose fee schedule correction triggered the bulk reprocessing that led to the 2023 payment corruption incident [confidence: 0.8]
- **NACHA File Generation Process** (process) — Nightly batch process that creates EFT payment files in NACHA format for submission to banking partner [confidence: 0.9]
- **Payment Recoupment Process** (process) — Manual process for recovering overpaid amounts from providers through recoupment requests and deductions from future payments [confidence: 0.8]
- **NACHA File Duplicate Detection** (domain-logic) — Validation logic added to detect duplicate payment records before NACHA file submission to banking partner [confidence: 0.9]
- **NACHA File Reconciliation Check** (domain-logic) — Financial control that compares NACHA file totals against expected payment totals before banking partner release [confidence: 0.9]
- **Void/Reissue Fencing Logic** (domain-logic) — Proposed time-based restriction preventing void/reissue operations during payment cycle windows to avoid race conditions [confidence: 0.8]
- **Payment Void Linkage Enhancement** (data-model) — Enhancement to payment data model adding void_reason and linked_payment_id fields for better void/reissue tracking [confidence: 0.9]
- **INC-2023-0031** (jargon-business) — Incident tracking number for the 2023 payment file corruption incident [confidence: 0.9]

### meeting-notes-fraud-detection-integration.txt
*Meeting notes from July 22, 2025 discussing integration of real-time fraud detection scoring into Claims Gateway routing, including performance requirements, failure modes, scoring thresholds, and implementation timeline.*

- **Fraud Detection Pre-Payment Integration** (process) — Migration from asynchronous to synchronous fraud scoring in Claims Gateway intake flow [confidence: 0.9]
- **Fraud Detection Sidecar Model** (process) — Current asynchronous fraud scoring approach where Claims Gateway sends Kafka messages for scoring [confidence: 0.9]
- **Fraud Detection Circuit Breaker Logic** (domain-logic) — Circuit breaker pattern for fraud service calls with 5-second timeout and failure thresholds [confidence: 0.9]
- **New Fraud Scoring Thresholds** (domain-logic) — Updated fraud model scoring thresholds with three-tier classification system [confidence: 0.9]
- **Fraud Model Retraining Pipeline** (process) — Monthly automated retraining of fraud detection models using historical claims and investigation outcomes [confidence: 0.9]
- **XGBoost Fraud Model** (data-model) — Machine learning model for real-time fraud scoring with 120ms p99 latency [confidence: 0.9]
- **Denormalized Provider Profiles** (data-model) — Local fraud detection database containing provider history for fast scoring queries [confidence: 0.8]
- **Provider Profile Sync Event** (business-event) — Nightly Kafka event flow updating fraud detection's denormalized provider profiles [confidence: 0.8]
- **Parallel Fraud Scoring Validation** (process) — One-week validation process running old and new fraud models simultaneously for comparison [confidence: 0.9]
- **Fraud Investigation Status Display Rules** (domain-logic) — Business rule hiding fraud investigation details from members in portal, showing only 'processing' status [confidence: 0.9]

### meeting-notes-member-portal-redesign.txt
*Sprint planning meeting for Member Portal redesign focused on November launch, covering new claims status timeline view, benefit balance improvements, provider search enhancements, digital ID card redesign, and secure messaging integration with Zendesk.*

- **Claims Status History Endpoint** (api) — New API endpoint to expose claims processing timeline data for member portal redesign [confidence: 0.9]
- **Claims Status History Model** (data-model) — Data model for claims status transitions with timestamps used in timeline view [confidence: 0.8]
- **Claims Status Masking Workflow** (process) — Business process for displaying appropriate claim status to members while hiding fraud investigation details [confidence: 0.9]
- **Benefit Balance Visualization Process** (process) — Enhanced display of member deductible and out-of-pocket maximum progress with visual progress bars [confidence: 0.8]
- **Digital ID Card Redesign Process** (process) — Redesign of member ID card display from static image to dynamic data-driven view with sharing functionality [confidence: 0.9]
- **Provider Search Enhancement Process** (process) — Enhancement of provider search with accepting new patients filter and future distance-based search capability [confidence: 0.8]
- **Secure Messaging Claim Context Process** (process) — Enhancement to show claim details inline when members message about specific claims [confidence: 0.7]
- **Zendesk Integration** (software-component) — Third-party customer service platform underlying secure messaging functionality [confidence: 0.8]
- **Clinical Reviewer** (persona) — Internal staff persona who reviews pended claims and pre-authorization requests requiring clinical evaluation [confidence: 0.9]
- **Clinical Reviewer Interface Project** (process) — Q1 2026 project to build proper review interface for clinical reviewers replacing current database query tools [confidence: 0.8]

### meeting-notes-vendor-migration-kickoff.txt
*Kickoff meeting for migrating from HealthLogic Adjudicator to a custom-built rules engine using Drools, with detailed technical architecture discussion, timeline planning, and domain education on medical coding systems*

- **HealthLogic Adjudicator** (system) — Legacy claims rules engine being migrated away from due to cost and flexibility issues [confidence: 0.9]
- **Drools-Based Rules Engine** (system) — New custom claims adjudication engine being built to replace HealthLogic Adjudicator [confidence: 0.9]
- **Drools** (software-component) — Rules execution engine that will power the new custom adjudication system [confidence: 0.9]
- **DRG Grouper Library** (software-component) — Java library needed for calculating Diagnosis Related Groups for institutional claims [confidence: 0.8]
- **Rules Engine Migration Process** (process) — Three-phase process to migrate from HealthLogic Adjudicator to custom Drools-based rules engine [confidence: 0.9]
- **Rachel Dominguez** (persona) — Contractor from Apex Consulting specializing in claims adjudication system migrations [confidence: 0.9]
- **CPT** (jargon-business) — Current Procedural Terminology - codes for medical procedures and services on professional claims [confidence: 0.9]
- **HCPCS** (jargon-business) — Healthcare Common Procedure Coding System - broader coding system including CPT plus supply and equipment codes [confidence: 0.9]
- **ICD-10-CM** (jargon-business) — International Classification of Diseases, 10th Revision, Clinical Modification - diagnosis codes for claims [confidence: 0.9]
- **ICD-10-PCS** (jargon-business) — ICD-10 Procedure Coding System used for DRG grouper calculations [confidence: 0.9]
- **DRG** (jargon-business) — Diagnosis Related Group - payment categories for inpatient hospital stays [confidence: 0.9]
- **DRL** (jargon-tech) — Drools Rule Language - the format for authoring rules in the new custom rules engine [confidence: 0.9]
- **Parallel Testing Accuracy Targets** (domain-logic) — Accuracy thresholds for validating new rules engine during parallel processing phase [confidence: 0.9]
- **CMS DRG Grouper Definitions** (reference-data) — Annual DRG grouper algorithm definitions published by CMS each October [confidence: 0.9]

---

## All Unresolved Questions

- What is the specific content and rationale documented in ADR-2024-007 regarding the Rules Engine replacement?
- Who maintains and updates the auth-required service lists that are updated quarterly?
- What is the specific process for credentialing workflows mentioned in the seed context - is this part of the re-credentialing process or separate?
- What are the deployment procedures referenced in the separate deployment runbook?
- What specific fraud patterns does the post-payment analysis detect beyond the general categories mentioned?
- How are the soft reservations implemented technically in the Eligibility Service?
- What is the OCR pipeline mentioned for paper claims processing?
- What specific issues are documented in ADR-2024-007 that make the HealthLogic selection 'a mistake in hindsight'?
- What was the specific timeline and process for the team split in late 2022 - was it driven by headcount growth, domain complexity, or other factors?
- Are the Lucidchart links (https://lucidchart.com/clearview/claims-platform-v1 and https://lucidchart.com/clearview/claimspro-migration-plan) still accessible, and do they contain useful architectural diagrams?
- What were the specific data quality issues with provider records that required 15% of records to be cleaned up, and how were they resolved?
- What is the current status of CLV-3904 and the circuit breaker implementation - is this still a priority issue in 2024?
- What was the specific HIPAA compliance issue discovered in the 2022 audit related to clinical data in logs, and how was the log partitioning implemented?
- What were the alternatives considered to TriZetto Facets, and what were the specific evaluation criteria used in the vendor selection?
- What was the business impact of the RabbitMQ message loss issue - how many claims were lost and what was the financial exposure?
- What drove the decision to use Quarkus for the Eligibility Service 'startup time improvements' - what were the specific performance issues with Spring Boot?
- What is the specific format and validation rules for the claim_id generation (CLM-YYYYMMDD-NNNNNN) - is NNNNNN sequential per day or globally unique?
- The document mentions 'design session' for adding void_reason fields in 2025-06 - what specific requirements drove this payment reconciliation rework?
- What are the specific business rules for the minimum payment threshold of $5 - does this apply to all payment types or just provider payments?
- How does the 15-minute cache TTL for benefit plan configuration interact with real-time adjudication - what happens if plan changes occur during processing?
- What is the relationship between the actuarial team's 'Clearview standard fee schedule' and the contracted fee schedules - who maintains the standard schedule?
- The accumulator reservation cleanup 'every 6 hours' for reservations 'older than 4 hours' seems like a 2-hour gap - is this intentional buffer time?
- What triggers the transition from ADJUDICATED status to PAID/DENIED/PENDED status in the claim lifecycle - is this automatic or manual?
- How are family-level accumulators (FAM_DEDUCTIBLE, FAM_OOP_MAX) calculated across multiple family members - is this aggregated in real-time?
- What were the specific details of the 2024 connection pool incident that led to the 2,000 claim batch size limit?
- What is the SIU case management system that consumes fraud alerts, and is it internal or external?
- How does the 'admin console' for manual payment approval work, and who specifically has access to approve payments?
- What are the specific fraud detection meeting notes referenced for the sync migration decision, and where are they stored?
- What is the 'reporting pipeline' that consumes multiple Kafka events - is this an internal system or external analytics platform?
- How are the state regulatory agency reporting requirements structured, and what are the three different formats mentioned?
- What specific issues does ADR-2024-007 identify with HealthLogic, and how does this integrate with the SOAP web services mentioned?
- What is the relationship between the VPN tunnel to HealthLogic data center and the overall HealthLogic replacement strategy?
- Are there any disaster recovery or failover procedures for the external partner integrations (clearinghouses, banking)?
- What monitoring and alerting exists for the various batch jobs, especially the financial payment cycles?
- What specific criteria determine when a claim gets a PEND disposition versus PAY/DENY? The document mentions 'complex scenarios' and 'edge cases' but doesn't detail what triggers manual review.
- What is the exact process for IRO selection and how long does Level 2 external review typically take?
- How does the system handle claims that are submitted very close to the 90-day duplicate detection window - are there edge cases where legitimate resubmissions get flagged?
- What happens to claims that are held for SIU review but never get cleared or investigated - is there a maximum hold time?
- How are the quarterly updates to auth-required service lists coordinated across different benefit plans, and who makes the decisions about what services to add or remove?
- What specific 'signals' does the fraud ML model evaluate beyond the general categories mentioned (billing patterns, member history, etc.)?
- How does the system handle scenarios where a member's eligibility status is itself disputed or unclear on the date of service?
- What is the process for updating usual-and-customary rates, and how frequently are they refreshed?
- Are there different processing SLAs for the three claim channels beyond the 30-second professional claim intake mentioned?
- What constitutes 'urgent/pre-service appeals' that get the 72-hour turnaround versus the standard 30-day timeline?
- What is the current state of enrollment workflow documentation - is there any existing partial documentation or is this completely undocumented?
- What specific issues or confusion have new engineers encountered regarding enrollment flows that triggered the need for this documentation?
- Are there existing technical implementations in the Eligibility Service for enrollment processing that just need documentation, or do both the process and implementation need to be designed?
- What is the relationship between enrollment changes and the retroactive claims reprocessing mentioned - does every enrollment change trigger claims reprocessing?
- Who are the key stakeholders beyond Dana Okafor who should be involved in documenting the enrollment workflow?
- What is the priority and urgency of this documentation given the Q4 2025 target date?
- What specific technical limitations or business drivers are motivating the migration from PharmaCore to the main platform?
- What is the current integration between PharmaCore and other Clearview systems for member eligibility, benefit verification, and reporting?
- What are the specific decision criteria for the PBM integration choice (continue external vs bring in-house)?
- How will the pharmacy claims migration align with or impact the ongoing HealthLogic Rules Engine replacement mentioned in previous ADRs?
- What is the current data flow between PharmaCore and the quarterly metrics reporting that shows 50K claims per quarter?
- Are there existing contracts or vendor relationships with PharmaCore that will impact migration timing or approach?
- What is the complete NCQA-compliant credentialing workflow that James Whitfield was supposed to document?
- What are the specific re-credentialing timelines mentioned in the TODO?
- How exactly does the system handle expired credentials during claims adjudication - does it deny claims, pend them, or have other logic?
- Is there a current credentialing system in place that's undocumented, or is this a gap in the process?
- What triggered the need to document this process - was there a compliance issue or operational problem?
- Does the existing Provider Re-credentialing Process entity cover what was intended to be documented here, or are there additional workflows missing?
- What specific OpenAPI specification format and tooling is used for API documentation, and how is it integrated with the development workflow?
- What are the specific technical limitations of the HealthLogic Rules Engine that make it problematic (beyond the SOAP web service limitations mentioned in previous documents)?
- How does the Node.js BFF layer handle authentication and session management for member-scoped access, and what specific APIs does it aggregate?
- What specific CI/CD tools and security scanning tools are used to enforce the code coverage, security, and HIPAA compliance requirements?
- What is the complete list of hardened base images maintained by Clearview (beyond base-java:17) and what security hardening is applied?
- How does the 7-year data retention requirement vary by state, and what specific mechanisms implement automated data lifecycle management?
- What specific ML libraries beyond scikit-learn and XGBoost are used in the Fraud Detection service, and how does Poetry handle their complex dependency requirements?
- What specific incident response documentation is missing that Marcus would need to provide the link for?
- What technical capabilities or experience does Kenji Watanabe bring from Meridian Health Systems that makes him valuable for the Rules Engine migration?
- What is the current Technical Account Manager situation with GCP Premium Support, and when will a new TAM be assigned?
- Are there formal SLAs with the clearinghouses (Northeast Clearinghouse, MedConnect Exchange, DirectSubmit) or just best-effort support?
- What monitoring systems integrate with PagerDuty to trigger the incident alerts?
- What specific knowledge transfer is planned between Rachel Dominguez (contractor ending Oct 2025) and Kenji Watanabe (starting Nov 2025)?
- What specific technical limitations beyond SOAP are driving the HealthLogic Rules Engine replacement mentioned in the context?
- Are there formal SLAs with banking partners for payment processing cutoffs, and what are the penalties for missing them?
- What is the relationship between CLV-3903 and the 2024 Connection Pool Incident - are they the same event or different incidents?
- What monitoring exists for the PgBouncer layer introduced in Q3 2024, and does it have its own alerting?
- Is there a Member Portal dashboard mentioned as TODO that provides insights into the current state of this monitoring gap?
- What are the false positive rates mentioned for Fraud Detection, and how do they relate to the circuit breaker behavior?
- Why is there a separate Member Services on-call rotation, and how do incidents get routed between Claims Ops and Member Services?
- What specific rules migration issues are causing the auto-adjudication rate to remain at 81% instead of the 85% target?
- What specific technical capabilities will Kenji Watanabe bring from his previous health plan experience that will help accelerate the rules migration?
- Are there formal SLAs or penalties with HealthLogic for the VPN connectivity issues, and how does this factor into the migration timeline?
- What is the current staffing plan for replacing the two SIU investigators who left in August - is this blocking the fraud investigation performance improvement?
- How does the Provider Network team coordinate fee schedule updates with the Actuarial team's analysis process?
- What are the specific integration points between formulary data and the main claims processing pipeline that make pharmacy migration challenging?
- Is there a formal process for coordinating Cloud SQL maintenance windows with critical batch job schedules to prevent future accumulator cleanup failures?
- What criteria determine whether a provider group qualifies for capitation contracts versus fee-for-service arrangements?
- How does the 'aberrant billing patterns' detection in post-payment analysis differ from the pre-payment fraud scoring models?
- What is the actual uptime SLA for the Eligibility API and how does it impact claims processing when the service is unavailable?
- How are OAuth 2.0 tokens managed in terms of expiration and refresh - what happens when a long-running batch process token expires mid-operation?
- What specific monitoring and alerting exists around the 6-hour accumulator cleanup job - how does the team know if cleanup volume indicates systemic problems?
- Are there any caching layers in front of the Eligibility API to reduce database load, and how is cache invalidation handled for real-time eligibility changes?
- What is the actual root cause of CLV-4890 batch partial failures under load - is it database timeouts, memory issues, or something else?
- How does the point-in-time eligibility lookup handle mid-year plan changes or retroactive enrollment adjustments?
- What happens to soft reservations if the Eligibility Service itself crashes or restarts during claim processing?
- How does the WebSocket eligibility feed planned for Q1 2026 relate to the existing accumulator cleanup and reservation management?
- What specific technical mechanism caused the March 2024 outage - was it memory exhaustion, database connection pool limits, or something else?
- Has the unnamed provider group been contacted by James Whitfield yet, and what's their migration timeline?
- Is DirectSubmit actually on track to migrate by Q2 2025, or is the June 2025 decommission date likely to slip?
- What is the compatibility shim approach - will it translate v1 requests to v2 format, or proxy them?
- Are there any other undiscovered v1 consumers beyond the two mentioned, and how will request logging help identify them?
- What specific Avro schema support was added in v2, and how does it relate to the existing EDI X12 support?
- How does the fraud score field work in v2 responses - is it the same score from Fraud Detection system?
- What wiki page did Nadia write for the migration guide, and is it current?
- What happened when Clearview switched from ABBYY to Google Document AI in 2023 - was this purely a cost decision or were there performance/accuracy improvements?
- Why hasn't the UB-04 template been updated since the vendor switch - is this just resource constraints or technical complexity?
- How does the manual data entry tool's direct database connection impact data consistency and transaction integrity compared to going through the Claims Gateway API?
- What specific changes would Valley Orthopedic Associates need to make to use standard CMS-1500 forms, and has Clearview attempted to work with them on this issue?
- What are the actual storage costs and compliance risks of the 2-year retention gap between the 7-year requirement and 5-year GCS policy?
- Are there any plans to modernize the manual data entry tool or is the low volume (5% of claims) making this a low priority?
- What percentage of the 10,000 monthly paper claims require manual intervention due to low OCR confidence, and what's the processing time impact?
- How does the OCR pipeline handle multi-page faxes that arrive as separate images - is there automated document assembly logic?
- What specific incident caused the 'never connect dev or staging to production databases' rule - what were the consequences of the two previous violations?
- What is the 'Claims War Room Zoom' and how does it relate to the deployment incident response process?
- What percentage of deployments actually use the canary strategy vs rolling updates, and what criteria determine the choice?
- How are the 'custom metrics' for HPA scaling defined - what business metrics beyond CPU trigger scaling?
- What is Leo working on regarding 'new Istio service mesh configuration' and how will it change the deployment process?
- What specific monitoring alerts exist for the auto-adjudication rate drops that trigger Rules Engine rollbacks?
- How is the 30-minute canary window enforced technically - is it automated or manual monitoring?
- What constitutes a 'high-risk change' that mandates canary deployment beyond Rules Engine and Payment Engine?
- What is the approval workflow mechanism - is it GitHub's built-in approvals or a custom tool?
- What specific failure modes cause the soft reservation system to fail, leading to double-applied deductible scenarios?
- How does the 6-hour cleanup job for soft reservations work, and why does it sometimes conflict with active adjudication?
- What is the 'admin API' specifically - is this part of the Eligibility Service or a separate administrative system?
- What are the current COB auto-detection design approach and timeline - is this a 2026 initiative?
- How does the point-in-time query cache work, and what causes cache hit rate to drop below 85%?
- What monitoring exists for the Benefits Administration Team's system availability and file delivery reliability?
- How does accumulator reconciliation handle cases where claims have been voided or adjusted after the monthly reconciliation cutoff?
- What approval workflow exists for the Member Services lead approval required for admin API operations?
- How does the system handle accumulator transitions for members who change plans mid-year vs at plan year boundaries?
- What are the 'COB handling design session notes' and where can they be accessed for understanding the auto-detection project?
- What is the exact threshold number for the auth request processing backlog alert - is 342 just an example or the actual configured threshold?
- What is the 'scheduler' component mentioned that picks up PENDING requests every 60 seconds - is this part of the Pre-Auth Service or a separate component?
- What specific access issues with the GCS bucket require Platform Engineering assistance - are these IAM permission problems or network connectivity issues?
- What is the #preauth-ops Slack channel governance - who monitors it and how are manual override logs reviewed?
- What determines the assignment of standard vs surgical authorization validity periods (90 vs 60 days) - is this based on service category or other criteria?
- What is the 'new batch auth import process' that Priya is documenting - is this a replacement for individual auth request processing?
- How does the clinical criteria loading failure impact the auto-approval rate - does it default to manual review or deny all requests?
- What is the relationship between the auth_requests and authorizations tables - does one record become one record in both tables?
- What monitoring exists in Datadog specifically for the Pre-Auth Service beyond the manual reprocessing mention?
- Who has access to kill database connections and what are the risks of terminating idle connections during business hours?
- Which document management system will be used for credentialing uploads? The document mentions this is TBD and Nadia suggested GCS + metadata service - has this been decided?
- How will large provider groups with hundreds of providers be handled? Will there be bulk upload or CSV import capabilities?
- What is the current status of CAQH ProView integration feasibility assessment that James mentioned?
- Has the authentication system been selected between FIDO2/WebAuthn and SAML SSO options?
- What was the cost estimate that was supposed to be completed before re-prioritization?
- How does the fee schedule comparison tool compliance concern mentioned by the Compliance team get resolved?
- What specific notification preferences system will be implemented for email vs portal alerts?
- What specific mechanism will trigger the removal of the 6-hour cleanup batch job once the transactional reservation approach is deployed?
- How will the migration from soft reservations to transactional reservations be executed with zero downtime - will there be a gradual rollout or feature flag approach?
- What are the specific accumulator types mentioned (individual deductible, family deductible, individual OOP, family OOP) and are there others not mentioned?
- What was the exact impact of the November 2024 accumulator incident - how long were members affected and what was the business impact?
- What current performance metrics exist for accumulator operations that will be used to validate the new approach doesn't degrade performance?
- Why is accumulator drift still possible with the current soft reservation system if reservations are supposed to prevent over-allocation?
- What exactly is Clearview's current access level to HETS - can they do COB-specific lookups or only the existing 270/271 transactions?
- How will the batch analysis handle the computational complexity of analyzing billed amounts across all procedure codes for the entire member base?
- What is the current process for handling recoupment when overpayments are discovered, and how does it integrate with provider payment systems?
- Does Clearview have any existing data sharing agreements with large employers that could support signal #5 (spouse employment changes)?
- How will the system handle members who legitimately have low billed amounts due to high deductibles or other plan features versus COB situations?
- What is the estimated volume of members that would be flagged weekly by this system, and does Member Services have capacity for the resulting manual reviews?
- Are there any current pharmacy system integration capabilities that could support signal #3, or would this require the 2026 PharmaCore migration?
- How does the regulatory recoupment time limit interact with claim reprocessing workflows - is there existing infrastructure for bulk claim reprocessing?
- What specific format and API does the banking partner provide for EFT settlement confirmation - is it real-time webhooks, batch files, or API polling?
- For the void linkage fields, should linked_payment_id be nullable to handle voids that don't have replacements (e.g., pure cancellations)?
- How does the recoupment spreading algorithm currently prioritize multiple simultaneous recoupments - first-in-first-out, by dollar amount, or some other logic?
- What happens to ERA 835s that were already generated but the corresponding EFT settlement is later modified - do providers get corrected 835s?
- For the $0 payment scenario in recoupment spreading, do providers prefer to receive $0 payments or have payments held until they exceed the minimum threshold?
- Are there regulatory or compliance requirements around ERA 835 timing that could be affected by delaying generation until settlement confirmation?
- What specific changes were made to the connection pool configuration when they moved to PgBouncer in Q3 2024, and where is the current configuration documented?
- Why was CLV-3904 (circuit breaker between Claims Gateway and Eligibility Service) deprioritized in favor of the rules engine migration, and does this architectural gap still exist?
- What is the current batch size limit for institutional claims after the CLV-3902 implementation - is it still 2,000 claims per batch?
- How does the current system handle the coordination between batch processing job killing and pod restarts during incident response?
- What specific metrics does the connection pool utilization alert (CLV-3903) monitor - total connections, active connections, or both?
- Are there separate Datadog alerts for the new PgBouncer configuration versus the legacy HikariCP alerts mentioned in this postmortem?
- What happened to the PostgreSQL migration best practices document that Tom Nguyen wrote? The 2023 note says it's 'somewhere in the wiki' but can't be found - was it lost during a wiki migration or reorganization?
- Why has the circuit breaker action item (INC-2022-0094-A4, later CLV-3904) been consistently deprioritized for over 2 years despite being flagged as important after both the 2022 and 2024 outages?
- What specific throughput limitations does the HealthLogic Adjudicator have that made clearing the 18K claim backlog take 2+ hours? Is this a licensing constraint, API rate limit, or processing capacity issue?
- What is the current process for testing database migrations against prod-sized datasets in staging - was this implemented as part of the follow-up actions?
- How do the 3 provider groups that called during the outage connect to Clearview's systems - are they using the Claims Gateway directly or through clearinghouse partners?
- What specific database transaction isolation level was used before and after the fix to the payment batching query?
- How exactly does the FOR UPDATE SKIP LOCKED syntax prevent the race condition - does it skip the entire row or just during the concurrent modification?
- What is the typical timeline for recoupment recovery - is 4 months standard or was this incident particularly challenging?
- Why was the void/reissue fencing logic (INC-2023-0031-A4) deprioritized when it seems like a fundamental fix for the race condition?
- What happened to Nina Petrovich's original design documentation for the void/reissue workflow?
- How does the banking partner's EFT processing work - can they reverse payments after 6 AM processing but before provider deposit?
- What are the compliance or regulatory implications of duplicate payments to providers?
- How does the current payment reconciliation rework compare to the manual recoupment process used after this incident?
- Does the Fraud Detection wiki page mentioned by Tariq actually exist, and if not, where should fraud model documentation be maintained?
- What are the specific features used by the XGBoost fraud model for scoring (e.g., provider history, claim patterns, amounts)?
- How does the fraud model handle claims from new providers with no historical data in the denormalized provider profiles?
- What is the exact mechanism for Fraud Detection service to 'pick up' new model binaries from GCS - is it automatic on restart or triggered by some other event?
- Should pre-authorization requests also be scored for fraud when submitted by providers with existing fraud flags, as mentioned in the side discussion?
- What happens to claims that score between 0.65-0.82 - is the 'post-payment review' flag just metadata or does it trigger an actual review process?
- How long do held claims remain in SIU review status before timeout or escalation?
- What are the current performance benchmarks for the 30-second professional claims SLA mentioned, and how much headroom actually exists for the additional 120ms?
- How is the 8% false positive rate target measured - against SIU investigation outcomes or member complaints?
- What specific data fields are included in the claims_status_history table that will be exposed by the new API endpoint?
- How does the Member Portal BFF currently handle claims status data, and what changes are needed to consume the new timeline endpoint?
- What are the specific compliance requirements that mandate masking fraud investigation status from members?
- What geocoding service or approach would be needed for distance-based provider search implementation?
- What is the current technical architecture of the Zendesk integration and what API capabilities exist for passing claim context?
- Who specifically owns the messaging service integration - Member Services team or a different technical team?
- What are the specific clinical criteria that clinical reviewers need to see in their improved interface?
- Is the claims adjudicator persona mentioned the same as clinical reviewer or a separate role?
- What is the current database query tool that clinical reviewers use, and what team built/maintains it?
- What is the current process for clinical teams to request rule changes, and how will this change during the dual maintenance period?
- Are there specific performance benchmarks the new Drools engine must meet beyond the accuracy targets?
- What is the fallback plan if parallel testing reveals significant issues with the new engine?
- How will the team handle rule versioning and rollback capabilities in the Git-based approach?
- What specific open-source DRG grouper libraries is Rachel recommending?
- Will there be automated testing infrastructure for the 4,200 rules during development?
- How will clinical knowledge be captured before Rachel's contract ends in October?
