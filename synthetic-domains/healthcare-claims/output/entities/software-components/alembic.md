---
type: software-component
id: alembic
name: Alembic
description: Python database migration tool used by Fraud Detection service
status: active
tags:
- database
- python
source_documents:
- deployment-guide.txt
confidence: 0.85
used_by:
- fraud-detection
part_of:
- database-migration-process
---

# Alembic

## Overview

Database migration framework used specifically by the Fraud Detection service (Python-based) for managing schema changes.

## Details

Python-based database migration tool used by the Fraud Detection service for managing schema evolution. Uses timestamp-based naming convention (<timestamp>_<description>.py) and runs automatically on service startup. Must follow backward compatibility rules where old code works with new schema.
