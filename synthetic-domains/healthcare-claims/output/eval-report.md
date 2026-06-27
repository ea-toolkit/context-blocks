# KB Coverage Report

**Generated:** 2026-06-20 19:53
**Questions:** 60
**Time:** 856.0s
**Estimated cost:** $1.20

## Coverage Summary

| DDC Class | Count | % |
|-----------|-------|---|
| CLEAN (answerable) | 37 | 61.7% |
| INCOMPLETE (partial) | 22 | 36.7% |
| MISSING (not answerable) | 1 | 1.7% |

## By Question Source

| Source | CLEAN | INCOMPLETE | MISSING | Total |
|--------|-------|------------|---------|-------|
| doc | 23 | 7 | 0 | 30 |
| persona | 4 | 15 | 1 | 20 |
| seed | 10 | 0 | 0 | 10 |

## By Knowledge Layer

| Layer | CLEAN | INCOMPLETE | MISSING | Total | Coverage |
|-------|-------|------------|---------|-------|----------|
| behavioral | 14 | 7 | 0 | 21 | 67% |
| cross-cutting | 0 | 1 | 0 | 1 | 0% |
| decision | 9 | 3 | 0 | 12 | 75% |
| language | 3 | 0 | 0 | 3 | 100% |
| organizational | 5 | 3 | 1 | 9 | 56% |
| structural | 4 | 8 | 0 | 12 | 33% |
| unclassified | 2 | 0 | 0 | 2 | 100% |

## By Persona

| Persona | CLEAN | INCOMPLETE | MISSING | Total | Coverage |
|---------|-------|------------|---------|-------|----------|
| architect | 0 | 5 | 0 | 5 | 0% |
| developer | 1 | 4 | 0 | 5 | 20% |
| new-joiner | 3 | 1 | 1 | 5 | 60% |
| product-owner | 0 | 5 | 0 | 5 | 0% |

## Question Results

