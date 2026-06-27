---
type: domain-logic
id: payment-batching-query-logic
name: Payment Batching Query Logic
description: |-
  SQL query logic that selects pending payments for NACHA file generation, historically vulnerable to race conditions
status: active
tags:
- financial-logic
- concurrency
- fixed
source_documents:
- postmortem-2023-payment-file-corruption.txt
confidence: 0.9
enforced_by:
- payment-engine
applies_to:
- payment
---

# Payment Batching Query Logic

## Overview

The payment batching process uses a SQL query to identify all claims with PAY disposition awaiting payment for inclusion in the nightly NACHA EFT file. The original implementation had a race condition vulnerability where concurrent void/reissue operations could cause both original and replacement payments to be selected.

## Details

Original vulnerable query: SELECT claim_id, SUM(plan_paid) as total FROM payment_claims pc JOIN payments p ON pc.payment_id = p.payment_id WHERE p.status NOT IN ('VOIDED', 'HELD') AND p.payment_date IS NULL GROUP BY claim_id. The problem was that payments being voided in concurrent transactions still showed status = 'PROCESSED' until the void transaction committed, while replacement payments were already committed separately. Fixed in May 2023 to use FOR UPDATE SKIP LOCKED to avoid picking up rows being modified by concurrent transactions.
