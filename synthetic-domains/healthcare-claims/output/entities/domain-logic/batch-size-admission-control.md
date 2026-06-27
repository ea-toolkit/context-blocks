---
type: domain-logic
id: batch-size-admission-control
name: Batch Size Admission Control
description: |-
  Business rule limiting the maximum number of claims that can be submitted in a single batch
status: active
tags:
- admission-control
- resource-protection
- api-limit
source_documents:
- 2024-claims-gateway-outage-postmortem.txt
confidence: 0.95
enforced_by:
- claims-submission-api
motivated_by:
- march-2024-claims-gateway-outage
implemented_via:
- clv-3902
---

# Batch Size Admission Control

## Overview

This rule caps batch submissions at 2,000 claims per batch to prevent resource exhaustion. Large submissions must be split into multiple smaller batches.

## Details

The batch size admission control rule was implemented after the March 2024 incident where Northeast Clearinghouse submitted an abnormally large batch of 14,000 institutional claims, far exceeding their normal 2,000-3,000 claim batches. The rule sets a hard limit of 2,000 claims per batch at the Claims Submission API /claims/batch endpoint. This prevents single large batches from overwhelming system resources, particularly database connection pools. Submitters requiring larger volumes must split their submissions into multiple 2,000-claim batches. The rule was implemented as CLV-3902 and completed by March 25, 2024. Northeast Clearinghouse was specifically notified about this new limit and adjusted their submission process accordingly.
