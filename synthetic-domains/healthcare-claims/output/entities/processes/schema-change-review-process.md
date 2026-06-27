---
type: process
id: schema-change-review-process
name: Schema Change Review Process
description: |-
  DBA review requirement for all database schema changes established after 2022 outage
status: active
tags:
- legacy-era
- governance
- database
source_documents:
- postmortem-2022-eligibility-outage.txt
confidence: 1.0
implements:
- postgresql-migration-best-practices
resulted_from:
- september-2022-eligibility-outage
---

# Schema Change Review Process

## Overview

A governance process implemented as follow-up action INC-2022-0094-A1 requiring DBA or senior engineer review for all schema changes before deployment. This process was completed to prevent similar migration-related outages.

## Details

This review process was established as a direct response to the September 2022 outage where Tom Nguyen deployed a blocking database migration without senior oversight. The process requires that all DDL operations, particularly index creation and schema modifications, undergo review by either a DBA or senior engineer before deployment. This ensures that best practices like CREATE INDEX CONCURRENTLY are followed and that migrations are properly planned for off-hours deployment when appropriate.
