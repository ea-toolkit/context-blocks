---
type: software-component
id: resilience4j
name: Resilience4j
description: |-
  Circuit breaker library implementing fault tolerance for service-to-service calls
status: active
tags:
- infrastructure
- fault-tolerance
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
part_of:
- istio-service-mesh
---

# Resilience4j

## Overview

Resilience4j provides circuit breaker functionality in the Istio service mesh, opening circuits after 3 consecutive failures for 30-second periods. This prevents cascading failures across the claims platform microservices architecture.

## Details

Configured with a 3-failure threshold before opening the circuit, 30-second recovery window, and integration with the Istio service mesh for automatic fault tolerance. This replaced earlier approaches that led to cascading failures in the platform.
