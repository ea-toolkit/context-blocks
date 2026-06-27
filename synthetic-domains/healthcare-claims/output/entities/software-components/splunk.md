---
type: software-component
id: splunk
name: Splunk
description: |-
  Log aggregation and analysis platform for centralized logging across the claims processing systems
status: active
tags:
- infrastructure
- logging
source_documents:
- architecture-overview.txt
- monitoring-alerting-runbook.txt
confidence: 1.0
used_by:
- claims-operations
- claims-gateway
- rules-engine
- payment-engine
---

# Splunk

## Overview

Splunk provides centralized log aggregation and analysis for the claims processing platform. It collects logs from all systems and infrastructure components, enabling troubleshooting, audit trails, and operational analysis.

## Details

Serves as the centralized logging platform for all claims processing systems. Aggregates logs from the GKE clusters, applications, databases, and other infrastructure components. Enables the engineering teams to troubleshoot issues, perform root cause analysis, and maintain audit trails for compliance. Works alongside Datadog to provide comprehensive observability for the platform.

## Additional Details
[from monitoring-alerting-runbook.txt]

Splunk indexes logs from all Claims Platform services with specific indexes including 'claims-gateway', 'rules-engine', 'claims-batch-processing', and 'claims-*' for general claim-related logs. The platform supports structured logging with fields like claim_id that enable tracing individual claims across services over extended periods (up to 7 days shown in examples). Common operational queries include error analysis (level=ERROR), batch job monitoring, and specific claim investigation. All services implement structured logging to ensure consistent field naming and searchability across the platform.
