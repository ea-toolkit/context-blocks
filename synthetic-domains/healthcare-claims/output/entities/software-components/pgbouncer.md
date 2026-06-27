---
type: software-component
id: pgbouncer
name: PgBouncer
description: PostgreSQL connection pooling proxy introduced in Q3 2024 migration
status: active
tags:
- infrastructure
- database
source_documents:
- monitoring-alerting-runbook.txt
confidence: 0.9
used_by:
- claims-gateway
communicates_with:
- cloud-sql-postgresql
---

# PgBouncer

## Overview

PgBouncer is a PostgreSQL connection pooling proxy that was introduced during Q3 2024 as part of database connectivity improvements following the connection pool incidents. It now manages database connections with a maximum of 200 connections for the Claims Gateway.

## Details

PgBouncer was implemented during Q3 2024 as part of the post-incident improvements following CLV-3903. It serves as a connection pooling proxy for PostgreSQL databases, managing connection limits and improving database connectivity reliability. The current configuration supports a maximum of 200 connections, which represents a change from the previous direct connection architecture. This migration coincided with updates to HikariCP pool monitoring and connection pool exhaustion alerting. PgBouncer helps isolate application connection pools from database connection limits, providing an additional layer of connection management and potentially reducing the risk of connection exhaustion incidents.

## Open Questions

- PgBouncer helps isolate application connection pools from database connection limits, providing an additional layer of connection management and potentially reducing the risk of connection exhaustion incidents
