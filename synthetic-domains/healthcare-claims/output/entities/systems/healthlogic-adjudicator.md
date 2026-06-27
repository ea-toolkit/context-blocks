---
type: system
id: healthlogic-adjudicator
name: HealthLogic Adjudicator
description: |-
  Legacy claims rules engine being migrated away from due to cost and flexibility issues
status: deprecated
tags:
- legacy-era
- vendor
- migration-source
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.95
owned_by:
- healthlogic-systems
superseded_by:
- drools-rules-engine
used_by:
- claims-operations
---

# HealthLogic Adjudicator

## Overview

HealthLogic Adjudicator 4.2 has served as Clearview's claims rules engine since 2019, handling ~4,200 active rules for claim adjudication. The system works reliably but costs $1.2M annually and requires 8-12 weeks for new rule implementations through vendor professional services.

## Details

The system contains approximately 4,200 active rules broken down as: 60% straightforward claim edits (procedure-diagnosis validation), 30% benefit plan rules (copay, coinsurance, deductible calculations), and 10% complex logic (COB, accumulators, multi-claim bundling). It includes a built-in DRG grouper for institutional claims reimbursement. The system provides a web UI for clinical teams to define rules, but the vendor dependency creates significant delays for rule changes. The migration away from this system is driven by licensing costs and the need for faster rule deployment cycles.
