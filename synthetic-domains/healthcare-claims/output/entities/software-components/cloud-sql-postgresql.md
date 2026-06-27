---
type: software-component
id: cloud-sql-postgresql
name: Cloud SQL PostgreSQL
description: |-
  Managed PostgreSQL 15 database service with high availability failover for claims data storage
status: active
tags:
- database
- postgresql
- managed-service
- high-availability
source_documents:
- architecture-overview.txt
confidence: 0.95
used_by:
- claims-gateway
- eligibility-service
- payment-engine
- fraud-detection
- provider-directory
---

# Cloud SQL PostgreSQL

## Overview

Cloud SQL provides the primary data persistence layer for the claims processing platform. Running PostgreSQL 15 with high availability failover, it stores claim tracking data, member eligibility information, payment records, and other critical business data.

## Details

Uses PostgreSQL version 15 with HA (high availability) failover configuration. Serves as the primary database for Claims Gateway claim tracking, Eligibility Service member data, Payment Engine financial records, and other systems. The HA setup ensures continuity during database failures. All systems in the platform depend on this managed database service for data persistence.
