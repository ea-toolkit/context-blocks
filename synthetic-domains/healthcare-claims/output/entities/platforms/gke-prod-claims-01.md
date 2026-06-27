---
type: platform
id: gke-prod-claims-01
name: GKE Production Cluster (prod-claims-01)
description: Google Kubernetes Engine cluster hosting production claims processing
  workloads
status: active
tags:
- kubernetes
- production
- google-cloud
source_documents:
- architecture-overview.txt
confidence: 0.95
hosted_by:
- clearview-health-plans
used_by:
- claims-gateway
- rules-engine
- payment-engine
- fraud-detection
- pre-auth-service
- eligibility-service
- member-portal
- provider-directory
---

# GKE Production Cluster (prod-claims-01)

## Overview

The prod-claims-01 cluster is the primary production environment for all claims processing systems at Clearview Health Plans. It runs on Google Kubernetes Engine in the us-central1 region and hosts all eight core systems in the claims platform.

## Details

Deployed in us-central1 region on Google Cloud Platform. Hosts Claims Gateway, Rules Engine, Payment Engine, Fraud Detection, Pre-Auth Service, Eligibility Service, Member Portal, and Provider Directory. Paired with a separate nonprod-claims-01 cluster for development, staging, and QA environments. Uses Cloud SQL PostgreSQL 15 with HA failover for data persistence, Confluent Cloud Kafka for messaging, and HashiCorp Vault for secrets management.
