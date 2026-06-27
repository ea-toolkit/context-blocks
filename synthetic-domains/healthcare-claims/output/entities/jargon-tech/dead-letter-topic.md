---
type: jargon-tech
id: dead-letter-topic
name: Dead Letter Topic (DLT)
description: |-
  Kafka topic pattern for handling failed message processing using .dlt suffix convention
status: active
tags:
- kafka
- error-handling
- pattern
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
---

# Dead Letter Topic (DLT)

## Overview

Standard pattern where every Kafka consumer must have a dead letter topic configured following the naming convention <original-topic>.dlt. Messages that fail processing are sent to DLT for investigation and potential replay.

## Details

Required pattern for all Kafka consumers to handle message processing failures. DLT topics follow the naming pattern of appending .dlt to the original topic name. Enables investigation of failed messages and potential replay after fixing underlying issues. Part of the overall fault tolerance strategy in the event-driven architecture.
