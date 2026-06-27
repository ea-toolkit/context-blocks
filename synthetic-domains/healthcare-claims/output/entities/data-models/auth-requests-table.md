---
type: data-model
id: auth-requests-table
name: Auth Requests Table
description: |-
  Database table storing authorization requests with status and processing timestamps
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

# Auth Requests Table

## Overview

PostgreSQL table in the preauth_prod database that tracks authorization requests through their lifecycle. Contains fields for status tracking, timestamps, and processing metadata.

## Details

Table structure includes auth_id, member_id, provider_npi, service_category, status (PENDING, PROCESSING, etc.), created_at, updated_at timestamps, and other authorization request metadata. Used for monitoring stuck requests (PROCESSING status older than 2 hours), tracking volume by day, and managing the authorization workflow. The scheduler picks up PENDING requests every 60 seconds for processing.
