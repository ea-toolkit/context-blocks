---
type: business-event
id: soft-reservation-released-event
name: Soft Reservation Released Event
description: |-
  Event flow when temporary benefit reservations are released after claim finalization or denial
status: active
tags:
- accumulator-management
- cleanup
source_documents:
- eligibility-api-reference.txt
confidence: 0.8
published_by:
- eligibility-service
triggered_by:
- rules-engine
---

# Soft Reservation Released Event

## Overview

Triggered when claims are finalized or denied, releasing temporary accumulator reservations to make benefit amounts available for other claims. Also occurs during batch cleanup of expired reservations from crashed adjudication processes.

## Details

The event fires when the Rules Engine completes claim adjudication (whether approved or denied) or when the 6-hour batch cleanup job expires reservations older than 4 hours from crashed processes. The event removes pending_reservations entries from the accumulator endpoint response and makes the reserved amounts available for subsequent claims. This is critical for preventing benefit exhaustion from stuck reservations due to system failures, addressing the known issue CLV-4521 where Rules Engine crashes leave orphaned reservations.

## Open Questions

- This appears to be an implied event flow for reservation cleanup
