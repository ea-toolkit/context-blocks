---
type: domain-logic
id: auto-adjudication-rate-targets
name: Auto-Adjudication Rate Targets
description: Target 85% auto-adjudication rate with alerts when dropping below 75%
  threshold
status: active
tags:
- performance
- business-logic
source_documents:
- monitoring-alerting-runbook.txt
confidence: 1.0
applies_to:
- rules-engine
impacted_by:
- healthlogic-adjudicator
---

# Auto-Adjudication Rate Targets

## Overview

Claims Platform maintains an 85% target auto-adjudication rate with monitoring alerts when the rolling 24-hour rate drops below 75%. Current performance runs approximately 81%, with rate drops often attributed to incomplete rules migration from HealthLogic.

## Details

The system monitors auto-adjudication rates continuously with a 24-hour rolling window, targeting 85% automatic processing of claims without manual intervention. When rates drop below 75%, a SEV-2 alert (AUTO-ADJUDICATION-RATE-DROP) triggers investigation. Current performance averages 81%, indicating room for improvement toward the target. Rate degradation commonly correlates with rules engine migration issues where business rules from HealthLogic haven't been fully ported to the new system. The runbook includes a SQL query to analyze pend reasons: 'SELECT pend_reason, count(*) FROM claims WHERE status='PENDED' AND created_at > now() - interval '24 hours' GROUP BY 1 ORDER BY 2 DESC' to identify specific bottlenecks in automated processing.
