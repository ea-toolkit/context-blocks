---
type: api
id: claims-submission-api
name: Claims Submission API
description: REST API exposed by Claims Gateway for claim submission and status retrieval
status: active
tags:
- rest-api
- claims-processing
- external-interface
source_documents:
- architecture-overview.txt
confidence: 0.95
exposed_by:
- claims-gateway
consumed_by:
- member-portal
---

# Claims Submission API

## Overview

The Claims Submission API is the primary interface for submitting claims to the Claims Gateway. It accepts both single claims and batch submissions in EDI or JSON formats, and provides endpoints for checking claim status and retrieving EOBs.

## Details

Endpoints include: POST /claims for single claim submission (EDI or JSON), POST /claims/batch for batch submissions (EDI 837 files), GET /claims/{id} for status and details, and GET /claims/{id}/eob for EOB retrieval. The API operates with a 30-second SLA for real-time EDI 837 Professional submissions and 4-hour batch processing windows for EDI 837 Institutional claims. JSON submissions are primarily used by the Member Portal for out-of-network claim submissions.
