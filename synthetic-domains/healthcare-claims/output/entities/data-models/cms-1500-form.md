---
type: data-model
id: cms-1500-form
name: CMS-1500 Form
description: |-
  Standardized paper form structure for professional healthcare claims with specific field mappings
status: active
tags:
- professional-claims
- paper-form
- standardized
source_documents:
- ocr-pipeline-extracted-spec.txt
confidence: 0.95
used_by:
- ocr-pipeline
contains:
- npi
- tin
---

# CMS-1500 Form

## Overview

Professional claims form with standardized boxes for insurance information, patient demographics, diagnosis codes, service lines, and provider details. Used by healthcare professionals to submit claims for services rendered. OCR pipeline achieves 94.2% field-level accuracy when processing these forms.

## Details

Form contains specific numbered boxes including: Box 1 (insurance type), Box 1a (member ID), Box 2 (patient name), Box 3 (birth date/sex), Box 11 (group number), Box 17 (referring provider NPI), Box 21 (ICD-10 diagnosis codes), Box 24a-j (service lines with dates, places, procedure codes, modifiers, charges, units), Box 25 (provider TIN), Box 31 (physician signature), and Box 33 (billing provider NPI). The OCR pipeline uses specialized templates to extract data from these standardized field positions.