| # | Source | Question | Score | Entities | Time |
|---|--------|----------|-------|----------|------|
| 1 | seed | What happens to a claim between the moment a provider submit... | **CLEAN** | 15 | 23026ms |
| 2 | seed | Which team is responsible for maintaining the source of trut... | **CLEAN** | 15 | 9291ms |
| 3 | seed | What does it mean when a claim is 'pended,' and what trigger... | **CLEAN** | 15 | 11061ms |
| 4 | seed | How does the Rules Engine use the Eligibility Service during... | **CLEAN** | 15 | 18533ms |
| 5 | seed | What are the three possible dispositions a claim can receive... | **CLEAN** | 15 | 10247ms |
| 6 | seed | What formats does Claims Gateway accept for incoming claims,... | **CLEAN** | 15 | 11156ms |
| 7 | seed | At what fraud score threshold does a claim get held for SIU ... | **CLEAN** | 15 | 10139ms |
| 8 | seed | What is the difference between an EOB and an ERA 835, and wh... | **CLEAN** | 15 | 13081ms |
| 9 | seed | How does prior authorization relate to the main claims proce... | **CLEAN** | 15 | 12923ms |
| 10 | seed | If a member has coverage from two different insurers, which ... | **CLEAN** | 15 | 13419ms |
| 11 | doc | Why was Option C (transactional reservations with SELECT FOR... | **CLEAN** | 15 | 18963ms |
| 12 | doc | What caused the November 2024 plan year boundary incident wi... | **CLEAN** | 15 | 9614ms |
| 13 | doc | Where are pharmacy claims currently processed, and what is t... | **CLEAN** | 15 | 10136ms |
| 14 | doc | Who should be contacted for knowledge about the PharmaCore s... | **CLEAN** | 15 | 5412ms |
| 15 | doc | Why was HealthLogic Adjudicator chosen as the rules engine d... | **INCOMPLETE** | 15 | 13824ms |
| 16 | doc | What messaging system was used in the original 2021 claims p... | **CLEAN** | 15 | 7469ms |
| 17 | doc | What partitioning strategy is used for the clearview.claims.... | **CLEAN** | 15 | 9389ms |
| 18 | doc | Why was the fraud detection integration changed from asynchr... | **CLEAN** | 15 | 16412ms |
| 19 | doc | Why does the member portal show the same 'Under Review' stat... | **INCOMPLETE** | 15 | 14753ms |
| 20 | doc | What API change is required to support the claims timeline v... | **INCOMPLETE** | 15 | 10854ms |
| 21 | doc | What decision was made regarding when to generate the ERA 83... | **CLEAN** | 15 | 9024ms |
| 22 | doc | What database fields were proposed to fix void/reissue track... | **CLEAN** | 15 | 10861ms |
| 23 | doc | What fraud score threshold causes a claim to be automaticall... | **CLEAN** | 15 | 8478ms |
| 24 | doc | Why is member cost-sharing calculated against the allowed am... | **CLEAN** | 15 | 12495ms |
| 25 | doc | Why has the auto-adjudication rate been stuck around 81% and... | **INCOMPLETE** | 15 | 13822ms |
| 26 | doc | What is capitation and what decision was made regarding its ... | **CLEAN** | 15 | 10154ms |
| 27 | doc | What are the required steps an on-call engineer must follow ... | **CLEAN** | 15 | 12373ms |
| 28 | doc | Who is the primary contact for the Rules Engine migration, a... | **CLEAN** | 15 | 8852ms |
| 29 | doc | What were the key technical deficiencies in the Claims Submi... | **CLEAN** | 15 | 15723ms |
| 30 | doc | When migrating from v1 to v2, how should the v1 claim status... | **INCOMPLETE** | 15 | 11897ms |
| 31 | doc | What confidence score thresholds determine how an OCR-proces... | **CLEAN** | 15 | 9324ms |
| 32 | doc | What is the known discrepancy between the regulatory require... | **CLEAN** | 15 | 8941ms |
| 33 | doc | What are the common causes of an auth request processing bac... | **INCOMPLETE** | 15 | 22982ms |
| 34 | doc | What is required before manually approving an authorization ... | **CLEAN** | 15 | 8192ms |
| 35 | doc | How is a provider's network status determined for a specific... | **CLEAN** | 15 | 16128ms |
| 36 | doc | What are the possible values for a claim's status field, and... | **CLEAN** | 15 | 10903ms |
| 37 | doc | Which endpoint does the Rules Engine call to evaluate a memb... | **CLEAN** | 15 | 12492ms |
| 38 | doc | What happens to accumulator soft reservations if a claim is ... | **CLEAN** | 15 | 18431ms |
| 39 | doc | What steps should be taken to prepare the Eligibility Servic... | **INCOMPLETE** | 15 | 14009ms |
| 40 | doc | What are the known issues with Coordination of Benefits (COB... | **CLEAN** | 15 | 12511ms |
| 41 | persona | Where are the source code repositories located for each of t... | **INCOMPLETE** | 15 | 9011ms |
| 42 | persona | What are the steps to set up a local development environment... | **INCOMPLETE** | 15 | 19354ms |
| 43 | persona | Where can a new developer find logs for the Claims Gateway a... | **CLEAN** | 15 | 16008ms |
| 44 | persona | What is the deployment and release process for Claims Operat... | **INCOMPLETE** | 15 | 17384ms |
| 45 | persona | What is the testing strategy for the claims processing pipel... | **INCOMPLETE** | 15 | 11559ms |
| 46 | persona | What are the SLA targets for claims processing throughput an... | **INCOMPLETE** | 15 | 18228ms |
| 47 | persona | What is the security and authorization model across the clai... | **INCOMPLETE** | 15 | 17361ms |
| 48 | persona | How does the system scale to handle peak load periods such a... | **INCOMPLETE** | 15 | 19196ms |
| 49 | persona | What is the disaster recovery plan for the claims processing... | **INCOMPLETE** | 15 | 10378ms |
| 50 | persona | Beyond the Rules Engine vendor migration, what are the docum... | **INCOMPLETE** | 15 | 27610ms |
| 51 | persona | What are the key business capabilities delivered by each maj... | **INCOMPLETE** | 15 | 24372ms |
| 52 | persona | What are the primary user personas interacting with the clai... | **INCOMPLETE** | 15 | 33795ms |
| 53 | persona | What regulatory and compliance requirements govern the claim... | **INCOMPLETE** | 15 | 21229ms |
| 54 | persona | What are the key metrics used to measure the health and succ... | **INCOMPLETE** | 15 | 21365ms |
| 55 | persona | What are the most frequently reported pain points or recurri... | **INCOMPLETE** | 15 | 18328ms |
| 56 | persona | How do I get access to Confluence, the code repositories, an... | **MISSING** | 15 | 9710ms |
| 57 | persona | Who should a new joiner in Claims Engineering go to when the... | **INCOMPLETE** | 15 | 13961ms |
| 58 | persona | What does the Provider Directory contain, who on the Provide... | **CLEAN** | 15 | 13296ms |
| 59 | persona | What is the 'allowed amount' for a service, where does it co... | **CLEAN** | 15 | 16657ms |
| 60 | persona | What is the Rules Engine migration that is currently underwa... | **CLEAN** | 15 | 13005ms |

## Detailed Results

### Q1: What happens to a claim between the moment a provider submits it and when a payment is issued to them?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 23026ms

**Answer:** ## From Claim Submission to Provider Payment: The End-to-End Flow

Here is a step-by-step account of what happens to a claim between submission and payment:

---

### Step 1: Claim Submission & Initial Event
A provider submits a claim via EDI 837, REST API, or paper/OCR channels. This triggers the **Claim Submitted Event**, which initiates the processing pipeline in the Claims Gateway [Claim Submitted Event (business-event)]. Professional claims (EDI 837P) are processed in real-time with a 30-se...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claim Submitted Event | business-event | behavioral | vector+keyword+graph | 90% | 1.223 |  |
| 1 | Payment Engine | system | structural | vector+keyword+graph | 90% | 0.814 | executed_by from provider-payment-batching |
| 0 | Provider Payment Batching | process | behavioral | vector+keyword+graph | 90% | 1.169 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.669 |  |
| 0 | Payment Recoupment Process | process | behavioral | vector+keyword+graph | 85% | 0.994 |  |
| 1 | Duplicate Detection Process | process | behavioral | vector+keyword+graph | 90% | 0.881 | triggers from claim-submitted-event |
| 0 | Claims Processing Workflow | process | behavioral | vector+graph | 95% | 0.835 |  |
| 0 | Professional Claims Processing | process | behavioral | vector+graph | 90% | 0.818 |  |
| 0 | Post-Payment Fraud Analysis | process | behavioral | vector+keyword | 90% | 0.812 |  |
| 0 | Claim Submitted Event (Kafka) | business-event | behavioral | vector+keyword | 95% | 0.789 |  |
| 0 | Payment Cycle Processing | process | behavioral | vector+keyword | 90% | 0.766 |  |
| 1 | Claim Routing Process | process | behavioral | vector+graph | 95% | 0.762 | triggers from claim-submitted-event |
| 0 | Payment Completed Event | business-event | behavioral | vector+keyword | 95% | 0.755 |  |
| 0 | Claim Adjudicated Event | business-event | behavioral | vector+keyword | 90% | 0.734 |  |
| 0 | Payment Threshold Rules | domain-logic | behavioral | vector+keyword | 95% | 0.727 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Claim Submitted Event' and 'Claim Submitted Event (Kafka)' may be the same entity

---

### Q2: Which team is responsible for maintaining the source of truth for member enrollment and deductible tracking?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 9291ms

**Answer:** ## Team Responsible for Member Enrollment and Deductible Tracking

The **Member Services** team is responsible for maintaining the source of truth for member enrollment and deductible tracking.

Here's the breakdown:

- The **Eligibility Service** serves as the "source of truth for member enrollment information" and "maintains running totals of member accumulators including deductible amounts met and out-of-pocket maximum progress." [Eligibility Service]

- The Eligibility Service is **owned by ...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Benefits Administration Team | team | organizational | vector+keyword+graph | 90% | 1.154 |  |
| 0 | Eligibility Service | system | structural | vector+keyword+graph | 90% | 0.866 |  |
| 0 | Member Enrollment Workflow | process | behavioral | vector+keyword | 90% | 0.572 |  |
| 0 | Member Services ⚠️ | team | organizational | vector+keyword+graph | 90% | 1.119 |  |
| 0 | Benefits Administration System | system | structural | vector+keyword+graph | 90% | 0.740 |  |
| 0 | Accumulator Types Logic | domain-logic | behavioral | vector+keyword | 95% | 0.533 |  |
| 0 | Provider Network ⚠️ | team | organizational | vector+graph | 90% | 0.773 |  |
| 0 | Member | data-model | structural | vector+keyword | 100% | 0.533 |  |
| 0 | Enrollment Change Event | business-event | behavioral | vector+keyword | 95% | 0.497 |  |
| 0 | Dana Okafor | persona | organizational | vector+keyword | 95% | 0.691 |  |
| 0 | Accumulator | data-model | structural | vector+keyword | 100% | 0.521 |  |
| 0 | Compliance Team | team | organizational | vector+keyword | 85% | 0.648 |  |
| 0 | Members Table | data-model | structural | vector+keyword | 90% | 0.500 |  |
| 0 | Actuarial Team | team | organizational | vector+keyword | 80% | 0.586 |  |
| 0 | Claims Platform Team (2021) | team | organizational | vector+keyword | 95% | 0.498 |  |

**Gaps:**
- [low] orphan_entity: Member Services has no typed relationships
- [low] orphan_entity: Provider Network has no typed relationships

---

### Q3: What does it mean when a claim is 'pended,' and what triggers that outcome?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 11061ms

**Answer:** ## What It Means When a Claim Is 'Pended'

### Definition

When a claim is **pended**, it means the automated adjudication system has determined that the claim **cannot be automatically processed** and requires manual review by a claims examiner or specialist before a final pay or deny decision can be made. [Pend]

It is one of three possible dispositions — PAY, DENY, or PEND — that the Rules Engine can assign to a claim after evaluating it. [Rules Engine]

---

### What Triggers a Pend Outcome
...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | Rules Engine | system | structural | keyword+graph | 90% | 0.819 | used_in from pend |
| 0 | Pend | jargon-business | language | vector+keyword+graph | 90% | 1.068 |  |
| 0 | Claim Adjudicated Event | business-event | behavioral | vector+keyword+graph | 90% | 0.820 |  |
| 1 | Payment Engine | system | structural | vector+keyword+graph | 90% | 0.781 | consumed_by from claim-adjudicated-event |
| 0 | Claims Adjudicator Queue | jargon-business | language | vector+keyword+graph | 90% | 0.983 |  |
| 0 | Claim Submitted Event (Kafka) | business-event | behavioral | vector+keyword | 95% | 0.575 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.737 |  |
| 0 | Adjudication | jargon-business | language | vector+keyword+graph | 90% | 0.930 |  |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+graph | 90% | 0.564 |  |
| 0 | Claims API v1 Status Model | data-model | structural | vector+keyword | 95% | 0.576 |  |
| 0 | Multi-Claim Bundling | jargon-business | language | vector+keyword | 80% | 0.559 |  |
| 0 | Claim Submitted Event | business-event | behavioral | vector+keyword | 90% | 0.550 |  |
| 0 | Claims Gateway | system | structural | vector+keyword | 90% | 0.558 |  |
| 0 | 2024 Connection Pool Incident | jargon-business | language | vector+keyword | 80% | 0.536 |  |
| 0 | Fraud Circuit Breaker Logic | domain-logic | behavioral | vector+keyword | 100% | 0.468 |  |

---

### Q4: How does the Rules Engine use the Eligibility Service during adjudication, and what information does it look up?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 18533ms

**Answer:** ## How the Rules Engine Uses the Eligibility Service During Adjudication

### Overview of the Relationship

The Rules Engine communicates directly with the Eligibility Service during claim adjudication [Rules Engine], consuming the Eligibility Check API that the Eligibility Service exposes [Eligibility Check API]. This interaction is central to determining claim dispositions (PAY/DENY/PEND) [Adjudication Disposition Rules].

---

### Step-by-Step Flow

**1. Eligibility Verification at the Date o...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Point-in-Time Eligibility Rules | domain-logic | behavioral | vector+keyword+graph | 90% | 1.233 |  |
| 0 | Eligibility Service | system | structural | vector+keyword+graph | 90% | 1.003 |  |
| 0 | Eligibility Date of Service Rule | domain-logic | behavioral | vector+keyword+graph | 95% | 1.202 |  |
| 0 | Eligibility Check API | api | structural | vector+keyword+graph | 95% | 0.988 |  |
| 0 | Adjudication Disposition Rules | domain-logic | behavioral | vector+keyword | 90% | 0.828 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 0.987 |  |
| 0 | September 2022 Eligibility Service Outage | business-event | behavioral | vector+keyword | 100% | 0.824 |  |
| 0 | Eligibility Service Monitoring | process | behavioral | vector+keyword | 90% | 0.816 |  |
| 0 | Soft Reservation Created Event | business-event | behavioral | vector+keyword | 85% | 0.775 |  |
| 0 | Rules Engine Deployment | process | behavioral | vector+keyword | 90% | 0.739 |  |
| 0 | Eligibility Service Deployment | process | behavioral | vector+keyword | 85% | 0.711 |  |
| 0 | Claim Adjudicated Event | business-event | behavioral | vector+keyword | 90% | 0.701 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword | 95% | 0.689 |  |
| 0 | Eligibility Service Timeout Cascade | business-event | behavioral | vector+keyword | 85% | 0.689 |  |
| 0 | Authorization Validity Rules | domain-logic | behavioral | vector+keyword | 90% | 0.682 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Eligibility Service' and 'Eligibility Service Monitoring' may be the same entity
- [medium] ambiguous_entity: 'Eligibility Service' and 'Eligibility Service Deployment' may be the same entity
- [medium] ambiguous_entity: 'Rules Engine' and 'Rules Engine Deployment' may be the same entity

---

### Q5: What are the three possible dispositions a claim can receive from the Rules Engine, and what happens next in each case?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 10247ms

**Answer:** ## Three Possible Claim Dispositions from the Rules Engine

The Rules Engine produces one of three possible dispositions when adjudicating a claim: **PAY**, **DENY**, or **PEND**. [Rules Engine]

---

### 1. PAY Disposition

A PAY disposition occurs when the service is covered, the provider is contracted with rates available, medical policies are met, and the member has remaining benefits. [Adjudication Disposition Rules]

**What happens next:** A PAY disposition triggers the **Payment Engine** ...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Adjudication Disposition Rules | domain-logic | behavioral | vector+keyword+graph | 90% | 1.232 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 0.946 |  |
| 0 | Adjudication | jargon-business | language | vector+keyword+graph | 90% | 0.791 |  |
| 0 | Claim Adjudicated Event | business-event | behavioral | vector+keyword+graph | 90% | 1.168 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.632 |  |
| 0 | Multi-Claim Bundling | jargon-business | language | vector+keyword+graph | 80% | 0.687 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword | 95% | 0.823 |  |
| 0 | OCR Confidence Scoring Rules | domain-logic | behavioral | vector+keyword | 95% | 0.785 |  |
| 0 | Claim Routing Process | process | behavioral | vector+keyword | 95% | 0.744 |  |
| 0 | Point-in-Time Eligibility Rules | domain-logic | behavioral | vector+keyword | 90% | 0.726 |  |
| 0 | Rules Engine Deployment | process | behavioral | vector+keyword | 90% | 0.713 |  |
| 0 | Payment Threshold Rules | domain-logic | behavioral | vector+keyword | 95% | 0.648 |  |
| 0 | Claim Submitted Event (Kafka) | business-event | behavioral | vector+keyword | 95% | 0.642 |  |
| 0 | Soft Reservation Created Event | business-event | behavioral | vector+keyword | 85% | 0.637 |  |
| 0 | Payment Reconciliation Rework | process | behavioral | vector+keyword | 95% | 0.626 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Rules Engine' and 'Rules Engine Deployment' may be the same entity

---

### Q6: What formats does Claims Gateway accept for incoming claims, and what does it do before routing them downstream?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 11156ms

**Answer:** ## Claims Gateway: Accepted Formats and Pre-Routing Processing

### Incoming Claim Formats Accepted

Claims Gateway accepts three types of incoming claim submissions:

1. **EDI 837 files** from clearinghouses [Claims Gateway]
2. **JSON submissions** from the portal (primarily used by the Member Portal for out-of-network claim submissions) [Claims Submission API]
3. **OCR-processed paper claims** (originating from fax/mail, processed through the OCR Pipeline before reaching Claims Gateway) [Claim...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claim Routing Process | process | behavioral | vector+keyword+graph | 95% | 0.926 |  |
| 0 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.911 |  |
| 1 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.674 | owned_by from claims-gateway |
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword+graph | 90% | 0.857 |  |
| 0 | Claims Submission API | api | structural | vector+keyword+graph | 95% | 0.883 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 0.799 |  |
| 1 | Datadog | software-component | structural | vector+keyword+graph | 100% | 0.643 | monitors_via from claims-gateway-deployment |
| 0 | Fraud Detection Pre-Payment Integration | process | behavioral | vector+keyword | 95% | 0.566 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.604 |  |
| 0 | Claims Gateway Incident Response | process | behavioral | vector+keyword | 90% | 0.548 |  |
| 2 | Payment Engine | system | structural | vector+keyword+graph | 90% | 0.532 | applies_to from payment-cycle-timing-constraints |
| 0 | Claim Submitted Event (Kafka) | business-event | behavioral | vector+keyword | 95% | 0.544 |  |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword | 90% | 0.522 |  |
| 0 | March 2024 Claims Gateway Outage | business-event | behavioral | vector+keyword | 90% | 0.518 |  |
| 0 | Professional Claims Processing | process | behavioral | vector+keyword | 90% | 0.513 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Claims Gateway' and 'Claims Gateway Deployment' may be the same entity

---

### Q7: At what fraud score threshold does a claim get held for SIU review, and when during the claims lifecycle does fraud scoring occur?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 10139ms

**Answer:** ## Fraud Score Threshold and Timing for SIU Review

### Fraud Score Threshold

Claims are held for SIU review when they score **above 0.82** on the fraud detection model. This is part of a three-tier scoring system [Fraud Scoring Thresholds]:

| Score Range | Classification | Processing Path |
|-------------|---------------|-----------------|
| > 0.82 | HOLD | Immediately stopped and routed to SIU for manual review |
| 0.65 – 0.82 | FLAG | Proceeds to adjudication but tagged for post-payment ana...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | Fraud Detection | system | structural | vector+keyword+graph | 90% | 1.130 | enforced_by from fraud-scoring-thresholds |
| 0 | SIU | jargon-business | language | vector+keyword | 90% | 0.672 |  |
| 0 | SIU Review Process | process | behavioral | vector+keyword+graph | 90% | 0.919 |  |
| 2 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.551 | owned_by from rules-engine |
| 0 | XGBoost Fraud Model | data-model | structural | vector+keyword | 90% | 0.597 |  |
| 0 | Fraud Scoring Thresholds | domain-logic | behavioral | vector+keyword+graph | 95% | 0.919 |  |
| 0 | New Fraud Scoring Thresholds | domain-logic | behavioral | vector+keyword+graph | 95% | 0.864 |  |
| 0 | Post-Payment Fraud Analysis | process | behavioral | vector+keyword+graph | 90% | 0.862 |  |
| 0 | SIU Investigation Targets | domain-logic | behavioral | vector+keyword+graph | 90% | 0.730 |  |
| 0 | Fraud Scoring Algorithm | domain-logic | behavioral | vector+keyword | 90% | 0.593 |  |
| 0 | Fraud Circuit Breaker Logic | domain-logic | behavioral | vector+keyword | 100% | 0.586 |  |
| 0 | Fraud Detection Pre-Payment Integration | process | behavioral | vector+keyword | 95% | 0.579 |  |
| 0 | Fraud Alert Event | business-event | behavioral | vector+keyword | 85% | 0.577 |  |
| 0 | Fraud Detection Circuit Breaker Logic | domain-logic | behavioral | vector+keyword | 95% | 0.565 |  |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+keyword | 90% | 0.551 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Fraud Scoring Thresholds' and 'New Fraud Scoring Thresholds' may be the same entity

---

### Q8: What is the difference between an EOB and an ERA 835, and which systems or teams produce each one?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 13081ms

**Answer:** ## EOB vs. ERA 835: Key Differences

### What Each Document Is

**EOB (Explanation of Benefits)** is a document sent to **health plan members** that explains what services were covered, how much the plan paid, and what the member owes (copayments, deductibles, etc.) for a processed claim. [EOB]

**ERA 835 (Electronic Remittance Advice)** is a standardized electronic format sent to **healthcare providers** that communicates payment details — including what was paid, denied, or adjusted for each c...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | ERA 835 | data-model | structural | vector+keyword+graph | 95% | 1.250 |  |
| 0 | EOB | jargon-business | language | vector+keyword+graph | 90% | 1.023 |  |
| 0 | ERA 835 Timing Mismatch Problem | business-event | behavioral | vector+keyword+graph | 90% | 0.856 |  |
| 1 | Payment API | api | structural | vector+keyword+graph | 95% | 0.960 | contracts from era-835 |
| 0 | ERA 835 Settlement Confirmation | domain-logic | behavioral | vector+keyword+graph | 85% | 0.801 |  |
| 1 | Payment Engine | system | structural | vector+keyword+graph | 90% | 0.876 | produced_by from era-835 |
| 0 | EOB Generation Process | process | behavioral | vector+keyword+graph | 90% | 0.787 |  |
| 1 | Member Portal | system | structural | keyword+graph | 90% | 0.655 | used_in from eob |
| 1 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 0.524 | triggered_by from eob-generation-process |
| 0 | Rules Engine | system | structural | vector+keyword | 90% | 0.642 |  |
| 0 | EDI 834 | data-model | structural | vector+keyword | 90% | 0.629 |  |
| 2 | Claims Gateway | system | structural | keyword+graph | 90% | 0.626 | executed_by from claims-processing-workflow |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.525 |  |
| 0 | Manual Data Entry Tool | software-component | structural | vector+keyword | 90% | 0.506 |  |
| 0 | Splunk | software-component | structural | keyword | 100% | 0.492 |  |

---

### Q9: How does prior authorization relate to the main claims processing pipeline, and what percentage of auth requests are auto-approved?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 12923ms

**Answer:** ## Prior Authorization's Role in the Claims Processing Pipeline

### Where Prior Authorization Fits in the Main Pipeline

Prior authorization is **step 5 of the 9-step claims processing workflow**, occurring after fraud scoring and before rules engine adjudication. Specifically, the workflow sequence is: claim submission → format/duplicate validation → eligibility verification → fraud scoring → **pre-authorization checks** → rules engine adjudication → payment processing → post-payment analysis ...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Pre-Authorization Requirements | domain-logic | behavioral | vector+keyword+graph | 90% | 1.142 |  |
| 0 | Pre-Auth Service | system | structural | vector+keyword+graph | 90% | 1.020 |  |
| 0 | Auto-Approval Rate Investigation Process | process | behavioral | vector+keyword+graph | 90% | 1.129 |  |
| 0 | Authorization | data-model | structural | vector+keyword | 100% | 0.710 |  |
| 0 | OCR Pipeline Processing | process | behavioral | vector+keyword+graph | 85% | 1.096 |  |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.689 | executed_by from ocr-pipeline-processing |
| 0 | Manual Payment Approval Gate | process | behavioral | vector+keyword+graph | 90% | 0.998 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword | 95% | 0.819 |  |
| 0 | Pharmacy Claims Integration Scoping | process | behavioral | vector+keyword | 85% | 0.780 |  |
| 0 | Professional Claims Processing | process | behavioral | vector+keyword | 90% | 0.746 |  |
| 0 | Auth Request Processing Backlog | business-event | behavioral | vector+keyword | 95% | 0.723 |  |
| 0 | Auto-Approval Rate Drop | business-event | behavioral | vector+keyword | 95% | 0.720 |  |
| 0 | Pre-Auth Backlog Resolution Process | process | behavioral | vector+keyword | 90% | 0.711 |  |
| 0 | Institutional Claims Batch Processing | process | behavioral | vector+keyword | 90% | 0.686 |  |
| 0 | Auto-Adjudication Rate Targets | domain-logic | behavioral | vector+keyword | 100% | 0.675 |  |

---

### Q10: If a member has coverage from two different insurers, which concept governs how Clearview determines what to pay, and which systems would be involved in resolving it?
**Source:** seed (seed-context) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 13419ms

**Answer:** ## Coordination of Benefits (COB) When a Member Has Dual Coverage

### The Governing Concept

When a member has coverage from two different insurers, the concept that governs how Clearview determines what to pay is **Coordination of Benefits (COB)** [COB]. This is the business process and set of rules that determines which insurance plan pays primary, secondary, or tertiary to ensure proper payment coordination and prevent overpayment [COB].

More specifically, **COB Payer Order Rules** govern t...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 2 | Benefit Plan | data-model | structural | vector+keyword+graph | 100% | 0.823 | links_to from member |
| 0 | COB ⚠️ | jargon-business | language | vector+keyword+graph | 90% | 1.032 |  |
| 0 | Coordination of Benefits Logic | domain-logic | behavioral | vector+keyword+graph | 85% | 0.804 |  |
| 0 | Clearview Health Plans ⚠️ | external-party | organizational | vector+keyword+graph | 90% | 0.772 |  |
| 1 | Member | data-model | structural | keyword+graph | 100% | 0.777 | applies_to from coordination-of-benefits-logic |
| 0 | Clearview Standard Schedules | jargon-business | language | vector+graph | 85% | 0.718 |  |
| 2 | COB Payer Order Rules | domain-logic | behavioral | vector+keyword+graph | 95% | 0.648 | advises_on from compliance-team |
| 2 | Accumulator | data-model | structural | vector+keyword+graph | 100% | 0.752 | links_to from member |
| 0 | Adjudication | jargon-business | language | vector+keyword | 90% | 0.586 |  |
| 0 | COB Overpayment Problem | business-event | behavioral | vector+graph | 95% | 0.613 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.721 |  |
| 1 | COB Auto-Detection Project | process | behavioral | vector+keyword+graph | 90% | 0.595 | drives from cob-overpayment-incident |
| 1 | Rules Engine | system | structural | vector+graph | 90% | 0.660 | enforced_by from coordination-of-benefits-logic |
| 1 | Allowed Amount Calculation | domain-logic | behavioral | vector+keyword+graph | 95% | 0.572 | used_by from clearview-standard-schedules |
| 0 | Provider Self-Service Portal | system | structural | vector+keyword | 90% | 0.561 |  |

**Gaps:**
- [low] orphan_entity: COB has no typed relationships
- [low] orphan_entity: Clearview Health Plans has no typed relationships

---

### Q11: Why was Option C (transactional reservations with SELECT FOR UPDATE) chosen over Option A (event-sourced accumulators) and Option B (distributed locks) for the accumulator rework?
**Source:** doc (design-session-accumulator-rework.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 18963ms

**Answer:** ## Why Option C (Transactional Reservations with SELECT FOR UPDATE) Was Chosen

### The Three Options Evaluated

The team evaluated three candidate approaches before selecting Option C [Accumulator Rework - Transactional Reservations Decision]:

1. **Option A – Event-Sourced Accumulators**: Store every accumulator event as an immutable log, deriving balances by replaying events [Event-Sourced Accumulator Approach]
2. **Option B – Distributed Redis Locks**: Acquire a Redis lock scoped to member +...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | Accumulator | data-model | structural | vector+keyword+graph | 100% | 0.947 | applies_to from accumulator-rework-transactional-reservations |
| 0 | CLV-4521 | jargon-business | language | vector+keyword+graph | 90% | 0.876 |  |
| 0 | Accumulator Rework - Transactional Reservations Decision | decision | decision | vector+keyword+graph | 100% | 0.965 |  |
| 0 | Distributed Lock Accumulator Approach | domain-logic | behavioral | vector+keyword+graph | 90% | 0.868 |  |
| 2 | Eligibility Service | system | structural | keyword+graph | 90% | 0.682 | owned_by from accumulator |
| 0 | CLV-3901 | jargon-business | language | vector+keyword | 100% | 0.583 |  |
| 0 | Accumulator Concurrent Claim Analysis | domain-logic | behavioral | vector+keyword+graph | 90% | 0.844 |  |
| 0 | Payment Void Linkage Enhancement | data-model | structural | vector+keyword | 90% | 0.503 |  |
| 0 | Event-Sourced Accumulator Approach | domain-logic | behavioral | vector+keyword+graph | 90% | 0.833 |  |
| 1 | Soft Reservation Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 0.639 | supersedes from accumulator-rework-transactional-reservations |
| 0 | Accumulator Drift Event | business-event | behavioral | vector+keyword | 90% | 0.563 |  |
| 0 | November 2024 Accumulator Plan Year Incident | business-event | behavioral | vector+keyword | 90% | 0.537 |  |
| 0 | Accumulator Reservation Cleanup | process | behavioral | vector+keyword | 85% | 0.511 |  |
| 0 | Accumulator Cleanup Job Failures | business-event | behavioral | vector+keyword | 85% | 0.510 |  |
| 0 | Soft Reservation Created Event | business-event | behavioral | vector+keyword | 85% | 0.496 |  |

---

### Q12: What caused the November 2024 plan year boundary incident with accumulators, and what change was decided to prevent it from recurring?
**Source:** doc (design-session-accumulator-rework.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 9614ms

**Answer:** ## November 2024 Accumulator Plan Year Boundary Incident

### What Caused It

The incident occurred at the plan year boundary when **new plan year accumulators were not pre-created in advance**. When the transition happened, members were left without proper deductible and out-of-pocket maximum tracking until the batch job eventually ran and created the missing accumulators. [November 2024 Accumulator Plan Year Incident]

This caused two specific disruptions:
1. Disruption to **claims processing*...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 3 | Benefit Plan | data-model | structural | keyword+graph | 100% | 0.807 | links_to from member |
| 0 | CLV-3903 | jargon-business | language | vector+keyword | 100% | 0.703 |  |
| 0 | November 2024 Accumulator Plan Year Incident | business-event | behavioral | vector+keyword+graph | 90% | 0.916 |  |
| 1 | Accumulator Rework - Transactional Reservations Decision | decision | decision | vector+keyword+graph | 100% | 0.789 | triggered from november-2024-accumulator-incident |
| 1 | Accumulator | data-model | structural | vector+graph | 100% | 0.703 | affects from november-2024-accumulator-incident |
| 0 | 2024 Connection Pool Incident | jargon-business | language | vector+keyword | 80% | 0.662 |  |
| 0 | Plan Year Boundary Event | business-event | behavioral | vector+keyword+graph | 90% | 0.864 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.569 |  |
| 0 | INC-2022-0094 | jargon-business | language | vector+keyword | 100% | 0.584 |  |
| 0 | Open Enrollment Accumulator Pre-Creation | process | behavioral | vector+keyword+graph | 90% | 0.851 |  |
| 0 | CLV-3901 | jargon-business | language | vector+keyword | 100% | 0.583 |  |
| 0 | Accumulator Reset Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 0.808 |  |
| 0 | CLV-3902 | jargon-business | language | vector+keyword | 100% | 0.568 |  |
| 0 | Accumulator Cleanup Job Failures | business-event | behavioral | vector+graph | 85% | 0.568 |  |
| 0 | INC-2023-0031 | jargon-business | language | vector+keyword | 95% | 0.546 |  |

---

### Q13: Where are pharmacy claims currently processed, and what is the planned timeline for migrating them to the Clearview platform?
**Source:** doc (pharmacy-claims.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 10136ms

**Answer:** ## Pharmacy Claims: Current Processing and Migration Timeline

### Current Processing Location

Pharmacy claims are currently processed in **PharmaCore**, a legacy system that operates **entirely outside Clearview's main claims platform** [PharmaCore]. This system handles approximately **50,000 pharmacy claims per quarter** [PharmaCore]. Dana Okafor is identified as the person with the most knowledge about PharmaCore's current operations [PharmaCore].

### Migration Timeline

The migration plan ...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | PharmaCore | system | structural | vector+keyword+graph | 90% | 1.198 |  |
| 0 | Pharmacy Claims Integration Scoping | process | behavioral | vector+keyword+graph | 85% | 0.893 |  |
| 2 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.656 | belongs_to from priya-anand |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.898 | superseded_by from claimspro |
| 0 | Pharmacy Claims Migration (2026) | process | behavioral | vector+keyword+graph | 80% | 0.891 |  |
| 0 | Northeast Clearinghouse | external-party | organizational | vector+graph | 90% | 0.598 |  |
| 0 | ClaimsPro | system | structural | vector+graph | 95% | 0.874 |  |
| 0 | Clearview-Infra Repository | software-component | structural | vector+keyword | 85% | 0.687 |  |
| 0 | Provider Self-Service Portal | system | structural | vector+keyword | 90% | 0.666 |  |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword | 90% | 0.656 |  |
| 0 | GitHub | software-component | structural | vector+keyword | 90% | 0.654 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.641 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.632 |  |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.594 |  |
| 1 | Payment Engine | system | structural | vector+graph | 90% | 0.593 | superseded_by from claimspro |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q14: Who should be contacted for knowledge about the PharmaCore system, and who is the engineering contact for the future pharmacy claims migration?
**Source:** doc (pharmacy-claims.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 5412ms

**Answer:** ## Answer

**Knowledge Contact for PharmaCore:**
Dana Okafor is identified as the person with the most knowledge about PharmaCore's current operations. As stated in the PharmaCore documentation: "Dana Okafor has the most knowledge about this system's current operations." [PharmaCore (system, confidence: 90%)]

**Engineering Contact for the 2026 Pharmacy Claims Migration:**
Priya Anand is designated as the engineering contact for the future pharmacy claims migration planning. [Pharmacy Claims Mig...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | PharmaCore | system | structural | vector+keyword+graph | 90% | 1.234 |  |
| 1 | Formulary | jargon-business | language | vector+graph | 90% | 0.565 | related_to from pharmacy-claims-integration-scoping |
| 0 | Pharmacy Claims Integration Scoping | process | behavioral | vector+keyword+graph | 85% | 0.847 |  |
| 0 | Claims Platform Team (2021) | team | organizational | vector+keyword+graph | 95% | 0.782 |  |
| 0 | ClaimsPro | system | structural | vector+keyword+graph | 95% | 1.020 |  |
| 0 | Pharmacy Claims Migration (2026) | process | behavioral | vector+keyword+graph | 80% | 0.842 |  |
| 1 | Priya Anand | persona | organizational | vector+keyword+graph | 95% | 0.766 | involves from pharmacy-claims-migration-2026 |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.972 | superseded_by from claimspro |
| 1 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.673 | split_into from claims-platform-team-2021 |
| 1 | Provider Directory | system | structural | vector+keyword+graph | 80% | 0.826 | superseded_by from claimspro |
| 0 | ClaimsPro Inc. | external-party | organizational | vector+keyword | 90% | 0.508 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.712 |  |
| 0 | Samir Patel | persona | organizational | vector+keyword | 95% | 0.504 |  |
| 1 | Payment Engine | system | structural | vector+graph | 90% | 0.697 | superseded_by from claimspro |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.524 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q15: Why was HealthLogic Adjudicator chosen as the rules engine during the 2021 claims platform migration, and what were the alternatives considered?
**Source:** doc (original-architecture-2021.txt) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 13824ms

**Answer:** ## Why HealthLogic Adjudicator Was Chosen and Alternatives Considered

### Important Clarification on Timing

The question asks about a "2021 claims platform migration," but the available context indicates that HealthLogic Adjudicator was actually **selected in 2019**, not 2021. [HealthLogic Adjudicator] The 2021 period corresponds to the replacement of ClaimsPro, the legacy monolithic system. [ClaimsPro] HealthLogic was already in place by then.

---

### The 2019 Selection Decision

When Clear...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword+graph | 95% | 1.317 |  |
| 0 | HealthLogic SDK | jargon-tech | language | vector+keyword | 100% | 0.716 |  |
| 0 | HealthLogic Selection Decision | decision | decision | vector+keyword+graph | 95% | 0.949 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword+graph | 95% | 0.895 |  |
| 0 | HealthLogic Systems | external-party | organizational | vector+keyword+graph | 95% | 0.850 |  |
| 1 | Drools-Based Rules Engine | system | structural | vector+keyword+graph | 90% | 1.190 | superseded_by from healthlogic-adjudicator |
| 0 | Claims Adjudicator Queue | jargon-business | language | vector+keyword | 90% | 0.602 |  |
| 0 | ADR-2024-007 | decision | decision | vector+keyword+graph | 80% | 0.816 |  |
| 1 | Rachel Dominguez | persona | organizational | vector+keyword+graph | 95% | 0.684 | involves from rules-engine-migration-process |
| 1 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.122 | applies_to from healthlogic-selection-decision |
| 2 | Apex Consulting | external-party | organizational | vector+keyword+graph | 90% | 0.650 | belongs_to from rachel-dominguez |
| 2 | Drools | software-component | structural | vector+keyword+graph | 95% | 0.992 | depends_on from drools-rules-engine |
| 0 | HealthLogic SOAP Endpoint | api | structural | vector+keyword | 100% | 0.877 |  |
| 0 | ClaimsPro | system | structural | vector+keyword | 95% | 0.721 |  |
| 0 | Splunk | software-component | structural | vector+keyword | 100% | 0.711 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Drools-Based Rules Engine' and 'Rules Engine' may be the same entity

---

### Q16: What messaging system was used in the original 2021 claims platform architecture, what problem did it cause, and what replaced it?
**Source:** doc (original-architecture-2021.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 7469ms

**Answer:** ## Messaging System in the Original 2021 Claims Platform Architecture

### What It Was
The original 2021 claims platform architecture used **RabbitMQ** as its message broker for asynchronous communication between services. It served as the async messaging backbone for the initial microservices architecture. [RabbitMQ (2021)]

### The Problem It Caused
RabbitMQ had critical reliability issues under heavy load: **messages would be dropped if the queue depth exceeded memory limits, causing claims t...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | ClaimsPro | system | structural | vector+keyword+graph | 95% | 1.261 |  |
| 0 | Claims Platform Team (2021) | team | organizational | vector+keyword+graph | 95% | 0.902 |  |
| 0 | Pharmacy Claims Migration (2026) | process | behavioral | vector+keyword+graph | 80% | 0.748 |  |
| 0 | RabbitMQ (2021) | software-component | structural | vector+keyword+graph | 95% | 1.226 |  |
| 0 | ClaimsPro Inc. | external-party | organizational | vector+keyword+graph | 90% | 0.777 |  |
| 1 | PharmaCore | system | structural | vector+keyword+graph | 90% | 1.004 | supersedes from pharmacy-claims-migration-2026 |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.962 | superseded_by from claimspro |
| 1 | GKE Single Cluster (2021) | platform | structural | vector+keyword+graph | 90% | 0.892 | deployed_on from rabbitmq-2021 |
| 1 | Confluent Cloud Kafka | software-component | structural | vector+keyword+graph | 90% | 0.887 | superseded_by from rabbitmq-2021 |
| 1 | Payment Engine | system | structural | vector+keyword+graph | 90% | 0.844 | superseded_by from claimspro |
| 2 | GKE Production Cluster (prod-claims-01) | platform | structural | vector+keyword+graph | 95% | 0.822 | superseded_by from gke-single-cluster-2021 |
| 0 | Claims Submission API v1 | api | structural | vector+keyword | 95% | 0.749 |  |
| 2 | GKE Non-Production Cluster (nonprod-claims-01) | platform | structural | keyword+graph | 90% | 0.723 | superseded_by from gke-single-cluster-2021 |
| 0 | Claims API v1 Status Model | data-model | structural | vector+keyword | 95% | 0.710 |  |
| 3 | Rules Engine | system | structural | vector+keyword+graph | 90% | 0.706 | used_by from gke-prod-claims-01 |

---

### Q17: What partitioning strategy is used for the clearview.claims.claim.submitted Kafka topic, and why is that partitioning key significant?
**Source:** doc (integration-patterns-guide.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 9389ms

**Answer:** ## Partitioning Strategy for `clearview.claims.claim.submitted`

### Partitioning Key

The `clearview.claims.claim.submitted` Kafka topic is **partitioned by `member_id`**. [Claim Submitted Event (Kafka)]

### Why This Partitioning Key Is Significant

The `member_id` partitioning key is significant because it **ensures that all claims belonging to the same member are routed to the same partition**, which guarantees **ordering** of those messages. [Claim Submitted Event (Kafka)]

This ordering gu...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Confluent Cloud Kafka | software-component | structural | vector+keyword+graph | 90% | 1.107 |  |
| 0 | Consumer Groups ⚠️ | jargon-tech | language | vector+graph | 90% | 0.696 |  |
| 0 | Claim Submitted Event (Kafka) | business-event | behavioral | vector+keyword+graph | 95% | 0.882 |  |
| 1 | Claim | data-model | structural | vector+keyword+graph | 100% | 1.055 | carries from claim-submitted-event-kafka |
| 0 | Dead Letter Topic (DLT) ⚠️ | jargon-tech | language | vector+keyword | 90% | 0.575 |  |
| 0 | GKE Production Cluster (prod-claims-01) | platform | structural | vector+keyword+graph | 95% | 1.035 |  |
| 0 | Clearview-Infra Repository | software-component | structural | vector+keyword+graph | 85% | 0.957 |  |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.854 | published_by from claim-submitted-event-kafka |
| 1 | Fraud Detection | system | structural | keyword+graph | 90% | 0.742 | consumed_by from claim-submitted-event-kafka |
| 0 | Splunk | software-component | structural | vector+keyword | 100% | 0.715 |  |
| 1 | Kubernetes Deployment Manifests | data-model | structural | vector+graph | 90% | 0.683 | contains from clearview-infra-repo |
| 1 | Rules Engine | system | structural | keyword+graph | 90% | 0.661 | used_by from gke-prod-claims-01 |
| 1 | Member Portal | system | structural | keyword+graph | 90% | 0.640 | used_by from gke-prod-claims-01 |
| 0 | Claims Status History Model | data-model | structural | vector+keyword | 80% | 0.577 |  |
| 0 | Claims War Room Zoom | software-component | structural | vector+keyword | 90% | 0.574 |  |

**Gaps:**
- [low] orphan_entity: Consumer Groups has no typed relationships
- [low] orphan_entity: Dead Letter Topic (DLT) has no typed relationships

---

### Q18: Why was the fraud detection integration changed from asynchronous (Kafka) to synchronous (HTTP/REST), and what technical factor made this feasible?
**Source:** doc (integration-patterns-guide.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 16412ms

**Answer:** ## Why Fraud Detection Integration Changed from Async (Kafka) to Synchronous (HTTP/REST)

### The Core Problem with the Asynchronous Approach

The original fraud detection architecture used an asynchronous sidecar model where the Claims Gateway sent claims data via Kafka messages for fraud scoring. The fundamental problem was timing: "by the time fraud scores are returned, claims have already entered the Rules Engine for adjudication, eliminating the ability to block fraudulent claims before pay...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Fraud Detection Sync Migration | decision | decision | vector+keyword+graph | 90% | 1.124 |  |
| 0 | Fraud Detection Pre-Payment Integration | process | behavioral | vector+keyword+graph | 95% | 0.874 |  |
| 0 | Confluent Cloud Kafka | software-component | structural | vector+keyword+graph | 90% | 0.801 |  |
| 1 | Claims Operations ⚠️ | team | organizational | keyword+graph | 90% | 0.506 | owned_by from fraud-detection-pre-payment-integration |
| 0 | ClaimsPro Migration Decision | decision | decision | vector+keyword | 95% | 0.533 |  |
| 0 | Fraud Detection Sidecar Model | process | behavioral | vector+keyword+graph | 90% | 0.857 |  |
| 1 | Fraud Detection | system | structural | vector+keyword+graph | 90% | 0.715 | applies_to from fraud-detection-sync-migration |
| 0 | Provider Profile Sync Event | business-event | behavioral | vector+keyword+graph | 80% | 0.722 |  |
| 2 | XGBoost Fraud Model | data-model | structural | vector+keyword+graph | 90% | 0.677 | used_by from denormalized-provider-profiles |
| 3 | Fraud Model Retraining Pipeline | process | behavioral | vector+keyword+graph | 90% | 0.711 | produced_by from xgboost-fraud-model |
| 1 | Denormalized Provider Profiles | data-model | structural | vector+keyword+graph | 85% | 0.584 | updates from provider-profile-sync-event |
| 0 | Fraud Detection Deployment | process | behavioral | vector+keyword | 90% | 0.564 |  |
| 0 | Fraud Detection Circuit Breaker Logic | domain-logic | behavioral | vector+keyword | 95% | 0.541 |  |
| 0 | Fraud Alert Generated Event | business-event | behavioral | vector+keyword | 95% | 0.539 |  |
| 0 | Fraud Model Retraining Batch | process | behavioral | vector+keyword | 90% | 0.520 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q19: Why does the member portal show the same 'Under Review' status and visual treatment for both manually pended claims and claims held for SIU fraud investigation, and what message is displayed to members for these claims?
**Source:** doc (meeting-notes-member-portal-redesign.txt) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 14753ms

**Answer:** ## Why the Member Portal Shows Identical 'Under Review' Status for Both Manually Pended Claims and SIU Fraud Investigation Holds

### The Core Reason: Fraud Investigation Confidentiality

The Member Portal deliberately displays the same status for both types of held claims as a **compliance-driven requirement** to protect the integrity of fraud investigations. [Claims Status Masking Workflow] The specific rationale is that revealing a claim is under fraud investigation could alert potential frau...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Member Portal | system | structural | vector+keyword+graph | 90% | 1.132 |  |
| 0 | SIU | jargon-business | language | vector+keyword | 90% | 0.676 |  |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+keyword+graph | 90% | 0.923 |  |
| 1 | Member Services ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.649 | owned_by from claims-status-masking-workflow |
| 1 | Fraud Detection | system | structural | vector+keyword+graph | 90% | 0.973 | executed_by from post-payment-fraud-analysis |
| 0 | Claims Adjudicator Queue | jargon-business | language | vector+keyword | 90% | 0.657 |  |
| 0 | Fraud Investigation Status Display Rules | domain-logic | behavioral | vector+keyword+graph | 90% | 0.879 |  |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword | 90% | 0.757 |  |
| 0 | SIU Review Process | process | behavioral | vector+keyword+graph | 90% | 0.852 |  |
| 0 | Claims API v2 Status Model | data-model | structural | vector+keyword | 95% | 0.650 |  |
| 0 | Post-Payment Fraud Analysis | process | behavioral | vector+keyword+graph | 90% | 0.798 |  |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.647 |  |
| 1 | Fraud Scoring Thresholds | domain-logic | behavioral | vector+keyword+graph | 95% | 0.720 | triggered_by from siu-review-process |
| 0 | Claims API v1 Status Model | data-model | structural | vector+keyword | 95% | 0.640 |  |
| 0 | Member Portal Redesign | process | behavioral | vector+keyword | 95% | 0.619 |  |

**Gaps:**
- [low] orphan_entity: Member Services has no typed relationships

---

### Q20: What API change is required to support the claims timeline view in the portal redesign, where does the underlying data come from, and which team is responsible for implementing it?
**Source:** doc (meeting-notes-member-portal-redesign.txt) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 10854ms

**Answer:** ## Claims Timeline View: API Change, Data Source, and Ownership

### API Change Required

A new endpoint, **GET /claims/{id}/history**, needs to be added to the Claims Gateway API. [Claims Status History Endpoint] This endpoint will return each status transition with associated timestamps, enabling the member portal to display a visual timeline of claim processing progress (e.g., Received → Validated → Eligibility Verified → Adjudicated → Payment Scheduled → Paid). [Claims Status History Endpoin...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims Platform Team (2021) | team | organizational | vector+keyword+graph | 95% | 1.166 |  |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword+graph | 90% | 0.888 |  |
| 0 | API Versioning Lifecycle | process | behavioral | vector+keyword+graph | 90% | 0.741 |  |
| 0 | Claims Operations ⚠️ | team | organizational | vector+keyword | 90% | 0.679 |  |
| 0 | Claims Status History Model | data-model | structural | vector+keyword+graph | 80% | 0.787 |  |
| 0 | Member Portal Redesign | process | behavioral | vector+keyword | 95% | 0.589 |  |
| 0 | Marcus Reeves | persona | organizational | vector+keyword | 95% | 0.600 |  |
| 0 | Claims Submission API v2 | api | structural | vector+keyword+graph | 80% | 0.723 |  |
| 0 | Claims API v1 Decommission | process | behavioral | vector+keyword | 90% | 0.525 |  |
| 0 | Leo Chen | persona | organizational | vector+keyword | 90% | 0.594 |  |
| 0 | Claims Submission API v1 | api | structural | vector+keyword | 95% | 0.583 |  |
| 0 | Mei-Lin Torres | persona | organizational | vector+keyword | 90% | 0.537 |  |
| 0 | Claims API v2 Status Model | data-model | structural | vector+keyword | 95% | 0.579 |  |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.578 |  |
| 0 | Claims API v1 Status Model | data-model | structural | vector+keyword | 95% | 0.534 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q21: What decision was made regarding when to generate the ERA 835, and what dependency does this create?
**Source:** doc (design-session-payment-reconciliation.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 9024ms

**Answer:** ## Decision on ERA 835 Generation Timing and Its Dependencies

### The Decision

The team decided to **delay ERA 835 generation until EFT settlement confirmation is received from the banking partner**, accepting a 2-3 business day delay as preferable to reconciliation mismatches. [ERA 835 Timing Mismatch Problem]

This decision was driven by a specific problem: the Payment Engine was previously generating ERA 835 remittance advice at payment batch time, but EFT settlement occurs 2-3 business day...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | ERA 835 | data-model | structural | vector+keyword+graph | 95% | 1.201 |  |
| 0 | CLV-3901 | jargon-business | language | vector+keyword | 100% | 0.497 |  |
| 0 | ERA 835 Timing Mismatch Problem | business-event | behavioral | vector+keyword+graph | 90% | 0.836 |  |
| 0 | ADR-2024-007 | decision | decision | vector+keyword+graph | 80% | 0.729 |  |
| 1 | Payment Engine | system | structural | vector+keyword+graph | 90% | 0.743 | enforced_by from era-835-settlement-confirmation |
| 0 | ERA 835 Settlement Confirmation | domain-logic | behavioral | vector+keyword+graph | 85% | 0.834 |  |
| 0 | Database Restart Decision (2022 Outage) | decision | decision | vector+keyword | 100% | 0.568 |  |
| 1 | Payment API | api | structural | keyword+graph | 95% | 0.712 | contracts from era-835 |
| 0 | Payment Reconciliation Rework | process | behavioral | vector+keyword+graph | 95% | 0.706 |  |
| 0 | HealthLogic Selection Decision | decision | decision | vector+keyword | 95% | 0.550 |  |
| 1 | Eligibility Service | system | structural | vector+graph | 90% | 0.633 | involves from payment-reconciliation-rework |
| 0 | Provider Portal Deprioritization (2023) | decision | decision | vector+keyword | 95% | 0.547 |  |
| 1 | Rules Engine | system | structural | vector+graph | 90% | 0.607 | applies_to from adr-2024-007 |
| 0 | Accumulator Rework - Transactional Reservations Decision | decision | decision | vector+keyword | 100% | 0.501 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.568 |  |

---

### Q22: What database fields were proposed to fix void/reissue tracking in the payments table, and was a backfill of historical void records included in the plan?
**Source:** doc (design-session-payment-reconciliation.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 10861ms

**Answer:** ## Database Fields Proposed for Void/Reissue Tracking

### Proposed Fields

Three new fields were proposed to be added to the payments table to fix void/reissue tracking [Payments Table Void Linkage Schema]:

1. **`void_reason`** — VARCHAR(100) field providing human-readable context for why a payment was voided [Payments Table Void Linkage Schema]
2. **`linked_payment_id`** — BIGINT foreign key that links a voided payment to its replacement payment, establishing bidirectional linkage between voi...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Payments Table Void Linkage Schema | data-model | structural | vector+keyword+graph | 95% | 1.278 |  |
| 0 | INC-2023-0031 | jargon-business | language | vector+keyword | 95% | 0.592 |  |
| 0 | Void/Reissue Tracking Problem | business-event | behavioral | vector+keyword+graph | 90% | 0.860 |  |
| 1 | Nina Petrovich | persona | organizational | vector+keyword+graph | 95% | 0.595 | designed_by from void-reissue-workflow |
| 0 | Payment Void Linkage Enhancement | data-model | structural | vector+keyword+graph | 90% | 1.228 |  |
| 1 | Payment Reconciliation Rework | process | behavioral | vector+keyword+graph | 95% | 0.816 | part_of from payment-void-linkage-enhancement |
| 1 | Payment | data-model | structural | vector+keyword+graph | 100% | 1.173 | maps_to from payments-table-void-linkage |
| 0 | Void/Reissue Fencing Logic | domain-logic | behavioral | vector+keyword+graph | 85% | 0.813 |  |
| 3 | Authorization | data-model | structural | vector+keyword+graph | 100% | 0.763 | links_to from claim |
| 0 | Void/Reissue Workflow | process | behavioral | vector+keyword+graph | 90% | 0.789 |  |
| 3 | Member | data-model | structural | keyword+graph | 100% | 0.692 | links_to from claim |
| 2 | Payment Batching Query Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 0.697 | governed_by from nacha-file-generation |
| 0 | Members Table | data-model | structural | vector+keyword | 90% | 0.642 |  |
| 0 | Auth Requests Table | data-model | structural | vector+keyword | 95% | 0.640 |  |
| 0 | Criteria Load History Table | data-model | structural | vector+keyword | 90% | 0.630 |  |

---

### Q23: What fraud score threshold causes a claim to be automatically held and routed to the SIU for review in the Claims Gateway?
**Source:** doc (architecture-overview.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 8478ms

**Answer:** ## Fraud Score Threshold for Automatic Hold and SIU Routing

In the Claims Gateway, a claim is automatically held and routed to the Special Investigation Unit (SIU) for review when its fraud score exceeds **0.82**.

Specifically, any claim receiving a fraud score **above 0.82** (i.e., >0.82) triggers the **HOLD** status, which immediately stops processing and routes the claim to the SIU for manual review [Fraud Scoring Thresholds]. These claims **cannot proceed to adjudication** until the SIU ta...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | Fraud Detection | system | structural | vector+keyword+graph | 90% | 1.117 | enforced_by from fraud-scoring-thresholds |
| 0 | SIU | jargon-business | language | vector+keyword | 90% | 0.639 |  |
| 0 | SIU Review Process | process | behavioral | vector+keyword+graph | 90% | 0.910 |  |
| 2 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.569 | owned_by from fraud-detection |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.694 |  |
| 0 | Fraud Scoring Thresholds | domain-logic | behavioral | vector+keyword+graph | 95% | 0.892 |  |
| 0 | Claims Gateway | system | structural | vector+keyword | 90% | 0.637 |  |
| 0 | Post-Payment Fraud Analysis | process | behavioral | vector+keyword+graph | 90% | 0.854 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.616 |  |
| 0 | SIU Investigation Targets | domain-logic | behavioral | vector+keyword+graph | 90% | 0.791 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.581 |  |
| 0 | New Fraud Scoring Thresholds | domain-logic | behavioral | vector+graph | 95% | 0.653 |  |
| 0 | Fraud Detection Pre-Payment Integration | process | behavioral | vector+keyword | 95% | 0.623 |  |
| 0 | Fraud Circuit Breaker Logic | domain-logic | behavioral | vector+keyword | 100% | 0.589 |  |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+keyword | 90% | 0.582 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q24: Why is member cost-sharing calculated against the allowed amount rather than the billed amount, and where does the allowed amount come from?
**Source:** doc (architecture-overview.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 12495ms

**Answer:** ## Why Member Cost-Sharing Is Calculated Against the Allowed Amount

### The Core Principle

Member cost-sharing (deductible, copay, coinsurance) is **always calculated against the allowed amount, never the billed amount**. [Cost-Sharing Calculation Rules] This rule exists to **protect members from balance billing and ensure predictable out-of-pocket costs** regardless of what providers choose to bill. [Cost-Sharing Calculation Rules]

A concrete example illustrates this: if a provider bills $20...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Fee Schedule | data-model | structural | vector+keyword+graph | 100% | 1.034 |  |
| 0 | Allowed amount | jargon-business | language | vector+keyword+graph | 90% | 1.030 |  |
| 0 | Cost-Sharing Calculation Rules | domain-logic | behavioral | vector+keyword+graph | 95% | 0.934 |  |
| 3 | Member Services ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.583 | owned_by from eligibility-service |
| 2 | Accumulator | data-model | structural | vector+keyword+graph | 100% | 1.019 | links_to from member |
| 0 | Usual and Customary | jargon-business | language | vector+keyword+graph | 90% | 0.838 |  |
| 0 | Allowed Amount Calculation | domain-logic | behavioral | vector+keyword+graph | 95% | 0.876 |  |
| 1 | Member | data-model | structural | vector+keyword+graph | 100% | 0.968 | applies_to from cost-sharing-calculation-rules |
| 0 | Usual and Customary Rate | jargon-business | language | vector+keyword | 90% | 0.682 |  |
| 1 | Rules Engine | system | structural | keyword+graph | 90% | 0.791 | enforced_by from cost-sharing-calculation-rules |
| 0 | COB ⚠️ | jargon-business | language | vector+keyword | 90% | 0.591 |  |
| 2 | Benefit Plan | data-model | structural | vector+graph | 100% | 0.724 | links_to from member |
| 0 | Capitation | jargon-business | language | vector+keyword | 95% | 0.580 |  |
| 2 | Eligibility Service | system | structural | vector+graph | 90% | 0.582 | communicates_with from rules-engine |
| 0 | Member ID | jargon-business | language | vector+keyword | 95% | 0.524 |  |

**Gaps:**
- [low] orphan_entity: Member Services has no typed relationships
- [low] orphan_entity: COB has no typed relationships
- [medium] ambiguous_entity: 'Allowed amount' and 'Allowed Amount Calculation' may be the same entity

---

### Q25: Why has the auto-adjudication rate been stuck around 81% and when is it expected to reach the 85% target?
**Source:** doc (meeting-notes-quarterly-ops-review-2025q3.txt) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 13822ms

**Answer:** ## Why the Auto-Adjudication Rate Is Stuck at ~81% and When It's Expected to Reach 85%

### Current Performance

The auto-adjudication rate is currently running at approximately **81%** (specifically 81.3% in Q3 2025), against a target of **85%** [Auto-Adjudication Rate Targets] [Q3 2025 Performance Metrics].

### Why It's Stuck at ~81%

The primary reason the rate has not reached the 85% target is the **incomplete migration of business rules from the HealthLogic Adjudicator to the new Drools-ba...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | HealthLogic Adjudicator | system | structural | vector+keyword+graph | 95% | 1.033 | impacted_by from auto-adjudication-rate-targets |
| 0 | Adjudication | jargon-business | language | vector+keyword | 90% | 0.647 |  |
| 0 | Auto-Adjudication Rate Targets | domain-logic | behavioral | vector+keyword+graph | 100% | 0.949 |  |
| 2 | HealthLogic Systems | external-party | organizational | keyword+graph | 95% | 0.565 | owned_by from healthlogic-adjudicator |
| 3 | Drools | software-component | structural | vector+keyword+graph | 95% | 0.741 | depends_on from drools-rules-engine |
| 0 | Pend | jargon-business | language | vector+keyword | 90% | 0.580 |  |
| 0 | Auto-Approval Rate Drop | business-event | behavioral | vector+keyword+graph | 95% | 0.810 |  |
| 2 | Drools-Based Rules Engine | system | structural | vector+keyword+graph | 90% | 0.722 | superseded_by from healthlogic-adjudicator |
| 0 | Auto-Approval Rate Investigation Process | process | behavioral | vector+keyword+graph | 90% | 0.810 |  |
| 1 | Rules Engine | system | structural | vector+keyword+graph | 90% | 0.717 | applies_to from auto-adjudication-rate-targets |
| 0 | Q3 2025 Performance Metrics | domain-logic | behavioral | vector+keyword+graph | 90% | 0.726 |  |
| 1 | Fraud Detection | system | structural | vector+graph | 90% | 0.636 | enforced_by from siu-investigation-targets |
| 0 | SIU Investigation Targets | domain-logic | behavioral | vector+keyword+graph | 90% | 0.716 |  |
| 0 | Pre-Auth Service | system | structural | vector+keyword | 90% | 0.576 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.554 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Drools-Based Rules Engine' and 'Rules Engine' may be the same entity

---

### Q26: What is capitation and what decision was made regarding its potential implementation in the payment system?
**Source:** doc (meeting-notes-quarterly-ops-review-2025q3.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 10154ms

**Answer:** ## What is Capitation and the Decision Regarding Its Implementation

### What is Capitation?

Capitation is an alternative payment model where providers receive fixed monthly payments per enrolled member rather than being paid for each individual service rendered. [Capitation] This is expressed using the PMPM (Per-Member-Per-Month) metric, which represents the fixed monthly payment amount a provider receives for each enrolled member regardless of what services are actually provided to that membe...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Payment Engine | system | structural | vector+keyword+graph | 90% | 1.098 |  |
| 0 | Capitation | jargon-business | language | vector+keyword+graph | 95% | 1.114 |  |
| 0 | Provider Payment Batching | process | behavioral | vector+keyword+graph | 90% | 0.750 |  |
| 0 | Provider Portal Deprioritization (2023) | decision | decision | vector+keyword | 95% | 0.548 |  |
| 2 | Payment API | api | structural | vector+keyword+graph | 95% | 0.916 | contracts from era-835 |
| 0 | PMPM | jargon-business | language | vector+keyword+graph | 95% | 1.038 |  |
| 1 | Payment Threshold Rules | domain-logic | behavioral | vector+keyword+graph | 95% | 0.736 | governed_by from provider-payment-batching |
| 1 | ERA 835 | data-model | structural | vector+keyword+graph | 95% | 0.861 | produces from provider-payment-batching |
| 0 | Fee-for-Service | jargon-business | language | vector+graph | 90% | 0.773 |  |
| 0 | Post-Payment Fraud Analysis | process | behavioral | vector+keyword | 90% | 0.547 |  |
| 3 | Fraud Detection | system | structural | vector+keyword+graph | 90% | 0.804 | consumed_by from payment-api |
| 0 | INC-2023-0031 | jargon-business | language | vector+keyword | 95% | 0.570 |  |
| 0 | Payment | data-model | structural | vector+keyword | 100% | 0.678 |  |
| 0 | RBRVS | jargon-tech | language | vector+keyword | 100% | 0.532 |  |
| 0 | HETS (Healthcare Eligibility Transaction System) | system | structural | vector+keyword | 85% | 0.631 |  |

---

### Q27: What are the required steps an on-call engineer must follow when a SEV-1 incident occurs, and what are the response time expectations?
**Source:** doc (claims-ops-contacts-and-escalation.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 12373ms

**Answer:** ## Required Steps for On-Call Engineers During a SEV-1 Incident

### Definition of SEV-1
A SEV-1 incident represents the highest severity level, reserved for complete service outages, data loss, or severe business impact — such as full outage or data loss scenarios [SEV-1].

---

### Required Steps (in sequence)

1. **Acknowledge in PagerDuty within 15 minutes** of the alert firing [Incident Escalation Process]. PagerDuty manages the alerting and requires this acknowledgment within the 15-minute...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Incident Escalation Process | process | behavioral | vector+keyword+graph | 95% | 1.216 |  |
| 0 | PagerDuty | software-component | structural | vector+keyword | 95% | 0.663 |  |
| 0 | SEV-1 | jargon-business | language | vector+keyword+graph | 90% | 0.861 |  |
| 0 | Rules Engine Connectivity Incident (August 15) | business-event | behavioral | vector+keyword+graph | 90% | 1.135 |  |
| 0 | INC-2022-0094 | jargon-business | language | vector+keyword+graph | 100% | 0.775 |  |
| 0 | Alert Severity Classification | domain-logic | behavioral | vector+keyword+graph | 100% | 1.099 |  |
| 0 | Claims Operations On-Call Rotation | process | behavioral | vector+keyword | 100% | 0.833 |  |
| 0 | On-Call Handoff Process | process | behavioral | vector+keyword | 90% | 0.787 |  |
| 0 | Claims Gateway Incident Response | process | behavioral | vector+keyword | 90% | 0.766 |  |
| 0 | HikariCP Pool Exhaustion Event | business-event | behavioral | vector+keyword | 100% | 0.763 |  |
| 0 | MedConnect Encoding Issue | business-event | behavioral | vector+keyword | 85% | 0.697 |  |
| 0 | September 2022 Eligibility Service Outage | business-event | behavioral | vector+keyword | 100% | 0.689 |  |
| 0 | Payment Batch Failure Event | business-event | behavioral | vector+keyword | 100% | 0.628 |  |
| 0 | Accumulator Cleanup Job Failures | business-event | behavioral | vector+keyword | 85% | 0.602 |  |
| 0 | Soft Reservation Created Event | business-event | behavioral | vector+keyword | 85% | 0.580 |  |

---

### Q28: Who is the primary contact for the Rules Engine migration, and what is the status of the contractor supporting that work?
**Source:** doc (claims-ops-contacts-and-escalation.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 8852ms

**Answer:** ## Primary Contact and Contractor Status for Rules Engine Migration

### Primary Contact

The primary contact for the Rules Engine migration is **Rachel Dominguez**, a contractor serving as the Subject Matter Expert (SME) for the project. [Rachel Dominguez] She can be reached via:
- **Slack:** @rachel.dominguez
- **Email:** rachel.dominguez@apexconsulting.com [Rachel Dominguez]

Rachel brings deep expertise in claims adjudication system migrations, having successfully completed three similar pro...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.139 |  |
| 0 | DRL | jargon-tech | language | vector+keyword | 90% | 0.600 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword+graph | 95% | 0.903 |  |
| 0 | Rachel Dominguez | persona | organizational | vector+keyword+graph | 95% | 0.882 |  |
| 1 | Eligibility Service | system | structural | keyword+graph | 90% | 0.691 | communicates_with from rules-engine |
| 0 | CLV-4521 | jargon-business | language | vector+keyword | 90% | 0.546 |  |
| 0 | Rules Engine Connectivity Incident (August 15) | business-event | behavioral | vector+keyword+graph | 90% | 0.740 |  |
| 0 | Apex Consulting | external-party | organizational | vector+keyword+graph | 90% | 0.810 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword | 95% | 0.684 |  |
| 0 | Rules Engine Deployment | process | behavioral | vector+keyword | 90% | 0.575 |  |
| 1 | HealthLogic Systems | external-party | organizational | vector+keyword+graph | 95% | 0.772 | caused_by from rules-engine-connectivity-incident-aug-15 |
| 0 | Drools | software-component | structural | vector+keyword | 95% | 0.670 |  |
| 0 | Kenji Watanabe | persona | organizational | vector+keyword | 95% | 0.562 |  |
| 0 | Drools-Based Rules Engine | system | structural | vector+keyword | 90% | 0.661 |  |
| 0 | HealthLogic SOAP Endpoint | api | structural | vector+keyword | 100% | 0.581 |  |

---

### Q29: What were the key technical deficiencies in the Claims Submission API v1 that motivated the development of v2?
**Source:** doc (claims-gateway-api-v1-deprecated.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 15723ms

**Answer:** ## Key Technical Deficiencies in Claims Submission API v1

The development of Claims Submission API v2 was motivated by several critical technical deficiencies identified in v1:

### 1. Unlimited Batch Size (Stability Risk)
The `/claims/batch` endpoint in v1 had **no batch size limit**, which directly caused the March 2024 outage when a 14,000-claim batch overwhelmed the system [Claims Submission API v1]. This was the most severe deficiency, as it created a systemic availability risk. A remediat...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims Submission API v1 | api | structural | vector+keyword+graph | 95% | 1.225 |  |
| 0 | CLV-3902 | jargon-business | language | vector+keyword | 100% | 0.661 |  |
| 0 | Claims API v2 Validation Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 0.852 |  |
| 2 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.594 | owned_by from claims-gateway |
| 0 | Claims API v2 Status Model | data-model | structural | vector+keyword+graph | 95% | 1.194 |  |
| 0 | Claims API v1 Validation Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 0.835 |  |
| 0 | Claims Submission API v2 | api | structural | vector+keyword+graph | 80% | 1.187 |  |
| 0 | Claims API v1 Decommission | process | behavioral | vector+keyword | 90% | 0.577 |  |
| 1 | Claims API v1 Status Model | data-model | structural | vector+keyword+graph | 95% | 1.152 | supersedes from claims-api-v2-status-model |
| 1 | Claims Submission API | api | structural | vector+keyword+graph | 95% | 1.131 | supersedes from claims-submission-api-v2 |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.874 | exposed_by from claims-submission-api-v2 |
| 0 | Eligibility API v2 | api | structural | vector+keyword | 95% | 0.813 |  |
| 0 | Eligibility Check API | api | structural | vector+keyword | 95% | 0.600 |  |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword | 90% | 0.590 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.553 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Claims Submission API v1' and 'Claims Submission API' may be the same entity
- [medium] ambiguous_entity: 'Claims API v2 Validation Logic' and 'Claims API v1 Validation Logic' may be the same entity
- [medium] ambiguous_entity: 'Claims API v2 Status Model' and 'Claims API v1 Status Model' may be the same entity
- [medium] ambiguous_entity: 'Claims Submission API v2' and 'Claims Submission API' may be the same entity

---

### Q30: When migrating from v1 to v2, how should the v1 claim status 'COMPLETED' be mapped to v2 statuses, and what field should be checked to determine the correct mapping?
**Source:** doc (claims-gateway-api-v1-deprecated.txt) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 11897ms

**Answer:** ## Mapping v1 'COMPLETED' Status to v2 Statuses

### What 'COMPLETED' Meant in v1

In the v1 status model, **COMPLETED** indicated that a claim had been processed, but critically, it could mean either **paid or denied** — the status itself did not distinguish between these two outcomes. [Claims API v1 Status Model]

### The Key Field to Check

When a v1 claim showed `COMPLETED`, API consumers needed to check **additional fields** (such as `disposition`) to determine the actual outcome — whether ...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims API v2 Status Model | data-model | structural | vector+keyword+graph | 95% | 1.234 |  |
| 0 | Claims API v2 Validation Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 0.737 |  |
| 0 | Claims API v1 Status Model | data-model | structural | vector+keyword+graph | 95% | 1.225 |  |
| 0 | Claims API v1 Validation Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 0.732 |  |
| 1 | Claims Submission API v1 | api | structural | vector+keyword+graph | 95% | 1.079 | used_by from claims-api-v1-status-model |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+keyword | 90% | 0.562 |  |
| 0 | Claims Submission API v2 | api | structural | vector+keyword+graph | 80% | 1.043 |  |
| 0 | Claims API v1 Decommission | process | behavioral | vector+keyword | 90% | 0.545 |  |
| 1 | Claims Submission API | api | structural | vector+keyword+graph | 95% | 0.857 | supersedes from claims-submission-api-v2 |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword | 90% | 0.676 |  |
| 0 | Claims Status History Model | data-model | structural | vector+keyword | 80% | 0.665 |  |
| 0 | Eligibility API v2 | api | structural | vector+keyword | 95% | 0.639 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.588 |  |
| 1 | Claims Gateway | system | structural | vector+graph | 90% | 0.564 | exposed_by from claims-submission-api-v2 |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.549 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Claims API v2 Status Model' and 'Claims API v1 Status Model' may be the same entity
- [medium] ambiguous_entity: 'Claims API v2 Validation Logic' and 'Claims API v1 Validation Logic' may be the same entity
- [medium] ambiguous_entity: 'Claims Submission API v1' and 'Claims Submission API' may be the same entity
- [medium] ambiguous_entity: 'Claims Submission API v2' and 'Claims Submission API' may be the same entity

---

### Q31: What confidence score thresholds determine how an OCR-processed paper claim is routed — auto-submitted versus sent to manual data entry with pre-filled results versus sent with a blank form?
**Source:** doc (ocr-pipeline-extracted-spec.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 9324ms

**Answer:** ## OCR Confidence Score Routing Thresholds

The three confidence score thresholds that determine how a paper claim is routed are clearly defined as follows:

### Tier 1: Auto-Submit (>0.90)
Claims where the overall confidence score exceeds **0.90** are automatically routed to the Claims Gateway without human intervention — straight-through processing with no manual review required. [OCR Confidence Scoring Rules] [OCR Pipeline]

### Tier 2: Manual Data Entry with Pre-Filled OCR Results (0.70–0.90...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | OCR Confidence Scoring Rules | domain-logic | behavioral | vector+keyword+graph | 95% | 0.931 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword+graph | 95% | 0.873 |  |
| 1 | Maria Chen | persona | organizational | vector+keyword+graph | 90% | 0.712 | involves from manual-data-entry-process |
| 0 | Manual Data Entry Queue | jargon-business | language | vector+keyword | 85% | 0.576 |  |
| 0 | Manual Data Entry Process | process | behavioral | vector+keyword+graph | 95% | 0.868 |  |
| 1 | Manual Data Entry Tool | software-component | structural | vector+keyword+graph | 90% | 0.763 | executed_by from manual-data-entry-process |
| 0 | OCR Pipeline Processing | process | behavioral | vector+keyword+graph | 85% | 0.830 |  |
| 0 | Google Document AI | software-component | structural | vector+keyword | 95% | 0.529 |  |
| 0 | Fraud Scoring Thresholds | domain-logic | behavioral | vector+keyword+graph | 95% | 0.813 |  |
| 0 | CMS-1500 Form | data-model | structural | vector+keyword | 95% | 0.525 |  |
| 1 | OCR Extracted Claim Data Event | business-event | behavioral | vector+keyword+graph | 90% | 0.806 | produces from ocr-pipeline |
| 0 | UB-04 Form | data-model | structural | vector+keyword | 90% | 0.504 |  |
| 1 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 0.657 | part_of from ocr-pipeline-processing |
| 1 | SIU Review Process | process | behavioral | vector+keyword+graph | 90% | 0.657 | triggers from fraud-scoring-thresholds |
| 0 | Auto-Adjudication Rate Targets | domain-logic | behavioral | vector+keyword | 100% | 0.565 |  |

**Gaps:**
- [medium] ambiguous_entity: 'OCR Pipeline' and 'OCR Pipeline Processing' may be the same entity

---

### Q32: What is the known discrepancy between the regulatory requirement and the actual configured policy for scanned claims archive retention, and what is the ticket tracking it?
**Source:** doc (ocr-pipeline-extracted-spec.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 8941ms

**Answer:** ## Scanned Claims Archive Retention Discrepancy

### The Regulatory vs. Configured Policy Gap

There is a known 2-year discrepancy between the regulatory requirement and the actual configured retention policy for scanned claims archives:

- **Regulatory requirement**: State regulation mandates that original scanned claim images must be retained for **7 years** from the processing date. [Seven Year Retention Rule]
- **Actual configured policy**: The GCS lifecycle policy on the `gs://clearview-cla...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | OCR Pipeline | system | structural | vector+keyword+graph | 95% | 0.965 | part_of from claims-archive-process |
| 0 | CLV-5102 | jargon-business | language | vector+keyword+graph | 95% | 1.096 |  |
| 0 | Seven Year Retention Rule | domain-logic | behavioral | vector+keyword+graph | 90% | 0.853 |  |
| 2 | Claims Gateway | system | structural | keyword+graph | 90% | 0.831 | communicates_with from ocr-pipeline |
| 0 | CLV-4521 | jargon-business | language | vector+keyword+graph | 90% | 0.905 |  |
| 0 | Claims Archive Process | process | behavioral | vector+keyword+graph | 90% | 0.848 |  |
| 1 | Rules Engine | system | structural | keyword+graph | 90% | 0.756 | involves from void-reissue-tracking-problem |
| 0 | Claims Adjudicator Queue | jargon-business | language | vector+keyword | 90% | 0.684 |  |
| 0 | Void/Reissue Tracking Problem | business-event | behavioral | vector+keyword+graph | 90% | 0.800 |  |
| 3 | Authorization | data-model | structural | keyword+graph | 100% | 0.718 | links_to from claim |
| 0 | INC-2022-0094 | jargon-business | language | vector+keyword | 100% | 0.589 |  |
| 3 | Manual Data Entry Process | process | behavioral | vector+keyword+graph | 95% | 0.653 | triggers from ocr-extracted-claim-data-event |
| 2 | Eligibility Service | system | structural | keyword+graph | 90% | 0.615 | communicates_with from rules-engine |
| 0 | Manual Data Entry Tool | software-component | structural | vector+keyword | 90% | 0.585 |  |
| 2 | Claim | data-model | structural | vector+graph | 100% | 0.579 | maintains from leo-chen |

---

### Q33: What are the common causes of an auth request processing backlog in the Pre-Auth Service, and what steps should be taken to diagnose database connection pool exhaustion?
**Source:** doc (pre-auth-runbook.txt) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 22982ms

**Answer:** ## Common Causes of Auth Request Processing Backlog in the Pre-Auth Service

### Common Causes

The **PRE-AUTH-BACKLOG** alert fires when more than a configured threshold of authorization requests remain unprocessed after 4 hours. The common causes are:

1. **Pre-Auth Service Pod Failures** — Pod crashes or crashloops can halt all request processing entirely. [Auth Request Processing Backlog]

2. **Eligibility Service Unavailability** — If the Eligibility Service is down or unresponsive, the Pre...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Pre-Auth Backlog Resolution Process | process | behavioral | vector+keyword+graph | 90% | 1.234 |  |
| 0 | Auth Requests Table | data-model | structural | vector+keyword+graph | 95% | 0.904 |  |
| 0 | CLV-3905 | jargon-business | language | vector+keyword+graph | 100% | 0.806 |  |
| 0 | Auth Request Processing Backlog | business-event | behavioral | vector+keyword+graph | 95% | 1.222 |  |
| 0 | Pre-Auth Service | system | structural | vector+keyword+graph | 90% | 0.891 |  |
| 0 | HikariCP Pool Exhaustion Event | business-event | behavioral | vector+keyword | 100% | 0.850 |  |
| 0 | Connection Pool Utilization Alerting | domain-logic | behavioral | vector+keyword | 90% | 0.761 |  |
| 0 | Pre-Auth Service Deployment | process | behavioral | vector+keyword | 90% | 0.731 |  |
| 0 | Eligibility Service Timeout Cascade | business-event | behavioral | vector+keyword | 85% | 0.728 |  |
| 0 | Pre-Authorization Requirements | domain-logic | behavioral | vector+keyword | 90% | 0.724 |  |
| 0 | Auto-Approval Rate Investigation Process | process | behavioral | vector+keyword | 90% | 0.715 |  |
| 0 | Batch vs Real-time Connection Separation | domain-logic | behavioral | vector+keyword | 90% | 0.710 |  |
| 0 | Connection Pool Utilization Thresholds | domain-logic | behavioral | vector+keyword | 100% | 0.699 |  |
| 0 | Auto-Approval Rate Drop | business-event | behavioral | vector+keyword | 95% | 0.646 |  |
| 0 | September 2022 Eligibility Service Outage | business-event | behavioral | vector+keyword | 100% | 0.626 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Pre-Auth Service' and 'Pre-Auth Service Deployment' may be the same entity

---

### Q34: What is required before manually approving an authorization in the Pre-Auth Service, and how should the approval be recorded?
**Source:** doc (pre-auth-runbook.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 8192ms

**Answer:** ## Manual Authorization Approval in the Pre-Auth Service

### What is Required Before Manually Approving an Authorization

Before a manual authorization approval can be made, **written approval from Dr. Sarah Lin (Clinical Review Lead)** must be obtained — either via email or Slack. [Manual Auth Override Process]

This is described as an emergency procedure that "bypasses normal clinical criteria evaluation and requires explicit clinical leadership authorization for emergency situations." [Manua...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Authorization | data-model | structural | vector+keyword+graph | 100% | 1.289 |  |
| 2 | EOB | jargon-business | language | keyword+graph | 90% | 0.575 | produces from payment-cycle-processing |
| 0 | Pre-Authorization Requirements | domain-logic | behavioral | vector+keyword+graph | 90% | 0.888 |  |
| 1 | Auth-Required Service Lists | reference-data | reference | vector+keyword+graph | 85% | 0.769 | derives_from from pre-authorization-requirements |
| 1 | Dr. Sarah Lin | persona | organizational | vector+keyword+graph | 90% | 0.658 | involves from manual-auth-override |
| 0 | Pre-Auth Service | system | structural | vector+keyword+graph | 90% | 1.214 |  |
| 0 | Manual Auth Override Process | process | behavioral | vector+keyword+graph | 95% | 0.838 |  |
| 1 | Benefit Plan | data-model | structural | keyword+graph | 100% | 0.748 | applies_to from pre-authorization-requirements |
| 0 | Manual Payment Approval Gate | process | behavioral | vector+keyword+graph | 90% | 0.794 |  |
| 0 | Auth Requests Table | data-model | structural | vector+keyword | 95% | 0.730 |  |
| 0 | Pre-Auth Service Deployment | process | behavioral | vector+keyword | 90% | 0.606 |  |
| 0 | IAM Service | software-component | structural | vector+keyword | 90% | 0.648 |  |
| 0 | Auto-Approval Rate Investigation Process | process | behavioral | vector+keyword | 90% | 0.587 |  |
| 2 | Eligibility Service | system | structural | vector+graph | 90% | 0.603 | owned_by from member |
| 0 | Auto-Approval Rate Drop | business-event | behavioral | vector+keyword | 95% | 0.575 |  |

---

### Q35: How is a provider's network status determined for a specific claim, and can a provider be in-network for one plan but out-of-network for another?
**Source:** doc (claims-data-model-reference.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 16128ms

**Answer:** ## How Provider Network Status Is Determined for a Specific Claim

### 1. Network Status Is Plan-Specific

Yes, a provider can absolutely be in-network for one plan but out-of-network for another. Network participation is tracked **per plan** via the `provider_network_status` table, which stores status values (IN_NETWORK/OUT_OF_NETWORK/PENDING) with effective dates for each plan separately. [Provider]

### 2. The Provider Directory Is the Authoritative Source

The Provider Directory maintains ma...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | Provider | data-model | structural | vector+keyword+graph | 100% | 0.986 | applies_to from provider-network-date-of-service-rule |
| 0 | OON | jargon-business | language | vector+keyword+graph | 90% | 1.000 |  |
| 0 | Provider Network Date of Service Rule | domain-logic | behavioral | vector+keyword+graph | 90% | 0.861 |  |
| 0 | Unnamed Provider Group | external-party | organizational | vector+keyword+graph | 80% | 0.733 |  |
| 1 | Provider Directory | system | structural | vector+keyword+graph | 80% | 0.961 | uses from provider-network-date-of-service-rule |
| 0 | Credentialing Status Propagation | process | behavioral | vector+keyword+graph | 90% | 0.835 |  |
| 0 | Provider Network ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.702 |  |
| 2 | Member Portal | system | structural | vector+keyword+graph | 90% | 0.827 | consumed_by from provider-status-changed-event |
| 1 | Provider Status Changed Event | business-event | behavioral | vector+keyword+graph | 95% | 0.706 | triggered_by from credentialing-status-propagation |
| 1 | Credentialing Status Model | data-model | structural | vector+keyword+graph | 85% | 0.826 | updates from credentialing-status-propagation |
| 3 | Claims Submission API | api | structural | keyword+graph | 95% | 0.816 | supersedes from claims-submission-api-v2 |
| 2 | Provider Self-Service Portal | system | structural | keyword+graph | 90% | 0.803 | used_by from credentialing-status-model |
| 1 | Claims Submission API v1 | api | structural | keyword+graph | 95% | 0.768 | consumes from unnamed-provider-group |
| 0 | Benefit Plan | data-model | structural | vector+keyword | 100% | 0.698 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.682 |  |

**Gaps:**
- [low] orphan_entity: Provider Network has no typed relationships
- [medium] ambiguous_entity: 'Claims Submission API' and 'Claims Submission API v1' may be the same entity

---

### Q36: What are the possible values for a claim's status field, and what disposition values can be set after adjudication?
**Source:** doc (claims-data-model-reference.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 10903ms

**Answer:** ## Claim Status Field Values and Adjudication Disposition Values

### Status Field Values

The status values available depend on which API version is being used:

**Claims API v1 (deprecated)** uses a simplified four-state model [Claims API v1 Status Model]:
- **RECEIVED** — claim accepted
- **PROCESSING** — covers everything between intake and final disposition
- **COMPLETED** — claim processed (could be paid or denied)
- **REJECTED** — validation failure or system rejection

**Claims API v2 (c...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims API v1 Status Model | data-model | structural | vector+keyword+graph | 95% | 0.880 |  |
| 0 | Claim Adjudicated Event | business-event | behavioral | vector+keyword+graph | 90% | 0.825 |  |
| 0 | Pend | jargon-business | language | vector+keyword | 90% | 0.576 |  |
| 0 | Claims API v2 Status Model | data-model | structural | vector+keyword+graph | 95% | 0.811 |  |
| 0 | Adjudication Disposition Rules | domain-logic | behavioral | vector+keyword+graph | 90% | 0.818 |  |
| 0 | Adjudication | jargon-business | language | vector+keyword | 90% | 0.575 |  |
| 0 | Claims Status History Model | data-model | structural | vector+keyword+graph | 80% | 0.739 |  |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+keyword | 90% | 0.552 |  |
| 0 | Claims Adjudicator Queue | jargon-business | language | vector+keyword | 90% | 0.532 |  |
| 1 | Claims Status History Endpoint | api | structural | vector+keyword+graph | 90% | 0.691 | used_by from claims-status-history-model |
| 0 | Claim Submitted Event (Kafka) | business-event | behavioral | vector+keyword | 95% | 0.519 |  |
| 2 | Claims Submission API | api | structural | vector+keyword+graph | 95% | 0.671 | supersedes from claims-submission-api-v2 |
| 0 | Auto-Adjudication Rate Targets | domain-logic | behavioral | vector+keyword | 100% | 0.493 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.599 |  |
| 1 | Claims Submission API v1 | api | structural | vector+keyword+graph | 95% | 0.569 | used_by from claims-api-v1-status-model |

**Gaps:**
- [medium] ambiguous_entity: 'Claims API v1 Status Model' and 'Claims API v2 Status Model' may be the same entity

---

### Q37: Which endpoint does the Rules Engine call to evaluate a member's eligibility during claim adjudication, and why does it use that specific endpoint instead of the current eligibility endpoint?
**Source:** doc (eligibility-api-reference.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 12492ms

**Answer:** ## Endpoint Used by Rules Engine for Eligibility Evaluation During Claim Adjudication

### The Specific Endpoint

During claim adjudication, the Rules Engine calls the **point-in-time eligibility endpoint**:

**`GET /eligibility/{memberId}/asof/{date}`**

This endpoint is described as "critical for adjudication" and is used to evaluate member coverage as of the claim's **date of service**. [Eligibility Check API]

### Why This Endpoint Instead of the Current Eligibility Endpoint

The Rules Engin...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | HealthLogic SOAP Endpoint | api | structural | vector+keyword+graph | 100% | 1.255 |  |
| 0 | Adjudication | jargon-business | language | vector+keyword | 90% | 0.679 |  |
| 0 | Point-in-Time Eligibility Rules | domain-logic | behavioral | vector+keyword+graph | 90% | 0.891 |  |
| 2 | HealthLogic Systems | external-party | organizational | vector+keyword+graph | 95% | 0.691 | owned_by from healthlogic-adjudicator |
| 1 | Eligibility API v2 | api | structural | vector+keyword+graph | 95% | 1.202 | enforced_by from point-in-time-eligibility-rules |
| 0 | Eligibility Date of Service Rule | domain-logic | behavioral | vector+keyword+graph | 95% | 0.850 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.186 |  |
| 0 | Eligibility Check API | api | structural | vector+keyword+graph | 95% | 1.164 |  |
| 1 | Eligibility Service | system | structural | vector+keyword+graph | 90% | 1.068 | communicates_with from rules-engine |
| 1 | HealthLogic Adjudicator | system | structural | vector+keyword+graph | 95% | 1.041 | exposed_by from healthlogic-soap-endpoint |
| 2 | Accumulator | data-model | structural | vector+keyword+graph | 100% | 0.994 | contracts from eligibility-api-v2 |
| 2 | Drools-Based Rules Engine | system | structural | vector+keyword+graph | 90% | 0.899 | superseded_by from healthlogic-adjudicator |
| 1 | Claim | data-model | structural | vector+keyword+graph | 100% | 0.847 | applies_to from eligibility-date-of-service-rule |
| 3 | Drools | software-component | structural | vector+keyword+graph | 95% | 0.840 | depends_on from drools-rules-engine |
| 2 | Benefit Plan | data-model | structural | vector+graph | 100% | 0.684 | contracts from eligibility-api-v2 |

**Gaps:**
- [medium] ambiguous_entity: 'Rules Engine' and 'Drools-Based Rules Engine' may be the same entity

---

### Q38: What happens to accumulator soft reservations if a claim is denied or if the Rules Engine crashes mid-adjudication?
**Source:** doc (eligibility-api-reference.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 18431ms

**Answer:** ## What Happens to Accumulator Soft Reservations on Claim Denial or Rules Engine Crash

### Scenario 1: Claim is Denied

When a claim is denied, the soft reservation is released normally through the standard adjudication completion flow:

- The Rules Engine emits a **Claim Adjudicated Event** with a DENY disposition [Claim Adjudicated Event]
- This triggers the **Soft Reservation Released Event**, which fires when the Rules Engine completes claim adjudication — whether approved **or denied** [So...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Accumulator Reservation Cleanup | process | behavioral | vector+keyword+graph | 85% | 1.214 |  |
| 0 | CLV-4521 | jargon-business | language | vector+keyword+graph | 90% | 0.848 |  |
| 0 | Soft Reservation Created Event | business-event | behavioral | vector+keyword+graph | 85% | 1.195 |  |
| 0 | Soft Reservation Released Event | business-event | behavioral | vector+keyword+graph | 80% | 1.102 |  |
| 0 | Soft Reservation Logic | domain-logic | behavioral | vector+keyword+graph | 90% | 1.081 |  |
| 0 | Claim Adjudicated Event | business-event | behavioral | vector+keyword | 90% | 0.805 |  |
| 0 | Accumulator Drift Event | business-event | behavioral | vector+keyword | 90% | 0.783 |  |
| 0 | Adjudication Disposition Rules | domain-logic | behavioral | vector+keyword | 90% | 0.773 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword | 95% | 0.689 |  |
| 0 | Rules Engine Deployment | process | behavioral | vector+keyword | 90% | 0.684 |  |
| 0 | Accumulator Concurrent Claim Analysis | domain-logic | behavioral | vector+keyword | 90% | 0.681 |  |
| 0 | Auto-Adjudication Rate Targets | domain-logic | behavioral | vector+keyword | 100% | 0.675 |  |
| 0 | Accumulator Cleanup Job Failures | business-event | behavioral | vector+keyword | 85% | 0.663 |  |
| 0 | Event-Sourced Accumulator Approach | domain-logic | behavioral | vector+keyword | 90% | 0.647 |  |
| 0 | OCR Confidence Scoring Rules | domain-logic | behavioral | vector+keyword | 95% | 0.636 |  |

---

### Q39: What steps should be taken to prepare the Eligibility Service for the open enrollment period, and in what order?
**Source:** doc (eligibility-monitoring-guide.txt) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 14009ms

**Answer:** ## Steps to Prepare the Eligibility Service for Open Enrollment

Based on the available knowledge, here is the ordered sequence of preparation steps:

---

### Pre-Enrollment Preparation (2 Weeks Before November 1)

1. **Scale up pods** — Increase HPA minimum replicas from 3 to 6 to handle the anticipated 10x enrollment update volume [Open Enrollment Scaling Process]

2. **Increase database connection pool** — Expand from 100 to 200 connections to support the increased load [Open Enrollment Scal...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Open Enrollment Scaling Process | process | behavioral | vector+keyword+graph | 95% | 1.271 |  |
| 0 | Eligibility Service | system | structural | vector+keyword+graph | 90% | 0.912 |  |
| 0 | Open Enrollment Preparation | process | behavioral | vector+keyword+graph | 90% | 1.239 |  |
| 0 | Eligibility Service Deployment | process | behavioral | vector+keyword+graph | 85% | 1.213 |  |
| 0 | Open Enrollment Process | process | behavioral | vector+keyword+graph | 80% | 1.058 |  |
| 1 | Accumulator Audit Job | process | behavioral | vector+keyword+graph | 85% | 0.838 | triggers from open-enrollment-scaling |
| 0 | Member Enrollment Workflow | process | behavioral | vector+keyword | 90% | 0.818 |  |
| 0 | Open Enrollment Accumulator Pre-Creation | process | behavioral | vector+keyword | 90% | 0.790 |  |
| 0 | Eligibility Service Monitoring | process | behavioral | vector+keyword | 90% | 0.772 |  |
| 0 | Eligibility Date of Service Rule | domain-logic | behavioral | vector+keyword | 95% | 0.771 |  |
| 0 | September 2022 Eligibility Service Outage | business-event | behavioral | vector+keyword | 100% | 0.743 |  |
| 0 | EDI 834 Processing | process | behavioral | vector+keyword | 80% | 0.740 |  |
| 0 | Enrollment Change Event | business-event | behavioral | vector+keyword | 95% | 0.700 |  |
| 0 | Eligibility Service Timeout Cascade | business-event | behavioral | vector+keyword | 85% | 0.697 |  |
| 0 | New Member Enrollment | process | behavioral | vector+keyword | 80% | 0.662 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Open Enrollment Scaling Process' and 'Open Enrollment Process' may be the same entity
- [medium] ambiguous_entity: 'Eligibility Service' and 'Eligibility Service Deployment' may be the same entity
- [medium] ambiguous_entity: 'Eligibility Service' and 'Eligibility Service Monitoring' may be the same entity

---

### Q40: What are the known issues with Coordination of Benefits (COB) data, and what is the typical consequence when COB data is incorrect?
**Source:** doc (eligibility-monitoring-guide.txt) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 12511ms

**Answer:** ## Known Issues with COB Data and Consequences of Incorrect COB Data

### Known Issues with COB Data

**1. Data Staleness**
COB data is frequently outdated because members don't promptly report changes in their other coverage. [COB Data Model] This affects an estimated **30–40% of members** who have other coverage on file. [COB Overpayment Problem]

**2. Inadequate Verification Methods**
Current methods to keep COB data current are proving insufficient:
- The **Member Portal COB Questionnaire** ...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | COB Data Model | data-model | structural | vector+keyword+graph | 95% | 1.266 |  |
| 0 | COB ⚠️ | jargon-business | language | vector+keyword+graph | 90% | 1.076 |  |
| 0 | COB Overpayment Problem | business-event | behavioral | vector+keyword+graph | 95% | 0.908 |  |
| 1 | Compliance Team | team | organizational | vector+keyword+graph | 85% | 0.691 | identified_by from cob-overpayment-incident |
| 2 | Benefit Plan | data-model | structural | vector+keyword+graph | 100% | 0.902 | links_to from member |
| 0 | EOB | jargon-business | language | vector+keyword | 90% | 0.638 |  |
| 0 | COB Auto-Detection Project | process | behavioral | vector+keyword+graph | 90% | 0.908 |  |
| 2 | Accumulator | data-model | structural | vector+keyword+graph | 100% | 0.819 | links_to from member |
| 0 | COB Questionnaire | process | behavioral | vector+keyword+graph | 90% | 0.878 |  |
| 0 | Eligibility Response | data-model | structural | vector+keyword | 90% | 0.685 |  |
| 1 | COB Payer Order Rules | domain-logic | behavioral | vector+keyword+graph | 95% | 0.730 | governed_by from cob-data-model |
| 1 | Member Portal | system | structural | keyword+graph | 90% | 0.682 | hosted_on from cob-questionnaire |
| 0 | Annual COB Verification Letters | process | behavioral | vector+keyword | 90% | 0.645 |  |
| 0 | Benefits Administration System | system | structural | vector+keyword | 90% | 0.591 |  |
| 0 | Coordination of Benefits Logic | domain-logic | behavioral | vector+keyword | 85% | 0.596 |  |

**Gaps:**
- [low] orphan_entity: COB has no typed relationships

---

### Q41: Where are the source code repositories located for each of the core systems — Claims Gateway, Rules Engine, Eligibility Service, Payment Engine, Pre-Auth Service, Fraud Detection, Member Portal, and Provider Directory — and what branching strategy is used?
**Source:** persona (developer) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 9011ms

**Answer:** ## Source Code Repositories and Branching Strategy

### Repository Location

All claims platform services — including Claims Gateway, Rules Engine, Eligibility Service, Payment Engine, Pre-Auth Service, Fraud Detection, Member Portal, and Provider Directory — have their source code hosted on **GitHub** under the **clearview-health organization**. [GitHub]

Specifically:
- **Claims Gateway**, **Rules Engine**, **Payment Engine**, **Fraud Detection**, and **Pre-Auth Service** are core claims proce...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 1 | Eligibility Service | system | structural | vector+keyword+graph | 90% | 1.164 | communicates_with from rules-engine |
| 0 | Spring Boot | jargon-tech | language | vector+keyword | 100% | 0.748 |  |
| 0 | Claims-Ops Namespace | platform | structural | vector+keyword+graph | 90% | 1.152 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.141 |  |
| 1 | Payment Engine | system | structural | vector+keyword+graph | 90% | 1.010 | hosts from claims-ops-namespace |
| 1 | Fraud Detection | system | structural | keyword+graph | 90% | 0.956 | hosts from claims-ops-namespace |
| 0 | GitHub | software-component | structural | vector+graph | 90% | 0.931 |  |
| 0 | Claims Gateway | system | structural | vector+graph | 90% | 0.917 |  |
| 1 | Pre-Auth Service | system | structural | vector+keyword+graph | 90% | 0.902 | hosts from claims-ops-namespace |
| 0 | PharmaCore | system | structural | vector+graph | 90% | 0.891 |  |
| 0 | Provider Self-Service Portal | system | structural | vector+keyword | 90% | 0.841 |  |
| 0 | GKE Production Cluster (prod-claims-01) | platform | structural | vector+keyword | 95% | 0.835 |  |
| 0 | Datadog | software-component | structural | vector+keyword | 100% | 0.805 |  |
| 0 | Member Portal | system | structural | vector+keyword | 90% | 0.775 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.743 |  |

---

### Q42: What are the steps to set up a local development environment for Claims Gateway, including required dependencies, environment variables, service mocks or stubs needed for downstream systems, and how to submit a test claim end-to-end locally?
**Source:** persona (developer) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 19354ms

**Answer:** ## Setting Up a Local Development Environment for Claims Gateway

Based on the available knowledge entities, I can provide **partial** guidance on this topic. Here is what the documentation covers:

---

### What We Know About Environments

The environment structure follows a three-stage promotion pipeline: **dev → staging → production**. The dev environment runs in the `nonprod-claims-01` dev namespace, deploys on feature branch pushes, uses a shared database instance with separate logical data...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claim Routing Process | process | behavioral | vector+keyword+graph | 95% | 1.206 |  |
| 0 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.985 |  |
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword+graph | 90% | 1.190 |  |
| 0 | Claim | data-model | structural | vector+keyword+graph | 100% | 0.980 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 1.146 |  |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.696 |  |
| 0 | Claims Gateway Incident Response | process | behavioral | vector+keyword | 90% | 0.739 |  |
| 0 | Claim Submitted Event (Kafka) | business-event | behavioral | vector+keyword | 95% | 0.729 |  |
| 0 | Claims Appeals Process | process | behavioral | vector+keyword | 90% | 0.686 |  |
| 0 | GitHub Actions CI/CD Pipeline | process | behavioral | vector+keyword | 95% | 0.674 |  |
| 0 | Environment Promotion Pipeline | process | behavioral | vector+keyword | 95% | 0.661 |  |
| 0 | Claims Archive Process | process | behavioral | vector+keyword | 90% | 0.649 |  |
| 0 | March 2024 Claims Gateway Outage | business-event | behavioral | vector+keyword | 90% | 0.641 |  |
| 0 | Secure Messaging Claim Context Process | process | behavioral | vector+keyword | 70% | 0.633 |  |
| 0 | Eligibility Service Timeout Cascade | business-event | behavioral | vector+keyword | 85% | 0.603 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Claims Gateway' and 'Claims Gateway Deployment' may be the same entity

---

### Q43: Where can a new developer find logs for the Claims Gateway and Rules Engine in production, what logging aggregation tool is used, and what dashboards or alerts exist for monitoring claim processing throughput and error rates?
**Source:** persona (developer) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 16008ms

**Answer:** ## Logs, Monitoring Tools, and Dashboards for Claims Gateway and Rules Engine

### Where to Find Logs

A new developer can find logs for the Claims Gateway and Rules Engine in **Splunk**, which serves as the centralized logging platform for all claims processing systems. [Splunk]

Specifically, Splunk indexes logs from all Claims Platform services using dedicated indexes:
- **`claims-gateway`** — for Claims Gateway logs
- **`rules-engine`** — for Rules Engine logs
- **`claims-batch-processing`**...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Splunk | software-component | structural | vector+keyword+graph | 100% | 1.320 |  |
| 0 | Claims Gateway Incident Response | process | behavioral | vector+keyword+graph | 90% | 0.817 |  |
| 0 | Datadog | software-component | structural | vector+keyword+graph | 100% | 1.274 |  |
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword+graph | 90% | 0.813 |  |
| 3 | Claims Submission API | api | structural | vector+keyword+graph | 95% | 1.009 | supersedes from claims-submission-api-v2 |
| 1 | March 2024 Claims Gateway Outage | business-event | behavioral | vector+keyword+graph | 90% | 0.684 | triggered_by from claims-gateway-incident-response |
| 0 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 1.003 |  |
| 1 | Rules Engine | system | structural | vector+keyword+graph | 90% | 0.986 | used_by from splunk |
| 0 | GKE Production Cluster (prod-claims-01) | platform | structural | vector+keyword | 95% | 0.869 |  |
| 2 | Claims Submission API v1 | api | structural | vector+keyword+graph | 95% | 0.793 | triggered_by from march-2024-claims-gateway-outage |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.722 |  |
| 1 | PagerDuty | software-component | structural | vector+graph | 95% | 0.688 | communicates_with from datadog |
| 0 | HealthLogic SOAP Endpoint | api | structural | vector+keyword | 100% | 0.664 |  |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword | 90% | 0.663 |  |
| 0 | Drools-Based Rules Engine | system | structural | vector+keyword | 90% | 0.656 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Claims Gateway Deployment' and 'Claims Gateway' may be the same entity
- [medium] ambiguous_entity: 'Claims Submission API' and 'Claims Submission API v1' may be the same entity

---

### Q44: What is the deployment and release process for Claims Operations-owned services — specifically Claims Gateway and Payment Engine — including how code moves from a feature branch to production, who approves releases, and how often deployments occur?
**Source:** persona (developer) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 17384ms

**Answer:** ## Deployment and Release Process for Claims Gateway and Payment Engine

### How Code Moves from Feature Branch to Production

The pipeline follows a standardized six-stage process for all claims platform services [GitHub Actions CI/CD Pipeline]:

1. **Build** — Code is compiled and unit tests run
2. **Test** — Integration tests run against test containers
3. **Security Scan** — Snyk scans dependencies; Trivy scans container images
4. **Build Image** — Docker image is built and pushed to Artifac...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword+graph | 90% | 1.263 |  |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 1.031 | applies_to from claims-gateway-deployment |
| 0 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.828 |  |
| 0 | Manual Payment Approval Gate | process | behavioral | vector+keyword+graph | 90% | 1.093 |  |
| 0 | Claims-Ops Namespace | platform | structural | vector+graph | 90% | 0.874 |  |
| 0 | Claim Routing Process | process | behavioral | vector+keyword+graph | 95% | 1.092 |  |
| 0 | GKE Production Cluster (prod-claims-01) | platform | structural | vector+keyword | 95% | 0.824 |  |
| 1 | Payment Cycle Processing | process | behavioral | vector+keyword+graph | 90% | 0.957 | part_of from manual-payment-approval-gate |
| 1 | Rules Engine | system | structural | vector+keyword+graph | 90% | 0.812 | hosts from claims-ops-namespace |
| 1 | Payment Cycle Timing Constraints | domain-logic | behavioral | vector+keyword+graph | 100% | 0.898 | governed_by from claims-gateway-deployment |
| 0 | Payment Engine Deployment | process | behavioral | vector+keyword | 95% | 0.854 |  |
| 0 | Claims Operations On-Call Rotation | process | behavioral | vector+keyword | 100% | 0.822 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword | 95% | 0.797 |  |
| 0 | Code Review Process | process | behavioral | vector+keyword | 100% | 0.768 |  |
| 0 | GitHub Actions CI/CD Pipeline | process | behavioral | vector+keyword | 95% | 0.767 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Claims Gateway Deployment' and 'Claims Gateway' may be the same entity

---

### Q45: What is the testing strategy for the claims processing pipeline — what types of tests exist (unit, integration, end-to-end), how does a developer run the test suite locally, and are there shared test fixtures or sample EDI 837 files for simulating claim submissions?
**Source:** persona (developer) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 11559ms

**Answer:** ## Testing Strategy for the Claims Processing Pipeline

Based on the available knowledge entities, here is what can be determined about testing:

### What the Context Tells Us

**CI/CD Pipeline Stages (Including Tests)**
The GitHub Actions CI/CD pipeline includes two test-related stages:
- **Stage 1 – Build**: Compiles code and runs **unit tests** [GitHub Actions CI/CD Pipeline]
- **Stage 2 – Test**: Runs **integration tests against test containers** [GitHub Actions CI/CD Pipeline]

These are th...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 1.251 |  |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 1.001 | executed_by from professional-claims-processing |
| 0 | Professional Claims Processing | process | behavioral | vector+keyword+graph | 90% | 1.188 |  |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.750 |  |
| 0 | EDI Transaction Processing | process | behavioral | vector+keyword+graph | 95% | 1.169 |  |
| 0 | EDI 837 Professional | data-model | structural | vector+keyword | 95% | 0.717 |  |
| 0 | Institutional Claims Batch Processing | process | behavioral | vector+keyword+graph | 90% | 1.146 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.707 |  |
| 0 | Institutional Claims Intake Batch | process | behavioral | vector+keyword+graph | 95% | 1.111 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.699 |  |
| 0 | GitHub Actions CI/CD Pipeline | process | behavioral | vector+keyword | 95% | 0.777 |  |
| 0 | OCR Pipeline Processing | process | behavioral | vector+keyword | 85% | 0.737 |  |
| 0 | Pharmacy Claims Integration Scoping | process | behavioral | vector+keyword | 85% | 0.730 |  |
| 0 | Claim Submitted Event | business-event | behavioral | vector+keyword | 90% | 0.723 |  |
| 0 | Claims Appeals Process | process | behavioral | vector+keyword | 90% | 0.713 |  |

---

### Q46: What are the SLA targets for claims processing throughput and end-to-end latency — specifically, what is the expected time from Claims Gateway ingestion to adjudication completion under normal load, and what volume of claims per day or hour does the system need to handle?
**Source:** persona (architect) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 18228ms

**Answer:** ## SLA Targets for Claims Processing Throughput and End-to-End Latency

### Latency / Time-from-Ingestion SLAs

The available information provides **partial** latency targets, broken down by claim type rather than a single end-to-end figure:

- **Professional Claims (EDI 837P):** A **30-second SLA applies at the intake level** through the Claims Gateway. [Professional Claims Processing] The Claims Submission API also confirms this: "The API operates with a 30-second SLA for real-time EDI 837 Pro...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 1.171 |  |
| 0 | CLV-3902 | jargon-business | language | vector+graph | 100% | 0.785 |  |
| 0 | Professional Claims Processing | process | behavioral | vector+keyword+graph | 90% | 0.851 |  |
| 1 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.776 | owned_by from claims-gateway |
| 1 | Claims Submission API | api | structural | vector+keyword+graph | 95% | 1.133 | affects from clv-3902 |
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword+graph | 90% | 0.807 |  |
| 1 | Datadog | software-component | structural | vector+keyword+graph | 100% | 0.929 | monitors_via from claims-gateway-deployment |
| 0 | Q3 2025 Performance Metrics | domain-logic | behavioral | vector+keyword+graph | 90% | 0.794 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.824 |  |
| 1 | March 2024 Claims Gateway Outage | business-event | behavioral | vector+keyword+graph | 90% | 0.747 | addresses from clv-3902 |
| 2 | Claims Submission API v1 | api | structural | vector+keyword+graph | 95% | 0.808 | triggered_by from march-2024-claims-gateway-outage |
| 1 | Batch Size Admission Control | domain-logic | behavioral | vector+keyword+graph | 95% | 0.682 | implements from clv-3902 |
| 1 | Fraud Detection | system | structural | vector+keyword+graph | 90% | 0.758 | enforced_by from q3-2025-performance-metrics |
| 0 | Claims Status History Endpoint | api | structural | vector+keyword | 90% | 0.689 |  |
| 1 | Rules Engine | system | structural | keyword+graph | 90% | 0.681 | enforced_by from q3-2025-performance-metrics |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Claims Gateway' and 'Claims Gateway Deployment' may be the same entity
- [medium] ambiguous_entity: 'Claims Submission API' and 'Claims Submission API v1' may be the same entity

---

### Q47: What is the security and authorization model across the claims pipeline — how are inter-service calls authenticated (e.g., mTLS, service accounts, API keys), how is PHI access controlled within the Rules Engine and Eligibility Service, and what data encryption standards apply at rest and in transit?
**Source:** persona (architect) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 17361ms

**Answer:** ## Security and Authorization Model Across the Claims Pipeline

### Inter-Service Authentication

Inter-service calls are authenticated using **OAuth 2.0 Bearer tokens** via the client credentials grant flow. The IAM Service at `https://auth.clearviewhealth.internal/oauth/token` issues tokens when services provide `client_id`, `client_secret`, `grant_type=client_credentials`, and the appropriate `scope` (e.g., `eligibility.read` for Eligibility API access). [IAM Service]

The IAM Service is used...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | HIPAA Compliance Requirements | domain-logic | behavioral | vector+keyword+graph | 100% | 1.256 |  |
| 1 | Eligibility API v2 | api | structural | vector+keyword+graph | 95% | 1.205 | used_by from iam-service |
| 0 | Point-in-Time Eligibility Rules | domain-logic | behavioral | vector+keyword | 90% | 0.823 |  |
| 0 | IAM Service | software-component | structural | vector+keyword+graph | 90% | 1.203 |  |
| 0 | Pre-Authorization Requirements | domain-logic | behavioral | vector+keyword | 90% | 0.812 |  |
| 0 | Authorization | data-model | structural | vector+keyword+graph | 100% | 1.191 |  |
| 0 | Authorization Validity Rules | domain-logic | behavioral | vector+keyword | 90% | 0.787 |  |
| 0 | Claim | data-model | structural | vector+keyword+graph | 100% | 1.181 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword | 95% | 0.751 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.117 |  |
| 2 | Eligibility Check API | api | structural | vector+keyword+graph | 95% | 1.079 | supersedes from eligibility-api-v2 |
| 2 | Benefit Plan | data-model | structural | vector+keyword+graph | 100% | 0.978 | links_to from member |
| 1 | Eligibility Service | system | structural | vector+keyword+graph | 90% | 0.885 | communicates_with from rules-engine |
| 1 | Cloud SQL PostgreSQL | software-component | structural | vector+keyword+graph | 95% | 0.818 | enforced_by from hipaa-compliance-requirements |
| 1 | Pre-Auth Service | system | structural | vector+graph | 90% | 0.758 | owned_by from authorization |

---

### Q48: How does the system scale to handle peak load periods such as open enrollment or end-of-year claims surges — are Claims Gateway, the Rules Engine, and the Payment Engine horizontally scalable, and what infrastructure or orchestration layer manages that scaling?
**Source:** persona (architect) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 19196ms

**Answer:** ## Scaling for Peak Load Periods: Claims Gateway, Rules Engine, and Payment Engine

### What We Know About Scaling Infrastructure

**Kubernetes as the Orchestration Layer**
All core claims processing services — Claims Gateway, Rules Engine, Payment Engine, Fraud Detection, and Pre-Auth Service — are hosted in the **claims-ops Kubernetes namespace** [Claims-Ops Namespace]. This confirms that Kubernetes is the underlying orchestration platform for these systems.

**Horizontal Pod Autoscaling (HPA)...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Open Enrollment Scaling Process | process | behavioral | vector+keyword+graph | 95% | 1.271 |  |
| 0 | Claims Operations ⚠️ | team | organizational | vector+keyword | 90% | 0.758 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 0.952 |  |
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword+graph | 90% | 1.062 |  |
| 0 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.926 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword | 95% | 0.806 |  |
| 0 | Claims-Ops Namespace | platform | structural | vector+graph | 90% | 0.720 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword | 95% | 0.739 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.654 |  |
| 0 | Fraud Detection Pre-Payment Integration | process | behavioral | vector+keyword | 95% | 0.702 |  |
| 0 | Payment Engine | system | structural | vector+keyword | 90% | 0.644 |  |
| 0 | March 2024 Claims Gateway Outage | business-event | behavioral | vector+keyword | 90% | 0.699 |  |
| 0 | Claims Gateway Incident Response | process | behavioral | vector+keyword | 90% | 0.670 |  |
| 0 | Claim Routing Process | process | behavioral | vector+keyword | 95% | 0.654 |  |
| 0 | Payment Threshold Rules | domain-logic | behavioral | vector+keyword | 95% | 0.624 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Claims Gateway Deployment' and 'Claims Gateway' may be the same entity

---

### Q49: What is the disaster recovery plan for the claims processing pipeline — what are the RPO and RTO targets for critical systems like the Rules Engine and Eligibility Service, where are backups stored, and has a DR failover been tested end-to-end?
**Source:** persona (architect) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 10378ms

**Answer:** ## Disaster Recovery Plan for the Claims Processing Pipeline

Based on the available knowledge entities, I can only partially address your question. Here is what the context does and does not cover:

### RPO and RTO Targets

The provided entities contain **no information about Recovery Point Objectives (RPO) or Recovery Time Objectives (RTO)** for any system, including the Rules Engine or Eligibility Service. These targets are not mentioned in any of the available entities.

### Backup Storage

...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword+graph | 95% | 1.236 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.131 |  |
| 1 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.806 | owned_by from rules-engine |
| 1 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 1.150 | part_of from ocr-pipeline-processing |
| 0 | OCR Pipeline | system | structural | vector+keyword+graph | 95% | 1.065 |  |
| 0 | Parallel Testing Accuracy Targets | domain-logic | behavioral | vector+keyword+graph | 95% | 1.117 |  |
| 1 | Drools-Based Rules Engine | system | structural | vector+keyword+graph | 90% | 0.988 | enforced_by from parallel-testing-accuracy-targets |
| 0 | OCR Pipeline Processing | process | behavioral | vector+keyword+graph | 85% | 1.097 |  |
| 2 | HealthLogic Adjudicator | system | structural | vector+keyword+graph | 95% | 0.968 | supersedes from drools-rules-engine |
| 0 | Point-in-Time Eligibility Rules | domain-logic | behavioral | vector+keyword | 90% | 0.827 |  |
| 1 | Eligibility Service | system | structural | keyword+graph | 90% | 0.765 | communicates_with from rules-engine |
| 0 | Rules Engine Deployment | process | behavioral | vector+keyword | 90% | 0.761 |  |
| 0 | GKE Production Cluster (prod-claims-01) | platform | structural | vector+keyword | 95% | 0.720 |  |
| 0 | OCR Confidence Scoring Rules | domain-logic | behavioral | vector+keyword | 95% | 0.742 |  |
| 0 | Splunk | software-component | structural | vector+keyword | 100% | 0.718 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Rules Engine' and 'Drools-Based Rules Engine' may be the same entity
- [medium] ambiguous_entity: 'Rules Engine' and 'Rules Engine Deployment' may be the same entity
- [medium] ambiguous_entity: 'OCR Pipeline' and 'OCR Pipeline Processing' may be the same entity

---

### Q50: Beyond the Rules Engine vendor migration, what are the documented technical debt items and known architectural risks in the claims pipeline — for example, are there known scalability bottlenecks in Claims Gateway, data consistency risks between Eligibility Service and the Rules Engine's accumulator checks, or integration fragility points with the Provider Directory?
**Source:** persona (architect) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 27610ms

**Answer:** ## Technical Debt and Architectural Risks in the Claims Pipeline

Based on the available documentation, here is a structured summary of known technical debt items and architectural risks. Note that the context does **not** cover all the specific areas you asked about, so I'll be explicit about what is and isn't documented.

---

### 1. Rules Engine: Vendor Dependency & External Infrastructure Risk

The most clearly documented architectural risk is the **external dependency on HealthLogic's infra...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword+graph | 95% | 1.210 |  |
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.015 |  |
| 0 | Rules Engine Connectivity Incident (August 15) | business-event | behavioral | vector+keyword+graph | 90% | 1.176 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword+graph | 95% | 0.924 |  |
| 0 | OCR Confidence Scoring Rules | domain-logic | behavioral | vector+keyword+graph | 95% | 1.075 |  |
| 1 | Manual Data Entry Process | process | behavioral | keyword+graph | 95% | 0.891 | triggers from ocr-confidence-scoring-rules |
| 0 | Point-in-Time Eligibility Rules | domain-logic | behavioral | vector+keyword | 90% | 0.826 |  |
| 0 | Rules Engine Deployment | process | behavioral | vector+keyword | 90% | 0.730 |  |
| 0 | Fraud Detection Pre-Payment Integration | process | behavioral | vector+keyword | 95% | 0.705 |  |
| 0 | GitHub Actions CI/CD Pipeline | process | behavioral | vector+keyword | 95% | 0.701 |  |
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword | 90% | 0.693 |  |
| 0 | Pharmacy Claims Integration Scoping | process | behavioral | vector+keyword | 85% | 0.688 |  |
| 0 | Data Replication Rules ⚠️ | domain-logic | behavioral | vector+keyword | 90% | 0.680 |  |
| 0 | Eligibility Service Timeout Cascade | business-event | behavioral | vector+keyword | 85% | 0.675 |  |
| 0 | Adjudication Disposition Rules | domain-logic | behavioral | vector+keyword | 90% | 0.672 |  |

**Gaps:**
- [low] orphan_entity: Data Replication Rules has no typed relationships
- [medium] ambiguous_entity: 'Rules Engine' and 'Rules Engine Deployment' may be the same entity

---

### Q51: What are the key business capabilities delivered by each major system in the claims pipeline — specifically, what measurable value does the Pre-Auth Service, Fraud Detection, and Member Portal each deliver to their respective users (providers, members, and internal staff)?
**Source:** persona (product-owner) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 24372ms

**Answer:** ## Business Capabilities Delivered by Each Major System in the Claims Pipeline

### Pre-Auth Service — Value to Providers

The Pre-Auth Service manages prior authorization requests submitted by providers, delivering two primary capabilities:

1. **Automated approvals**: The system auto-approves routine authorization requests, targeting a **60% automation rate**, which reduces administrative burden on providers waiting for authorization decisions [Pre-Auth Service].
2. **Clinical routing for comp...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Member Portal Redesign | process | behavioral | vector+keyword+graph | 95% | 1.243 |  |
| 0 | Member Portal | system | structural | vector+keyword+graph | 90% | 0.986 |  |
| 0 | Member Services ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.753 |  |
| 0 | Fraud Detection Pre-Payment Integration | process | behavioral | vector+keyword | 95% | 0.867 |  |
| 0 | Fraud Detection | system | structural | vector+keyword+graph | 90% | 0.972 |  |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+keyword | 90% | 0.818 |  |
| 0 | Pre-Auth Service | system | structural | vector+keyword+graph | 90% | 0.964 |  |
| 0 | Post-Payment Fraud Analysis | process | behavioral | vector+keyword | 90% | 0.742 |  |
| 0 | Provider Self-Service Portal | system | structural | vector+keyword | 90% | 0.697 |  |
| 0 | Claims Appeals Process | process | behavioral | vector+keyword | 90% | 0.710 |  |
| 0 | Duplicate Detection Logic | domain-logic | behavioral | vector+keyword | 90% | 0.687 |  |
| 0 | Duplicate Detection Process | process | behavioral | vector+keyword | 90% | 0.658 |  |
| 0 | Pre-Authorization Requirements | domain-logic | behavioral | vector+keyword | 90% | 0.657 |  |
| 0 | Claim Routing Process | process | behavioral | vector+keyword | 95% | 0.651 |  |
| 0 | Member Reimbursement Process | process | behavioral | vector+keyword | 85% | 0.649 |  |

**Gaps:**
- [low] orphan_entity: Member Services has no typed relationships
- [medium] ambiguous_entity: 'Member Portal Redesign' and 'Member Portal' may be the same entity

---

### Q52: What are the primary user personas interacting with the claims domain — including providers submitting claims, members checking status, and internal roles like clinical reviewers and SIU investigators — and what are the core workflows each persona performs on a typical day?
**Source:** persona (product-owner) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 33795ms

**Answer:** ## Primary User Personas in the Claims Domain

### 1. Provider Office Manager

**Who they are:** The primary administrative user at healthcare provider offices who handles business operations and interactions with the health plan on behalf of providers. [Provider Office Manager]

**Core daily workflows:**
- Managing provider demographic information and updating practice details [Provider Office Manager]
- Uploading and managing credentialing documents [Provider Office Manager]
- Monitoring netwo...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Clinical Reviewer | persona | organizational | vector+keyword+graph | 90% | 0.875 |  |
| 0 | Claims Status Masking Workflow | process | behavioral | vector+keyword+graph | 90% | 0.823 |  |
| 0 | Claim | data-model | structural | vector+keyword+graph | 100% | 0.777 |  |
| 1 | EOB | jargon-business | language | keyword+graph | 90% | 0.528 | produces from claims-processing-workflow |
| 0 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.696 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 0.795 |  |
| 1 | Member Portal | system | structural | vector+keyword+graph | 90% | 0.692 | executed_by from claims-status-masking-workflow |
| 0 | Provider Office Manager | persona | organizational | vector+keyword | 95% | 0.590 |  |
| 0 | Claims Appeals Process | process | behavioral | vector+keyword | 90% | 0.581 |  |
| 1 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.628 | persisted_by from claim |
| 0 | Credentialing Specialist | persona | organizational | vector+keyword | 90% | 0.510 |  |
| 0 | Claims Operations On-Call Rotation | process | behavioral | vector+keyword | 100% | 0.560 |  |
| 2 | Pre-Auth Service | system | structural | vector+keyword+graph | 90% | 0.623 | owned_by from authorization |
| 0 | Clinical Reviewer Interface Project | process | behavioral | vector+keyword | 80% | 0.532 |  |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.530 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q53: What regulatory and compliance requirements govern the claims processing pipeline — for example, are there federally mandated timelines for claim adjudication, ACA-specific rules affecting coverage decisions, or HIPAA obligations that constrain how claims data flows between Claims Gateway, the Rules Engine, and the Eligibility Service?
**Source:** persona (product-owner) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 21229ms

**Answer:** ## Regulatory and Compliance Requirements Governing the Claims Processing Pipeline

### HIPAA Obligations

The most explicitly documented regulatory framework is HIPAA. The following requirements apply to all systems handling Protected Health Information (PHI), which would include Claims Gateway, the Rules Engine, and the Eligibility Service:

- **No PHI in plaintext logs** [HIPAA Compliance Requirements]
- **All data at rest must be encrypted** (Cloud SQL, GCS) [HIPAA Compliance Requirements]
-...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword+graph | 95% | 1.262 |  |
| 0 | Claim | data-model | structural | vector+keyword+graph | 100% | 1.046 |  |
| 0 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 0.773 |  |
| 0 | Claim Routing Process | process | behavioral | vector+keyword+graph | 95% | 1.248 |  |
| 0 | Claims Gateway | system | structural | vector+keyword+graph | 90% | 0.848 |  |
| 0 | HIPAA Compliance Requirements | domain-logic | behavioral | vector+keyword | 100% | 0.790 |  |
| 0 | OCR Pipeline | system | structural | vector+keyword | 95% | 0.656 |  |
| 0 | Claims Archive Process | process | behavioral | vector+keyword | 90% | 0.778 |  |
| 0 | Point-in-Time Eligibility Rules | domain-logic | behavioral | vector+keyword | 90% | 0.772 |  |
| 0 | Adjudication Disposition Rules | domain-logic | behavioral | vector+keyword | 90% | 0.741 |  |
| 0 | Claims Gateway Deployment | process | behavioral | vector+keyword | 90% | 0.732 |  |
| 0 | OCR Confidence Scoring Rules | domain-logic | behavioral | vector+keyword | 95% | 0.715 |  |
| 0 | OCR Pipeline Processing | process | behavioral | vector+keyword | 85% | 0.660 |  |
| 0 | Pre-Authorization Requirements | domain-logic | behavioral | vector+keyword | 90% | 0.657 |  |
| 0 | Eligibility Service Monitoring | process | behavioral | vector+keyword | 90% | 0.649 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships
- [medium] ambiguous_entity: 'Claims Gateway' and 'Claims Gateway Deployment' may be the same entity

---

### Q54: What are the key metrics used to measure the health and success of the claims processing pipeline — beyond the auto-adjudication rate target of 85%, what KPIs does the Product Owner track across Claims Operations, Member Services, and Provider Network, and how are they reported?
**Source:** persona (product-owner) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 21365ms

**Answer:** ## Key Metrics for Claims Processing Pipeline Health

### Auto-Adjudication Rate (Primary KPI)
The primary metric is the **85% auto-adjudication rate target**, with a SEV-2 alert triggered when the rolling 24-hour rate drops below 75% [Auto-Adjudication Rate Targets]. Current performance is running at **81.3%**, below the 85% target, largely due to incomplete rules migration from HealthLogic [Q3 2025 Performance Metrics].

---

### Additional KPIs Tracked in the Quarterly Operations Review

The ...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Auto-Adjudication Rate Targets | domain-logic | behavioral | vector+keyword+graph | 100% | 1.284 |  |
| 0 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 1.173 |  |
| 0 | Datadog | software-component | structural | vector+keyword+graph | 100% | 1.026 |  |
| 0 | Q3 2025 Performance Metrics | domain-logic | behavioral | vector+keyword+graph | 90% | 1.229 |  |
| 0 | OCR Pipeline Processing | process | behavioral | vector+keyword+graph | 85% | 1.081 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword | 95% | 0.851 |  |
| 0 | Quarterly Operations Review | process | behavioral | vector+keyword | 95% | 0.851 |  |
| 0 | Professional Claims Processing | process | behavioral | vector+keyword | 90% | 0.751 |  |
| 0 | Claims Operations On-Call Rotation | process | behavioral | vector+keyword | 100% | 0.741 |  |
| 0 | Eligibility Service Monitoring | process | behavioral | vector+keyword | 90% | 0.734 |  |
| 0 | Auto-Approval Rate Investigation Process | process | behavioral | vector+keyword | 90% | 0.692 |  |
| 0 | Pharmacy Claims Integration Scoping | process | behavioral | vector+keyword | 85% | 0.687 |  |
| 0 | Post-Payment Fraud Analysis | process | behavioral | vector+keyword | 90% | 0.685 |  |
| 0 | Payment Cycle Processing | process | behavioral | vector+keyword | 90% | 0.676 |  |
| 0 | Member Reimbursement Process | process | behavioral | vector+keyword | 85% | 0.660 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q55: What are the most frequently reported pain points or recurring issues raised by providers, members, or internal teams — for example, are there known patterns of incorrect denials, provider directory data mismatches causing claim failures, or member portal usability issues that regularly generate support tickets?
**Source:** persona (product-owner) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 18328ms

**Answer:** ## Frequently Reported Pain Points and Recurring Issues

Based on the available domain knowledge, here are the documented pain points and recurring issues:

---

### 1. OCR Processing Failures Due to Non-Standard Claim Forms

A known, recurring issue involves **Valley Orthopedic Associates**, which uses modified CMS-1500 forms with non-standard field positions. These don't align with the OCR pipeline's extraction templates, consistently producing low confidence scores. As a result, **all** of th...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Member Portal | system | structural | vector+keyword+graph | 90% | 1.166 |  |
| 0 | Provider Portal Design | process | behavioral | vector+keyword+graph | 80% | 0.734 |  |
| 0 | Valley Orthopedic Associates | external-party | organizational | vector+keyword+graph | 95% | 0.732 |  |
| 0 | Provider Self-Service Portal | system | structural | vector+keyword+graph | 90% | 1.159 |  |
| 0 | Member Portal Redesign | process | behavioral | vector+keyword | 95% | 0.580 |  |
| 1 | Provider Directory | system | structural | vector+keyword+graph | 80% | 0.979 | communicates_with from provider-portal |
| 0 | Datadog | software-component | structural | vector+graph | 100% | 0.894 |  |
| 2 | Manual Data Entry Tool | software-component | structural | keyword+graph | 90% | 0.737 | executed_by from manual-data-entry-process |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.736 |  |
| 0 | Elasticsearch | software-component | structural | vector+keyword | 95% | 0.685 |  |
| 1 | PagerDuty | software-component | structural | vector+graph | 95% | 0.674 | communicates_with from datadog |
| 1 | Pre-Auth Service | system | structural | vector+graph | 90% | 0.631 | communicates_with from provider-portal |
| 2 | Eligibility Service | system | structural | keyword+graph | 90% | 0.625 | communicates_with from rules-engine |
| 1 | Payment Engine | system | structural | vector+graph | 90% | 0.624 | communicates_with from provider-portal |
| 0 | Payment | data-model | structural | vector+keyword | 100% | 0.579 |  |

---

### Q56: How do I get access to Confluence, the code repositories, and other internal tools on my first day — who provisions access and is there a checklist or ticket I should follow?
**Source:** persona (new-joiner) | **Score:** ❌ MISSING | **Entities:** 15 | **Time:** 9710ms

**Answer:** ## Access Provisioning for New Employees

Based on the available knowledge entities, I can provide only limited information relevant to your question:

### GitHub / Code Repository Access

Access to the **clearview-health GitHub organization** is required before any development or deployment activities can begin. [GitHub] specifically notes that "access to the clearview-health org is a prerequisite for any deployment activities," and it houses repositories for all claims platform services. [GitH...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Code Review Process | process | behavioral | vector+keyword+graph | 100% | 1.150 |  |
| 0 | GitHub | software-component | structural | vector+keyword+graph | 90% | 0.918 |  |
| 0 | Clearview Provider Relations Rep | persona | organizational | vector+keyword | 90% | 0.510 |  |
| 0 | Open Enrollment Preparation | process | behavioral | vector+graph | 90% | 0.805 |  |
| 0 | Clearview-Infra Repository | software-component | structural | vector+graph | 85% | 0.643 |  |
| 0 | Provider Portal Design | process | behavioral | vector+graph | 80% | 0.745 |  |
| 0 | IAM Service | software-component | structural | vector+keyword | 90% | 0.486 |  |
| 0 | On-Call Handoff Process | process | behavioral | vector+keyword | 90% | 0.702 |  |
| 0 | New Member Enrollment | process | behavioral | vector+keyword | 80% | 0.699 |  |
| 0 | Claims Operations On-Call Rotation | process | behavioral | vector+keyword | 100% | 0.626 |  |
| 0 | Clinical Reviewer Interface Project | process | behavioral | vector+keyword | 80% | 0.623 |  |
| 0 | Credentialing Document Workflow | process | behavioral | vector+keyword | 90% | 0.523 |  |
| 0 | Claims Appeals Process | process | behavioral | keyword | 90% | 0.514 |  |
| 0 | Member Enrollment Workflow | process | behavioral | vector+keyword | 90% | 0.508 |  |
| 0 | COB Auto-Detection Project | process | behavioral | vector+keyword | 90% | 0.467 |  |

**Gaps:**
- [high] thin_coverage: Found 15 related entities but content is insufficient

---

### Q57: Who should a new joiner in Claims Engineering go to when they are stuck on a technical problem — is there a buddy system, a team lead, a Slack channel, or an on-call rotation they can reach out to?
**Source:** persona (new-joiner) | **Score:** ⚠️ INCOMPLETE | **Entities:** 15 | **Time:** 13961ms

**Answer:** ## Who a New Joiner in Claims Engineering Should Reach Out to for Technical Help

Based on the available information, here are the key people and channels a new joiner could turn to, though note that the entities describe **Claims Operations** specifically (which appears to be the closest match to "Claims Engineering"):

### Team Lead
**Marcus Reeves** is the team lead for Claims Operations [Marcus Reeves (persona, confidence: 95%)]. He is hands-on with system documentation and architecture, mak...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Marcus Reeves | persona | organizational | vector+keyword+graph | 95% | 1.052 |  |
| 0 | Claims Operations On-Call Rotation | process | behavioral | vector+keyword+graph | 100% | 0.885 |  |
| 0 | PagerDuty | software-component | structural | vector+graph | 95% | 0.583 |  |
| 0 | Claims Adjudicator Queue | jargon-business | language | vector+keyword | 90% | 0.554 |  |
| 0 | Claims Operations ⚠️ | team | organizational | vector+keyword+graph | 90% | 1.027 |  |
| 0 | On-Call Handoff Process | process | behavioral | vector+keyword+graph | 90% | 0.842 |  |
| 0 | Claims Platform Team (2021) | team | organizational | vector+keyword | 95% | 0.768 |  |
| 0 | Claims Appeals Process | process | behavioral | vector+keyword | 90% | 0.544 |  |
| 0 | Tom Nguyen | persona | organizational | vector+keyword | 90% | 0.722 |  |
| 0 | Claims Gateway Incident Response | process | behavioral | vector+keyword | 90% | 0.463 |  |
| 0 | Kenji Watanabe | persona | organizational | vector+keyword | 95% | 0.715 |  |
| 0 | Priya Anand | persona | organizational | vector+keyword | 95% | 0.691 |  |
| 0 | Rachel Dominguez | persona | organizational | vector+keyword | 95% | 0.550 |  |
| 0 | Clinical Reviewer | persona | organizational | vector+keyword | 90% | 0.537 |  |
| 0 | Leo Chen | persona | organizational | vector+keyword | 90% | 0.492 |  |

**Gaps:**
- [low] orphan_entity: Claims Operations has no typed relationships

---

### Q58: What does the Provider Directory contain, who on the Provider Network team is responsible for it day-to-day, and who specifically should be contacted about credentialing workflows (the doc mentions asking James — who is James and what is his role)?
**Source:** persona (new-joiner) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 13296ms

**Answer:** ## Answer

### What the Provider Directory Contains

The Provider Directory is the master data system for all contracted healthcare providers. It contains:

- **Provider demographics** and organizational name [Provider Directory]
- **Credentials** (MD, DO, NP, PA) and licensing information with expiration tracking [Provider]
- **Specialty taxonomy codes** [Provider]
- **Network participation status** (IN_NETWORK/OUT_OF_NETWORK/PENDING), tracked per plan with effective dates [Provider]
- **Fee sc...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | James Whitfield | persona | organizational | vector+keyword+graph | 95% | 1.278 |  |
| 0 | Provider Directory | system | structural | vector+keyword+graph | 80% | 1.057 |  |
| 0 | Credentialing Document Workflow | process | behavioral | vector+keyword+graph | 90% | 0.783 |  |
| 0 | Provider Network ⚠️ | team | organizational | vector+keyword+graph | 90% | 1.187 |  |
| 0 | Provider | data-model | structural | vector+keyword+graph | 100% | 1.023 |  |
| 0 | Credentialing Status Propagation | process | behavioral | vector+keyword | 90% | 0.601 |  |
| 0 | Credentialing Specialist | persona | organizational | vector+keyword | 90% | 0.793 |  |
| 1 | Provider Self-Service Portal | system | structural | vector+keyword+graph | 90% | 1.013 | executed_by from credentialing-document-workflow |
| 0 | Provider Re-credentialing Process | process | behavioral | vector+keyword | 85% | 0.572 |  |
| 0 | Provider Office Manager | persona | organizational | vector+keyword | 95% | 0.773 |  |
| 0 | Provider-Net Namespace | platform | structural | vector+keyword | 90% | 0.602 |  |
| 0 | Clearview Provider Relations Rep | persona | organizational | vector+keyword | 90% | 0.757 |  |
| 0 | Unnamed Provider Group | external-party | organizational | vector+keyword | 80% | 0.651 |  |
| 0 | Dana Okafor | persona | organizational | vector+keyword | 95% | 0.612 |  |
| 0 | Claims Platform Team (2021) | team | organizational | vector+keyword | 95% | 0.571 |  |

**Gaps:**
- [low] orphan_entity: Provider Network has no typed relationships

---

### Q59: What is the 'allowed amount' for a service, where does it come from in the claims pipeline, and how does it differ from the billed amount a provider submits?
**Source:** persona (new-joiner) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 16657ms

**Answer:** ## What Is the Allowed Amount, Where Does It Come From, and How Does It Differ from the Billed Amount?

### Definition of the Allowed Amount

The **allowed amount** is the maximum reimbursement amount that the health plan will pay for a covered service. It represents the ceiling for payment established for specific healthcare services, typically based on negotiated contracts with in-network providers or established fee schedules. [Allowed amount]

Critically, it is also the basis for member cost...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Allowed Amount Calculation | domain-logic | behavioral | vector+keyword+graph | 95% | 1.241 |  |
| 0 | Fee Schedule | data-model | structural | vector+keyword+graph | 100% | 1.033 |  |
| 0 | Allowed amount | jargon-business | language | vector+keyword+graph | 90% | 1.041 |  |
| 0 | Cost-Sharing Calculation Rules | domain-logic | behavioral | vector+keyword+graph | 95% | 1.138 |  |
| 0 | Claim | data-model | structural | vector+keyword | 100% | 0.710 |  |
| 0 | CLV-3902 | jargon-business | language | vector+graph | 100% | 0.738 |  |
| 0 | Payment Threshold Rules | domain-logic | behavioral | vector+keyword | 95% | 0.683 |  |
| 0 | Claims Submission API | api | structural | vector+keyword | 95% | 0.682 |  |
| 0 | Fee-for-Service | jargon-business | language | vector+keyword | 90% | 0.610 |  |
| 0 | Batch Size Admission Control | domain-logic | behavioral | vector+keyword | 95% | 0.668 |  |
| 0 | Claims Appeals Process | process | behavioral | vector+keyword | 90% | 0.653 |  |
| 0 | Eligibility Service Monitoring | process | behavioral | vector+keyword | 90% | 0.647 |  |
| 0 | Claim Submitted Event | business-event | behavioral | vector+keyword | 90% | 0.632 |  |
| 0 | Claims Processing Workflow | process | behavioral | vector+keyword | 95% | 0.600 |  |
| 0 | Eligibility Date of Service Rule | domain-logic | behavioral | vector+keyword | 95% | 0.586 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Allowed Amount Calculation' and 'Allowed amount' may be the same entity

---

### Q60: What is the Rules Engine migration that is currently underway — what vendor product is being replaced, what is it being replaced with, and what is the current status or timeline for the migration?
**Source:** persona (new-joiner) | **Score:** ✅ CLEAN | **Entities:** 15 | **Time:** 13005ms

**Answer:** ## Rules Engine Migration Overview

### What is Being Replaced

The current system being replaced is the **HealthLogic Adjudicator 4.2**, a vendor product provided by **HealthLogic Systems** that has been in use since 2019. [HealthLogic Adjudicator] It handles approximately 4,200 active rules and costs **$1.2 million annually**, with new rule implementations requiring 8–12 weeks of vendor professional services engagement. [HealthLogic Adjudicator] The system communicates via a SOAP endpoint, whi...

**Retrieval Trace:**
| Hop | Entity | Type | Layer | Found By | Confidence | Score | Via |
|-----|--------|------|-------|----------|------------|-------|-----|
| 0 | Rules Engine | system | structural | vector+keyword+graph | 90% | 1.220 |  |
| 0 | DRL | jargon-tech | language | vector+keyword | 90% | 0.642 |  |
| 0 | Rules Engine Migration Process | process | behavioral | vector+keyword+graph | 95% | 0.915 |  |
| 0 | HealthLogic Systems | external-party | organizational | vector+keyword+graph | 95% | 0.851 |  |
| 0 | HealthLogic Selection Decision | decision | decision | vector+keyword | 95% | 0.534 |  |
| 0 | HealthLogic Adjudicator | system | structural | vector+keyword+graph | 95% | 1.137 |  |
| 0 | HealthLogic SDK | jargon-tech | language | vector+keyword | 100% | 0.614 |  |
| 0 | Rules Engine Deployment | process | behavioral | vector+keyword | 90% | 0.567 |  |
| 0 | Rachel Dominguez | persona | organizational | vector+keyword+graph | 95% | 0.798 |  |
| 1 | Drools-Based Rules Engine | system | structural | vector+keyword+graph | 90% | 1.087 | superseded_by from healthlogic-adjudicator |
| 0 | CLV-4521 | jargon-business | language | vector+keyword | 90% | 0.569 |  |
| 0 | Rules Engine Connectivity Incident (August 15) | business-event | behavioral | vector+keyword | 90% | 0.547 |  |
| 1 | Apex Consulting | external-party | organizational | vector+keyword+graph | 90% | 0.652 | belongs_to from rachel-dominguez |
| 2 | Drools | software-component | structural | vector+keyword+graph | 95% | 1.073 | depends_on from drools-rules-engine |
| 0 | HealthLogic SOAP Endpoint | api | structural | vector+keyword | 100% | 0.654 |  |

**Gaps:**
- [medium] ambiguous_entity: 'Rules Engine' and 'Drools-Based Rules Engine' may be the same entity

---

## Gap Summary

**Total unique gaps:** 30

### ambiguous_entity (21)
- [medium] 'Claim Submitted Event' and 'Claim Submitted Event (Kafka)' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Eligibility Service' and 'Eligibility Service Monitoring' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Eligibility Service' and 'Eligibility Service Deployment' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Rules Engine' and 'Rules Engine Deployment' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Claims Gateway' and 'Claims Gateway Deployment' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Fraud Scoring Thresholds' and 'New Fraud Scoring Thresholds' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Drools-Based Rules Engine' and 'Rules Engine' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Allowed amount' and 'Allowed Amount Calculation' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Claims Submission API v1' and 'Claims Submission API' may be the same entity
  → Disambiguate or merge these entities
- [medium] 'Claims API v2 Validation Logic' and 'Claims API v1 Validation Logic' may be the same entity
  → Disambiguate or merge these entities
- ... and 11 more

### orphan_entity (8)
- [low] Member Services has no typed relationships
  → Add relationships for Member Services
- [low] Provider Network has no typed relationships
  → Add relationships for Provider Network
- [low] Claims Operations has no typed relationships
  → Add relationships for Claims Operations
- [low] COB has no typed relationships
  → Add relationships for COB
- [low] Clearview Health Plans has no typed relationships
  → Add relationships for Clearview Health Plans
- [low] Consumer Groups has no typed relationships
  → Add relationships for Consumer Groups
- [low] Dead Letter Topic (DLT) has no typed relationships
  → Add relationships for Dead Letter Topic (DLT)
- [low] Data Replication Rules has no typed relationships
  → Add relationships for Data Replication Rules

### thin_coverage (1)
- [high] Found 15 related entities but content is insufficient
  → Enrich existing entities with more detail from source documents
