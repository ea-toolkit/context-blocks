---
type: data-model
id: payments-table-void-linkage
name: Payments Table Void Linkage Schema
description: |-
  Database schema changes to add void reason tracking and payment chain linkage to payments table
status: planned
tags:
- database-migration
- audit-trail
- payment-processing
source_documents:
- design-session-payment-reconciliation.txt
confidence: 0.95
maps_to:
- payment
used_by:
- payment-engine
---

# Payments Table Void Linkage Schema

## Overview

Proposed database migration to add three new fields to payments table: void_reason (VARCHAR 100), linked_payment_id (BIGINT foreign key), and void_type (ENUM with values REPROCESS, FRAUD, MANUAL, RECOUP). These fields establish bidirectional linkage between voided payments and their replacements.

## Details

Schema changes enable proper audit trails for payment voids and reissues. Every void will point to its replacement payment via linked_payment_id, and void_reason provides human-readable context. The void_type enum categorizes voids by cause: REPROCESS (Rules Engine reprocessing), FRAUD (SIU holds), MANUAL (manual intervention), RECOUP (recoupment processing). No backfill planned for historical data due to incomplete audit trails from 2024 voids.
