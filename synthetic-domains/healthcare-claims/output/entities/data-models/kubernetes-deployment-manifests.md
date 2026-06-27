---
type: data-model
id: kubernetes-deployment-manifests
name: Kubernetes Deployment Manifests
description: Service deployment configurations stored in clearview-infra repository
status: active
tags:
- kubernetes
- configuration
source_documents:
- deployment-guide.txt
confidence: 0.9
stored_in:
- clearview-infra-repo
uses:
- kubernetes-resource-defaults
---

# Kubernetes Deployment Manifests

## Overview

Kubernetes resource definitions for all claims platform services, stored centrally in the clearview-infra repository and organized by service namespace.

## Details

All service manifests stored in clearview-infra repo. Key resources per service: Deployment (pods, replicas, resource limits), Service (ClusterIP for internal, LoadBalancer for external), ConfigMap (environment-specific configuration), HPA (scales on CPU and custom metrics), PDB (minimum 2 pods during updates). Namespace layout: claims-ops (Claims Gateway, Rules Engine, Payment Engine, Fraud Detection, Pre-Auth Service), member-svc (Eligibility Service, Member Portal BFF), provider-net (Provider Directory).
