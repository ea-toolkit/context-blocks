---
type: system
id: hets
name: HETS (Healthcare Eligibility Transaction System)
description: |-
  CMS system for Medicare beneficiary identifier lookups and eligibility verification
status: active
tags:
- external-system
- medicare
- verification
source_documents:
- design-session-cob-handling.txt
confidence: 0.85
operated_by:
- external-parties
used_by:
- eligibility-service
supports:
- cob-detection-signals
---

# HETS (Healthcare Eligibility Transaction System)

## Overview

CMS-operated system that allows payers to verify Medicare enrollment status. Clearview already has some access for 270/271 transactions through the eligibility team.

## Details

Healthcare Eligibility Transaction System operated by CMS that provides Medicare Beneficiary Identifier (MBI) lookups. Clearview currently uses it for some eligibility transactions, but needs to verify access specifically for COB lookups. This system would support signal #4 of the COB auto-detection by allowing automated verification of Medicare enrollment when members turn 65.

## Open Questions

- Clearview already has some access for 270/271 transactions through the eligibility team
