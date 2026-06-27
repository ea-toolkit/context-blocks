---
type: domain-logic
id: fraud-scoring-thresholds
name: Fraud Scoring Thresholds
description: |-
  Three-tier fraud scoring system with thresholds at 0.65 and 0.82 for different processing paths
status: active
tags:
- fraud-prevention
- ml-scoring
- risk-management
source_documents:
- claims-processing-workflow.txt
confidence: 0.95
enforced_by:
- fraud-detection
triggers:
- siu-review-process
---

# Fraud Scoring Thresholds

## Overview

Risk-based claim routing logic that uses ML fraud scores to determine processing paths. Claims scoring above 0.82 are held for SIU review, scores 0.65-0.82 are flagged for post-payment analysis, and scores below 0.65 proceed normally.

## Details

The fraud detection system returns scores between 0 and 1, with three distinct processing paths: CLEAR (<0.65) allows normal processing with no additional scrutiny. FLAG (0.65-0.82) allows normal adjudication but tags the claim for post-payment pattern analysis to identify broader fraud schemes. HOLD (>0.82) immediately stops processing and routes to the Special Investigations Unit (SIU) for manual review - these claims cannot proceed to adjudication until SIU clearance. The model evaluates billing patterns, member history, procedure/diagnosis combinations, geographic anomalies, and other fraud indicators, with monthly retraining to adapt to new fraud patterns.
