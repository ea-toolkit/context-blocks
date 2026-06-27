---
type: domain-logic
id: soft-reservation-logic
name: Soft Reservation Logic
description: |-
  Business rule preventing over-application of benefit accumulators during concurrent claim processing
status: active
tags:
- concurrency
- accumulators
- eligibility
source_documents:
- architecture-overview.txt
confidence: 0.9
enforced_by:
- eligibility-service
---

# Soft Reservation Logic

## Overview

The soft reservation logic ensures that benefit accumulators (like deductibles) aren't over-applied when multiple claims are being processed simultaneously for the same member. This prevents two concurrent claims from both counting the same dollars toward the deductible.

## Details

Implemented in the Eligibility Service to handle concurrent claim processing scenarios. When a claim is being adjudicated, the system places a soft reservation on the accumulator amounts being applied (e.g., $500 toward deductible). This prevents another simultaneous claim from applying those same dollars. The reservation is released when adjudication completes. Without this logic, race conditions could cause incorrect accumulator calculations, leading to wrong member cost-sharing amounts.
