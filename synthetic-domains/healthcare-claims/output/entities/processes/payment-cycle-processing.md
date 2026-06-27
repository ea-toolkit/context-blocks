---
type: process
id: payment-cycle-processing
name: Payment Cycle Processing
description: |-
  Nightly batch job process that generates provider payments and member reimbursements
status: active
tags:
- payments
- batch-processing
- nightly-jobs
source_documents:
- architecture-overview.txt
confidence: 0.9
executed_by:
- payment-engine
produces:
- era-835
- eob
---

# Payment Cycle Processing

## Overview

The payment cycle processing runs as nightly batch jobs to convert adjudicated claims into actual financial transactions. It handles provider payments, member reimbursements, and remittance advice generation according to business rules and payment schedules.

## Details

Runs nightly as batch jobs to process payments from adjudicated claims. Generates provider payments batched per TIN (Tax Identification Number) per payment cycle via EFT, check, or virtual card. Processes member reimbursements for out-of-network claims within 10 business days. Applies business rules including $5 minimum payment threshold (amounts below are held until threshold is met) and spreads recoupments exceeding 50% of a payment across multiple cycles. Also generates ERA 835 electronic remittance advice and EOB documents.
