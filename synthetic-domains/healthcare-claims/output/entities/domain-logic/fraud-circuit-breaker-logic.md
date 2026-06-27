---
type: domain-logic
id: fraud-circuit-breaker-logic
name: Fraud Circuit Breaker Logic
description: |-
  Fraud Detection circuit breaker that defaults claims to 0.0 fraud score when service is degraded
status: active
tags:
- reliability
- business-logic
source_documents:
- monitoring-alerting-runbook.txt
confidence: 1.0
enforced_by:
- fraud-detection
enables:
- claims-processing-workflow
---

# Fraud Circuit Breaker Logic

## Overview

When Fraud Detection service experiences high latency or failures, a circuit breaker pattern defaults all claims to a fraud score of 0.0, allowing claims processing to continue uninterrupted. This design prioritizes pipeline availability over fraud detection accuracy.

## Details

The Fraud Detection service implements circuit breaker logic that activates when p99 latency exceeds 500ms for 10 minutes or the service becomes unavailable. When the circuit breaker trips, all claims receive a default fraud score of 0.0, effectively bypassing fraud scoring to prevent pipeline blockage. This design decision reflects the business priority that missing fraud flags is preferable to blocking legitimate claim payments. The circuit breaker behavior is explicitly documented as intentional design rather than a failure mode, indicating claims processing availability takes precedence over fraud detection completeness.
