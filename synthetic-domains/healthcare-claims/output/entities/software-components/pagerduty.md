---
type: software-component
id: pagerduty
name: PagerDuty
description: Incident management and on-call scheduling platform
status: active
tags:
- incident-management
- on-call
- alerting
source_documents:
- claims-ops-contacts-and-escalation.txt
confidence: 0.95
used_by:
- claims-operations
supports:
- incident-escalation-process
---

# PagerDuty

## Overview

PagerDuty manages the on-call schedule for Claims Operations and handles incident alerting. It requires acknowledgment within specific timeframes based on incident severity.

## Details

PagerDuty is the incident management platform used by Claims Operations for managing on-call schedules and incident alerting. The schedule is accessible at https://pagerduty.clearviewhealth.internal/schedules/claims-ops. It integrates with the incident escalation process, requiring acknowledgment within 15 minutes for SEV-1 incidents and 30 minutes for SEV-2 incidents. PagerDuty likely connects to monitoring systems to automatically alert on-call engineers when issues are detected.
