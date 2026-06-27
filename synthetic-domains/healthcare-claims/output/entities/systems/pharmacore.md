---
type: system
id: pharmacore
name: PharmaCore
description: |-
  Legacy system currently processing all pharmacy claims outside the main Clearview platform
status: active
tags:
- legacy
- pharmacy
- migration-target
source_documents:
- pharmacy-claims.txt
confidence: 0.9
owned_by:
- dana-okafor
---

# PharmaCore

## Overview

PharmaCore is the existing pharmacy claims processing system that handles approximately 50K claims per quarter. It operates independently from Clearview's main claims platform and is scheduled for replacement as part of the 2026 roadmap migration.

## Details

PharmaCore processes all of Clearview's pharmacy claims volume (~50K per quarter) but operates entirely outside the modern claims platform. The system is considered legacy and is targeted for replacement in the 2026 roadmap. Dana Okafor has the most knowledge about this system's current operations. The migration planning will involve decisions about NCPDP transaction standards, formulary integration, PBM integration strategy, pharmacy network pricing, and clinical drug review integration.
