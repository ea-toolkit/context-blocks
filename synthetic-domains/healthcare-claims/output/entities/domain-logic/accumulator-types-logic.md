---
type: domain-logic
id: accumulator-types-logic
name: Accumulator Types Logic
description: |-
  Business rules defining four accumulator types for tracking member deductible and out-of-pocket progress
status: active
tags:
- accumulators
- benefit-calculation
- member-tracking
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.95
applies_to:
- accumulator
used_by:
- rules-engine
---

# Accumulator Types Logic

## Overview

Defines four accumulator types that track deductible and out-of-pocket maximum progress per member per plan year. Each type has specific meaning for individual vs family coverage levels.

## Details

Four accumulator types: IND_DEDUCTIBLE (individual deductible), FAM_DEDUCTIBLE (family deductible), IND_OOP_MAX (individual out-of-pocket maximum), FAM_OOP_MAX (family out-of-pocket maximum). These track member progress toward meeting their deductible and out-of-pocket maximum thresholds per plan year, enabling proper cost-sharing calculations during claim adjudication.
