---
type: business-event
id: provider-profile-sync-event
name: Provider Profile Sync Event
description: |-
  Nightly Kafka event flow updating fraud detection's denormalized provider profiles
status: active
tags:
- kafka
- nightly-sync
- denormalized
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.8
published_by:
- provider-directory
consumed_by:
- fraud-detection
updates:
- denormalized-provider-profiles
---

# Provider Profile Sync Event

## Overview

Kafka-based event flow that synchronizes provider profile changes from Provider Directory to Fraud Detection's local denormalized database on a nightly basis.

## Details

Nightly Kafka consumer process within Fraud Detection service that consumes provider change events from Provider Directory to maintain local denormalized provider profiles. This async synchronization approach ensures fraud scoring has access to current provider history without requiring real-time cross-service calls that would impact 120ms scoring latency requirements.

## Open Questions

- Provider Directory publishes provider change events - this is implied but not explicitly confirmed in the document
