---
type: platform
id: claims-ops-namespace
name: Claims-Ops Namespace
description: Kubernetes namespace hosting core claims processing services
status: active
tags:
- kubernetes
- claims-processing
source_documents:
- deployment-guide.txt
confidence: 0.9
hosts:
- claims-gateway
- rules-engine
- payment-engine
- fraud-detection
- pre-auth-service
---

# Claims-Ops Namespace

## Overview

Kubernetes namespace containing the primary claims processing services: Claims Gateway, Rules Engine, Payment Engine, Fraud Detection, and Pre-Auth Service.

## Details

Kubernetes namespace that groups the core claims processing workflow services. Contains Claims Gateway (intake), Rules Engine (adjudication), Payment Engine (disbursement), Fraud Detection (screening), and Pre-Auth Service (authorization). This logical grouping reflects the primary claims processing pipeline.
