---
type: business-event
id: hikaricp-pool-exhaustion-event
name: HikariCP Pool Exhaustion Event
description: |-
  Critical system event when database connection pool utilization exceeds 90% threshold
status: active
tags:
- infrastructure-failure
- database-connection
- cascading-failure
source_documents:
- monitoring-alerting-runbook.txt
- 2024-claims-gateway-outage-postmortem.txt
confidence: 1.0
governed_by: connection-pool-utilization-thresholds
published_by: claims-gateway
triggers:
- incident-escalation-process
- eligibility-service-timeout-cascade
triggered_by: institutional-claims-batch-processing
affects: claims-gateway
---

# HikariCP Pool Exhaustion Event

## Overview

Connection pool exhaustion events trigger immediate SEV-1 alerts when HikariCP utilization exceeds 90% for 2 minutes. These events indicate potential database connectivity issues that can cascade into system-wide failures if not addressed quickly.

## Details

HikariCP pool exhaustion events are detected when connection pool utilization exceeds 90% for a sustained 2-minute period, generating the CLAIMS-GW-POOL-EXHAUSTION alert. The event typically correlates with stuck database queries visible in pg_stat_activity or batch processing jobs holding connections longer than expected. Response protocol requires immediate investigation of active queries, with batch job termination taking priority over pod restarts to prevent connection state corruption. The current pool configuration allows 200 maximum connections via PgBouncer following the Q3 2024 architecture changes. These events were added to monitoring after the 2024-03-12 incident (CLV-3903) that highlighted connection pool management as a critical failure point.

## Additional Details
[from 2024-claims-gateway-outage-postmortem.txt]

The HikariCP pool exhaustion event occurs when all available database connections in the pool are in use, preventing new database operations from proceeding. During the March 2024 incident, this happened when 14,000 institutional claims were processed simultaneously, each acquiring a database connection for INSERT operations. The event has cascading effects - it causes the Claims Gateway to return 503 errors, stops all claims processing (both real-time and batch), and can trigger cascading failures in downstream services like the Eligibility Service when they timeout waiting for responses from the gateway.
