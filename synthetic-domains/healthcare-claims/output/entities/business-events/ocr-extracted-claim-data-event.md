---
type: business-event
id: ocr-extracted-claim-data-event
name: OCR Extracted Claim Data Event
description: |-
  Event containing structured claim data extracted from paper forms via OCR processing
status: active
tags:
- data-extraction
- confidence-scoring
- routing
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.9
published_by:
- ocr-pipeline
consumed_by:
- claims-gateway
triggers:
- manual-data-entry-process
---

# OCR Extracted Claim Data Event

## Overview

Business event generated when the OCR pipeline successfully extracts structured data from scanned paper claims. Contains the extracted claim fields along with confidence scores for routing decisions. High-confidence extractions are auto-submitted while lower confidence events trigger manual review workflows.

## Details

Event payload includes extracted claim data from either CMS-1500 or UB-04 forms with field-level confidence scores. Claim-level confidence is calculated as minimum of all required field confidences. Events with confidence >0.90 are automatically routed to Claims Gateway, 0.70-0.90 confidence events route to manual data entry queue with OCR results pre-filled, and <0.70 confidence events route to blank manual entry forms.
