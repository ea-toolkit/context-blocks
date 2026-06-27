---
type: domain-logic
id: event-sourced-accumulator-approach
name: Event-Sourced Accumulator Approach
description: |-
  Alternative approach storing accumulator events as immutable log with derived balance calculations
status: proposed
tags:
- architecture
- event-sourcing
- alternative-approach
source_documents:
- design-session-accumulator-rework.txt
confidence: 0.9
alternative_to:
- soft-reservation-logic
would_apply_to:
- accumulator
---

# Event-Sourced Accumulator Approach

## Overview

A proposed alternative to the current accumulator system that would store every accumulator event (reservation, application, release, adjustment) as an immutable log rather than maintaining running balances. The current balance would be derived by replaying events, providing perfect audit trails and eliminating state corruption.

## Details

This approach would fundamentally change how accumulators work by treating them as event streams rather than mutable state. Every accumulator operation becomes an immutable event in the log, with current balances calculated by replaying the event history. Benefits include no state corruption, perfect audit trails, and automatic handling of crash cleanup (orphaned reservations are just events without matching 'applied' events). However, performance concerns arise from needing to replay events to get current balances during adjudication, requiring a materialized view or CQRS pattern with sub-millisecond read performance. The approach provides eventual consistency rather than strong consistency, creating risk of over-applying deductibles if the materialized view lags behind the event stream.
