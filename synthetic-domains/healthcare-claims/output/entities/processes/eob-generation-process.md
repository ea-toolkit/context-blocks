---
type: process
id: eob-generation-process
name: EOB Generation Process
description: |-
  Automated generation of Explanation of Benefits documents for all processed claims
status: active
tags:
- member-communication
- regulatory-compliance
- digital-first
source_documents:
- claims-processing-workflow.txt
confidence: 0.9
triggered_by:
- claims-processing-workflow
produces:
- eob
uses:
- member-portal
---

# EOB Generation Process

## Overview

Process that creates EOB documents for every processed claim, showing services rendered, amounts billed, amounts allowed, plan payment, and member responsibility. EOBs are available digitally before physical mail delivery.

## Details

Every processed claim, regardless of disposition (PAY, DENY, or PEND after manual review), generates an Explanation of Benefits (EOB) document for the member. The EOB shows: services rendered, amounts billed by the provider, amounts allowed under the plan, plan payment amount, and member responsibility. EOBs are made available digitally in the Member Portal before physical mail delivery, allowing members faster access to their claim information. For denied claims, the EOB includes denial reason codes and explanations. This process ensures transparency and regulatory compliance for all claim adjudication decisions.
