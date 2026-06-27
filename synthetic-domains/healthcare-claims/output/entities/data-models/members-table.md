---
type: data-model
id: members-table
name: Members Table
description: Database table storing member enrollment data with approximately 800K
  rows
status: active
tags:
- legacy-era
- database
- core-data
source_documents:
- postmortem-2022-eligibility-outage.txt
confidence: 0.9
owned_by:
- eligibility-service
used_by:
- claims-gateway
- rules-engine
---

# Members Table

## Overview

A core database table in the Eligibility Service that stores member enrollment information for Clearview's approximately 800K covered members. This table is heavily accessed for eligibility verification and accumulator queries during claims processing.

## Details

The members table is a critical component of the Eligibility Service database, containing enrollment data for all covered members. During the September 2022 incident, a migration to add an index on this table used a blocking ALTER TABLE operation instead of CREATE INDEX CONCURRENTLY, which locked the entire table and prevented all read operations. The table's size (~800K rows) made the migration operation particularly lengthy and impactful when it acquired a full table lock.

## Open Questions

- The table appears to be part of the Eligibility Service database based on the context
