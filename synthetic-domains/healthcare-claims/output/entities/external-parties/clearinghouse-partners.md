---
type: external-party
id: clearinghouse-partners
name: Clearinghouse Partners
description: |-
  Healthcare clearinghouses submitting EDI 270/271 eligibility verification transactions via batch processing
status: active
tags:
- healthcare-intermediary
- edi-processing
source_documents:
- eligibility-api-reference.txt
confidence: 0.9
consumes:
- eligibility-api-v2
integrated_via:
- edi-270-271
---

# Clearinghouse Partners

## Overview

External healthcare intermediaries that facilitate eligibility verification transactions between providers and Clearview Health Plans using standard EDI 270/271 format. These partners primarily use the batch eligibility endpoint for bulk member verification.

## Details

Clearinghouses serve as intermediaries in the healthcare transaction ecosystem, aggregating eligibility inquiries from multiple providers and submitting them as batches to health plans. They consume the POST /eligibility/batch endpoint using EDI 270 request format and receive EDI 271 responses, following standard healthcare transaction protocols. These partners handle the technical complexity of EDI formatting and transmission, allowing smaller providers to access eligibility verification without implementing EDI capabilities directly. The batch processing pattern fits their business model of aggregating multiple inquiries for efficient processing. Rate limiting of 10 req/min accommodates their batch-oriented workflow while preventing system overload.
