---
type: business-event
id: accumulator-drift-event
name: Accumulator Drift Event
description: |-
  Data inconsistency event where accumulator amounts drift from actual claim payment totals
status: active
tags:
- data-inconsistency
- concurrency
- accumulators
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.9
affects:
- accumulator
resolved_by:
- accumulator-reconciliation-job
prevented_by:
- soft-reservation-logic
---

# Accumulator Drift Event

## Overview

Occurs when accumulator amounts become inconsistent with the actual sum of claim payments due to concurrent processing edge cases. Most drift is prevented by soft reservation system, but some cases slip through.

## Details

Accumulator drift happens due to concurrent processing where multiple claims might update accumulators simultaneously, or when claims are voided after accumulator updates have been applied. While the soft reservation system prevents most of this, edge cases exist. Detection typically comes from member complaints about incorrect charges. Resolution requires running the monthly accumulator reconciliation job or manual adjustment via admin API with Member Services lead approval.
