---
type: process
id: payment-reconciliation-rework
name: Payment Reconciliation Rework
description: |-
  Design initiative to fix three critical problems in Payment Engine reconciliation workflow
status: active
tags:
- payment-processing
- reconciliation
- provider-experience
source_documents:
- design-session-payment-reconciliation.txt
confidence: 0.95
owned_by:
- claims-operations
involves:
- payment-engine
- rules-engine
- eligibility-service
---

# Payment Reconciliation Rework

## Overview

Multi-phased project to address timing mismatches between ERA 835 generation and EFT settlement, improve void/reissue payment tracking, and redesign recoupment spreading logic. Session resulted in concrete decisions for first two problems but deferred complex recoupment logic requiring fraud team coordination.

## Details

The rework addresses three specific problems: (1) ERA 835 remittance advice generated at payment batch time but EFT settlement occurs 2-3 days later, causing provider office reconciliation issues when deposits don't match posted amounts, (2) void/reissue payment chains from Rules Engine reprocessing lack proper linkage tracking, creating orphaned records, and (3) recoupment spreading logic fails to coordinate multiple simultaneous recoupments, potentially zeroing out provider payments for extended periods. Team decided to delay ERA 835 until settlement confirmation and add void linkage database fields, but recoupment spreading requires additional design work involving fraud holds and minimum payment thresholds.
