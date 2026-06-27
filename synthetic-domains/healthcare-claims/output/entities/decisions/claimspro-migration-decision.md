---
type: decision
id: claimspro-migration-decision
name: ClaimsPro Migration Decision
description: |-
  Decision to migrate from ClaimsPro monolith to microservices architecture in 2020-2021
status: active
tags:
- legacy-era
- architecture
- migration
source_documents:
- original-architecture-2021.txt
confidence: 0.95
applies_to:
- claimspro
made_by:
- samir-patel
---

# ClaimsPro Migration Decision

## Overview

The decision to migrate away from ClaimsPro was driven by scalability issues and vendor abandonment. The migration was executed in Q4 2020 through Q1 2021 under the leadership of Principal Architect Samir Patel.

## Details

The migration decision was motivated by ClaimsPro's inability to handle the growing member base (500K to 800K projected) and the vendor's effective cessation of product development. The migration involved extracting key modules (eligibility, payment, provider directory) and building new components (Claims Gateway) while replacing adjudication with HealthLogic. The migration strategy included a 6-month dual-write period for the eligibility module to ensure data consistency during cutover. The payment module required a complete rewrite due to its deep entanglement with adjudication logic.
