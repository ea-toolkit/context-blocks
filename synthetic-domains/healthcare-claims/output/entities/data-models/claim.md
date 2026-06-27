---
type: data-model
id: claim
name: Claim
description: |-
  The central data entity representing a healthcare service claim submitted for payment processing
status: active
tags:
- core-entity
- transactional
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
persisted_by:
- claims-gateway
links_to:
- member
- provider
- authorization
processed_by:
- rules-engine
---

# Claim

## Overview

The core data model that everything in the claims platform revolves around, storing claim header information, submission details, and adjudication results. Claims flow through multiple status states from RECEIVED through PAID/DENIED/PENDED, with associated line items and diagnoses as child entities.

## Details

Stored in the Claims Gateway DB with format CLM-YYYYMMDD-NNNNNN. Contains submission metadata (type: EDI_837P/I, JSON, OCR), service details (date_of_service, facility_type, place_of_service), provider identifiers (NPI, TIN), member linkage, financial amounts (total_billed), and processing state (status, disposition, denial/pend reasons). Includes fraud scoring (0.000-1.000 scale) and optional pre-authorization reference. Status progression: RECEIVED → VALIDATED → ELIGIBLE → ADJUDICATED → PAID/DENIED/PENDED → REJECTED. Child tables include claim_lines (procedure codes, modifiers, amounts) and claim_diagnoses (ICD-10-CM codes with sequence).
