---
type: domain-logic
id: ocr-confidence-scoring-rules
name: OCR Confidence Scoring Rules
description: |-
  Business rules for routing claims based on OCR extraction confidence levels and field accuracy
status: active
tags:
- routing-logic
- quality-control
- confidence-thresholds
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.95
enforced_by:
- ocr-pipeline
triggers:
- manual-data-entry-process
---

# OCR Confidence Scoring Rules

## Overview

Algorithmic rules that determine claim routing based on confidence scores: >0.90 auto-submits to Claims Gateway, 0.70-0.90 routes to manual entry with pre-filled OCR results, <0.70 routes to blank manual entry forms. Claim-level confidence calculated as minimum of all required field confidences.

## Details

Multi-tier confidence scoring system where each extracted field receives confidence score from 0.0-1.0. Overall claim confidence is the minimum confidence of all required fields, creating a conservative approach to automatic processing. The three routing tiers balance processing efficiency with accuracy requirements: high confidence enables straight-through processing, medium confidence leverages OCR results while ensuring human review, and low confidence falls back to manual entry to avoid propagating unreliable data.
