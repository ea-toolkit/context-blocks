---
type: process
id: accumulator-reconciliation-job
name: Accumulator Reconciliation Job
description: |-
  Monthly batch job that corrects accumulator drift by recalculating from adjudicated claims
status: active
tags:
- batch-job
- reconciliation
- accumulators
- monthly
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.95
corrects:
- accumulator
depends_on:
- claim
---

# Accumulator Reconciliation Job

## Overview

Scheduled job that runs on the 1st of each month at 04:00 UTC to fix accumulator drift issues. Recalculates accumulator amounts from actual adjudicated claim payments and corrects any discrepancies.

## Details

Addresses accumulator drift where accumulator amounts can drift from actual sum of claim payments due to concurrent processing. While soft reservation system prevents most drift, edge cases exist (e.g., claim voided after accumulator was updated). Job recalculates accumulators from the source of truth (adjudicated claims) and applies corrections. Scheduled monthly on 1st at 04:00 UTC.
