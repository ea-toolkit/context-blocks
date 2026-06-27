---
type: domain-logic
id: claims-api-v1-validation-logic
name: Claims API v1 Validation Logic
description: |-
  Asynchronous validation approach in Claims Submission API v1 that accepts invalid claims
status: deprecated
tags:
- deprecated
- legacy-era
- async-validation
- user-experience-issue
source_documents:
- claims-gateway-api-v1-deprecated.txt
confidence: 0.9
enforced_by:
- claims-submission-api-v1
superseded_by:
- claims-api-v2-validation-logic
---

# Claims API v1 Validation Logic

## Overview

Claims Submission API v1 uses asynchronous validation, returning HTTP 200 status for all accepted submissions even if validation fails later in the pipeline. This approach created confusion for API consumers who received success responses for ultimately invalid claims.

## Details

v1 validation logic accepts claims into the system first, then validates asynchronously during processing. This means the API returns 200 OK and a claim_id even for claims that will fail validation downstream. Consumers only discover validation failures by polling the status endpoint later. This pattern was problematic because it gave false positive feedback at submission time and required consumers to implement additional polling logic to detect validation failures. v2 switched to synchronous validation, performing format and basic validation checks at submission time and returning 400 Bad Request for invalid claims immediately.
