---
type: process
id: nacha-file-generation
name: NACHA File Generation Process
description: |-
  Nightly batch process that creates EFT payment files in NACHA format for submission to banking partner
status: active
tags:
- financial-process
- nightly-batch
- enhanced
source_documents:
- postmortem-2023-payment-file-corruption.txt
confidence: 0.9
executed_by:
- payment-engine
produces:
- nacha-format
depends_on:
- banking-partner
governed_by:
- payment-batching-query-logic
---

# NACHA File Generation Process

## Overview

The payment engine's nightly batch job that queries pending payments, formats them into NACHA standard EFT files, and submits them to the banking partner's SFTP for processing. Runs at 2:00 AM as part of the payment cycle.

## Details

Process runs nightly at 2:00 AM, querying the payments table for all claims with PAY disposition awaiting payment. Originally vulnerable to race conditions with concurrent void/reissue operations. Enhanced after the 2023 incident with duplicate detection pass and reconciliation checks requiring human approval before release to banking partner. Files are submitted via SFTP to the banking partner and typically processed by 6:00 AM.
