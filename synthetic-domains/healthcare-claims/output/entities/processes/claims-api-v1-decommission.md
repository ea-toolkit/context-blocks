---
type: process
id: claims-api-v1-decommission
name: Claims API v1 Decommission
description: Planned process to retire Claims Submission API v1 by June 2025
status: active
tags:
- decommission
- migration
- in-progress
source_documents:
- claims-gateway-api-v1-deprecated.txt
confidence: 0.9
applies_to:
- claims-submission-api-v1
owned_by:
- priya-anand
involves:
- james-whitfield
depends_on:
- directsubmit
---

# Claims API v1 Decommission

## Overview

Multi-step decommission process to retire the deprecated Claims Submission API v1, including consumer migration, compatibility shimming, and final code removal. Target date of June 1, 2025 may slip depending on DirectSubmit migration progress.

## Details

Six-step decommission plan: 1) Deprecation notice sent (completed June 2024), 2) Sunset header added to responses (completed), 3) Chase remaining consumers to migrate (in progress), 4) Add request logging for undiscovered consumers (pending), 5) Route v1 traffic to v2 with compatibility shim (pending), 6) Decommission v1 code path (pending). Process managed by Priya Anand for technical aspects and James Whitfield for provider/clearinghouse outreach. Success depends on DirectSubmit completing their migration and identifying the unnamed provider group still using v1.
