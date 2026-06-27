---
type: business-event
id: auth-request-processing-backlog
name: Auth Request Processing Backlog
description: Alert triggered when pending authorization requests exceed threshold
  of 4 hours
status: active
tags:
- monitoring
- alert
- operational
source_documents:
- pre-auth-runbook.txt
confidence: 0.95
triggers:
- pre-auth-backlog-resolution
---

# Auth Request Processing Backlog

## Overview

A monitoring alert that fires when the Pre-Auth Service has more than a threshold number of authorization requests that haven't been processed within 4 hours. This indicates system performance degradation or service unavailability.

## Details

The PRE-AUTH-BACKLOG alert monitors the age of pending authorization requests in the system. When more than a configured threshold (example shows 342 requests) remain unprocessed after 4 hours, this alert fires to operations teams. Common causes include Pre-Auth Service pod failures, Eligibility Service unavailability, database connection pool exhaustion, or clinical criteria loading failures. The alert example shows '[PRE-AUTH-BACKLOG] Pending auth requests exceed threshold: 342 requests older than 4 hours'.
