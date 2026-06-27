---
type: process
id: manual-data-entry-process
name: Manual Data Entry Process
description: |-
  Manual review and correction process for low-confidence OCR extractions before Claims Gateway submission
status: active
tags:
- manual-process
- quality-control
- legacy-tooling
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.95
triggered_by:
- ocr-extracted-claim-data-event
owned_by:
- claims-operations
involves:
- maria-chen
executed_by:
- manual-data-entry-tool
---

# Manual Data Entry Process

## Overview

Workflow where data entry team reviews scanned images alongside OCR output to correct errors and fill missing fields. Triggered for OCR extractions with confidence scores between 0.70-0.90 (pre-filled) or below 0.70 (blank forms). Completed claims are submitted to Claims Gateway via JSON API.

## Details

Data entry team uses legacy web application from ClaimsPro era to review and correct OCR extractions. For confidence 0.70-0.90, OCR results are pre-filled for correction. For confidence <0.70, blank forms are provided as OCR is deemed too unreliable. Team supervisor is Maria Chen (contract team lead). The process represents a quality gate ensuring accurate claim data reaches Claims Gateway despite poor OCR confidence.
