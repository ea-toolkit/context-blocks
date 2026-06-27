---
type: process
id: environment-promotion-pipeline
name: Environment Promotion Pipeline
description: 'Three-stage environment promotion process: dev → staging → production'
status: active
tags:
- deployment
- infrastructure
source_documents:
- deployment-guide.txt
confidence: 0.95
uses:
- gke-nonprod-claims-01
- gke-prod-claims-01
governed_by:
- hipaa-compliance-requirements
integrates_with:
- healthlogic-systems
---

# Environment Promotion Pipeline

## Overview

The structured environment promotion flow that ensures changes are tested through progressively production-like environments before reaching live systems. Each environment has distinct characteristics and data isolation.

## Details

Three-stage promotion: dev (nonprod-claims-01 dev namespace, deploys on feature branch pushes, shared database instance with separate logical databases, uses mock external services), staging (nonprod-claims-01 staging namespace, automatic deploy on main merge, separate database instances, connected to HealthLogic sandbox, EDI testing via test clearinghouse with synthetic data), production (prod-claims-01, manual promotion, HA database with failover replica, real external services, real member/provider data under HIPAA). Critical rule: never connect dev or staging to production databases - this has caused incidents twice before.
