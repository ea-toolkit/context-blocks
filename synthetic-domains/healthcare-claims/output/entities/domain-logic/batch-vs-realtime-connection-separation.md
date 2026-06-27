---
type: domain-logic
id: batch-vs-realtime-connection-separation
name: Batch vs Real-time Connection Separation
description: |-
  Architectural pattern requiring separate connection pools for batch and real-time processing
status: active
tags:
- architectural-pattern
- performance
- sla-protection
source_documents:
- 2024-claims-gateway-outage-postmortem.txt
confidence: 0.9
applies_to:
- claims-gateway
motivated_by:
- march-2024-claims-gateway-outage
enforced_via:
- clv-3901
---

# Batch vs Real-time Connection Separation

## Overview

This design principle requires that batch operations and real-time operations use separate database connection pools to prevent batch processing from starving real-time operations of database connections.

## Details

This architectural pattern addresses the fundamental conflict between batch processing (which can consume many connections for extended periods) and real-time processing (which requires guaranteed connection availability for low-latency responses). The March 2024 incident demonstrated the risks when this separation doesn't exist - a large batch of 14,000 institutional claims exhausted all 100 connections in the shared pool, preventing real-time professional claims from being processed and violating the 30-second SLA. The lack of this separation was identified as a known design issue that was deprioritized in Q4 2023 but became critical after the incident. Implementation was completed in sprint 38 (CLV-3901) with separate connection pools for batch and real-time processing.
