---
type: data-model
id: batch-eligibility-request
name: Batch Eligibility Request
description: |-
  Data structure for submitting bulk eligibility verification requests in JSON or EDI 270 format
status: active
tags:
- batch-processing
- edi-format
source_documents:
- eligibility-api-reference.txt
confidence: 0.9
used_by:
- eligibility-api-v2
maps_to:
- edi-270-271
---

# Batch Eligibility Request

## Overview

Input format for the POST /eligibility/batch endpoint supporting both JSON array format with member_id/date_of_service pairs and standard EDI 270 transactions. Limited to 5000 records per batch with asynchronous processing and status polling.

## Details

JSON format contains a requests array with objects having member_id and date_of_service fields. EDI 270 format follows standard healthcare transaction format for eligibility inquiries. Responses include batch_id for tracking, results array with eligibility data, processed count, and errors count. EDI submissions receive EDI 271 response format. Batch processing is asynchronous requiring polling of GET /eligibility/batch/{batchId}/status endpoint. The 5000 record limit is enforced with BATCH_SIZE_EXCEEDED error for violations.
