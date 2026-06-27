---
type: api
id: claims-status-history-endpoint
name: Claims Status History Endpoint
description: |-
  New API endpoint to expose claims processing timeline data for member portal redesign
status: planned
tags:
- member-portal
- claims-processing
- november-launch
source_documents:
- meeting-notes-member-portal-redesign.txt
confidence: 0.9
exposed_by:
- claims-gateway
consumed_by:
- provider-portal-bff
contracts:
- claims-status-history-model
---

# Claims Status History Endpoint

## Overview

GET /claims/{id}/history endpoint that returns each status transition with timestamps for the claims timeline view. The endpoint will expose existing audit data from the claims_status_history table through Claims Gateway API.

## Details

The endpoint will be added to Claims Gateway as part of sprint 46 to support the Member Portal redesign timeline feature. It exposes the claims_status_history table data which already tracks status transitions for auditing purposes. The API will return timestamped status transitions including states like Received → Validated → Eligibility Verified → Adjudicated → Payment Scheduled → Paid. This enables the member portal to show a visual timeline of claim processing progress.
