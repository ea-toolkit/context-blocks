---
type: domain-logic
id: connection-pool-utilization-alerting
name: Connection Pool Utilization Alerting
description: |-
  Alert threshold rule triggering when database connection pool utilization exceeds 90% for 2 minutes
status: active
tags:
- alerting-rule
- proactive-monitoring
- performance
source_documents:
- 2024-claims-gateway-outage-postmortem.txt
confidence: 0.9
enforced_by:
- datadog
motivated_by:
- march-2024-claims-gateway-outage
monitors:
- hikaricp
---

# Connection Pool Utilization Alerting

## Overview

This alerting rule monitors database connection pool utilization and triggers alerts when usage exceeds 90% for a sustained 2-minute period, providing earlier detection of connection pool exhaustion than error-rate based alerts.

## Details

The connection pool utilization alerting rule was implemented as CLV-3903 after the March 2024 incident revealed that error-rate based alerts (50% error rate for 5 minutes) were too slow to detect connection pool exhaustion. The new rule monitors pool utilization in real-time and triggers alerts at >90% utilization sustained for 2 minutes, providing approximately 24 minutes earlier detection than the previous error-rate threshold. This proactive alerting allows operations teams to take preventive action before complete pool exhaustion occurs, such as scaling connection pools or throttling batch operations. The rule was implemented in Datadog and completed by March 19, 2024.
