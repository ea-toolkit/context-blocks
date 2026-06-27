---
type: api
id: claims-submission-api-v1
name: Claims Submission API v1
description: |-
  Deprecated REST API for claim submission built in 2020, scheduled for decommission June 2025
status: deprecated
tags:
- deprecated
- legacy-era
- needs-migration
source_documents:
- claims-gateway-api-v1-deprecated.txt
confidence: 0.95
exposed_by:
- claims-gateway
consumed_by:
- directsubmit
supersedes:
- claims-submission-api-v2
---

# Claims Submission API v1

## Overview

The original claims submission API built when Claims Gateway was first extracted from the monolith in 2020. Deprecated June 2024 due to critical limitations including unlimited batch sizes that caused the March 2024 outage, inconsistent error handling, and lack of fraud score support.

## Details

Base URL: https://api.clearviewhealth.internal/claims/v1. Major limitations include no batch size limit on /claims/batch endpoint (caused March 2024 outage), inconsistent error responses (JSON/plain text/HTTP status only), no correlation ID support, simplified status model (RECEIVED, PROCESSING, COMPLETED, REJECTED vs v2's full lifecycle), and no fraud score field support. Still used by DirectSubmit clearinghouse (~2% volume) and one direct-submitting provider group as of January 2025. Supports both JSON and EDI X12 content types. Authentication via OAuth 2.0 Bearer tokens. Decommission planned for June 1, 2025 pending final migrations.
