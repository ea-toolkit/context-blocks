---
type: domain-logic
id: fraud-scoring-algorithm
name: Fraud Scoring Algorithm
description: |-
  ML-based algorithm that scores claims for fraud, waste, and abuse risk using multiple models
status: active
tags:
- fraud-detection
- machine-learning
- scoring
source_documents:
- architecture-overview.txt
confidence: 0.9
enforced_by:
- fraud-detection
---

# Fraud Scoring Algorithm

## Overview

The fraud scoring algorithm uses machine learning models to evaluate claims for potential fraud, waste, and abuse. It operates in two modes: pre-payment scoring at intake and post-payment pattern analysis for investigation.

## Details

Implemented using scikit-learn and XGBoost models trained monthly on Vertex AI. Pre-payment mode scores individual claims at intake - scores >0.82 trigger automatic holds for SIU review, scores 0.65-0.82 proceed with tagging for post-payment review, scores <0.65 process normally. Post-payment mode analyzes historical patterns across adjudicated claims to detect aberrant billing, upcoding, unbundling, and phantom billing. Target false positive rate is below 8%. Models are retrained monthly to adapt to new fraud patterns.
