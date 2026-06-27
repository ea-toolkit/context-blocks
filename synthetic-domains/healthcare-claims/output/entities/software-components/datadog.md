---
type: software-component
id: datadog
name: Datadog
description: |-
  Monitoring and alerting platform for metrics, performance monitoring, and system observability
status: active
tags:
- infrastructure
- monitoring
source_documents:
- architecture-overview.txt
- monitoring-alerting-runbook.txt
confidence: 1.0
used_by:
- claims-operations
- member-services
- provider-network
- claims-gateway
- rules-engine
- payment-engine
communicates_with: pagerduty
---

# Datadog

## Overview

Datadog provides comprehensive monitoring and alerting for the claims processing platform. It collects metrics, tracks performance, and generates alerts for operational issues across all systems in the platform.

## Details

Used for metrics collection and alerting across the entire claims platform infrastructure. Monitors the health and performance of all eight primary systems, the GKE clusters, databases, and other infrastructure components. Provides dashboards for operational visibility and alert management for the Claims Operations, Member Services, and Provider Network teams.

## Additional Details
[from monitoring-alerting-runbook.txt]

Datadog monitors all Claims Platform services with specific dashboards for Claims Gateway, Rules Engine, Payment Engine, Fraud Detection, and Eligibility Service. Each dashboard tracks key metrics like request rate, error rate, latency percentiles (p50/p95/p99), and service-specific metrics like auto-adjudication rates and connection pool utilization. The platform generates alerts based on conditions like error rate thresholds (>50% for 5 minutes triggers SEV-1) and performance degradation (p95 latency >3s for Member Portal). Datadog APM provides distributed tracing capabilities that allow tracking claims across multiple services using structured claim_id logging.
