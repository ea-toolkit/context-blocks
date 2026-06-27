---
type: process
id: credentialing-status-propagation
name: Credentialing Status Propagation
description: Process by which provider credentialing approval updates network status across all downstream systems within 2 hours
status: active
triggered_by: [provider-status-changed-event]
updates: [provider-directory, credentialing-status-model]
executed_by: [provider-self-service-portal]
owned_by: provider-network
depends_on: [credentialing-document-workflow, provider-re-credentialing-process]
affects: [claim-routing-process, rules-engine]
confidence: 0.90
source_documents: [provider-credentialing.txt]
---

# Credentialing Status Propagation

## Overview
When a provider's credentialing is approved (initial or re-credentialing), the status must propagate from the Credentialing Document Workflow through to the Provider Directory and all downstream systems that check network status. The target SLA is 2 hours from approval to full propagation.

## Propagation Flow

1. **Credentialing Specialist** completes review in the Credentialing Document Workflow and marks provider as "approved"
2. System emits a **Provider Status Changed Event** with the new status (active/suspended/terminated)
3. **Provider Self-Service Portal** receives the event and updates the Credentialing Status Model
4. **Provider Directory** is updated with the new network status — this is the source of truth for all claims processing
5. **Rules Engine** picks up the updated provider status on next claim adjudication via the Provider Network Date of Service Rule
6. **Claim Routing Process** uses the updated Provider Directory data for network validation

## Known Issue: 24-48 Hour Delay
Currently, steps 3-4 have a batch synchronization process that runs every 24 hours instead of real-time event processing. This means:
- Claims submitted within 24-48 hours of credentialing approval may be incorrectly denied as "out-of-network"
- Provider Network team is aware but fix is deprioritized behind the Rules Engine migration
- Workaround: Claims Operations manually overrides network status for recently credentialed providers when notified

## Affected Systems
- Provider Self-Service Portal (writes credentialing status)
- Provider Directory (reads credentialing status, serves it to downstream)
- Rules Engine (reads provider network status during adjudication)
- Claim Routing Process (validates provider network before routing)
