---
type: system
id: eligibility-service
name: Eligibility Service
description: |-
  Source of truth for member enrollment, handling EDI transactions and tracking accumulators
status: active
tags:
- seed-context-derived
- foundation
source_documents:
- seed-context
confidence: 0.9
owned_by:
- member-services
---

# Eligibility Service

## Overview

Eligibility Service maintains authoritative member enrollment data and handles 270/271 EDI transactions. It also tracks member accumulators like deductible progress and out-of-pocket maximums.

## Details

This system serves as the source of truth for member enrollment information and processes eligibility verification through 270/271 EDI transactions. It maintains running totals of member accumulators including deductible amounts met and out-of-pocket maximum progress, which are checked by the rules engine during claim adjudication.
