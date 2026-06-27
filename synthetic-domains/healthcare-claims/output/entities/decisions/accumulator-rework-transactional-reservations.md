---
type: decision
id: accumulator-rework-transactional-reservations
name: Accumulator Rework - Transactional Reservations Decision
description: |-
  Decision to implement transactional accumulator reservations with SELECT FOR UPDATE to solve crash cleanup and concurrency issues
status: active
tags:
- architecture
- concurrency
- database
source_documents:
- design-session-accumulator-rework.txt
confidence: 1.0
applies_to:
- accumulator
made_by:
- priya-anand
supersedes:
- soft-reservation-logic
---

# Accumulator Rework - Transactional Reservations Decision

## Overview

The team decided to rework the accumulator system to use transactional reservations within the same database transaction as adjudication writes. This approach uses SELECT FOR UPDATE locks to prevent concurrent accumulator drift while maintaining the existing architecture with minimal disruption.

## Details

The decision followed evaluation of three options: event-sourced accumulators (complex performance concerns), distributed Redis locks (new critical dependency), and transactional reservations (minimal disruption). Option C was chosen because it addresses the core problems - crash cleanup (no orphaned reservations) and concurrent processing (row-level locking) - while keeping the existing read path intact. The solution serializes concurrent claims for the same member at the database level, with analysis showing most members have at most 2 concurrent claims, making contention minimal. This eliminates the need for the 6-hour cleanup batch job.
