---
type: data-model
id: denormalized-provider-profiles
name: Denormalized Provider Profiles
description: |-
  Local fraud detection database containing provider history for fast scoring queries
status: active
tags:
- denormalized
- performance
- local-cache
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.85
owned_by:
- fraud-detection
sourced_from:
- provider-directory
used_by:
- xgboost-fraud-model
---

# Denormalized Provider Profiles

## Overview

Denormalized provider profile data maintained locally within Fraud Detection service for real-time scoring performance. Updated nightly from Provider Directory via Kafka consumer to avoid synchronous cross-service calls during scoring.

## Details

Local database within Fraud Detection containing denormalized provider profile information required for fraud scoring. Eliminates need for synchronous calls to Provider Directory during the hot path scoring process, maintaining required 120ms p99 latency. Updated nightly through Kafka consumer that processes provider change events from Provider Directory. This approach trades data freshness for scoring performance, ensuring fraud detection doesn't introduce additional service dependencies during critical path processing.

## Open Questions

- Model queries local provider profiles for scoring - this relationship is implied but not explicitly confirmed
