---
type: process
id: duplicate-detection-process
name: Duplicate Detection Process
description: |-
  Process for identifying and preventing duplicate claim submissions using composite key matching
status: active
tags:
- claims-processing
- duplicate-prevention
- validation
source_documents:
- architecture-overview.txt
confidence: 0.9
executed_by:
- claims-gateway
involves:
- member-id
- npi
---

# Duplicate Detection Process

## Overview

The duplicate detection process runs in the Claims Gateway to prevent the same claim from being processed multiple times. It uses a composite key to identify potential duplicates before claims enter the adjudication pipeline.

## Details

Implemented in the Claims Gateway using a composite key consisting of: member ID + provider NPI + date of service + procedure codes. When a claim is submitted, this composite key is generated and checked against previously processed claims. If a match is found, the claim is flagged as a potential duplicate and handled according to business rules. This prevents duplicate payments and ensures claims are only adjudicated once. The process runs at claim intake before routing to downstream systems.
