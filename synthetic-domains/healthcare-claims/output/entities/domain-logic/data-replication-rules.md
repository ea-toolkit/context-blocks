---
type: domain-logic
id: data-replication-rules
name: Data Replication Rules
description: |-
  Governance rules for implementing data replication and denormalization across services
status: active
tags:
- data-governance
- architecture-rules
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
---

# Data Replication Rules

## Overview

Established rules governing when and how to implement data replication between services: source service remains source of truth, replicated data must have defined freshness SLA, cache invalidation events required, and replication must be documented.

## Details

Four-rule framework for data replication: 1) Source service always remains source of truth, 2) Replicated data must have defined freshness SLA (how stale can it be?), 3) Cache invalidation events must exist (Kafka topic or webhook), 4) Document the replication in integration guide to prevent debugging nightmares. Applied to current implementations like Fraud Detection's provider profile denormalization and Member Portal's eligibility caching.
