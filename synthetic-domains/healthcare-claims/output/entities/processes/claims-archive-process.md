---
type: process
id: claims-archive-process
name: Claims Archive Process
description: |-
  Process for storing and retaining original scanned claim images with regulatory compliance requirements
status: active
tags:
- archival
- compliance
- long-term-storage
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.9
part_of:
- ocr-pipeline
owned_by:
- leo-chen
governed_by:
- seven-year-retention-rule
---

# Claims Archive Process

## Overview

Archival workflow that stores original TIFF/PDF scanned images in GCS bucket gs://clearview-claims-scans/ with 7-year retention requirement per state regulation. Links archived images to claim records via claim_id for future reference and compliance audits.

## Details

Final stage of OCR pipeline that stores original scanned images after processing completion. Images are stored in Google Cloud Storage bucket with claim_id linkage for traceability. Currently has a compliance issue (CLV-5102) where GCS lifecycle policy is set to 5 years instead of the required 7-year retention period per state regulation.
