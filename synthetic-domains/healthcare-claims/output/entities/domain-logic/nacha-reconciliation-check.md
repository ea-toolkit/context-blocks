---
type: domain-logic
id: nacha-reconciliation-check
name: NACHA File Reconciliation Check
description: |-
  Financial control that compares NACHA file totals against expected payment totals before banking partner release
status: active
tags:
- financial-control
- human-approval
- post-incident
source_documents:
- postmortem-2023-payment-file-corruption.txt
confidence: 0.9
enforced_by:
- payment-engine
part_of:
- nacha-file-generation
---

# NACHA File Reconciliation Check

## Overview

Pre-submission validation that compares the total payment amount in generated NACHA files against expected totals from the payment batching process. Requires human approval before releasing files to the banking partner.

## Details

Implemented as action item INC-2023-0031-A3 and completed by Marcus Reeves on 2023-05-20. Provides a reconciliation check with human approval gate before NACHA file release to prevent financial discrepancies. Part of enhanced safeguards following the lesson learned that financial operations need more controls than non-financial operations.
