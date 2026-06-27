---
type: software-component
id: google-document-ai
name: Google Document AI
description: |-
  Google Cloud OCR service used for extracting structured data from scanned claim forms
status: active
tags:
- cloud-service
- third-party
- ocr-engine
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.95
used_by:
- ocr-pipeline
hosted_by:
- google-cloud-platform
---

# Google Document AI

## Overview

API-based OCR engine that processes TIFF and PDF images of paper claims with per-page pricing model. Configured with separate extraction templates for CMS-1500 and UB-04 forms. Achieves 94.2% field-level accuracy for professional claims and 91.8% for institutional claims.

## Details

Cloud-based document processing service that handles image preprocessing, form type detection, and field extraction. Costs approximately $0.02 per page processed, resulting in monthly costs of $600-800. The service extracts specific fields from standardized claim forms including member IDs, provider NPIs, diagnosis codes, procedure codes, and billing information. Common extraction errors include handwritten fields, fax artifacts, and formatting inconsistencies.
