---
type: process
id: retroactive-enrollment-reprocessing
name: Retroactive Enrollment Reprocessing
description: |-
  Automatic reprocessing of claims when retroactive enrollment changes occur within 60-day window
status: active
tags:
- exception-handling
- retroactive-processing
- enrollment-correction
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
triggered_by:
- eligibility-service
owned_by:
- member-services
affects:
- claim
---

# Retroactive Enrollment Reprocessing

## Overview

Exception workflow that automatically reprocesses affected claims when Member Services processes retroactive enrollment changes up to 60 days back, potentially changing claim dispositions.

## Details

When Member Services processes a retroactive enrollment change (coverage corrections, plan changes, or eligibility adjustments up to 60 days in the past), the Eligibility Service automatically triggers reprocessing of any claims from the affected date range. This reprocessing can result in previously denied claims being approved (if member gains coverage) or previously approved claims being denied (if coverage is removed). The 60-day window balances administrative practicality with member protection, allowing reasonable time for enrollment corrections while preventing indefinite claim liability exposure.
