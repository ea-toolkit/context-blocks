---
type: business-event
id: provider-status-changed-event
name: Provider Status Changed Event
description: |-
  Kafka event published when provider information or network status changes in Provider Directory
status: active
tags:
- event-driven
- kafka
- provider-data
source_documents:
- integration-patterns-guide.txt
confidence: 0.95
published_by:
- provider-directory
consumed_by:
- rules-engine
- member-portal
---

# Provider Status Changed Event

## Overview

Published by Provider Directory on clearview.providers.status.changed when provider data is updated. Consumed by Rules Engine for cache invalidation and Member Portal for provider search updates.

## Details

Topic: clearview.providers.status.changed with 7-day retention, partitioned by NPI. Triggers cache invalidation in Rules Engine to ensure current provider data during adjudication. Also updates Member Portal provider search to reflect current network status and provider information.
