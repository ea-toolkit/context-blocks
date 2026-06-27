---
type: domain-logic
id: cob-payer-order-rules
name: COB Payer Order Rules
description: |-
  Business rules determining primary vs secondary payer order using birthday rule, active/retired rule, etc.
status: active
tags:
- coordination-of-benefits
- payer-order
- birthday-rule
source_documents:
- eligibility-monitoring-guide.txt
confidence: 0.95
applies_to:
- cob-data-model
used_by:
- rules-engine
---

# COB Payer Order Rules

## Overview

Standard coordination of benefits rules that determine which payer is primary versus secondary when a member has coverage from multiple health plans. Uses industry-standard birthday rule and active/retired status rules.

## Details

Determines payer order (primary vs. secondary) using standard COB rules including birthday rule (older parent's plan is primary for dependent children) and active/retired rule (active employee's plan primary over retiree's plan). When Clearview is primary, claims adjudicate normally. When secondary, requires primary payer's EOB before adjudication, calculating remaining member balance up to Clearview's allowed amount.
