---
type: data-model
id: fee-schedule
name: Fee Schedule
description: |-
  Data model defining contracted allowed amounts for procedure codes by provider contract
status: active
tags:
- financial
- contracts
- lookup-table
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
owned_by:
- provider-directory
used_by:
- rules-engine
links_to:
- provider
---

# Fee Schedule

## Overview

Contract-specific fee schedules stored in Provider Directory that define allowed amounts for CPT/HCPCS procedure codes. Used by Rules Engine during adjudication to calculate the maximum amount payable for each service, with fallback to standard fee schedule for missing codes.

## Details

Stored in fee_schedules table in Provider Directory, keyed by contract_id + procedure_code + modifier + effective_date. Contains allowed_amount for the contracted rate, facility_flag for different facility vs non-facility rates, and date ranges for temporal validity. Rules Engine lookup chain: provider NPI → contract_id → fee_schedule → procedure_code → allowed_amount. Fallback to Clearview standard fee schedule (actuarial team, updated annually) when no contracted rate exists. OON providers use 'usual and customary' rates derived from Medicare RBRVS with geographic adjustment factors.
