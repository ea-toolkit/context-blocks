---
type: domain-logic
id: cost-sharing-calculation-rules
name: Cost-Sharing Calculation Rules
description: |-
  Algorithm for calculating member cost-sharing based on allowed amounts, not billed amounts
status: active
tags:
- financial-calculation
- member-protection
- contract-enforcement
source_documents:
- claims-processing-workflow.txt
confidence: 0.95
enforced_by:
- rules-engine
depends_on:
- allowed-amount-calculation
applies_to:
- member
---

# Cost-Sharing Calculation Rules

## Overview

Financial calculation logic that determines member responsibility (deductible, copay, coinsurance) using contracted allowed amounts rather than provider-billed amounts. This protects members from excessive provider billing.

## Details

Cost-sharing calculations (deductible, copay, coinsurance) are always calculated against the allowed amount, never the billed amount. The allowed amount is determined by: 1) Provider contract/fee schedule rates for in-network providers, 2) Usual and customary rates for out-of-network providers, or 3) Clearview standard schedules maintained by the actuarial team when no other rate applies. This rule protects members from balance billing and ensures predictable out-of-pocket costs regardless of what providers choose to bill. For example, if a provider bills $200 but the allowed amount is $120, member coinsurance of 20% would be calculated as $24 (20% of $120), not $40 (20% of $200).
