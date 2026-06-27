---
type: process
id: post-payment-fraud-analysis
name: Post-Payment Fraud Analysis
description: |-
  Analysis of flagged claims and provider patterns after payment to identify fraud schemes
status: active
tags:
- fraud-detection
- pattern-analysis
- post-payment
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
triggered_by:
- fraud-scoring-thresholds
executed_by:
- fraud-detection
may_trigger:
- siu-review-process
---

# Post-Payment Fraud Analysis

## Overview

Post-payment review process that analyzes claims flagged during pre-payment screening (score 0.65-0.82) and evaluates historical patterns across providers to identify potential fraud schemes requiring investigation.

## Details

After payment processing, claims that scored between 0.65-0.82 during pre-payment fraud screening are subjected to additional analysis. This post-payment review examines historical patterns across all of the provider's claims to identify suspicious trends that may not be apparent in individual claim reviews. The analysis looks for patterns like unusual billing frequencies, inappropriate procedure/diagnosis combinations, geographic anomalies, or other indicators that suggest systematic fraud rather than isolated incidents. When suspicious patterns are confirmed, SIU is alerted to consider opening a formal fraud investigation. This two-stage approach (pre-payment scoring plus post-payment pattern analysis) provides comprehensive fraud detection while allowing most legitimate claims to process without delay.

## Open Questions

- may_trigger
