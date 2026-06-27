---
type: jargon-business
id: member-id
name: Member ID
description: |-
  Unique identifier for health plan members used across all systems for member identification
status: active
tags:
- member-identification
- primary-key
- cross-system
source_documents:
- architecture-overview.txt
confidence: 0.95
used_in:
- duplicate-detection-process
- eligibility-check-api
---

# Member ID

## Overview

Member ID is the unique identifier used to identify health plan members across all systems in the claims processing platform. It's a key component in duplicate detection, eligibility verification, and claim processing workflows.

## Details

The primary key used to identify Clearview Health Plans members across all systems. Used as part of the composite key for duplicate detection (member ID + provider NPI + date of service + procedure codes). Essential for eligibility lookups, accumulator tracking, claim adjudication, and member portal access. Ensures that all member-related data and transactions can be properly attributed and tracked across the platform.
