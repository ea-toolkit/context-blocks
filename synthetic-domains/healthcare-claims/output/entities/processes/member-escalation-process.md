---
type: process
id: member-escalation-process
name: Member Escalation Process
description: |-
  Process for handling member complaints and escalations related to eligibility and accumulator issues
status: active
tags:
- member-service
- escalation
- complaints
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.85
owned_by:
- member-services
triggered_by:
- accumulator-drift-event
involves:
- member-services-call-center-supervisor
---

# Member Escalation Process

## Overview

Process used when members complain about incorrect charges or benefit calculations. Often triggered by accumulator-related issues like double-applied deductibles or drift problems.

## Details

Process activated when members call complaining about charges or benefit calculations that seem incorrect. Common triggers include accumulator drift (where member is charged more than expected due to data inconsistencies) and double-applied deductible scenarios. Investigation involves comparing member accumulator history against actual claim payments to identify discrepancies. Resolution may require manual adjustments via admin API with Member Services lead approval. Final escalation point is Member Services call center supervisor.

## Open Questions

- This appears to be a formal process based on the escalation contacts and approval requirements mentioned
