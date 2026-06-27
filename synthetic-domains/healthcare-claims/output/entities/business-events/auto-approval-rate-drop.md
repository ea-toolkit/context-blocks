---
type: business-event
id: auto-approval-rate-drop
name: Auto-Approval Rate Drop
description: Alert when Pre-Auth Service auto-approval rate falls below 50% target
  threshold
status: active
tags:
- monitoring
- alert
- business-metrics
source_documents:
- pre-auth-runbook.txt
confidence: 0.95
triggers:
- auto-approval-rate-investigation
---

# Auto-Approval Rate Drop

## Overview

Monitoring alert that fires when the Pre-Auth Service's auto-approval percentage drops below the 50% threshold, with a target rate of 60%. This typically indicates changes in clinical criteria rules or system issues affecting benefit plan data.

## Details

The PRE-AUTH-RATE alert monitors the percentage of authorization requests that are automatically approved without manual clinical review. Alert example: '[PRE-AUTH-RATE] Auto-approval rate dropped below 50% (current: 43%). Target: 60%'. Rate drops usually result from updated clinical criteria files loaded from GCS or incorrect benefit plan data from the Eligibility Service. The alert triggers investigation of recent criteria file updates, comparison between versions, and analysis by service category to identify specific areas experiencing approval rate degradation.
