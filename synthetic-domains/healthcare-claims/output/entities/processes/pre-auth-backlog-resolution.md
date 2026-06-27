---
type: process
id: pre-auth-backlog-resolution
name: Pre-Auth Backlog Resolution Process
description: Operational process for resolving Pre-Auth Service processing backlogs
status: active
tags:
- operational
- troubleshooting
- runbook
source_documents:
- pre-auth-runbook.txt
confidence: 0.9
triggered_by:
- auth-request-processing-backlog
involves:
- priya-anand
- marcus-reeves
---

# Pre-Auth Backlog Resolution Process

## Overview

A structured troubleshooting workflow triggered by auth request processing backlog alerts. The process includes checking pod health, examining logs, investigating common failure modes, and escalation paths.

## Details

Multi-step resolution process: 1) Check Pre-Auth Service pod status in claims-ops namespace using kubectl, 2) Examine crashloop logs if pods are failing, 3) Investigate common root causes including Eligibility Service downtime, database connection pool exhaustion, or clinical criteria file loading failures from GCS. For database issues, includes specific queries to check active connections, identify idle connections, and terminate long-running idle connections after 30 minutes. Escalates to Priya Anand or Marcus Reeves if standard resolution steps don't resolve the issue.
