---
type: domain-logic
id: recoupment-time-limits
name: Recoupment Time Limits
description: |-
  Regulatory constraints on how far back payers can recover overpayments from providers
status: active
tags:
- regulatory
- compliance
- financial-constraint
source_documents:
- design-session-cob-handling.txt
confidence: 0.85
constrains:
- cob-verification-workflow
applies_to:
- recoupment-distribution-rules
---

# Recoupment Time Limits

## Overview

State-specific regulations that limit recoupment periods to typically 12-18 months. Critical constraint for COB reprocessing when other coverage is discovered.

## Details

Regulatory limits that vary by state but typically allow recoupment of overpaid claims for 12-18 months from the original payment date. These limits are crucial for the COB verification workflow because when other coverage is discovered and Clearview determines they should have been secondary instead of primary, they can only recover overpayments within the regulatory window. This timing constraint affects the financial benefit calculation for COB auto-detection and requires careful handling in the reprocessing workflow.

## Open Questions

- Usually 12-18 months depending on the state
