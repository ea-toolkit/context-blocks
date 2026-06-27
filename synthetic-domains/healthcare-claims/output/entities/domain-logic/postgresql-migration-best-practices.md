---
type: domain-logic
id: postgresql-migration-best-practices
name: PostgreSQL Migration Best Practices
description: Guidelines requiring concurrent index creation and DBA review for schema
  changes
status: active
tags:
- legacy-era
- database
- operational-practices
source_documents:
- postmortem-2022-eligibility-outage.txt
confidence: 1.0
applies_to:
- cloud-sql-postgresql
enforced_via:
- schema-change-review-process
originated_from:
- september-2022-eligibility-outage
---

# PostgreSQL Migration Best Practices

## Overview

Best practices established after the September 2022 outage requiring database migrations to use CREATE INDEX CONCURRENTLY for non-blocking operations, mandatory DBA or senior engineer review for schema changes, and off-hours deployment for large DDL operations. These practices include testing against prod-sized datasets in staging.

## Details

Following the September 2022 incident, specific rules were established: 1) Use CREATE INDEX CONCURRENTLY instead of standard CREATE INDEX to avoid table locks, 2) All schema changes require DBA or senior engineer review before deployment, 3) Large DDL operations must be scheduled during off-hours rather than peak times (the original migration was deployed at 9 AM), 4) Migrations must be tested against production-sized datasets in staging environments first. A CI pre-deploy check was also implemented to warn about non-concurrent index creation.
