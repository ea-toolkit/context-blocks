---
type: system
id: payment-engine
name: Payment Engine
description: |-
  System that processes adjudicated claims into payments via EFT and handles remittance advice
status: active
tags:
- seed-context-derived
- foundation
source_documents:
- seed-context
confidence: 0.9
owned_by:
- claims-operations
---

# Payment Engine

## Overview

Payment Engine takes adjudicated claims and converts them into actual monetary transactions. It handles provider payments through EFT, member reimbursements, and generates ERA 835 remittance advice.

## Details

This system processes the financial fulfillment of adjudicated claims, managing provider payments via Electronic Funds Transfer (EFT), member reimbursements, and generation of ERA 835 remittance advice documents. It also handles void and reissue transactions when corrections are needed.
