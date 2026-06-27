---
type: data-model
id: edi-837-professional
name: EDI 837 Professional
description: |-
  Electronic data interchange format for professional healthcare claims (CMS-1500 equivalent)
status: active
tags:
- edi
- professional-claims
- real-time
source_documents:
- architecture-overview.txt
confidence: 0.95
used_by:
- claims-gateway
contracts:
- claims-submission-api
---

# EDI 837 Professional

## Overview

EDI 837 Professional is the standard electronic format for submitting professional healthcare claims. It's the electronic equivalent of the CMS-1500 paper form and is processed in real-time by the Claims Gateway with a 30-second SLA.

## Details

Standard EDI transaction format used for professional healthcare services claims. Contains member demographics, provider information, service dates, diagnosis codes, procedure codes, and billed amounts. Processed in real-time by the Claims Gateway with a 30-second SLA for faster provider cash flow. The Claims Gateway validates format and required fields before routing to downstream adjudication systems. This format is used for most outpatient professional services like physician visits, lab work, and outpatient procedures.
