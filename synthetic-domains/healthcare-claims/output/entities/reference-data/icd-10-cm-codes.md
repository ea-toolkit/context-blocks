---
type: reference-data
id: icd-10-cm-codes
name: ICD-10-CM Codes
description: |-
  International Classification of Diseases diagnosis codes used in US healthcare claims
status: active
tags:
- who-standard
- medical-necessity
- diagnosis
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
used_in:
- claim
- authorization
---

# ICD-10-CM Codes

## Overview

World Health Organization maintained diagnosis coding system adapted for clinical modification in the United States. Used to indicate medical conditions and justify medical necessity for procedures and services.

## Details

Alphanumeric codes up to 8 characters stored in the claim_diagnoses table with sequence indicators (1=primary, 2-12=secondary). These codes establish medical necessity for procedures and are required for proper claim adjudication. ICD-10-CM codes are also used in prior authorization requests to support service approval decisions. For institutional claims, present-on-admission indicators (Y/N/U/W) track whether conditions existed at admission time, which affects hospital quality metrics and payment adjustments.
