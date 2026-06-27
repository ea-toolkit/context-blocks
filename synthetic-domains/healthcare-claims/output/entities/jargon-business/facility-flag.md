---
type: jargon-business
id: facility-flag
name: Facility Flag
description: |-
  Indicator for different payment rates between facility and non-facility service locations
status: active
tags:
- pricing
- place-of-service
- overhead
source_documents:
- claims-data-model-reference.txt
confidence: 0.9
used_in:
- fee-schedule
---

# Facility Flag

## Overview

Boolean indicator in fee schedules that determines whether a procedure is performed in a facility (hospital, ASC) versus non-facility (physician office) setting. Different settings have different allowed amounts due to varying overhead costs.

## Details

Payment differentiation mechanism in fee schedules where the same procedure code can have different allowed amounts depending on whether it's performed in a facility versus non-facility setting. Facility settings (hospitals, ambulatory surgery centers) typically have lower physician payment rates because the facility bills separately for overhead costs, while non-facility settings (physician offices) include overhead in the physician payment. This flag in the fee_schedules table enables the Rules Engine to apply the correct allowed amount based on the place of service.
