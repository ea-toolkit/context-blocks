---
type: jargon-business
id: manual-data-entry-queue
name: Manual Data Entry Queue
description: |-
  Work queue for paper claims that failed OCR processing and require human data entry
status: active
tags:
- manual-processing
- data-entry
- paper-claims
source_documents:
- claims-processing-workflow.txt
confidence: 0.85
fed_by:
- ocr-pipeline-processing
part_of:
- claims-processing-workflow
---

# Manual Data Entry Queue

## Overview

Work queue containing the ~6% of paper claims that OCR cannot accurately parse, requiring manual transcription by data entry personnel to convert to digital claim format.

## Details

Paper claims that fail OCR processing (approximately 6% of the 5% paper volume) are routed to the manual data entry queue where trained personnel manually transcribe the claim information into the digital system. This queue represents the slowest processing path but ensures that even poorly-legible or complex paper claims can still be processed. The queue requires specialized staff who can accurately interpret handwritten forms, medical coding, and provider documentation to create valid digital claim records.
