---
type: business-event
id: payment-completed-event
name: Payment Completed Event
description: Kafka event published when Payment Engine completes a payment transaction
status: active
tags:
- event-driven
- kafka
- financial
source_documents:
- integration-patterns-guide.txt
confidence: 0.95
published_by:
- payment-engine
consumed_by:
- member-portal
- provider-directory
---

# Payment Completed Event

## Overview

Published by Payment Engine on clearview.claims.payment.completed topic when a payment is processed. Consumed by Member Portal for EOB availability, Provider Directory for payment preferences, and reporting pipeline.

## Details

Topic: clearview.claims.payment.completed with Avro schema, partitioned by payee_id (TIN or member_id), 90-day retention policy. Triggers EOB availability in Member Portal, updates payment preferences in Provider Directory, and feeds reporting analytics. Longer retention than other events due to financial reconciliation requirements.
