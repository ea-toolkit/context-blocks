---
type: business-event
id: void-reissue-tracking-problem
name: Void/Reissue Tracking Problem
description: |-
  Payment linkage issue where voided and reissued payments lack proper relationship tracking
status: active
tags:
- payment-processing
- data-integrity
- audit-trail
source_documents:
- design-session-payment-reconciliation.txt
confidence: 0.9
involves:
- payment-engine
- rules-engine
- payment
---

# Void/Reissue Tracking Problem

## Overview

When Rules Engine reprocesses claims due to retroactive enrollment changes, Payment Engine voids original payments and creates new ones, but the linkage between voided and reissued payments isn't tracked cleanly. This creates orphaned void records and makes payment chain analysis difficult.

## Details

Current void records lack structured reasons and links to replacement payments, making it impossible to trace payment chains or generate accurate reports. Team decided to add void_reason, linked_payment_id, and void_type fields to payments table to establish proper bidirectional linkage. New void types will include REPROCESS, FRAUD, MANUAL, and RECOUP. No backfill planned for historical voids due to incomplete audit trails from 2024.
