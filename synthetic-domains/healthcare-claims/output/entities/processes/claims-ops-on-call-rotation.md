---
type: process
id: claims-ops-on-call-rotation
name: Claims Operations On-Call Rotation
description: |-
  Weekly on-call rotation schedule for Claims Operations team covering Monday 9AM to Monday 9AM ET
status: active
tags:
- operational
- incident-response
source_documents:
- monitoring-alerting-runbook.txt
confidence: 1.0
owned_by:
- claims-operations
managed_via:
- pagerduty
---

# Claims Operations On-Call Rotation

## Overview

The Claims Operations team maintains a weekly on-call rotation to provide 24/7 incident response for the Claims Platform. The rotation runs from Monday 9AM to Monday 9AM Eastern Time, with engineers responsible for responding to PagerDuty alerts and following established runbooks.

## Details

The on-call rotation is managed through PagerDuty with a dedicated schedule at https://pagerduty.clearviewhealth.internal/schedules/claims-ops. On-call engineers are expected to respond to SEV-1 alerts immediately, SEV-2 alerts within 30 minutes, and review SEV-3 alerts the next business day. The escalation path for unresolved incidents goes from the on-call engineer to Marcus Reeves (Claims Ops lead), then Priya Anand (Engineering lead), and finally to VP Engineering for SEV-1 incidents lasting more than 2 hours. Member Services operates a separate parallel rotation on the same schedule.
