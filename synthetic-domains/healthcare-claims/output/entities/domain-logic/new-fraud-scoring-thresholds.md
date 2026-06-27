---
type: domain-logic
id: new-fraud-scoring-thresholds
name: New Fraud Scoring Thresholds
description: Updated fraud model scoring thresholds with three-tier classification
  system
status: active
tags:
- fraud-detection
- thresholds
- classification
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.95
enforced_by:
- fraud-detection
supersedes:
- fraud-scoring-thresholds
---

# New Fraud Scoring Thresholds

## Overview

New fraud detection model uses three scoring tiers: >0.82 holds for SIU review, 0.65-0.82 proceeds with post-payment review flag, and <0.65 clears without restriction. Maintains same 0.82 SIU threshold as previous model.

## Details

Updated XGBoost fraud model implements refined scoring thresholds: scores above 0.82 trigger immediate hold for SIU investigation (same threshold as before), scores between 0.65-0.82 allow processing but flag for post-payment review, and scores below 0.65 clear without additional scrutiny. Target false positive rate is 8% with current validation showing 6.3%. New model demonstrates improved detection of unbundling schemes, successfully identifying providers splitting procedures like knee surgeries into separate fraudulent claims.
