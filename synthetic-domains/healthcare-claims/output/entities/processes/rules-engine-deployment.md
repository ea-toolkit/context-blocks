---
type: process
id: rules-engine-deployment
name: Rules Engine Deployment
description: |-
  Mandatory canary deployment process for Rules Engine with auto-adjudication rate monitoring
status: active
tags:
- deployment
- high-risk
source_documents:
- deployment-guide.txt
confidence: 0.9
applies_to:
- rules-engine
governed_by:
- auto-adjudication-rate-targets
integrates_with:
- healthlogic-adjudicator
---

# Rules Engine Deployment

## Overview

High-risk deployment process for Rules Engine that requires canary deployment strategy and careful monitoring of auto-adjudication rates to prevent claims processing disruption.

## Details

ALWAYS requires canary deployment strategy. After deployment, auto-adjudication rate must be monitored for 30 minutes - if rate drops >5%, immediate rollback required. Rule changes and code changes should be deployed separately when possible. HealthLogic Adjudicator configuration is deployed separately via GCS bucket update, not through the standard CI pipeline. This reflects the critical nature of the Rules Engine in claims processing.
