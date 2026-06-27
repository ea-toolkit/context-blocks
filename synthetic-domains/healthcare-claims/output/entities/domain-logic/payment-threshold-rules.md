---
type: domain-logic
id: payment-threshold-rules
name: Payment Threshold Rules
description: |-
  Business rules governing minimum payment amounts and recoupment spreading for provider payments
status: active
tags:
- payments
- thresholds
- recoupment
source_documents:
- architecture-overview.txt
confidence: 0.95
enforced_by:
- payment-engine
---

# Payment Threshold Rules

## Overview

Payment threshold rules control when and how provider payments are made. They include minimum payment thresholds to reduce transaction costs and recoupment spreading rules to maintain provider cash flow when recovering overpayments.

## Details

Implemented in the Payment Engine with two key rules: 1) Minimum payment threshold of $5 - amounts below this are held until the threshold is met across multiple claims, reducing transaction costs for small payments. 2) Recoupments exceeding 50% of a payment are spread across multiple payment cycles to avoid severe cash flow impact on providers. These rules balance operational efficiency with provider relationship management. Payment batching is done per TIN (Tax Identification Number) per payment cycle.
