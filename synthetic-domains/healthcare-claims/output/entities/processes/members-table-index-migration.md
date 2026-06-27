---
type: process
id: members-table-index-migration
name: Members Table Index Migration
description: |-
  Database migration to add index on members table that caused September 2022 outage
status: active
tags:
- legacy-era
- database
- migration
- incident-trigger
source_documents:
- postmortem-2022-eligibility-outage.txt
confidence: 1.0
executed_by:
- tom-nguyen
applies_to:
- members-table
triggered:
- september-2022-eligibility-outage
---

# Members Table Index Migration

## Overview

A database migration process initiated by Tom Nguyen to add an index on the members table for a new query pattern. The migration used ALTER TABLE members ADD INDEX instead of CREATE INDEX CONCURRENTLY, causing a table-level lock on the 800K-row table that blocked all reads and triggered the outage.

## Details

The migration was deployed at 09:12 ET on September 17, 2022 without senior engineer or DBA review. It was intended to support a new query pattern but used a blocking index creation approach. When Tom realized the migration was causing the outage at 09:25, he tried to cancel it but it was partway through index creation. Dana Okafor later attempted to kill the query via pg_terminate_backend() but dependent transactions kept the table lock active, ultimately requiring a database restart to resolve.
