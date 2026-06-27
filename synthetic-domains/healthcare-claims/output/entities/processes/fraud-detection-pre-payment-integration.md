---
type: process
id: fraud-detection-pre-payment-integration
name: Fraud Detection Pre-Payment Integration
description: |-
  Migration from asynchronous to synchronous fraud scoring in Claims Gateway intake flow
status: active
tags:
- integration
- real-time
- pre-payment
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.95
involves:
- claims-gateway
- fraud-detection
replaces:
- fraud-detection-sidecar-model
owned_by:
- claims-operations
---

# Fraud Detection Pre-Payment Integration

## Overview

Process to integrate real-time fraud detection scoring directly into the Claims Gateway routing logic, replacing the current asynchronous sidecar model. The integration aims to enable pre-payment blocking of high-fraud-score claims before they reach the Rules Engine.

## Details

Currently fraud scoring runs as a sidecar process where Claims Gateway sends a Kafka message for async scoring, but by the time scores return, claims have already entered the Rules Engine making pre-payment blocking impossible. The new integration implements synchronous calls from Claims Gateway to Fraud Detection service during intake, with 120ms p99 latency target and circuit breaker protection. Includes fallback logic (score 0.0 and continue) when fraud service is unavailable, and extends Datadog dashboard with pre-payment scoring metrics. Implementation scheduled for sprint 42 with parallel scoring validation planned.
