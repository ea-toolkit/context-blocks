---
type: jargon-business
id: sev-1
name: SEV-1
description: |-
  Highest severity incident classification for complete service outages affecting business operations
status: active
tags:
- incident-management
- classification
source_documents:
- postmortem-2022-eligibility-outage.txt
confidence: 0.9
applies_to:
- september-2022-eligibility-outage
related_to:
- march-2024-claims-gateway-outage
---

# SEV-1

## Overview

Severity 1 incident designation used at Clearview for the most critical production issues that cause complete service outages or severe business impact. The September 2022 Eligibility Service outage was classified as SEV-1 due to its cascading impact across multiple systems and complete halt of claims processing.

## Details

SEV-1 represents the highest severity level in Clearview's incident classification system, reserved for incidents that cause complete service outages, data loss, or severe business impact. The September 2022 incident qualified as SEV-1 because it took down the Eligibility Service completely, cascaded to Claims Gateway and Rules Engine failures, prevented claims processing for nearly 4 hours, and impacted member-facing services. SEV-1 incidents trigger immediate escalation procedures and require post-incident reviews.

## Open Questions

- SEV-1 likely triggers specific escalation procedures based on the incident response pattern
