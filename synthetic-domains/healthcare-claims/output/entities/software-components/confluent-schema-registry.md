---
type: software-component
id: confluent-schema-registry
name: Confluent Schema Registry
description: |-
  Schema registry managing Avro schemas for Kafka message evolution and compatibility
status: active
tags:
- infrastructure
- kafka
- schema-management
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
part_of:
- confluent-cloud-kafka
---

# Confluent Schema Registry

## Overview

Confluent Schema Registry manages schema evolution for all Kafka messages using Avro format with backward compatibility enforcement. All schemas must be registered before deploying producers.

## Details

Hosted at https://confluent.clearviewhealth.internal/schema-registry with CI pipeline validation for schema compatibility. Enforces backward compatible changes only to prevent breaking downstream consumers. All Kafka messages use Avro schemas registered here, enabling schema evolution without service coupling.
