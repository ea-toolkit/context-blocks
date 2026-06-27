---
type: process
id: parallel-fraud-scoring-validation
name: Parallel Fraud Scoring Validation
description: |-
  One-week validation process running old and new fraud models simultaneously for comparison
status: planned
tags:
- validation
- parallel-testing
- staging
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.95
owned_by:
- fraud-detection-team
involves:
- xgboost-fraud-model
---

# Parallel Fraud Scoring Validation

## Overview

Planned validation process to run both existing and new XGBoost fraud models in parallel for one week in staging environment to compare scoring performance before production deployment.

## Details

Validation process scheduled for end of July 2025 to deploy new XGBoost model to staging environment and run parallel scoring with both old and new models for one week. This approach allows comparison of scoring differences, performance characteristics, and model accuracy before committing to production deployment. Results will be reviewed in August 5 meeting to make go/no-go decision for production rollout.
