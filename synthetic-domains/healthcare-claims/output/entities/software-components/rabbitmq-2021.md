---
type: software-component
id: rabbitmq-2021
name: RabbitMQ (2021)
description: |-
  Message broker used in original 2021 architecture, later replaced by Kafka in Q2 2022
status: deprecated
tags:
- legacy-era
- messaging
- replaced
- reliability-issues
source_documents:
- original-architecture-2021.txt
confidence: 0.95
superseded_by:
- confluent-cloud-kafka
deployed_on:
- gke-single-cluster-2021
---

# RabbitMQ (2021)

## Overview

RabbitMQ was the original message broker used for asynchronous communication between services in the 2021 architecture. It was replaced by Kafka in Q2 2022 due to message loss issues under heavy load.

## Details

RabbitMQ served as the async messaging backbone for the initial microservices architecture. However, it had critical reliability issues under heavy load where messages would be dropped if the queue depth exceeded memory limits, causing claims to disappear without a trace. This was identified as one of the major architectural problems that needed to be addressed. The move to Kafka in Q2 2022 solved this issue by providing persistent, replicated message storage. The message loss problem was particularly problematic for claims processing where every message represents financial transactions that cannot be lost.
