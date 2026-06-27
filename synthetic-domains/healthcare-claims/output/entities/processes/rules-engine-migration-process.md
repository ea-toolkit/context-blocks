---
type: process
id: rules-engine-migration-process
name: Rules Engine Migration Process
description: |-
  Three-phase process to migrate from HealthLogic Adjudicator to custom Drools-based rules engine
status: active
tags:
- migration
- multi-phase
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.95
owned_by:
- claims-operations
involves:
- rachel-dominguez
---

# Rules Engine Migration Process

## Overview

A structured migration approach spanning 2025-2026 with three distinct phases: build (Q1-Q3 2025), parallel processing (Q4 2025), and cutover (Q1 2026). The process includes rigorous accuracy testing with 99.5% disposition match and 99.9% payment amount accuracy targets.

## Details

Phase 1 focuses on building the new Drools-based engine, starting with the 60% of simple edit rules for lowest-risk highest-coverage implementation. Phase 2 involves running both engines in parallel for months to ensure accuracy, with detailed comparison of results. Phase 3 is the final cutover once confidence is established. The migration strategy prioritizes simple claim edits first, then benefit plan rules, with complex logic (COB, accumulators, bundling) handled last as these areas hide the most bugs. Rachel Dominguez brings experience from three similar payer migrations to guide the process.
