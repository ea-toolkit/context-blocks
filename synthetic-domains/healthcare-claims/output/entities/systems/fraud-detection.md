---
type: system
id: fraud-detection
name: Fraud Detection
description: |-
  ML-based system that scores claims for fraud risk at intake and post-payment analysis
status: active
tags:
- seed-context-derived
- foundation
source_documents:
- seed-context
confidence: 0.9
owned_by:
- claims-operations
---

# Fraud Detection

## Overview

Fraud Detection uses machine learning models to score claims for fraud risk both at intake (pre-payment) and through post-payment pattern analysis. Claims scoring above 0.82 are held for SIU review.

## Details

This system employs machine learning models that evaluate claims for fraud indicators during the intake process before payment and analyze patterns after payment completion. Any claims receiving a fraud score above 0.82 are automatically held for Special Investigation Unit (SIU) review. The ML models are retrained on a monthly basis to maintain accuracy.
