---
type: external-party
id: valley-orthopedic-associates
name: Valley Orthopedic Associates
description: |-
  Provider group that submits non-standard CMS-1500 forms causing OCR processing issues
status: active
tags:
- problematic-provider
- non-standard-forms
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.95
integrated_via:
- ocr-pipeline
impacts:
- manual-data-entry-process
---

# Valley Orthopedic Associates

## Overview

Healthcare provider that uses modified CMS-1500 forms with non-standard field positions, causing consistently low OCR confidence scores. Their faxed claims require manual data entry intervention and have generated repeated complaints from the data entry team.

## Details

Uses non-standard CMS-1500 forms with modified field positions that don't align with the OCR pipeline's extraction templates. This causes the OCR system to produce consistently low confidence scores, forcing all their claims through manual data entry review rather than automatic processing.
