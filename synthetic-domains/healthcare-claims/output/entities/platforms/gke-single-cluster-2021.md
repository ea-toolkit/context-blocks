---
type: platform
id: gke-single-cluster-2021
name: GKE Single Cluster (2021)
description: |-
  Original single GKE cluster in us-central1 that hosted all services before prod/nonprod separation
status: deprecated
tags:
- legacy-era
- infrastructure
- single-cluster
- replaced
source_documents:
- original-architecture-2021.txt
confidence: 0.9
superseded_by:
- gke-prod-claims-01
- gke-nonprod-claims-01
---

# GKE Single Cluster (2021)

## Overview

The 2021 architecture used a single GKE cluster in us-central1 to host all services without separation between production and non-production environments. This was later upgraded to separate clusters for better isolation.

## Details

The initial post-migration infrastructure used a single Google Kubernetes Engine cluster located in us-central1 region. This cluster hosted all microservices without any environment separation - both production and non-production workloads ran on the same cluster. This setup was acknowledged as inadequate for the current volume and was later upgraded to separate production and non-production clusters for better isolation, security, and capacity management. The single-cluster approach was a migration simplification that was always intended to be temporary.
