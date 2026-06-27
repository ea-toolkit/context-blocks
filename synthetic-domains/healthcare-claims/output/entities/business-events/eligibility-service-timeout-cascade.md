---
type: business-event
id: eligibility-service-timeout-cascade
name: Eligibility Service Timeout Cascade
description: |-
  Cascading failure event where Eligibility Service's connection pool fills up due to timeouts from Claims Gateway
status: active
tags:
- cascading-failure
- timeout
- infrastructure-failure
source_documents:
- 2024-claims-gateway-outage-postmortem.txt
confidence: 0.85
triggered_by:
- hikaricp-pool-exhaustion-event
affects:
- eligibility-service
- member-portal
---

# Eligibility Service Timeout Cascade

## Overview

When Claims Gateway fails and stops responding, the Eligibility Service experiences timeout errors on synchronous calls from the gateway. These timeouts cause the Eligibility Service's own connection pool to fill up, creating a cascading failure.

## Details

This cascading failure occurs because the Eligibility Service receives synchronous calls from the Claims Gateway during claim intake processing. When the Claims Gateway is failing (such as during connection pool exhaustion), these calls timeout but still consume connection pool resources in the Eligibility Service while waiting. The accumulation of these hanging connections eventually fills up the Eligibility Service's connection pool, causing it to also become unavailable. This demonstrates the lack of circuit breaker patterns between the services, which was identified as a preventive action item (CLV-3904) but was later deprioritized.
