---
type: data-model
id: xgboost-fraud-model
name: XGBoost Fraud Model
description: Machine learning model for real-time fraud scoring with 120ms p99 latency
status: active
tags:
- machine-learning
- real-time
- fraud-detection
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.9
used_by:
- fraud-detection
produced_by:
- fraud-model-retraining-pipeline
depends_on:
- denormalized-provider-profiles
---

# XGBoost Fraud Model

## Overview

Updated XGBoost-based fraud detection model optimized for real-time scoring during claims intake. Achieves 120ms p99 latency with improved unbundling detection compared to previous model.

## Details

New XGBoost fraud detection model designed for synchronous scoring calls from Claims Gateway with 120ms p99 latency requirement. Model demonstrates superior performance in detecting unbundling fraud schemes, successfully identifying providers who split legitimate procedures (like knee surgeries) into separate fraudulent claims. Uses denormalized provider profile data from local database rather than real-time Provider Directory queries to maintain scoring performance. Model binary deployment handled through GCS bucket with automatic pickup by Fraud Detection service on restart.
