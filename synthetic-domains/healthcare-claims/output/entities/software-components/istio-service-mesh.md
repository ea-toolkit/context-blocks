---
type: software-component
id: istio-service-mesh
name: Istio Service Mesh
description: |-
  Internal service mesh handling all synchronous inter-service communication with circuit breakers and timeouts
status: active
tags:
- infrastructure
- internal-networking
source_documents:
- integration-patterns-guide.txt
confidence: 0.95
used_by:
- claims-gateway
- rules-engine
- member-portal
---

# Istio Service Mesh

## Overview

Istio service mesh routes all HTTP/REST calls between claims platform services, providing service discovery, circuit breaking, and observability. All sync calls must go through the mesh rather than direct pod-to-pod calls.

## Details

The service mesh enforces standard communication patterns across the platform with DNS-based service discovery (e.g., eligibility-service.member-svc.svc.cluster.local), 5-second default timeouts configurable per route, Resilience4j circuit breakers (3 consecutive failures → open for 30 seconds), and correlation ID header propagation (X-Correlation-ID). All services must log correlation IDs for cross-service tracing during incidents.
