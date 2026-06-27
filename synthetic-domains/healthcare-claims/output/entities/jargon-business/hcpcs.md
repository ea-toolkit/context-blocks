---
type: jargon-business
id: hcpcs
name: HCPCS
description: |-
  Healthcare Common Procedure Coding System - broader coding system including CPT plus supply and equipment codes
status: active
tags:
- coding-system
- comprehensive
source_documents:
- meeting-notes-vendor-migration-kickoff.txt
confidence: 0.95
contains:
- cpt
used_by:
- rules-engine
---

# HCPCS

## Overview

HCPCS (Healthcare Common Procedure Coding System) is a comprehensive coding system that includes CPT codes (Level I) plus additional codes for medical supplies, equipment, and drugs (Level II). Level II codes start with a letter.

## Details

HCPCS encompasses both Level I codes (CPT codes for procedures and services) and Level II codes for supplies, equipment, and drugs. Level II codes are distinguished by starting with a letter, such as J0129 for abciximab injection. This coding system is essential for the rules engine to properly process all types of medical claims, from basic procedures to complex drug administrations and equipment rentals. The rules engine must understand both levels for comprehensive claim adjudication.
