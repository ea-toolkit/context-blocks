---
type: software-component
id: artifact-registry
name: Artifact Registry
description: Google Cloud container image registry for storing Docker images
status: active
tags:
- infrastructure
- google-cloud
source_documents:
- deployment-guide.txt
confidence: 0.9
used_by:
- github-actions-cicd-pipeline
deployed_on:
- google-cloud-platform
---

# Artifact Registry

## Overview

Google Cloud's Artifact Registry (gcr.io/clearview-prod/) stores all Docker images built by the CI/CD pipeline. Services require read access to this registry for deployment operations.

## Details

Container registry hosted at gcr.io/clearview-prod/ that stores Docker images built during the CI/CD pipeline's image build stage. All deployment personnel require read access to this registry as a prerequisite. The registry integrates with the Google Cloud Platform infrastructure and supports the rolling update and canary deployment strategies.
