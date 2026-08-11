---
type: system
id: claims-gateway
name: Claims Gateway
description: Central ingress for all claim submissions
status: active
confidence: 0.92
related_systems: [adjudication-engine]
depends_on: [member-registry]
source_documents: [doc-001.md]
routing:
  logs: "Grafana/Loki k8s=claims-gateway.*"
  api: "https://api.example.com/claims-gateway"
---

# Claims Gateway

## Overview
Central ingress point that receives, validates, and routes all incoming health insurance claims.

## Details
Handles EDI 837 and direct API submissions. Validates member eligibility before routing to the adjudication engine.
