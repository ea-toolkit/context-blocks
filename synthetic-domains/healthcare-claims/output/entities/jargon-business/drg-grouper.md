---
type: jargon-business
id: drg-grouper
name: DRG Grouper
description: System logic that assigns Diagnosis Related Group codes to institutional
  claims
status: active
tags:
- medical-coding
- institutional-claims
- complex-rules
source_documents:
- meeting-notes-quarterly-ops-review-2025q3.txt
confidence: 0.85
used_in:
- rules-engine
---

# DRG Grouper

## Overview

Complex algorithmic logic that categorizes inpatient hospital stays into Diagnosis Related Groups (DRGs) for payment purposes. Represents some of the most complex rules in the migration from HealthLogic to the new rules engine.

## Details

Sophisticated medical coding and payment logic that analyzes institutional claims (hospital inpatient stays) and assigns them to appropriate Diagnosis Related Group (DRG) categories. DRGs are used to determine payment amounts for hospital services based on diagnosis, procedures, patient characteristics, and discharge status. The DRG grouper logic includes complex edge cases that are among the most challenging rules to migrate from the HealthLogic system to Clearview's new rules engine.
