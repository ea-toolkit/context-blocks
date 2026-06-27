---
type: software-component
id: manual-data-entry-tool
name: Manual Data Entry Tool
description: |-
  Legacy web application from ClaimsPro era used for manual claim data entry and OCR correction
status: active
tags:
- legacy
- technical-debt
- claimspro-era
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.9
used_by:
- manual-data-entry-process
part_of:
- claimspro
communicates_with:
- claims-gateway
---

# Manual Data Entry Tool

## Overview

Web-based tool that allows data entry team to review scanned claim images and correct OCR extractions. Last surviving piece of ClaimsPro system, connects directly to Claims Gateway database to insert claims. Described as ugly but functional by the team.

## Details

Legacy application that bypasses the Claims Gateway API and connects directly to the database for claim insertion - a known technical debt issue that should route through the API instead but hasn't been prioritized. Used for both correcting low-confidence OCR extractions and entering claims from blank forms when OCR confidence is too low. The interface allows side-by-side viewing of scanned images and extracted data for correction.

## Open Questions

- This should go through the API instead but nobody has prioritized the change
