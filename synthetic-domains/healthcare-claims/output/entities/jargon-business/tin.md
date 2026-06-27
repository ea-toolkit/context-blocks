---
type: jargon-business
id: tin
name: TIN
description: Tax Identification Number used for provider payment batching and tax
  reporting
status: active
tags:
- payments
- provider-identification
- tax-reporting
source_documents:
- architecture-overview.txt
confidence: 0.9
used_in:
- payment-cycle-processing
---

# TIN

## Overview

TIN (Tax Identification Number) is used to identify providers for payment and tax reporting purposes. Provider payments are batched per TIN per payment cycle, which means all claims for providers sharing the same TIN are grouped together for payment processing.

## Details

Used in the Payment Engine for batching provider payments - all claims for providers sharing the same TIN are grouped together in a single payment per payment cycle. This batching approach reduces transaction costs and simplifies reconciliation for providers who may have multiple practice locations or NPIs under the same tax entity. The TIN is also used for generating 1099 tax forms and other tax reporting requirements.
