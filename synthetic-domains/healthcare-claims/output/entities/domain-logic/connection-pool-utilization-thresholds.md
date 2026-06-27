---
type: domain-logic
id: connection-pool-utilization-thresholds
name: Connection Pool Utilization Thresholds
description: |-
  HikariCP connection pool monitoring with 90% utilization threshold triggering immediate alerts
status: active
tags:
- infrastructure
- database
- legacy-era
source_documents:
- monitoring-alerting-runbook.txt
confidence: 1.0
applies_to:
- claims-gateway
derives_from:
- 2024-connection-pool-incident
---

# Connection Pool Utilization Thresholds

## Overview

Claims Gateway monitors HikariCP connection pool utilization with alerts triggered when utilization exceeds 90% for 2 minutes. This threshold was established after the 2024-03-12 connection pool incident (CLV-3903) to prevent similar outages.

## Details

The connection pool monitoring specifically tracks HikariCP pools with a critical alert (CLAIMS-GW-POOL-EXHAUSTION) at 90% utilization for 2 minutes. The current configuration supports maximum 200 connections via PgBouncer following the Q3 2024 migration. When triggered, the runbook requires immediately checking pg_stat_activity for stuck queries, with batch processing jobs being the first suspect. The response protocol prioritizes killing batch jobs before restarting pods to prevent cascading failures. This monitoring was added specifically after CLV-3903 incident analysis.
