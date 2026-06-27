---
type: business-event
id: november-2024-accumulator-incident
name: November 2024 Accumulator Plan Year Incident
description: |-
  Plan year boundary failure where accumulators weren't created for new plan year until batch job ran
status: active
tags:
- incident
- plan-year
- accumulator
source_documents:
- design-session-accumulator-rework.txt
confidence: 0.9
affects:
- accumulator
triggered:
- accumulator-rework-transactional-reservations
---

# November 2024 Accumulator Plan Year Incident

## Overview

A critical incident during plan year transition in November 2024 where new plan year accumulators were not pre-created, leaving members without proper accumulator tracking until the batch job executed. This incident highlighted the fragility of plan year boundary handling in the accumulator system.

## Details

The incident occurred at the plan year boundary when the system failed to create accumulators for the new plan year in advance. Members were left without proper deductible and out-of-pocket maximum tracking until the batch job eventually ran and created the missing accumulators. This caused disruption to claims processing and member portal benefit balance displays. The incident directly motivated the decision to pre-create next plan year accumulators during open enrollment processing rather than relying on batch jobs at the plan year transition.
