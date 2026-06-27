---
type: jargon-tech
id: consumer-groups
name: Consumer Groups
description: Kafka consumer group naming pattern following team.service.purpose convention
status: active
tags:
- kafka
- naming-convention
- operations
source_documents:
- integration-patterns-guide.txt
confidence: 0.9
---

# Consumer Groups

## Overview

Standardized naming pattern for Kafka consumer groups using the format <team>.<service>.<purpose>, such as claims-ops.payment-engine.adjudicated-claims. Enables clear ownership and purpose identification.

## Details

All Kafka consumers must follow the naming pattern <team>.<service>.<purpose> for consumer groups. Example: claims-ops.payment-engine.adjudicated-claims identifies the Claims Operations team's Payment Engine service consuming adjudicated claims. This pattern enables clear operational ownership and troubleshooting during incidents.
