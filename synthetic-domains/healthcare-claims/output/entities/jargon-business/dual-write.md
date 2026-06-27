---
type: jargon-business
id: dual-write
name: Dual-Write
description: |-
  Migration strategy where data is written to both old and new systems simultaneously during transition
status: active
tags:
- migration-pattern
- data-consistency
source_documents:
- original-architecture-2021.txt
confidence: 0.95
used_in:
- eligibility-service
---

# Dual-Write

## Overview

Dual-write was the migration strategy used during the eligibility service extraction where data was written to both ClaimsPro and the new eligibility database simultaneously for 6 months to ensure data consistency during cutover.

## Details

Dual-write is a common migration pattern where during the transition period, all data changes are written to both the legacy system (ClaimsPro database) and the new system (new eligibility service database) simultaneously. This ensures that both systems remain in sync and allows for safe cutover with the ability to rollback if needed. Clearview used this approach for 6 months during the eligibility service migration, writing eligibility changes to both the ClaimsPro database via database views and the new dedicated database. This pattern reduces risk during critical system migrations but adds complexity during the transition period.
