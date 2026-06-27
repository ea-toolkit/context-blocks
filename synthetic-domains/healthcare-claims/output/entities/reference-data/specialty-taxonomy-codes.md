---
type: reference-data
id: specialty-taxonomy-codes
name: Specialty Taxonomy Codes
description: Healthcare provider specialty classification codes maintained by NUCC
status: active
tags:
- nucc-standard
- provider-classification
- network-management
source_documents:
- claims-data-model-reference.txt
confidence: 0.9
used_in:
- provider
influences:
- benefit-plan
---

# Specialty Taxonomy Codes

## Overview

National Uniform Claim Committee (NUCC) maintained codes that classify healthcare provider specialties and subspecialties. Used for provider credentialing, network management, and claims processing validation.

## Details

Standardized 10-character codes stored in the specialty_code field of the provider data model. These codes define provider specialties (e.g., family medicine, cardiology, orthopedic surgery) and are used for network adequacy reporting, provider directory searches, and validating that services are performed by appropriately specialized providers. The codes include primary specialty assignments and may influence referral requirements in HMO plans or specialty copay structures in benefit plans.
