---
type: process
id: cob-batch-analysis
name: COB Batch Analysis
description: Weekly batch job analyzing claims data for COB detection signals
status: planned
tags:
- batch-processing
- analytics
source_documents:
- design-session-cob-handling.txt
confidence: 0.9
part_of:
- cob-auto-detection-project
consumes:
- claims-gateway
- eligibility-service
triggers:
- cob-verification-workflow
implements:
- cob-detection-signals
---

# COB Batch Analysis

## Overview

Planned weekly batch processing job that will analyze historical claims data to identify members who may have unreported other coverage.

## Details

Weekly batch analysis process that pulls claims data (billed amounts, procedure codes) from the reporting database and member data from Eligibility Service to identify COB detection signals. For signal #1, compares billed amounts against the 25th percentile for each procedure code to flag unusually low amounts. Outputs a list of member IDs flagged for COB review that feeds into the verification workflow. Designed as a reporting pipeline job rather than a real-time service feature.
