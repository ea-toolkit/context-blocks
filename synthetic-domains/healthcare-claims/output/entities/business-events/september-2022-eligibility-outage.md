---
type: business-event
id: september-2022-eligibility-outage
name: September 2022 Eligibility Service Outage
description: |-
  Complete Eligibility Service outage lasting 3 hours 47 minutes due to database migration table lock
status: active
tags:
- legacy-era
- sev-1
- database
- cascading-failure
source_documents:
- postmortem-2022-eligibility-outage.txt
confidence: 1.0
involved:
- eligibility-service
- claims-gateway
- rules-engine
- member-portal
caused_by:
- members-table-index-migration
---

# September 2022 Eligibility Service Outage

## Overview

A SEV-1 incident on September 17, 2022 where a database migration to add an index on the members table used a blocking operation instead of CREATE INDEX CONCURRENTLY. This locked the entire members table, causing Eligibility Service queries to timeout and cascading failures across Claims Gateway, Rules Engine, and Member Portal.

## Details

Timeline started at 09:12 ET when Tom Nguyen deployed a database migration using ALTER TABLE members ADD INDEX, acquiring a table-level lock on the 800K-row members table. By 09:14, Eligibility Service queries were timing out, and by 09:18 Claims Gateway was returning 503 errors because it couldn't verify eligibility. The incident escalated through multiple attempted fixes including pg_terminate_backend() before Dana Okafor decided to restart the Cloud SQL instance at 09:42. The database came back up at 09:55, but an 18K claim backlog took until 11:40 to fully clear due to HealthLogic Adjudicator throughput limitations. The incident was closed at 12:59 after 1 hour of stable metrics.
