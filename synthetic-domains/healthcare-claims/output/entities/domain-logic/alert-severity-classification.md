---
type: domain-logic
id: alert-severity-classification
name: Alert Severity Classification
description: |-
  Three-tier severity classification system for Claims Platform alerts with defined response times
status: active
tags:
- operational
- incident-response
source_documents:
- monitoring-alerting-runbook.txt
confidence: 1.0
enforced_by:
- datadog
- pagerduty
---

# Alert Severity Classification

## Overview

The Claims Platform uses a three-tier alert severity system: SEV-1 for critical alerts requiring immediate paging, SEV-2 for warning alerts requiring acknowledgment within 30 minutes, and SEV-3 for informational alerts reviewed next business day. Each severity level has specific conditions and response expectations.

## Details

SEV-1 (Critical) alerts include Claims Gateway error rate >50% for 5 minutes, connection pool exhaustion >90% for 2 minutes, Rules Engine down for 3 minutes, Payment Engine batch failures, and Eligibility Service down for 2 minutes. These trigger immediate paging. SEV-2 (Warning) alerts include processing backlogs >5000 claims older than 30 minutes, Fraud Detection p99 latency >500ms for 10 minutes, Pre-Auth backlogs >200 requests older than 4 hours, auto-adjudication rate drops below 75%, and Member Portal p95 latency >3s for 10 minutes. SEV-3 (Informational) alerts include EDI batch partial failures >5% parse errors, excessive accumulator reservation cleanup >100 expired reservations, and provider credential expiration notifications >20 providers in 30 days.
