---
type: business-event
id: era-835-timing-mismatch
name: ERA 835 Timing Mismatch Problem
description: |-
  Reconciliation problem where ERA 835 remittance advice doesn't match actual EFT settlement amounts
status: active
tags:
- payment-processing
- provider-experience
- reconciliation-issue
source_documents:
- design-session-payment-reconciliation.txt
confidence: 0.9
involves:
- payment-engine
- era-835
- banking-partner
---

# ERA 835 Timing Mismatch Problem

## Overview

Current Payment Engine generates ERA 835 remittance advice at payment batch time, but EFT settlement occurs 2-3 business days later. During this gap, payment amounts can change due to fraud holds or claim voids, causing provider office reconciliation failures when deposits don't match posted ERA amounts.

## Details

The timing gap creates real operational problems for provider offices who receive the 835, post it to their accounts receivable, then discover the bank deposit doesn't match. Changes during the settlement window include fraud holds placed by SIU, claim voids from Rules Engine reprocessing, or other payment adjustments. Team decided to delay ERA 835 generation until EFT settlement confirmation is received from the banking partner, accepting 2-3 business day delay as preferable to reconciliation mismatches.
