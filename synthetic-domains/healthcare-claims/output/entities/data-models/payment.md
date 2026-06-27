---
type: data-model
id: payment
name: Payment
description: Data model representing provider and member payments with void/reissue
  tracking
status: active
tags:
- financial
- batched
- reconciliation
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
owned_by:
- payment-engine
links_to:
- claim
- era-835
---

# Payment

## Overview

Payment records stored in Payment Engine supporting provider EFT batching and member reimbursements. Includes payment lifecycle tracking from SCHEDULED through SETTLED, with comprehensive void/reissue workflow support and fraud hold capabilities.

## Details

Stored in payments table in Payment Engine. Payment types include PROVIDER and MEMBER_REIMB with methods EFT/CHECK/VCARD. Batching by TIN and payment cycle (YYYY-WNN format). Status progression: SCHEDULED → PROCESSED → SETTLED → VOIDED/HELD. Void/reissue fields added 2025-06: void_reason, linked_payment_id, void_type (REPROCESS/FRAUD/MANUAL/RECOUP). Payment-to-claim linkage via payment_claims join table supporting line-level detail. Minimum payment threshold of $5 (configurable). ERA 835 remittance advice generated for provider payments. Hold reasons include fraud and compliance holds.
