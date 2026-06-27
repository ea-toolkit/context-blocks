---
type: process
id: ocr-pipeline-processing
name: OCR Pipeline Processing
description: Paper claims processing through OCR with 94% accuracy and manual fallback
status: active
tags:
- manual-processing
- low-volume
- accuracy-limited
source_documents:
- claims-processing-workflow.txt
confidence: 0.85
part_of:
- claims-processing-workflow
executed_by:
- claims-gateway
---

# OCR Pipeline Processing

## Overview

Processing pipeline for paper claims that uses OCR technology to extract claim data. Achieves 94% accuracy with failed OCR cases routed to manual data entry queue.

## Details

Paper claims represent ~5% of total volume and go through an OCR (Optical Character Recognition) pipeline to convert physical documents into digital claim data. The OCR system achieves approximately 94% accuracy, meaning 6% of paper claims cannot be parsed automatically and must be routed to a manual data entry queue for human processing. This is the slowest of the three submission channels due to the physical handling and potential manual intervention required.
