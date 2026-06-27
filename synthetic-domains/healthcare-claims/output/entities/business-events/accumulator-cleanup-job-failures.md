---
type: business-event
id: accumulator-cleanup-job-failures
name: Accumulator Cleanup Job Failures
description: |-
  Two SEV-2 incidents in Q3 2025 when accumulator reservation cleanup job failed due to Cloud SQL maintenance conflicts
status: active
tags:
- sev-2
- batch-job
- maintenance-conflict
source_documents:
- meeting-notes-quarterly-ops-review-2025q3.txt
confidence: 0.85
affects:
- eligibility-service
- cloud-sql-postgresql
---

# Accumulator Cleanup Job Failures

## Overview

Two separate SEV-2 incidents during Q3 2025 when the accumulator reservation cleanup job failed due to conflicts with Cloud SQL maintenance windows. Indicates need for better job scheduling coordination.

## Details

Two SEV-2 incidents occurred during Q3 2025 when the scheduled accumulator reservation cleanup job failed to execute properly due to timing conflicts with Cloud SQL database maintenance windows. The accumulator cleanup job is responsible for releasing expired soft reservations in the Eligibility Service after the 6-hour cleanup cycle. These failures suggest inadequate coordination between scheduled maintenance and critical batch job timing.
