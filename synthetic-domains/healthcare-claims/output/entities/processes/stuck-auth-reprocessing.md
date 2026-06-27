---
type: process
id: stuck-auth-reprocessing
name: Stuck Auth Reprocessing
description: Manual operation to reset stuck authorization requests for reprocessing
status: active
tags:
- operational
- manual
- troubleshooting
source_documents:
- pre-auth-runbook.txt
confidence: 0.9
operates_on:
- auth-requests-table
---

# Stuck Auth Reprocessing

## Overview

Operational procedure to identify authorization requests stuck in PROCESSING status and reset them to PENDING for scheduler pickup. Used when requests haven't been updated within 2 hours.

## Details

Process involves: 1) Query auth_requests table for records with status='PROCESSING' and updated_at older than 2 hours, 2) Reset status to 'PENDING' and update timestamp, 3) Monitor in Datadog as scheduler picks up PENDING requests every 60 seconds. This addresses situations where authorization processing gets stuck due to system issues or unexpected failures during processing workflow.
