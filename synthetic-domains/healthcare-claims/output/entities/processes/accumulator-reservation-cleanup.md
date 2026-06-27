---
type: process
id: accumulator-reservation-cleanup
name: Accumulator Reservation Cleanup
description: |-
  Batch process running every 6 hours to expire orphaned soft reservations from crashed adjudication processes
status: active
tags:
- batch-job
- system-recovery
- benefit-management
source_documents:
- eligibility-api-reference.txt
confidence: 0.85
owned_by:
- member-services
triggered_by:
- clv-4521
produces:
- soft-reservation-released-event
---

# Accumulator Reservation Cleanup

## Overview

Automated cleanup job addressing CLV-4521 issue where Rules Engine crashes leave persistent soft reservations that block benefit utilization. The process identifies reservations older than 4 hours and releases them to restore benefit availability.

## Details

This batch job runs on a 6-hour schedule to scan for soft reservations with reserved_at timestamps older than 4 hours, indicating likely orphaned reservations from crashed or hung adjudication processes. When found, these reservations are removed from the pending_reservations array and the reserved amounts are returned to available benefit balances. The 4-hour threshold provides sufficient time for normal claim adjudication while preventing indefinite benefit lockup. This addresses a critical operational issue where system failures could permanently exhaust member benefits without processing actual claims. The process likely includes monitoring and alerting for high volumes of expired reservations indicating systemic adjudication problems.

## Open Questions

- This appears to be a batch process based on the documented cleanup mechanism
