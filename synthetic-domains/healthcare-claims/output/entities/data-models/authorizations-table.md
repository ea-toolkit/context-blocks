---
type: data-model
id: authorizations-table
name: Authorizations Table
description: |-
  Database table storing approved/denied authorization decisions with validity periods
status: active
tags:
- database
- authorization
source_documents:
- pre-auth-runbook.txt
confidence: 0.95
used_by:
- pre-auth-service
---

# Authorizations Table

## Overview

PostgreSQL table containing authorization determinations, approval codes, expiration dates, and decision metadata. Tracks the final disposition of authorization requests.

## Details

Table includes auth_id, member_id, provider_npi, service_category, determination (APPROVED/DENIED), approval_code, approved_date, expiry_date, determined_at, determined_by, and notes fields. Standard auths valid for 90 days, surgical auths for 60 days. Used for tracking expiring authorizations and manual override operations. Manual approvals use format 'MANUAL-YYYYMMDD-HH24MI' with clinical lead approval documentation.
