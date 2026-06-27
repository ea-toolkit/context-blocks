---
type: data-model
id: ub-04-form
name: UB-04 Form
description: |-
  Standardized paper form structure for institutional healthcare claims with complex field layouts
status: active
tags:
- institutional-claims
- paper-form
- complex-layout
- needs-review
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.9
used_by:
- ocr-pipeline
---

# UB-04 Form

## Overview

Institutional claims form used by hospitals and facilities with more complex layout than CMS-1500. Contains fields for patient control numbers, type of bill, admission details, revenue codes, and procedure information. OCR pipeline achieves 91.8% field-level accuracy, lower than CMS-1500 due to layout complexity.

## Details

Form includes specific fields: Field 3a (patient control number), Field 4 (type of bill/TOB), Field 8 (patient name), Fields 12-13 (admission date/hour), Field 14 (priority/type of admission), Fields 38-41 (revenue codes), Field 42 (revenue description), Field 44 (HCPCS/rates), Field 67 (principal diagnosis), and Field 74 (principal procedure code). Multi-column fields with adjacent revenue codes and HCPCS codes create common extraction errors. The OCR template hasn't been updated since switching from ABBYY to Google Document AI in 2023.

## Open Questions

- Some field mappings might be suboptimal
