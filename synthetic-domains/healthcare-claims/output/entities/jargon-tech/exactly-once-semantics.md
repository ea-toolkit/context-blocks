---
type: jargon-tech
id: exactly-once-semantics
name: Exactly-Once Semantics
description: |-
  Kafka delivery guarantee ensuring messages are processed exactly once, used for financial transactions
status: active
tags:
- kafka
- financial
- delivery-guarantee
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
used_by:
- payment-engine
---

# Exactly-Once Semantics

## Overview

Kafka delivery guarantee configured for Payment Engine consumers to ensure financial transactions are processed exactly once. Other consumers use at-least-once with idempotent processing instead.

## Details

Critical for Payment Engine due to financial transaction requirements where duplicate processing could cause incorrect payments. More complex than at-least-once semantics but necessary for monetary operations. Other services use simpler at-least-once delivery with application-level idempotency to handle duplicates.
