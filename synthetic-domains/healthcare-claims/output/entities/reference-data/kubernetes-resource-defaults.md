---
type: reference-data
id: kubernetes-resource-defaults
name: Kubernetes Resource Defaults
description: Standard resource allocation settings for claims platform Kubernetes
  deployments
status: active
tags:
- kubernetes
- resource-management
source_documents:
- deployment-guide.txt
confidence: 0.9
used_by:
- kubernetes-deployment-manifests
---

# Kubernetes Resource Defaults

## Overview

Standardized CPU and memory resource requests and limits that serve as defaults for all claims platform services, with override capability in deployment manifests.

## Details

Default resource allocation: CPU request 500m, CPU limit 2000m, Memory request 512Mi, Memory limit 2Gi. These are baseline defaults that individual services can override in their deployment manifests. All services also include Horizontal Pod Autoscaler (HPA) for scaling based on CPU and custom metrics, plus Pod Disruption Budget (PDB) ensuring minimum 2 pods available during updates.
