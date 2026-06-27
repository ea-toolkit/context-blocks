---
type: process
id: open-enrollment-scaling
name: Open Enrollment Scaling Process
description: |-
  Preparation and scaling process for Eligibility Service during November-December open enrollment period
status: active
tags:
- scaling
- open-enrollment
- operations
- seasonal
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.95
applies_to:
- eligibility-service
coordinates_with:
- claims-operations
affects:
- member-portal
triggers:
- accumulator-audit-job
---

# Open Enrollment Scaling Process

## Overview

Open enrollment period (November through mid-December) requires significant scaling of Eligibility Service due to 10x enrollment update volume and 3-4x Member Portal traffic. Described as 'the Eligibility Service's Super Bowl'.

## Details

Preparation includes: scaling up pods 2 weeks before (HPA min replicas 3→6), increasing database connection pool (100→200), pre-warming benefit plan config cache, coordinating Claims Ops throttling of batch processing, and relaxing alert thresholds. Changes include 10x enrollment updates, batch plan assignment processing, accumulator resets for plan changes, and 3-4x Member Portal traffic. Post-enrollment cleanup involves accumulator audit job, orphaned reservation checks, and restoring normal thresholds.
