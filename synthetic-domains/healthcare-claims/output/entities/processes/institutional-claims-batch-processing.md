---
type: process
id: institutional-claims-batch-processing
name: Institutional Claims Batch Processing
description: Batch processing of 837I institutional claims in 4-hour windows
status: active
tags:
- batch-processing
- complex-claims
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
uses:
- edi-837-institutional
executed_by:
- claims-gateway
---

# Institutional Claims Batch Processing

## Overview

Processing flow for institutional claims submitted via EDI 837I format (UB-04 equivalent). These claims are processed in 4-hour batch windows rather than real-time due to their complexity and lower volume.

## Details

Institutional claims use the EDI 837I format and are more complex than professional claims, typically involving hospital stays, facility services, and other inpatient care. Due to this complexity and lower volume compared to professional claims, they are processed in batches every 4 hours rather than real-time. This batching allows for more thorough processing of the complex billing structures typical of institutional claims.
