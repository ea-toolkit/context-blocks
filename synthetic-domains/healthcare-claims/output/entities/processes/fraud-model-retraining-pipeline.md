---
type: process
id: fraud-model-retraining-pipeline
name: Fraud Model Retraining Pipeline
description: |-
  Monthly automated retraining of fraud detection models using historical claims and investigation outcomes
status: active
tags:
- machine-learning
- automation
- continuous-learning
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.9
owned_by:
- fraud-detection-team
deployed_on:
- vertex-ai
uses:
- google-cloud-storage
produces:
- xgboost-fraud-model
---

# Fraud Model Retraining Pipeline

## Overview

Automated monthly process that retrains fraud detection XGBoost models on Vertex AI using the last 12 months of claims data combined with SIU investigation outcomes. Trained model binaries are deployed via GCS bucket for fraud service pickup.

## Details

Monthly retraining pipeline runs on Vertex AI using training dataset comprising 12 months of historical claims data plus corresponding SIU investigation outcomes to create ground truth labels. Upon completion, model binary is pushed to a GCS bucket where the Fraud Detection service automatically picks up the new model on restart. This continuous learning approach ensures fraud detection stays current with evolving fraud patterns and investigation feedback.
