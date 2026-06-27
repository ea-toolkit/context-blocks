---
type: process
id: incident-escalation-process
name: Incident Escalation Process
description: Structured escalation workflow for handling system incidents by severity
  level
status: active
tags:
- incident-response
- escalation
- war-room
source_documents:
- claims-ops-contacts-and-escalation.txt
confidence: 0.95
owned_by:
- claims-operations
involves:
- marcus-reeves
- priya-anand
---

# Incident Escalation Process

## Overview

The incident escalation process defines how system incidents are handled based on severity levels (SEV-1, SEV-2, SEV-3) with specific response times and escalation paths. SEV-1 incidents require immediate war room activation.

## Details

The incident escalation process is structured around three severity levels: SEV-1 (full outage/data loss) requires on-call engineer response → Marcus → Priya with 15 minute acknowledgment and 30 minute war room activation; SEV-2 (degraded/partial) requires on-call engineer response with 30 minute acknowledgment; SEV-3 (minor/informational) is handled next business day without paging. For SEV-1 incidents, the on-call engineer must: 1) Acknowledge in PagerDuty within 15 minutes, 2) Open a Slack thread in #claims-incidents, 3) Start a war room if not resolved within 30 minutes using the permanent Zoom link, 4) Page Marcus and Priya if they haven't joined. This process ensures rapid response to critical issues affecting claims processing.
