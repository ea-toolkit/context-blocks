---
type: data-model
id: claims-api-v1-status-model
name: Claims API v1 Status Model
description: Simplified claim status enumeration used in deprecated Claims Submission
  API v1
status: deprecated
tags:
- deprecated
- legacy-era
- insufficient-granularity
source_documents:
- claims-gateway-api-v1-deprecated.txt
confidence: 0.95
used_by:
- claims-submission-api-v1
superseded_by:
- claims-api-v2-status-model
---

# Claims API v1 Status Model

## Overview

Limited set of claim status values (RECEIVED, PROCESSING, COMPLETED, REJECTED) used by Claims Submission API v1, significantly simpler than the full lifecycle status model implemented in v2. The simplified model masked important workflow states from API consumers.

## Details

Four-state model: RECEIVED (claim accepted), PROCESSING (covers everything between intake and final disposition), COMPLETED (claim processed, could be paid or denied), REJECTED (validation failure or system rejection). This simplification was problematic because PROCESSING covered multiple distinct workflow states (validation, eligibility check, adjudication, pending review) that consumers needed visibility into. COMPLETED status required additional fields to determine if claim was actually paid or denied. v2 expanded this to full lifecycle visibility: RECEIVED, VALIDATED, ELIGIBLE, ADJUDICATED, PAID, DENIED, PENDED, REJECTED.
