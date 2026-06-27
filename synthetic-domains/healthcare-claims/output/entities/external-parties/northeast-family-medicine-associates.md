---
type: external-party
id: northeast-family-medicine-associates
name: Northeast Family Medicine Associates
description: |-
  Provider group that experienced real-time claim submission failures during the March 2024 outage
status: active
tags:
- provider-group
- affected-party
source_documents:
- 2024-claims-gateway-outage-postmortem.txt
confidence: 0.9
affected_by:
- march-2024-claims-gateway-outage
uses:
- claims-submission-api
---

# Northeast Family Medicine Associates

## Overview

Northeast Family Medicine Associates is a provider group that was impacted by the March 2024 Claims Gateway outage. They called to complain about real-time submission failures during the incident.

## Details

Northeast Family Medicine Associates represents one of the affected provider groups during the March 2024 Claims Gateway outage. They experienced failures when attempting real-time professional claim submissions during the 65-minute window when professional claims processing was down (02:17 - 03:20 UTC). The provider group called Clearview to report the submission failures, demonstrating the direct business impact of the technical outage on provider operations. This feedback likely contributed to the urgency around implementing the remediation action items.
