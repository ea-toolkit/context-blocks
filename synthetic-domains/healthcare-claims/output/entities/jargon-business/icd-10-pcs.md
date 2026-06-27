---
type: jargon-business
id: icd-10-pcs
name: ICD-10-PCS
description: ICD-10 Procedure Coding System used for DRG grouper calculations
status: active
tags:
- coding-system
- institutional-claims
- drg
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.9
used_by:
- drg-grouper-library
related_to:
- icd-10-cm
---

# ICD-10-PCS

## Overview

ICD-10-PCS (Procedure Coding System) codes are used by the DRG grouper to calculate Diagnosis Related Groups for institutional claims reimbursement. CMS publishes annual updates to the grouper definitions each October.

## Details

ICD-10-PCS codes are specifically used in the DRG grouper algorithm to categorize inpatient hospital stays into payment groups. The DRG calculation considers principal diagnosis, procedures performed (coded in ICD-10-PCS), complications, and patient demographics to determine the appropriate payment category. CMS releases updated grouper definitions annually each October, requiring corresponding updates to any DRG grouper library used by the rules engine.
