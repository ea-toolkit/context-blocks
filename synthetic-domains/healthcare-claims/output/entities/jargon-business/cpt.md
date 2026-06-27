---
type: jargon-business
id: cpt
name: CPT
description: |-
  Current Procedural Terminology - codes for medical procedures and services on professional claims
status: active
tags:
- coding-system
- professional-claims
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.95
used_by:
- rules-engine
part_of:
- hcpcs
---

# CPT

## Overview

CPT (Current Procedural Terminology) codes are maintained by the AMA and used to identify medical procedures and services on professional claims. Each procedure or service has a specific CPT code that providers use for billing.

## Details

CPT codes are the standard coding system for medical procedures and services, maintained by the American Medical Association (AMA). These codes appear on professional claims and are used by the rules engine for procedure-specific logic. Example: 99213 represents an office visit. CPT codes form part of the broader HCPCS Level I coding system. The rules engine must understand these codes for proper claim adjudication, particularly in the 60% of simple edit rules that validate procedure-diagnosis relationships.
