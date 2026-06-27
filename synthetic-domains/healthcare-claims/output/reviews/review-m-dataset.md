# Pipeline Review — M Dataset Cross-Comparison (S, M, Real)

## Run Summary

| Metric | S Dataset | M Dataset | Real Data |
|--------|-----------|-----------|-----------|
| Documents | 8 | 28 | 54 |
| Entities | 139 | 409 | 410 |
| Entities/doc | 17.4 | 14.6 | 7.6 |
| Entity types used | 14/17 | 15/17 | 17/17 |
| Ground truth (of 51) | ~17 found | 40 found (78%) | N/A |

---

## 1. Over-Extraction Comparison

### The Numbers
- S: 17.4 entities/doc
- M: 14.6 entities/doc (16% improvement over S)
- Real: 7.6 entities/doc

### Why M Is Better Than S
M shows genuine improvement. The per-doc rate dropped from 17.4 to 14.6. With 3.5x more documents, the pipeline had more context to merge entities rather than create new ones. The growing knowledge summary helps the LLM recognize when a concept already exists.

### Why Synthetic Is Still 2x Real Data
This is a **data quality issue, not a pipeline issue.** Root causes:

1. **Synthetic docs are denser.** The synthetic healthcare corpus was written to be information-rich for testing purposes. Each document packs more named concepts per paragraph than real-world docs, which contain meeting chatter, action items, tangential discussion, and organizational context that dilutes entity density.

2. **Real docs have more "noise" content.** Real corporate docs include process descriptions, team rituals, ticket workflows, and organizational housekeeping that produce fewer extractable domain entities per page.

3. **Process explosion in M (88 entities).** The M dataset extracted 88 process entities — by far the largest category. Many are operational procedures (deployment steps, CI/CD pipelines, incident response, monitoring processes) rather than domain processes. Real data has 56 processes from 54 docs (1.0/doc) vs M's 88 from 28 docs (3.1/doc). The pipeline treats every described workflow as a process entity.

4. **Software component inflation in M (41 entities).** Every technology mentioned (Zoom, CDN, GitHub, Snyk, Trivy, PagerDuty, LaunchDarkly, Alembic, Poetry, Vite, Flyway, Dependabot) became its own entity. Real data has far fewer because real docs don't enumerate their full tech stack in every document.

### Verdict
The 2x gap is primarily data-driven. The synthetic corpus is more entity-dense by design. However, the pipeline also needs guardrails: process and software-component extraction thresholds would bring synthetic closer to real.

---

## 2. Ground Truth Misses (11 of 51)

### Missing entities from M dataset

| Entity | Type | Also Missing in S? | Root Cause |
|--------|------|--------------------|------------|
| deductible | jargon-business | Yes | **Generic concept bias**: LLM treats "deductible" as common English, not domain jargon worth extracting. It appears in other entities' descriptions but is never the subject of its own paragraph. |
| pre-authorization | jargon-business | Yes | **Extracted as system/process instead**: pre-auth-service (system) and pre-authorization-requirements (domain-logic) exist. The jargon entry itself is skipped because the concept is "covered" by related entities. |
| coordination-of-benefits | jargon-business | Partial (was `cob`) | **ID mismatch**: M has `cob` (jargon-business) which IS this entity. The ground truth expected `coordination-of-benefits` as the ID. This is a ground truth naming issue, not a miss. |
| claims-adjudicator | persona | Yes | **Named-individual bias**: Pipeline extracts 20 named personas (Marcus Reeves, Priya Anand, etc.) but zero role-based personas. The prompt does not distinguish between "person mentioned in a doc" and "role that exists in the organization." |
| special-investigations-unit | team | Partial (was `siu` jargon) | **Type mismatch**: M has `siu` as jargon-business. The ground truth expects a team entity. SIU is described as a unit but the pipeline classifies it as jargon/abbreviation. |
| claims-processing | capability | Yes | **Capability blind spot**: Zero capability entities in M (or S). The concept is captured as `claims-processing-workflow` (process). The LLM consistently classifies capabilities as processes. |
| enrollment | process | No (new miss) | **Stub document**: enrollment-workflow.txt is likely a stub. The pipeline extracted enrollment-related entities from other docs but not the process itself as named. |
| credentialing | process | No (S had it) | **ID mismatch**: M has `recredentialing-process` and `credentialing-document-workflow`. The ground truth expected a single `credentialing` process entity. |
| edi-837 | jargon-tech | Yes (partial) | **Split into subtypes**: M has `edi-837-professional` and `edi-837-institutional` as data-models, but no unified `edi-837` jargon-tech entry. |
| era-835 | jargon-business | Partial | **Type reclassification**: M has `era-835` as a data-model, not jargon-business. Correct concept, wrong type vs ground truth. |
| nacha | jargon-tech | N/A | **Reclassified**: M has `nacha-format` as a data-model. Concept captured, type differs from ground truth expectation. |

