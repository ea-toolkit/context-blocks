---
type: data-model
id: criteria-load-history-table
name: Criteria Load History Table
description: Database table tracking versions and load times of clinical criteria
  files
status: active
tags:
- database
- audit
- clinical
source_documents:
- pre-auth-runbook.txt
confidence: 0.9
used_by:
- pre-auth-service
---

# Criteria Load History Table

## Overview

Audit table that records when clinical criteria files are loaded from GCS, including version information and timestamps. Used for troubleshooting auto-approval rate changes.

## Details

Contains criteria_version and loaded_at fields to track when new clinical criteria configurations are deployed to the Pre-Auth Service. Clinical criteria files are stored in gs://clearview-preauth-config/criteria/ and loaded on service startup. This table enables correlation between criteria updates and changes in auto-approval rates, supporting root cause analysis for business metric degradation.
