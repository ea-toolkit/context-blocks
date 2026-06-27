---
type: reference-data
id: place-of-service-codes
name: Place of Service Codes
description: CMS standardized codes indicating where healthcare services were performed
status: active
tags:
- cms-standard
- location-based
- payment-impact
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
used_in:
- claim
influences:
- fee-schedule
---

# Place of Service Codes

## Overview

Standardized two-digit codes maintained by CMS that specify the location where healthcare services were rendered. Used in claims processing to determine appropriate payment rates and coverage rules based on service setting.

## Details

CMS-maintained codes stored in the place_of_service field of claims data model. Examples include office visits, inpatient hospital, outpatient hospital, emergency room, and skilled nursing facilities. These codes influence payment calculations (facility vs non-facility rates), coverage determinations, and may affect member cost-sharing amounts. The codes are essential for proper adjudication as the same procedure may have different coverage rules depending on where it was performed.