### Systemic Patterns (repeat across S and M)

**Pattern 1 — Generic Concept Blindness (deductible, pre-authorization):** The LLM's world knowledge makes it treat domain terms as "obvious" rather than extractable. It understands what a deductible is, so it doesn't flag it as domain jargon a newcomer would need defined.

**Root cause:** The prompt says to extract "terms a newcomer to the domain would need defined." The LLM interprets this as "obscure terms" not "foundational terms." Fix: add explicit instruction — "Extract ALL domain-specific terms including foundational concepts like deductible, copay, premium, authorization. A newcomer from a different industry would need these defined even if they seem common."

**Pattern 2 — Named Individuals Instead of Roles (claims-adjudicator):** Both S and M extract people by name (20 in M, 7 in S) but zero role-based personas.

**Root cause:** Meeting notes and docs mention people by name. The prompt says "persona" but doesn't distinguish role vs individual. Fix: add to prompt — "Personas should represent organizational ROLES (e.g., Claims Adjudicator, Clinical Reviewer, Provider Office Manager), not named individuals. Named individuals should be tagged as people associated with a role, not as separate persona entities."

**Pattern 3 — Capability Type Never Used:** Zero capability entities across S, M, or the architecture-overview doc that explicitly describes capabilities.

**Root cause:** The meta-model defines capabilities, but the prompt doesn't give clear guidance on when to use capability vs process. The LLM defaults to process for everything action-oriented. Fix: add disambiguation — "Capabilities describe WHAT the organization can do (nouns: 'Claims Processing', 'Fraud Detection'). Processes describe HOW it's done (verbs: 'the claims processing workflow', 'the fraud scoring pipeline')."

---

## 3. S Entities Lost in M (77 entities)

### Three categories of "loss"

**Category 1 — ID Instability (~30 entities):** Same concept, different ID between runs. This is the biggest category.

| S Entity ID | M Entity ID | Same Concept? |
|-------------|-------------|---------------|
| cost-sharing-calculation | cost-sharing-calculation-rules | Yes |
| fraud-circuit-breaker | fraud-circuit-breaker-logic | Yes |
| auth-required-service-list | auth-required-service-lists | Yes (singular vs plural) |
| duplicate-detection-rule | duplicate-detection-logic | Yes |
| soft-reservation-rule | soft-reservation-logic | Yes |
| fraud-scoring-tiers | new-fraud-scoring-thresholds | Partially |
| recoupment-spreading-rule/logic | recoupment-distribution-rules | Yes |
| date-of-service-eligibility-rule | eligibility-date-of-service-rule | Yes (word order) |
| network-status-date-rule | provider-network-date-of-service-rule | Yes |
| era (jargon) | era-835 (data-model) | Yes, reclassified |
| iro (jargon) | independent-review-organization (jargon) | Yes |
| xgboost-fraud-model (domain-logic) | xgboost-fraud-model (data-model) | Yes, reclassified |
| rules-engine-replacement (decision) | adr-2024-007 (decision) | Yes |
| connection-pool-exhaustion-incident (decision) | hikaricp-pool-exhaustion-event (business-event) | Yes, reclassified |
| adr-2024-007 (jargon-tech) | adr-2024-007 (decision) | Yes, correct in M |

**Root cause:** The LLM generates IDs non-deterministically. `-rule` vs `-logic` vs `-rules`, singular vs plural, word order flips. The pipeline's merge-by-ID approach cannot detect these as duplicates.

**Fix (high confidence):** Implement fuzzy ID matching during merge. When a new entity arrives, compare its ID against existing entities using: (a) Levenshtein distance < 3, (b) same entity type, (c) similar description embedding. If match found, merge instead of creating new.

**Category 2 — Granularity Absorbed (~25 entities):** S extracted fine-grained entities that M's additional documents caused to be merged or superseded.

Examples:
- S had `claims-processing-pipeline` (process) — M has `claims-processing-workflow` with richer content from more docs
- S had `payment-reconciliation` and `payment-reconciliation-design` — M consolidated into `payment-reconciliation-rework`
- S had `batch-auth-import`, `auth-request-force-reprocessing` — M has fewer pre-auth sub-processes

This is actually **desirable behavior.** More documents provide context to consolidate.

**Category 3 — Genuinely Lost (~22 entities):** Concepts that existed in S docs but weren't re-extracted in M despite the same docs being processed.

