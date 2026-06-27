---
type: data-model
id: authorization
name: Authorization
description: Data model for prior authorization requests and approvals with validity
  tracking
status: active
tags:
- authorization
- clinical
- time-limited
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
owned_by:
- pre-auth-service
links_to:
- member
- provider
---

# Authorization

## Overview

Pre-authorization records stored in Pre-Auth Service with format AUTH-YYYYMMDD-NNNNNN. Tracks authorization requests, determinations (approved/denied/pended), and validity periods with unit consumption tracking as claims are processed against approved authorizations.

## Details

Stored in authorizations table in Pre-Auth Service. Contains member and provider linkage, service categories (IMAGING/SURGERY/SPECIALTY_DRUG), arrays of approved procedure and diagnosis codes, determination status (APPROVED/DENIED/PENDED_CLINICAL), and validity periods (90 days standard, 60 for surgical). Auto-approval indicated by determined_by='auto-approve'. Unit tracking with units_approved and units_used, status transitions to EXHAUSTED when fully utilized. Authorization status: ACTIVE/EXPIRED/CANCELLED/EXHAUSTED. Claims reference authorizations via auth_id for validation during adjudication.
