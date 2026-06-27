---
type: domain-logic
id: api-rate-limiting-rules
name: API Rate Limiting Rules
description: |-
  Rate limiting policies enforcing 500 req/sec for real-time endpoints and 10 req/min for batch processing
status: active
tags:
- performance
- system-protection
source_documents:
- eligibility-api-reference.txt
confidence: 0.95
enforced_by:
- eligibility-api-v2
---

# API Rate Limiting Rules

## Overview

Differential rate limiting strategy protecting the Eligibility API from overload while accommodating different usage patterns. Real-time endpoints support high-frequency individual lookups while batch endpoints have stricter limits due to higher processing costs.

## Details

Real-time endpoints (GET /eligibility/{memberId}, /asof/{date}, /accumulators) allow 500 requests per second per client, supporting the high-volume needs of Claims Gateway and Rules Engine during peak processing. The batch endpoint (POST /eligibility/batch) is limited to 10 requests per minute with maximum 5000 records per batch, reflecting the higher resource cost of bulk processing. Rate limit violations return RATE_LIMIT_EXCEEDED error with backoff retry recommendations. This tiered approach balances system protection with operational requirements, recognizing that batch processing trades frequency for volume efficiency.
