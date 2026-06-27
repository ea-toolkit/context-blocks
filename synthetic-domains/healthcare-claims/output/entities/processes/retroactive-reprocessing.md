---
type: process
id: retroactive-reprocessing
name: Retroactive Reprocessing
description: |-
  Automated process that re-adjudicates claims when member enrollment changes are backdated
status: active
tags:
- claims-processing
- retroactive
- enrollment-changes
source_documents:
- architecture-overview.txt
confidence: 0.9
triggered_by:
- enrollment-change-event
executed_by:
- eligibility-service
---

# Retroactive Reprocessing

## Overview

The retroactive reprocessing process automatically triggers when member enrollment changes occur within the past 60 days. It identifies and re-adjudicates any claims that were processed during the affected time period to ensure accurate payment based on the updated enrollment information.

## Details

Triggered automatically by retroactive enrollment changes up to 60 days back. The Eligibility Service detects when member coverage is backdated and identifies all claims processed during the affected window. These claims are then sent through the adjudication pipeline again to ensure they are processed correctly based on the member's actual coverage at the time of service. This catches situations where a member's coverage was added, changed, or cancelled with a retroactive effective date, ensuring claims are paid correctly.
