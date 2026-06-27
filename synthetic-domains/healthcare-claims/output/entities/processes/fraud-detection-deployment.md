---
type: process
id: fraud-detection-deployment
name: Fraud Detection Deployment
description: |-
  Dual deployment process for Fraud Detection covering both model updates and code changes
status: active
tags:
- deployment
- machine-learning
source_documents:
- deployment-guide.txt
confidence: 0.9
applies_to:
- fraud-detection
uses:
- google-cloud-storage
governed_by:
- fraud-scoring-thresholds
---

# Fraud Detection Deployment

## Overview

Specialized deployment process for Fraud Detection that separates model updates (via GCS) from code updates (via CI/CD) with distinct monitoring requirements.

## Details

Separates model updates from code updates. Model updates: push new model binary to GCS bucket, restart pods (they pick up new model on startup). Code updates: follow normal CI/CD pipeline. After model update, fraud score distribution must be monitored for 24 hours - significant shifts may indicate model data issues. This dual deployment approach reflects the ML-driven nature of the fraud detection service.
