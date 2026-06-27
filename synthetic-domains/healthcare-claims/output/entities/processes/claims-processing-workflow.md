---
type: process
id: claims-processing-workflow
name: Claims Processing Workflow
description: |-
  Complete end-to-end workflow for processing health insurance claims from submission to payment
status: active
tags:
- core-business-process
- end-to-end
source_documents:
- claims-processing-workflow.txt
confidence: 0.95
executed_by:
- claims-gateway
involves:
- claims-operations
produces:
- eob
---

# Claims Processing Workflow

## Overview

The comprehensive 9-step workflow that processes claims from initial submission through validation, fraud screening, adjudication, and payment. Handles three submission channels (EDI 837, REST API, paper/OCR) with an 85% auto-adjudication rate target.

## Details

The workflow consists of: 1) Claim submission via EDI 837 (85%), REST API (10%), or paper/OCR (5%) channels, 2) Format and duplicate validation with 90-day lookback, 3) Eligibility verification using date of service, 4) Pre-payment fraud scoring with 0.82 threshold for SIU holds, 5) Pre-authorization checks against quarterly-updated service lists, 6) Rules engine adjudication producing PAY/DENY/PEND dispositions, 7) Payment processing with $5 minimum threshold and ERA 835 generation, 8) Post-payment fraud analysis and accumulator updates, and 9) Appeals process with Level 1 internal and Level 2 external review options. Exception flows handle retroactive enrollment changes (60 days back), COB scenarios, and provider network status changes using date-of-service rules.
