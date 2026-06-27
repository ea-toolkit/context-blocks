---
type: software-component
id: hikaricp
name: HikariCP
description: JDBC connection pool library used by Claims Gateway for PostgreSQL connections
status: active
tags:
- infrastructure
- database-connection
source_documents:
- 2024-claims-gateway-outage-postmortem.txt
confidence: 0.95
used_by:
- claims-gateway
connects_to:
- claims-gw-prod-01
---

# HikariCP

## Overview

HikariCP is the connection pooling library used by the Claims Gateway to manage database connections to PostgreSQL. The pool was configured with a maximum of 100 connections at the time of the March 2024 incident.

## Details

HikariCP manages the database connection pool for the Claims Gateway, configured with a maximum of 100 connections to the Cloud SQL PostgreSQL instance claims-gw-prod-01. The library provides connection pooling capabilities but was not configured with separate pools for batch vs real-time processing, which led to the March 2024 outage when a large batch exhausted all connections. The configuration was later changed in Q3 2024 when the system moved to PgBouncer connection pooling.