Examples:
- `reservation-cleanup-job` (system) — specific system mentioned in S but not re-extracted
- `provider-profile-database`, `pre-auth-postgresql` (software-component) — database instances
- `sidecar-pattern`, `p99-latency`, `hikaricp`, `pgbouncer` (jargon-tech) — tech jargon from S
- `eligibility-websocket-feed`, `provider-directory-sync` (business-event) — events from S
- `unbundling` (jargon-business) — fraud term

**Root cause:** As the knowledge summary grows, the LLM becomes more selective. With 28 docs of context, it deprioritizes what it now sees as minor details. The growing summary acts as a "this is already known" signal that suppresses re-extraction of peripheral entities.

**Fix (hypothesis to test):** This is partially a feature (less noise) and partially a bug (losing valid entities). Monitor: if a concept appears in a source doc but isn't extracted, the pipeline should flag it as "mentioned but not extracted" for human review.

---

## 4. Quality Comparison Across Datasets

### M Entity Quality (3 samples)

**claims-gateway (system) — GOOD:**
- Clear description, correct relationships, confidence 0.9
- Mentions all intake channels (EDI 837, JSON, OCR)
- Thin on details (27 lines total) given it appears in 13 documents

**code-review-process (process) — MARGINAL:**
- Well-written but questionable entity type. A code review process is engineering practice, not domain knowledge.
- Confidence 1.0 is over-calibrated for a generic dev process
- Should not be a separate entity — this is infrastructure, not domain

**inc-2022-0094 (jargon-business) — BAD ENTITY TYPE:**
- An incident ticket number classified as "jargon-business" — this is wrong
- Should be a business-event or not extracted at all
- Well-written content but fundamentally misclassified

### Real Data Entity Quality (3 samples)

**billing-engine (system) — GOOD:**
- Rich description covering responsibilities, tech stack, team ownership
- Proper relationships (communicates_with, handles, deployed_on)
- Confidence 0.95 appropriate for seed-context-derived entity

**billing-proposal-process (process) — GOOD:**
- Clear step-by-step process description
- Proper relationship chain (owned_by, executed_by, involves, produces)
- Domain-specific and valuable

**jargon-bp (jargon-business) — GOOD:**
- Concise, correct, includes lifecycle states
- Cross-references related jargon (synonymous_with)

### Quality Comparison Summary

| Dimension | M (Synthetic) | Real Data |
|-----------|---------------|-----------|
| Entity descriptions | Good quality | Good quality |
| Relationship richness | 2-3 per entity | 4-6 per entity |
| Confidence calibration | Over-confident (many 1.0) | Better calibrated (0.85-0.95) |
| Type accuracy | Misclassifications common | Fewer misclassifications |
| Signal-to-noise | ~60% signal | ~80% signal |
| Content depth | Thinner per entity | Richer per entity |

**Root cause of quality gap:** Real data has been through more human review cycles. The synthetic corpus is processed in one batch with no human curation. Additionally, real data benefits from seed context that was hand-crafted, while synthetic seed context is more generic.

---

## 5. Systemic Patterns Across All Three Datasets

### Pattern A — Process Explosion (ALL datasets)
- S: 24 processes from 8 docs (3.0/doc)
- M: 88 processes from 28 docs (3.1/doc)
- Real: 56 processes from 54 docs (1.0/doc)

Synthetic is 3x worse than real. The pipeline treats every described workflow, procedure, and operational step as a separate process entity. Deployment steps for each service become individual entities. Incident response procedures become entities. Meeting agenda items become entities.

**Root cause:** The prompt says to extract processes but doesn't define a minimum bar. Every verb phrase that describes steps qualifies.

**Fix (high confidence):** Add to prompt: "Only extract processes that are NAMED organizational workflows. 'Deploy the claims gateway' is a step, not a process entity. 'Claims Processing Workflow' is a named process. Deployment procedures, CI/CD steps, and incident response runbooks should be consolidated into a single entity per concern, not split per-service."

### Pattern B — Software Component Inflation (S and M, less in Real)
- S: 14 software-components from 8 docs
- M: 41 software-components from 28 docs
- Real: moderate (fewer commodity tools)

Every technology mentioned gets its own entity: Zoom, GitHub, CDN, Snyk, Trivy, Poetry, Vite, Dependabot, PagerDuty, LaunchDarkly.

**Root cause:** The prompt defines software-components but doesn't distinguish between "technology that is part of the domain architecture" and "commodity tool used by every engineering team."

**Fix (high confidence):** Add to prompt: "Software components should be domain-relevant infrastructure (e.g., the message broker connecting domain systems, the database storing domain data). Do NOT extract commodity development tools (GitHub, Dependabot, linters), generic SaaS (Zoom, PagerDuty, Slack), or build tools (Gradle, Poetry, Vite) unless they play a domain-specific role."

