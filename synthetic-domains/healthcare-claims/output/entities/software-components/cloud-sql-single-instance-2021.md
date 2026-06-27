---
type: software-component
id: cloud-sql-single-instance-2021
name: Cloud SQL Single Instance (2021)
description: |-
  Original single Cloud SQL PostgreSQL instance without HA failover used in 2021 architecture
status: deprecated
tags:
- legacy-era
- database
- single-point-failure
- replaced
source_documents:
- original-architecture-2021.txt
confidence: 0.95
superseded_by:
- cloud-sql-postgresql
---

# Cloud SQL Single Instance (2021)

## Overview

The 2021 architecture used a single Cloud SQL PostgreSQL instance for all services without high availability failover. This was acknowledged as inadequate and was later upgraded to separate instances per service.

## Details

The initial migration used a single Cloud SQL for PostgreSQL instance to host databases for all microservices. This instance had no high availability failover configuration, which was recognized as a significant risk. The document notes 'single instance, no HA failover — yes, really' indicating the team was aware this was not production-ready. This was addressed in Q2 2022 when the architecture moved to separate database instances per service, providing better isolation, performance, and reliability. The single-instance approach was likely a migration expedient to get off ClaimsPro quickly.
