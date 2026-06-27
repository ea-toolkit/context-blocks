---
type: process
id: provider-payment-batching
name: Provider Payment Batching
description: Batching of provider payments by TIN per payment cycle with $5 minimum
  threshold
status: active
tags:
- financial-processing
- batch-optimization
- cost-control
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
executed_by:
- payment-engine
produces:
- era-835
governed_by:
- payment-threshold-rules
---

# Provider Payment Batching

## Overview

Payment processing workflow that groups approved claims by provider Tax ID Number (TIN) for efficient payment cycles. Implements $5 minimum payment threshold with holdover for amounts below threshold.

## Details

Provider payments are batched by provider TIN (Tax Identification Number) within each payment cycle to consolidate multiple claims into single payments. Payment methods include EFT (preferred), check, and virtual card options. A $5 minimum payment threshold is enforced - amounts below this threshold are held and accumulated until the minimum is reached in subsequent cycles. Each payment batch generates an ERA 835 remittance advice document that details all claims included in the payment, allowing providers to reconcile their accounts receivable. This batching approach reduces transaction costs and administrative overhead while providing clear payment documentation.
