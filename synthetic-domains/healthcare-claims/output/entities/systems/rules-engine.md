---
type: system
id: rules-engine
name: Rules Engine
description: |-
  Vendor product that adjudicates claims against benefit plans, fee schedules, and medical policies
status: active
tags:
- seed-context-derived
- foundation
source_documents:
- seed-context
confidence: 0.9
owned_by:
- claims-operations
communicates_with:
- eligibility-service
---

# Rules Engine

## Overview

The Rules Engine is described as the 'adjudication brain' - a vendor product that evaluates validated claims against benefit plan rules, fee schedules, and medical policy edits. The team is currently mid-migration to replace it.

## Details

This system takes validated claims from the gateway and runs them through comprehensive rule evaluation including benefit plan coverage, fee schedules, and medical policy edits. It produces dispositions of pay, deny, or pend for manual review. It's a vendor product that's being replaced as part of an ongoing migration.
