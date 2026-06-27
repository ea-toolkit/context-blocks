---
type: jargon-business
id: icd-10-cm
name: ICD-10-CM
description: |-
  International Classification of Diseases, 10th Revision, Clinical Modification - diagnosis codes for claims
status: active
tags:
- coding-system
- diagnosis
- medical-necessity
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.95
used_by:
- rules-engine
related_to:
- icd-10-pcs
---

# ICD-10-CM

## Overview

ICD-10-CM codes are used to identify clinical diagnoses on all medical claims. Every claim must have at least one diagnosis code to justify the medical necessity of the services provided.

## Details

ICD-10-CM (International Classification of Diseases, 10th Revision, Clinical Modification) provides standardized diagnosis codes that appear on both professional and institutional claims. Example: E11.9 represents type 2 diabetes without complications. These codes are essential for claim adjudication as they establish medical necessity and are used in procedure-diagnosis validation rules. The rules engine uses ICD-10-CM codes in conjunction with CPT/HCPCS codes to validate appropriate care delivery and calculate DRGs for institutional claims.
