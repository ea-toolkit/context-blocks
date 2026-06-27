---
type: business-event
id: eft-settlement-confirmation
name: EFT Settlement Confirmation
description: |-
  Banking partner notification confirming actual Electronic Funds Transfer settlement completion
status: planned
tags:
- payment-processing
- banking-integration
- settlement
source_documents:
- design-session-payment-reconciliation.txt
confidence: 0.8
published_by:
- banking-partner
consumed_by:
- payment-engine
triggers:
- era-835-settlement-confirmation
---

# EFT Settlement Confirmation

## Overview

Settlement confirmation feed from banking partner that confirms EFT transactions have actually settled, including final amounts. This confirmation is needed to trigger ERA 835 generation in the revised Payment Engine workflow, replacing the current batch-time generation that causes reconciliation mismatches.

## Details

Currently under investigation by Leo Chen to determine format, latency, and consumption method from banking partner. The confirmation will serve as the trigger for generating final ERA 835 remittance advice, ensuring amounts match actual bank deposits. This replaces the current approach of generating provisional 835s at batch time, which providers dislike receiving multiple times.

## Open Questions

- What format will the banking partner use for settlement confirmation?
- What is the actual latency for settlement confirmation delivery?
