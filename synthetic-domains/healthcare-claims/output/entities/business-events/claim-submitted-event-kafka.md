---
type: business-event
id: claim-submitted-event-kafka
name: Claim Submitted Event (Kafka)
description: |-
  Kafka event published when Claims Gateway receives and validates a new claim submission
status: active
tags:
- event-driven
- kafka
source_documents:
- integration-patterns-guide.txt
confidence: 0.95
published_by:
- claims-gateway
consumed_by:
- fraud-detection
carries:
- claim
---

# Claim Submitted Event (Kafka)

## Overview

Published by Claims Gateway on the clearview.claims.claim.submitted topic when a claim passes initial validation. Consumed by Fraud Detection for post-payment analysis and the reporting pipeline for analytics.

## Details

Topic: clearview.claims.claim.submitted with Avro schema registered in Confluent Schema Registry. Partitioned by member_id to ensure all claims for a member go to the same partition for ordering. 30-day retention policy. Key consumers are Fraud Detection (for post-payment pattern analysis) and the reporting pipeline.
