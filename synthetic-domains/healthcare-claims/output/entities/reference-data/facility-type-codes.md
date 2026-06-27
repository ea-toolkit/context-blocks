---
type: reference-data
id: facility-type-codes
name: Facility Type Codes
description: |-
  Coded values identifying the type of healthcare facility where services were rendered
status: active
tags:
- facility-classification
- payment-rules
- coverage-impact
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
used_in:
- claim
influences:
- benefit-plan
---

# Facility Type Codes

## Overview

Standardized codes used to classify healthcare facilities in claims processing. Examples include office (11), inpatient hospital (21), outpatient hospital (22), emergency room (23), and skilled nursing facility (31).

## Details

Facility classification codes stored in the facility_type field of the claims data model. These codes help determine appropriate payment methodologies, coverage rules, and member cost-sharing requirements. For example, emergency room visits may have different copay structures, and inpatient services may be subject to different authorization requirements. The codes work in conjunction with place of service codes to provide complete context about the service setting.
