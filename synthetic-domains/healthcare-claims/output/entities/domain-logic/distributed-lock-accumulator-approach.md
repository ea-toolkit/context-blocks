---
type: domain-logic
id: distributed-lock-accumulator-approach
name: Distributed Lock Accumulator Approach
description: |-
  Alternative approach using Redis distributed locks with TTL to ensure accumulator update consistency
status: proposed
tags:
- architecture
- distributed-systems
- alternative-approach
source_documents:
- design-session-accumulator-rework.txt
confidence: 0.9
alternative_to:
- soft-reservation-logic
would_depend_on:
- software-component
---

# Distributed Lock Accumulator Approach

## Overview

A proposed alternative accumulator update mechanism using distributed locks acquired from Redis before applying accumulator changes. Each lock would be scoped to member + accumulator type with a 5-second TTL, providing strong consistency while handling crash scenarios through automatic lock expiration.

## Details

This approach would require acquiring a distributed lock from Redis before any accumulator update, scoped to the specific member and accumulator type combination. The lock would have a 5-second TTL that Redis would automatically expire if not properly released, handling crash scenarios. Benefits include strong consistency guarantees and simple conceptual model. However, downsides include adding latency to every adjudication (lock acquire + release operations), potential contention for members with many concurrent claims, and making Redis a critical dependency on the adjudication hot path. If Redis becomes unavailable, all claim adjudication would stop. The team also considered using PostgreSQL advisory locks instead to avoid the Redis dependency, though this would still add database round trips to each accumulator update.

## Open Questions

- Would require Redis for distributed locking (Redis not explicitly mentioned as existing component)
