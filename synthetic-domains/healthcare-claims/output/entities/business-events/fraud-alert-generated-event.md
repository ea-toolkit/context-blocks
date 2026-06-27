---
type: business-event
id: fraud-alert-generated-event
name: Fraud Alert Generated Event
description: |-
  Kafka event published when Fraud Detection generates a fraud alert requiring investigation
status: active
tags:
- event-driven
- kafka
- fraud
- compliance
source_documents:
- integration-patterns-guide.txt
confidence: 0.95
published_by:
- fraud-detection
consumed_by:
- payment-engine
---

# Fraud Alert Generated Event

## Overview

Published by Fraud Detection on clearview.fraud.alert.generated when suspicious patterns are detected. Consumed by SIU case management and Payment Engine for payment holds.

## Details

Topic: clearview.fraud.alert.generated with 365-day retention (compliance requirement), partitioned by provider_npi. Triggers SIU case creation and Payment Engine payment holds. Longest retention of any topic due to fraud investigation compliance requirements.
