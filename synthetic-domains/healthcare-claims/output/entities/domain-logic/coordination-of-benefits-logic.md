---
type: domain-logic
id: coordination-of-benefits-logic
name: Coordination of Benefits Logic
description: |-
  Business rules for determining payer order and calculating secondary payer responsibility
status: active
tags:
- dual-coverage
- industry-standards
- complex-logic
source_documents:
- claims-processing-workflow.txt
confidence: 0.85
enforced_by:
- rules-engine
uses:
- eob
applies_to:
- member
---

# Coordination of Benefits Logic

## Overview

Complex logic for handling dual coverage scenarios where members have multiple insurance policies. Determines primary/secondary payer order and calculates Clearview's liability as remaining balance after primary payer.

## Details

When a member has dual coverage from multiple insurance payers, COB logic determines the order of payment responsibility. Clearview evaluates whether it is the primary or secondary payer based on standard industry rules (birthday rule for dependent children, active vs. retired coverage, etc.). If Clearview is the secondary payer, claims adjudication is suspended until the primary payer's Explanation of Benefits (EOB) is received showing their payment amount. Clearview's member responsibility is then calculated as the remaining balance after the primary payer's contribution, subject to Clearview's own benefit limits. This ensures members don't receive duplicate payments while maximizing their total coverage benefits.
