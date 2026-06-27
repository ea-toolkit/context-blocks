---
type: software-component
id: vertex-ai
name: Vertex AI
description: Google Cloud machine learning platform used for fraud detection model
  training
status: active
tags:
- machine-learning
- model-training
- fraud-detection
- google-cloud
source_documents:
- architecture-overview.txt
confidence: 0.95
used_by:
- fraud-detection
---

# Vertex AI

## Overview

Vertex AI provides the machine learning infrastructure for training the fraud detection models used in the claims processing platform. It handles the monthly retraining pipeline for the ML models that score claims for fraud, waste, and abuse detection.

## Details

Google Cloud's managed ML platform used specifically for the fraud detection training pipeline. Handles monthly retraining of the scikit-learn and XGBoost models used for pre-payment claim scoring and post-payment pattern analysis. The models target a false positive rate below 8% and are retrained monthly to adapt to new fraud patterns. The trained models are then served via the FastAPI service in the Fraud Detection system.