### Pattern C — Named Individuals as Personas (ALL datasets)
- S: 7 named individuals, 0 roles
- M: 20 named individuals, 0 roles (clinical-reviewer exists but is an exception — extracted from the provider portal requirements doc)
- Real: 7 personas, mix of roles and named

Wait — M does have `clinical-reviewer`, `provider-office-manager`, `credentialing-specialist` as personas. So M partially fixed this from S. But it still has 17 named individuals alongside 3 roles.

**Updated assessment:** M improved from S (3 role-based personas appeared), but the ratio is still 17:3 individuals-to-roles. The prompt needs stronger guidance.

### Pattern D — Jargon Type Confusion (ALL datasets)
Incident ticket numbers (INC-2022-0094, CLV-3904, CLV-4521) are classified as jargon-business. Severity levels (SEV-1) are classified as jargon-business. These are identifiers and operational labels, not business terminology.

**Root cause:** The prompt doesn't distinguish between "domain vocabulary" and "identifiers/labels." The LLM sees a capitalized abbreviation and defaults to jargon.

**Fix:** Add to prompt: "Jargon entities are VOCABULARY TERMS that a newcomer needs defined. Ticket numbers (INC-*, CLV-*), severity labels (SEV-1), and identifier formats are NOT jargon. They may be mentioned in other entities but should not be standalone jargon entities."

### Pattern E — Confidence Over-Calibration (M worse than Real)
M has many entities at confidence 1.0, including:
- code-review-process: 1.0 (generic dev practice)
- spring-boot: 1.0 (commodity framework)
- quarkus: 1.0 (commodity framework)

Real data entities cluster around 0.85-0.95, which better reflects uncertainty.

**Root cause:** The coding standards and deployment guide documents are highly structured and explicit, so the LLM assigns maximum confidence. But confidence should reflect domain relevance, not just how clearly the source doc describes something.

**Fix (hypothesis):** Adjust prompt: "Confidence should reflect how important this entity is for domain understanding, not just how clearly it's described in the source document. A well-documented deployment step is still low-confidence as a domain entity."

---

## Recommendations

### Must Fix Before Next Run

1. **Process extraction guardrail** — Add prompt instruction to filter deployment-per-service, CI/CD steps, and generic dev processes. This alone would cut M from 409 to ~320 entities.

2. **Software component guardrail** — Add prompt instruction to exclude commodity tools. Would remove ~20 entities from M.

3. **Jargon type guidance** — Add prompt instruction distinguishing vocabulary from identifiers. Would fix ~10 misclassified entities.

4. **Foundational concept extraction** — Add explicit instruction to extract foundational domain terms (deductible, copay, etc.) even when they seem "obvious."

### Working Well

1. **Core system extraction** — All 8 core systems found across both S and M with correct descriptions and relationships.
2. **Data model extraction** — M successfully extracts claim, member, provider, benefit-plan, payment, fee-schedule, authorization, accumulator (S missed all of these). Major improvement.
3. **Decision extraction** — ADR-2024-007 correctly identified with context about why it was made.
4. **Domain logic extraction** — Rich set of business rules captured with specific thresholds and conditions.
5. **Cross-document merging** — Entities that appear in multiple docs get richer descriptions in M than S.

### Prompt Improvement Ideas

1. **Entity type disambiguation guide** in the prompt: "Use this decision tree: Is it a named workflow? -> process. Is it what the org CAN do? -> capability. Is it a rule with conditions? -> domain-logic."

2. **Dedup hint in prompt:** "Before creating a new entity, check if a similar concept exists in the knowledge summary under a slightly different name. If so, use the existing ID."

3. **Role vs Individual guidance** for personas.

4. **Minimum bar for extraction:** "If an entity would have less than 3 sentences of meaningful content, it probably shouldn't be its own entity."

---

## Overall Impression

M is a meaningful improvement over S: better entity density (14.6 vs 17.4/doc), dramatically better ground truth coverage (78% vs ~61%), and successful data-model extraction that S completely missed. The quality gap to real data (~7.6/doc, better calibrated) is roughly 50% data-driven (synthetic docs are denser) and 50% pipeline-driven (process explosion, software component inflation, jargon misclassification).

The 77 "lost" S entities break down as: ~30 ID instability (same concept, different ID), ~25 desirable consolidation, ~22 genuinely lost. The ID instability is the most actionable problem — fuzzy merge logic would recover most of these.

The systemic issues (process explosion, named-individual bias, confidence over-calibration, missing capabilities) repeat across all three datasets. These are prompt-level fixes that would improve all runs.
