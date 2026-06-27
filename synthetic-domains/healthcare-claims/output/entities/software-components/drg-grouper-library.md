---
type: software-component
id: drg-grouper-library
name: DRG Grouper Library
description: |-
  Java library needed for calculating Diagnosis Related Groups for institutional claims
status: planned
tags:
- cms-compliance
- institutional-claims
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.8
used_by:
- drools-rules-engine
---

# DRG Grouper Library

## Overview

A Java library that implements CMS's ICD-10 PCS grouper for calculating DRGs used in inpatient reimbursement. The library must be updated annually when CMS releases new fiscal year definitions each October.

## Details

Required for institutional claims processing, particularly inpatient stays where hospitals are paid a flat rate per DRG rather than per service. The library implements CMS-published ICD-10 PCS grouper logic, grouping hospital stays into payment categories based on principal diagnosis, procedures performed, complications, and patient demographics. CMS releases updated grouper definitions annually each October that must be incorporated. Rachel Dominguez mentioned there are open-source Java libraries available that implement this functionality.

## Open Questions

- Rachel mentioned there are open-source options available
