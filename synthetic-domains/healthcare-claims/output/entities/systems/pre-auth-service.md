---
type: system
id: pre-auth-service
name: Pre-Auth Service
description: |-
  System managing prior authorization requests with auto-approval and clinical review routing
status: active
tags:
- seed-context-derived
- foundation
source_documents:
- seed-context
confidence: 0.9
owned_by:
- claims-operations
---

# Pre-Auth Service

## Overview

Pre-Auth Service manages prior authorization requests from providers. It auto-approves routine requests (targeting 60% automation) and routes complex cases to clinical reviewers for manual evaluation.

## Details

This system handles the prior authorization workflow where providers submit authorization requests for services. The system automatically approves routine requests with a target of 60% automation rate, while routing more complex or high-risk authorization requests to clinical reviewers for manual assessment.
