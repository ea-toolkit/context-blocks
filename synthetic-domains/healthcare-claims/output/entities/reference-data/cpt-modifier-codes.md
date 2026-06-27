---
type: reference-data
id: cpt-modifier-codes
name: CPT Modifier Codes
description: |-
  Two-character codes that provide additional information about procedures to affect payment
status: active
tags:
- ama-standard
- procedure-modification
- payment-impact
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
used_in:
- claim
affects:
- fee-schedule
---

# CPT Modifier Codes

## Overview

American Medical Association maintained codes that modify procedure codes to indicate special circumstances, multiple procedures, or service variations. Examples include modifier 25 for significant evaluation and management services and modifier 59 for distinct procedures.

## Details

Two-character alphanumeric codes stored in modifier_1 and modifier_2 fields of claim_lines table. These modifiers can significantly impact payment by indicating circumstances like bilateral procedures, multiple surgeries, or services provided at different anatomical sites. Common modifiers include 25 (significant, separately identifiable E&M service), 59 (distinct procedural service), and various anatomical modifiers. Fee schedules may have different allowed amounts for modified procedures, and some modifiers affect whether procedures can be billed together.
