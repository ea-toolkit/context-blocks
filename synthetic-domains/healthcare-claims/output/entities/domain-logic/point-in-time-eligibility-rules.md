---
type: domain-logic
id: point-in-time-eligibility-rules
name: Point-in-Time Eligibility Rules
description: |-
  Business rules governing historical eligibility lookups with 2-year retrospective limit and date validation
status: active
tags:
- date-validation
- retroactive-processing
source_documents:
- eligibility-api-reference.txt
confidence: 0.9
enforced_by:
- eligibility-api-v2
used_by:
- rules-engine
---

# Point-in-Time Eligibility Rules

## Overview

Rules Engine uses point-in-time eligibility verification during claim adjudication to evaluate member coverage as of the claim's date of service. The system supports lookups up to 2 years in the past but rejects future dates with validation errors.

## Details

The /eligibility/{memberId}/asof/{date} endpoint implements these rules: dates must be in YYYY-MM-DD format, cannot be in the future (returns 400 error), and cannot be more than 2 years in the past (DATE_OUT_OF_RANGE error). This supports retroactive claim processing scenarios where claims are submitted after the date of service. The Rules Engine specifically uses this for adjudication to ensure it evaluates coverage based on when services were rendered, not when the claim was received. The 2-year limit likely aligns with typical claim submission timely filing requirements and data retention policies.
