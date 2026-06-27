---
type: process
id: claim-routing-process
name: Claim Routing Process
description: |-
  Process that routes validated claims to appropriate downstream systems based on business rules
status: active
tags:
- claims-processing
- routing
- business-logic
source_documents:
- architecture-overview.txt
confidence: 0.95
executed_by:
- claims-gateway
involves:
- eligibility-service
- pre-auth-service
- fraud-detection
- rules-engine
---

# Claim Routing Process

## Overview

The claim routing process in the Claims Gateway determines where validated claims should be sent next based on various business criteria. It implements a multi-step routing logic that considers eligibility, authorization requirements, and fraud scores.

## Details

The routing logic follows this sequence: 1) All claims → Eligibility Service for coverage verification, 2) Claims for auth-required services → Pre-Auth Service for authorization status check, 3) Claims scoring >0.82 on the fraud model → held for SIU review, 4) Everything else → Rules Engine for adjudication. This ensures claims are properly validated and authorized before entering the expensive adjudication process, and high-risk claims are intercepted early.
