---
type: domain-logic
id: fraud-detection-circuit-breaker-logic
name: Fraud Detection Circuit Breaker Logic
description: |-
  Circuit breaker pattern for fraud service calls with 5-second timeout and failure thresholds
status: active
tags:
- resilience
- fault-tolerance
- real-time
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.95
enforced_by:
- claims-gateway
applies_to:
- fraud-detection
---

# Fraud Detection Circuit Breaker Logic

## Overview

Circuit breaker implementation to handle fraud detection service failures during synchronous scoring calls. Designed to prevent Claims Gateway performance degradation when fraud service is unavailable.

## Details

Circuit breaker configured with 5-second timeout for fraud detection calls and opens after 3 consecutive failures, remaining open for 30 seconds. When circuit is open or fraud service is unreachable, system falls back to score 0.0 (clear), logs warning, and continues claim processing. This ensures fraud service failures don't block the entire claims intake pipeline. Better to miss a fraud flag than hold up processing according to team decision.
