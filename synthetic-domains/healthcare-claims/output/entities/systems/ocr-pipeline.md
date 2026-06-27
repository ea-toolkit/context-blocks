---
type: system
id: ocr-pipeline
name: OCR Pipeline
description: |-
  System that processes paper claims from fax/mail, extracting structured data via OCR and routing to Claims Gateway
status: active
tags:
- processing
- legacy
- declining-volume
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.95
communicates_with:
- claims-gateway
owned_by:
- claims-operations
used_by:
- nadia-volkov
produces:
- ocr-extracted-claim-data-event
---

# OCR Pipeline

## Overview

The OCR Pipeline handles approximately 5% of total claim volume (~10,000 claims/month) from paper submissions. It processes scanned TIFF/PDF images through five stages: preprocessing, OCR extraction, validation, manual review, and archival. Volume is declining as providers move to electronic submission.

## Details

Multi-stage processing system built on Python 3.9 running in GKE claims-ops namespace. Uses Google Document AI for OCR extraction with separate templates for CMS-1500 and UB-04 forms. Implements confidence-based routing: >0.90 confidence auto-submits to Claims Gateway, 0.70-0.90 routes to manual data entry with pre-filled OCR results, <0.70 routes to blank manual entry form. Achieves 94.2% field-level accuracy for CMS-1500 and 91.8% for UB-04 forms. Monthly processing cost is $600-800 via Google Document AI at ~$0.02 per page.
