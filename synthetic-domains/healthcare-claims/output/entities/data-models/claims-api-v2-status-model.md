---
type: data-model
id: claims-api-v2-status-model
name: Claims API v2 Status Model
description: |-
  Comprehensive claim status enumeration providing full lifecycle visibility in Claims Submission API v2
status: active
tags:
- current
- enhanced-visibility
source_documents:
- claims-gateway-api-v1-deprecated.txt
confidence: 0.95
used_by:
- claims-submission-api-v2
supersedes:
- claims-api-v1-status-model
---

# Claims API v2 Status Model

## Overview

Enhanced claim status model in Claims Submission API v2 that provides granular visibility into claim processing stages: RECEIVED, VALIDATED, ELIGIBLE, ADJUDICATED, PAID, DENIED, PENDED, REJECTED. Addresses the visibility gaps from v1's simplified model.

## Details

Eight-state model providing full claim lifecycle visibility: RECEIVED (initial intake), VALIDATED (format and structure verified), ELIGIBLE (member eligibility confirmed), ADJUDICATED (rules engine processing complete), PAID (payment issued), DENIED (claim rejected with reason), PENDED (held for manual review), REJECTED (validation failure). This granular model allows API consumers to understand exactly where claims are in the processing pipeline, unlike v1's generic PROCESSING state. Includes additional fields like fraud_score, disposition, denial_reason, pend_reason, and correlation_id for enhanced troubleshooting and monitoring.
