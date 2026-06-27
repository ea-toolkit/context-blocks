---
type: process
id: pre-auth-service-deployment
name: Pre-Auth Service Deployment
description: |-
  Dual deployment process for Pre-Auth Service covering clinical criteria and code changes
status: active
tags:
- deployment
- clinical-policy
source_documents:
- deployment-guide.txt
confidence: 0.9
applies_to:
- pre-auth-service
uses:
- google-cloud-storage
governed_by:
- pre-authorization-requirements
---

# Pre-Auth Service Deployment

## Overview

Pre-Auth Service deployment process that separates clinical criteria file updates (via GCS) from code deployments (via CI/CD) with auto-approval rate monitoring.

## Details

Separates clinical criteria updates from code deployments. Clinical criteria file updates: push to GCS bucket gs://clearview-preauth-config/criteria/. Code deployments: follow normal CI/CD pipeline. After criteria updates, auto-approval rate must be monitored (target: 60%). This separation allows clinical policy changes independent of code deployment cycles.
