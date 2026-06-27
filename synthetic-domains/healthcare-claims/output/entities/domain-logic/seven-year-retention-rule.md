---
type: domain-logic
id: seven-year-retention-rule
name: Seven Year Retention Rule
description: |-
  Regulatory compliance requirement for retaining original scanned claim images for seven years
status: active
tags:
- regulatory-compliance
- data-retention
- state-regulation
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.9
applies_to:
- claims-archive-process
violated_by:
- clv-5102
---

# Seven Year Retention Rule

## Overview

State regulatory mandate requiring Clearview to retain original scanned claim images for seven years from processing date. Currently not properly enforced due to GCS lifecycle policy misconfiguration (CLV-5102) that deletes images after five years.

## Details

Legal compliance requirement that governs the claims archive process, ensuring claim documentation is available for audits, investigations, and regulatory review. The rule creates a compliance obligation that extends beyond typical business data retention needs and impacts storage infrastructure configuration and costs.
