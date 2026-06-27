---
type: api
id: healthlogic-soap-endpoint
name: HealthLogic SOAP Endpoint
description: |-
  SOAP web service endpoint used by Rules Engine to communicate with HealthLogic Adjudicator
status: active
tags:
- integration
- legacy
source_documents:
- monitoring-alerting-runbook.txt
confidence: 1.0
consumed_by:
- rules-engine
exposed_by:
- healthlogic-adjudicator
---

# HealthLogic SOAP Endpoint

## Overview

The HealthLogic SOAP endpoint provides the integration interface between Clearview's Rules Engine and the HealthLogic Adjudicator system. Connectivity issues with this endpoint can cause complete claims adjudication failures and trigger SEV-1 alerts.

## Details

The HealthLogic SOAP endpoint serves as the critical integration point for claim adjudication processing, handling requests from the Rules Engine service. When this endpoint becomes unavailable or unresponsive, it triggers the RULES-ENGINE-DOWN alert since adjudication cannot proceed. The endpoint connectivity is monitored as part of Rules Engine health checks with failure thresholds set at 3 minutes of unavailability. Issues with this endpoint prevent auto-adjudication entirely, causing claims to accumulate in the gateway queue. The SOAP protocol choice is noted in ADR-2024-007 as a limitation of the HealthLogic system that influenced the decision to migrate to a replacement adjudication platform.
