---
type: platform
id: gke-nonprod-claims-01
name: GKE Non-Production Cluster (nonprod-claims-01)
description: |-
  Google Kubernetes Engine cluster hosting development, staging, and QA environments
status: active
tags:
- kubernetes
- non-production
- testing
- google-cloud
source_documents:
- architecture-overview.txt
confidence: 0.9
hosted_by:
- clearview-health-plans
---

# GKE Non-Production Cluster (nonprod-claims-01)

## Overview

The nonprod-claims-01 cluster provides development, staging, and QA environments for the claims processing platform. It mirrors the production cluster architecture but serves pre-production workloads and testing.

## Details

Deployed on Google Kubernetes Engine in the same us-central1 region as production. Hosts dev, staging, and QA instances of all claims processing systems. Provides isolated environments for development and testing before production deployment. Uses the same CI/CD pipeline (GitHub Actions → Artifact Registry → GKE) as production.
