---
type: process
id: fraud-detection-sidecar-model
name: Fraud Detection Sidecar Model
description: |-
  Current asynchronous fraud scoring approach where Claims Gateway sends Kafka messages for scoring
status: deprecated
tags:
- async
- legacy
- being-replaced
source_documents:
- meeting-notes-fraud-detection-integration.txt
confidence: 0.9
involves:
- claims-gateway
- fraud-detection
superseded_by:
- fraud-detection-pre-payment-integration
---

# Fraud Detection Sidecar Model

## Overview

The existing fraud detection architecture where Claims Gateway sends claims data via Kafka message for asynchronous fraud scoring. By the time fraud scores are returned, claims have already entered the Rules Engine, making pre-payment blocking impossible.

## Details

Current implementation runs fraud scoring as a sidecar process that receives claim data through Kafka messaging from Claims Gateway. The async nature means fraud scores arrive after claims have already been routed to Rules Engine for adjudication, eliminating the ability to block fraudulent claims before payment processing. This model is being replaced by synchronous integration to enable pre-payment fraud detection.
