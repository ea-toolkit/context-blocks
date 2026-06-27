---
type: process
id: fraud-model-retraining-batch
name: Fraud Model Retraining Batch
description: |-
  Monthly batch job retraining fraud detection ML models using historical claims and investigation outcomes
status: active
tags:
- batch-processing
- ml
- scheduled
- fraud
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
executed_by:
- vertex-ai
feeds:
- fraud-detection
---

# Fraud Model Retraining Batch

## Overview

Monthly scheduled job on the 1st at 06:00 UTC that retrains fraud detection models using the last 12 months of claims data plus SIU investigation outcomes. Runs on Vertex AI and deploys new models to GCS.

## Details

Uses Vertex AI platform with input from 12 months of claims history combined with SIU investigation outcomes. Outputs new model binary pushed to Google Cloud Storage, which Fraud Detection service picks up on restart. Custom Python scripts handle the retraining workflow rather than Spring Batch framework used elsewhere.
