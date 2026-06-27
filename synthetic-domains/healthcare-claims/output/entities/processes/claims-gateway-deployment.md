---
type: process
id: claims-gateway-deployment
name: Claims Gateway Deployment
description: Specific deployment procedure for Claims Gateway with connection pool
  monitoring
status: active
tags:
- deployment
- claims-processing
source_documents:
- deployment-guide.txt
confidence: 0.9
applies_to:
- claims-gateway
governed_by:
- payment-cycle-timing-constraints
monitors_via:
- datadog
---

# Claims Gateway Deployment

## Overview

Claims Gateway deployment process with specific timing windows, connection pool health monitoring, and batch processing considerations during rolling updates.

## Details

Deployment window: anytime outside payment cycle (02:00-06:00 UTC). Critical monitoring: connection pool health after deployment via Datadog dashboard. If connection pool alert fires post-deploy, immediate rollback required. Batch processing (837I) pauses during rolling update but resumes when new pods become healthy. This service has specific infrastructure concerns due to its role as the primary claims intake point.
