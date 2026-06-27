---
type: domain-logic
id: accumulator-reset-logic
name: Accumulator Reset Logic
description: Business rules for resetting accumulators to zero at plan year boundaries
status: active
tags:
- plan-year
- accumulators
- reset
- transition
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.9
applies_to:
- accumulator
triggered_by:
- plan-year-boundary-event
---

# Accumulator Reset Logic

## Overview

Defines when and how accumulators reset to zero - typically January 1st for standard plan years, or the plan's effective date for off-cycle plans. Includes logic for maintaining dual-year accumulators during transitions.

## Details

Accumulators reset to zero on January 1 (or the plan's effective date for off-cycle plans) handled by batch job. Critical transition logic: claims processed in late December might hit accumulators that reset on Jan 1, but adjudication uses date_of_service not processing_date. December service processed in January correctly applies to December accumulator, requiring accumulators to exist for both years during transition period to handle timing edge cases.
