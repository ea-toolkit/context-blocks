---
type: business-event
id: plan-year-boundary-event
name: Plan Year Boundary Event
description: |-
  Annual event marking transition from one plan year to the next, triggering accumulator resets
status: active
tags:
- plan-year
- annual
- transition
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.9
triggers:
- accumulator-reset-logic
affects:
- accumulator
---

# Plan Year Boundary Event

## Overview

Occurs at plan year boundaries (typically January 1st, or plan effective date for off-cycle plans) when member benefit accumulators must reset to zero for the new plan year.

## Details

Annual boundary event typically on January 1st, though off-cycle plans have different effective dates. Triggers accumulator reset batch job and creates complex timing scenarios where claims with December date_of_service but processed in January need access to both old and new year accumulators. Requires careful handling to ensure proper accumulator application during transition period.
