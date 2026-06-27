---
type: business-event
id: soft-reservation-created-event
name: Soft Reservation Created Event
description: |-
  Event flow when the Eligibility Service creates temporary benefit amount holds during claim adjudication
status: active
tags:
- accumulator-management
- concurrent-processing
source_documents:
- eligibility-api-reference.txt
confidence: 0.85
published_by:
- eligibility-service
consumed_by:
- rules-engine
carries:
- accumulator
---

# Soft Reservation Created Event

## Overview

Generated when the Rules Engine requests accumulator data during claim adjudication, creating temporary reservations to prevent over-application of benefits during concurrent processing. These reservations include claim ID, reserved amount, target accumulator, and timestamp for cleanup tracking.

## Details

The event occurs when GET /eligibility/{memberId}/accumulators is called during active claim adjudication, creating soft reservations that appear in the pending_reservations array. Each reservation includes claim_id (e.g., CLM-20250814-002847), reserved_amount, target accumulator type (individual_deductible, family_deductible, individual_oop_max, family_oop_max), and reserved_at timestamp. Reservations prevent concurrent claims from double-applying against the same benefit limits. The system has a known issue (CLV-4521) where reservations aren't cleaned up if the Rules Engine crashes, requiring a 6-hour batch job to expire reservations older than 4 hours.

## Open Questions

- This appears to be an event flow based on the soft reservation mechanism described
