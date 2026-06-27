---
type: jargon-business
id: carc-rarc
name: CARC/RARC
description: |-
  Claim Adjustment Reason Code / Remittance Advice Remark Code - standard denial reason codes
status: active
tags:
- healthcare-standards
- denial-codes
- communication
source_documents:
- claims-data-model-reference.txt
confidence: 1.0
used_in:
- claim
communicated_via:
- era-835
---

# CARC/RARC

## Overview

Industry-standard codes used to communicate claim denial reasons to providers. CARC codes indicate financial adjustments while RARC codes provide additional explanatory remarks for claim processing decisions.

## Details

Standardized code sets used in healthcare claims processing to communicate denial and adjustment reasons. CARC (Claim Adjustment Reason Code) indicates why a financial adjustment was made to a claim line, while RARC (Remittance Advice Remark Code) provides additional explanatory information. These codes are stored in the denial_reason field of the claim data model and are used in ERA 835 remittance advice to inform providers why claims were denied or adjusted.
