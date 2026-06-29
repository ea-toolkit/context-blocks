---
type: process
id: claim-routing-process
name: Claim Routing Process
description: Routes claims to appropriate adjudication queues
status: active
confidence: 0.78
related_systems: [claims-gateway, adjudication-engine]
triggers: [claim-submitted]
source_documents: [doc-003.md]
---

# Claim Routing Process

## Overview
Determines which adjudication queue handles each claim based on type, amount, and policy rules.

## Details
Three routing paths: auto-adjudication (routine), specialist review (complex), and manual override (exceptions).
