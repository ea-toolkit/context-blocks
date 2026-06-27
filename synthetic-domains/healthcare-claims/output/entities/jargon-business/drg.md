---
type: jargon-business
id: drg
name: DRG
description: Diagnosis Related Group - payment categories for inpatient hospital stays
status: active
tags:
- payment-methodology
- institutional-claims
- cms
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.95
calculated_by:
- drg-grouper-library
used_by:
- rules-engine
---

# DRG

## Overview

DRG (Diagnosis Related Group) is a classification system that groups inpatient hospital stays into payment categories. Hospitals receive a flat rate per DRG rather than payment per individual service, creating a prospective payment system.

## Details

DRGs are calculated using a grouper algorithm that considers the principal diagnosis, procedures performed (coded in ICD-10-PCS), complications, comorbidities, and patient demographics. Each DRG represents a similar clinical condition and resource utilization pattern, allowing hospitals to be paid a predetermined amount regardless of actual length of stay or specific services provided. This system incentivizes efficient care delivery. The rules engine must include DRG grouper functionality to properly adjudicate institutional claims, and the grouper definitions must be updated annually with CMS releases.
