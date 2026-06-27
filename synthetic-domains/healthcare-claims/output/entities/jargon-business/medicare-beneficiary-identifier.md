---
type: jargon-business
id: medicare-beneficiary-identifier
name: Medicare Beneficiary Identifier (MBI)
description: Unique identifier used by CMS for Medicare beneficiaries
status: active
tags:
- medicare
- identifier
source_documents:
- design-session-cob-handling.txt
confidence: 0.9
managed_by:
- external-parties
accessible_via:
- hets
used_in:
- cob-detection-signals
---

# Medicare Beneficiary Identifier (MBI)

## Overview

CMS-assigned identifier for Medicare beneficiaries that can be looked up through HETS system. Would be used in COB auto-detection to verify Medicare enrollment when members turn 65.

## Details

Medicare Beneficiary Identifier is the unique ID assigned by CMS to Medicare enrollees. This identifier can be queried through the HETS system to verify whether a member has enrolled in Medicare, which is crucial for signal #4 of the COB auto-detection system since Medicare enrollment at age 65 is a strong indicator of other coverage that should be reported.
