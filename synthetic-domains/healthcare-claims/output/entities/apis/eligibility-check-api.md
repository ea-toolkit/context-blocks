---
type: api
id: eligibility-check-api
name: Eligibility Check API
description: |-
  REST API exposed by Eligibility Service for member eligibility verification and accumulator queries
status: active
tags:
- rest-api
- eligibility
- member-services
source_documents:
- architecture-overview.txt
confidence: 0.95
exposed_by:
- eligibility-service
consumed_by:
- rules-engine
- claims-gateway
---

# Eligibility Check API

## Overview

The Eligibility Check API provides real-time and point-in-time eligibility verification for members. It supports current eligibility lookups, historical as-of-date queries, benefit accumulator tracking, and batch EDI 270 processing.

## Details

Endpoints include: GET /eligibility/{memberId} for current eligibility, GET /eligibility/{memberId}/asof/{date} for point-in-time lookups (critical for adjudication), GET /eligibility/{memberId}/accumulators for benefit balances, and POST /eligibility/batch for batch EDI 270 verification. The API handles soft reservations for accumulators to prevent over-application during concurrent claim processing.
