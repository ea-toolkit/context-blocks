---
type: process
id: database-migration-process
name: Database Migration Process
description: |-
  Automated database schema change process using Flyway (Java) and Alembic (Python)
status: active
tags:
- database
- deployment
source_documents:
- deployment-guide.txt
confidence: 0.9
uses:
- flyway
- alembic
---

# Database Migration Process

## Overview

Standardized database schema evolution process that runs migrations automatically on service startup with strict backward compatibility requirements.

## Details

Uses Flyway for Java services and Alembic for Fraud Detection (Python). Migrations run automatically on service startup. Critical rule: migrations must be backward compatible - old code version must work with new schema. This requires adding columns as nullable first, deploying code that writes to new column, then making non-nullable in later migration. Manual DDL execution in production is prohibited - all changes must go through migrations. Naming convention: Java uses V<version>__<description>.sql (e.g., V042__add_void_linkage_fields.sql), Python uses <timestamp>_<description>.py format.
