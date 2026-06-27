---
type: software-component
id: flyway
name: Flyway
description: Database migration tool used for Java services schema evolution
status: active
tags:
- infrastructure
- database-migration
- java-ecosystem
source_documents:
- claims-coding-standards.txt
confidence: 1.0
used_by:
- claims-gateway
- eligibility-service
- payment-engine
integrates_with:
- cloud-sql-postgresql
---

# Flyway

## Overview

Database migration tool integrated into Java services for managing schema changes and version control. Ensures consistent database evolution across environments with rollback capabilities.

## Details

Flyway handles database schema migrations for Java services including Claims Gateway, Eligibility Service, Payment Engine, Pre-Auth Service, and Provider Directory. All database schema changes must include a corresponding Flyway migration script as part of the code review requirements. This ensures database schema evolution is version-controlled, repeatable, and can be applied consistently across development, staging, and production environments.
