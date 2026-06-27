---
type: process
id: member-portal-deployment
name: Member Portal Deployment
description: |-
  Multi-component deployment process for Member Portal covering frontend, BFF, and feature flags
status: active
tags:
- deployment
- frontend
- mobile
source_documents:
- deployment-guide.txt
confidence: 0.85
applies_to:
- member-portal
uses:
- launchdarkly
- cdn
---

# Member Portal Deployment

## Overview

Member Portal deployment process that handles independent frontend and backend deployments with feature flag integration and mobile testing requirements.

## Details

Frontend deployments are independent of backend (React SPA served from CDN). BFF layer deployments follow standard pipeline. Uses LaunchDarkly feature flags for gradual rollout of new features. Requires testing on mobile viewports before deployment due to high mobile usage. This architecture allows independent deployment of frontend and backend components while supporting progressive feature rollouts.
