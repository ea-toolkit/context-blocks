---
type: api
id: eligibility-api-v2
name: Eligibility API v2
description: Current version of Eligibility API following platform REST standards
status: active
tags:
- internal
- real-time
- batch-processing
source_documents:
- claims-coding-standards.txt
- eligibility-api-reference.txt
confidence: 0.95
exposed_by: eligibility-service
supersedes: eligibility-check-api
consumed_by:
- claims-gateway
- rules-engine
- pre-auth-service
- member-portal
contracts:
- member
- accumulator
- benefit-plan
---

# Eligibility API v2

## Overview

The current version of the Eligibility API, implementing the platform's standardized REST conventions for member eligibility verification and benefit checking operations.

## Details

Eligibility API v2 provides member eligibility verification, benefit balance queries, and accumulator tracking through standardized REST endpoints. Follows platform conventions including /eligibility resource naming, proper HTTP status codes, and structured JSON responses with correlation IDs. Likely handles the EDI 270/271 eligibility inquiry and response transactions in addition to JSON-based queries from internal systems and member portal.

## Open Questions

- Likely handles the EDI 270/271 eligibility inquiry and response transactions

## Additional Details
[from eligibility-api-reference.txt]

The API runs at https://api.clearviewhealth.internal/eligibility/v2 with OAuth 2.0 authentication and rate limits of 500 req/sec for real-time endpoints and 10 req/min for batch processing (max 5000 records per batch). Core endpoints include GET /eligibility/{memberId} for current eligibility, GET /eligibility/{memberId}/asof/{date} for point-in-time lookups supporting up to 2 years historical data, GET /eligibility/{memberId}/accumulators for benefit balance tracking with soft reservations, and POST /eligibility/batch for bulk processing. The API handles member status verification, plan assignment lookups, deductible and out-of-pocket maximum tracking, coordination of benefits data, and maintains soft reservations during concurrent claim adjudication to prevent over-application of benefits. Known issues include accumulator reservation cleanup requiring a 6-hour batch job (CLV-4521) and partial batch results under heavy load (CLV-4890).

## Conflicts

⚠️ Description differs: existing says 'Current version of Eligibility API following platform REST standards', [eligibility-api-reference.txt] says 'RESTful API providing member eligibility verification, benefit accumulator tracking, and point-in-time eligibility lookups'

