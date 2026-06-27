---
type: software-component
id: claims-gw-prod-01
name: claims-gw-prod-01
description: Production Cloud SQL PostgreSQL database instance for Claims Gateway
status: active
tags:
- database
- production
- cloud-sql
source_documents:
- 2024-claims-gateway-outage-postmortem.txt
confidence: 0.9
used_by:
- claims-gateway
deployed_on:
- google-cloud-platform
---

# claims-gw-prod-01

## Overview

The production PostgreSQL database instance hosted on Google Cloud SQL that serves as the primary data store for the Claims Gateway. This instance was the target of the connection pool exhaustion during the March 2024 incident.

## Details

claims-gw-prod-01 is the Cloud SQL PostgreSQL database instance that stores Claims Gateway data. During the March 2024 incident, this database became inaccessible when the HikariCP connection pool was exhausted by the large batch of institutional claims processing. The database itself was not the problem - it was the connection pool management that caused the outage. All 100 connections in the pool were active running INSERT statements for institutional claims batch processing.
