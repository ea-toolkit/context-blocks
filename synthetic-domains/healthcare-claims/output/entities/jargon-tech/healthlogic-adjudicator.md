---
type: jargon-tech
id: healthlogic-adjudicator
name: HealthLogic Adjudicator
description: |-
  Vendor rules engine product currently running version 4.2, being replaced per ADR-2024-007
status: deprecated
tags:
- vendor-product
- rules-engine
- being-replaced
source_documents:
- architecture-overview.txt
confidence: 0.95
used_by:
- rules-engine
owned_by:
- claims-operations
---

# HealthLogic Adjudicator

## Overview

HealthLogic Adjudicator 4.2 is the vendor product currently serving as the Rules Engine for claims adjudication. It's a third-party solution that executes business rules maintained by the Claims Operations team, though it's in the process of being replaced.

## Details

Third-party vendor product from HealthLogic serving as the current Rules Engine implementation. Running version 4.2 in production. The vendor provides the execution platform while Clearview's Claims Operations team maintains the actual business rules for adjudication. Currently being replaced as documented in ADR-2024-007 (referenced in the document but not detailed). Evaluates claims against benefit plan terms, provider contracts, medical policies, and authorization requirements to produce PAY/DENY/PEND dispositions.
