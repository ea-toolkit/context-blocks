---
type: data-model
id: accumulator
name: Accumulator
description: |-
  Data model tracking member benefit utilization including deductibles and out-of-pocket maximums
status: active
tags:
- financial
- concurrency
- batch-cleanup
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
owned_by:
- eligibility-service
links_to:
- member
used_by:
- rules-engine
---

# Accumulator

## Overview

Benefit accumulator records stored in Eligibility Service that track member progress toward annual limits like deductibles and out-of-pocket maximums. Includes soft reservation system to prevent race conditions during concurrent claim adjudication.

## Details

Stored in accumulators table in Eligibility Service, keyed by member_id + plan_year + accumulator_type. Types include IND_DEDUCTIBLE, FAM_DEDUCTIBLE, IND_OOP_MAX, FAM_OOP_MAX. Tracks limit_amount (from benefit plan), met_amount (applied so far), and computed remaining amount. Soft reservation system via accumulator_reservations table prevents double-counting during concurrent processing - reservations expire after 4 hours and are cleaned up every 6 hours by batch job. Known workaround for Rules Engine crash scenarios (JIRA CLV-4521).
