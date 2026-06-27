---
type: business-event
id: double-applied-deductible-event
name: Double Applied Deductible Event
description: |-
  Error condition where two claims incorrectly both apply toward deductible independently
status: active
tags:
- error-condition
- deductible
- soft-reservations
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.9
caused_by:
- soft-reservation-logic
affects:
- accumulator
triggers:
- member-escalation-process
---

# Double Applied Deductible Event

## Overview

Occurs when soft reservation system fails and two claims processing concurrently both count toward the member's deductible, resulting in incorrect member cost calculations and member complaints.

## Details

Happens when the soft reservation system fails, such as when the 6-hour cleanup job runs during active claim adjudication, allowing two claims to both apply toward the deductible independently instead of one reserving the amount while the other processes. Detection usually comes from member calls complaining about being charged too much. Investigation involves checking member accumulator history versus actual claim payments. Resolution requires manual adjustment via admin API with Member Services lead approval.
