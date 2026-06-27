---
type: business-event
id: march-2024-claims-gateway-outage
name: March 2024 Claims Gateway Outage
description: System outage caused by unlimited batch sizes in Claims Submission API
  v1
status: active
tags:
- incident
- legacy-era
- catalyst
source_documents:
- claims-gateway-api-v1-deprecated.txt
confidence: 0.9
triggered_by:
- claims-submission-api-v1
led_to:
- claims-submission-api-v2
---

# March 2024 Claims Gateway Outage

## Overview

Critical production incident in March 2024 caused by the lack of batch size limits on the Claims Submission API v1 /claims/batch endpoint. This outage was the primary driver for developing API v2 with proper batch size controls.

## Details

The outage occurred when large batch submissions overwhelmed the Claims Gateway system through the v1 /claims/batch endpoint, which had no size restrictions. This incident highlighted the need for better resource management and led directly to the development of Claims Submission API v2 with a 2,000 claim batch limit and improved error handling. The incident appears related to the broader connection pool issues that plagued the system in 2024.

## Open Questions

- The incident appears related to the broader connection pool issues that plagued the system in 2024
