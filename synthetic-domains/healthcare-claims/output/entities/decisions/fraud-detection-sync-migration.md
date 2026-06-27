---
type: decision
id: fraud-detection-sync-migration
name: Fraud Detection Sync Migration
description: |-
  2025 decision to move fraud detection integration from async Kafka to synchronous HTTP for real-time claim blocking
status: active
tags:
- architecture-decision
- performance
- fraud
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
applies_to:
- fraud-detection
- claims-gateway
---

# Fraud Detection Sync Migration

## Overview

Decision made in 2025 to migrate fraud detection integration from asynchronous Kafka sidecar to synchronous HTTP calls, enabling real-time claim blocking at intake. The 120ms p99 latency made this architectural change feasible.

## Details

Originally implemented as async Kafka-based sidecar pattern, but moved to synchronous HTTP in 2025 to enable blocking claims at intake based on fraud scores. The 120ms p99 latency performance made real-time integration viable without impacting overall intake throughput. Decision documented in fraud detection meeting notes with specific performance rationale.
