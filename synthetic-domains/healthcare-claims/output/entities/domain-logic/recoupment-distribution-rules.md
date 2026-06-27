---
type: domain-logic
id: recoupment-distribution-rules
name: Recoupment Distribution Rules
description: |-
  Logic for spreading large recoupments exceeding 50% of payment across multiple cycles
status: active
tags:
- provider-relations
- financial-protection
- cash-flow-management
source_documents:
- claims-processing-workflow.txt
confidence: 0.85
enforced_by:
- payment-engine
part_of:
- void-reissue-workflow
---

# Recoupment Distribution Rules

## Overview

Financial protection rule that prevents excessive recoupment impact on provider cash flow by spreading large recoupments across multiple payment cycles when they exceed 50% of a single payment.

## Details

When a provider overpayment requires recoupment, the system evaluates the recoupment amount against the provider's regular payment amounts. If the recoupment exceeds 50% of a typical payment cycle amount, the recoupment is automatically spread across multiple payment cycles to minimize cash flow impact on the provider. This rule balances Clearview's need to recover overpayments with maintaining positive provider relationships by avoiding sudden large payment reductions that could create financial hardship for provider practices.
