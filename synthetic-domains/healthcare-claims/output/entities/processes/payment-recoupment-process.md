---
type: process
id: payment-recoupment-process
name: Payment Recoupment Process
description: |-
  Manual process for recovering overpaid amounts from providers through recoupment requests and deductions from future payments
status: active
tags:
- financial-recovery
- manual-process
source_documents:
- postmortem-2023-payment-file-corruption.txt
confidence: 0.85
owned_by:
- claims-operations
triggered_by:
- inc-2023-0031
---

# Payment Recoupment Process

## Overview

When providers receive overpayments that cannot be reversed through banking channels, Claims Ops initiates recoupment requests to recover the funds. The process involves manual identification of overpayments, sending recoupment letters, and deducting amounts from future payments to the affected providers.

## Details

Used extensively after the 2023 payment corruption incident to recover $1.9M in duplicate payments that couldn't be reversed by the banking partner. Process took 4 months (through August 2023) to complete for 124 affected TINs. Generated complaints from 7 provider offices about recoupment letters. Recovery likely involves deducting amounts from future legitimate payments to gradually recover overpaid funds.

## Open Questions

- Recovery likely involves deducting amounts from future legitimate payments to gradually recover overpaid funds
