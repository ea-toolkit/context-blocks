---
type: data-model
id: payment-void-linkage-enhancement
name: Payment Void Linkage Enhancement
description: |-
  Enhancement to payment data model adding void_reason and linked_payment_id fields for better void/reissue tracking
status: active
tags:
- data-enhancement
- void-tracking
- completed-late
source_documents:
- postmortem-2023-payment-file-corruption.txt
confidence: 0.9
extends:
- payment
part_of:
- payment-reconciliation-rework
improves:
- void-reissue-workflow
---

# Payment Void Linkage Enhancement

## Overview

Data model enhancement completed in June 2025 as part of the payment reconciliation rework, adding void_reason and linked_payment_id fields to payment records for improved tracking of void/reissue relationships.

## Details

Implemented as action item INC-2023-0031-A5, taking 2 years from incident to completion (June 2025). Adds void_reason field to capture why a payment was voided and linked_payment_id to create explicit relationships between original and replacement payments. Part of broader payment reconciliation rework effort to improve financial tracking and auditability.
