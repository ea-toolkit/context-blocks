---
type: data-model
id: claims-status-history-model
name: Claims Status History Model
description: Data model for claims status transitions with timestamps used in timeline
  view
status: active
tags:
- claims-processing
- member-portal
- audit-data
source_documents:
- meeting-notes-member-portal-redesign.txt
confidence: 0.8
used_by:
- claims-status-history-endpoint
sourced_from:
- claims-gateway
---

# Claims Status History Model

## Overview

Data structure representing the sequence of status changes a claim goes through during processing, with timestamps for each transition. This model enables the member portal to display a visual timeline of claim progress.

## Details

The model contains status transition data including states like Received, Validated, Eligibility Verified, Adjudicated, Payment Scheduled, and Paid, each with associated timestamps. The data is sourced from the claims_status_history table which is maintained for auditing purposes. The model supports the new claims timeline feature in the Member Portal redesign, allowing members to see exactly where their claim is in the processing pipeline.
